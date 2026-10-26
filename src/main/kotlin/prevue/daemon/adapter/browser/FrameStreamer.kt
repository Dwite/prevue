package prevue.daemon.adapter.browser

import java.io.IOException
import java.io.OutputStream
import java.nio.charset.StandardCharsets.UTF_8
import kotlin.coroutines.CoroutineContext
import kotlinx.coroutines.CoroutineName
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.CoroutineStart
import kotlinx.coroutines.CancellationException
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.Job
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.coroutineScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import prevue.daemon.domain.model.LiveFrame

data class StreamStats(
    val encoded: Long = 0,
    val encodeMs: Long = 0,
    val encoderDropped: Long = 0,
    val conflated: Long = 0,
    val subscribers: Int = 0,
    val sent: Long = 0,
) {
    fun toJson(): Map<String, Any?> = mapOf(
        "encoded" to encoded, "encodeMs" to encodeMs, "encoderDropped" to encoderDropped,
        "conflated" to conflated, "subscribers" to subscribers, "sent" to sent,
    )
}

class FrameStreamer(
    screen: StateFlow<LiveFrame?>,
    watching: StateFlow<Boolean>,
    parent: CoroutineScope,
    private val log: (String) -> Unit,
    state: CoroutineContext = Dispatchers.Default.limitedParallelism(1, "prevue-frames"),
    encode: CoroutineContext = Dispatchers.Default.limitedParallelism(2, "prevue-encode"),
    private val write: CoroutineContext = Dispatchers.IO,
) {
    private sealed interface Cmd
    private class Show(val frame: LiveFrame?) : Cmd
    private class Watch(val on: Boolean) : Cmd
    private class Subscribe(val out: OutputStream, val viewer: String?) : Cmd
    private class Unsubscribe(val sub: Subscriber) : Cmd
    private class Viewport(val width: Int?) : Cmd
    private class Encoded(val e: FrameEncoder.Encoded) : Cmd

    private class Subscriber(val out: OutputStream, val viewer: String?) {
        val parts = Channel<FrameEncoder.Part>(Channel.CONFLATED)
        lateinit var job: Job
    }

    private val cmds = Channel<Cmd>(Channel.UNLIMITED)
    private val _stats = MutableStateFlow(StreamStats())
    val stats: StateFlow<StreamStats> = _stats
    val hasSubscribers: Boolean get() = _stats.value.subscribers > 0

    private val subscribers = ArrayList<Subscriber>()
    private var last: LiveFrame? = null
    private var lastPart: FrameEncoder.Part? = null
    private var lastSeq = 0L
    private var watched = false
    private var width: Int? = null
    private var conflated = 0L
    private var sent = 0L
    private lateinit var writers: CoroutineScope

    private val job = parent.launch(state + CoroutineName("prevue-frames"), CoroutineStart.ATOMIC) { run(screen, watching, encode) }

    fun subscribe(out: OutputStream, viewer: String? = null) { if (cmds.trySend(Subscribe(out, viewer)).isFailure) closeQuietly(out) }

    fun viewport(width: Int?) { cmds.trySend(Viewport(width?.takeIf { it > 0 })) }

    fun stop() { cmds.close(); job.cancel() }

    suspend fun awaitStopped() = job.join()

    private suspend fun run(screen: StateFlow<LiveFrame?>, watching: StateFlow<Boolean>, encode: CoroutineContext) = coroutineScope {
        writers = this
        launch { screen.collect { cmds.trySend(Show(it)) } }
        launch { watching.collect { cmds.trySend(Watch(it)) } }
        val encoder = FrameEncoder(this, encode, log) { cmds.trySend(Encoded(it)) }
        try {
            for (c in cmds) {
                handle(c, encoder)
                _stats.value = StreamStats(encoder.encoded, encoder.encodeMs, encoder.dropped, conflated, subscribers.size, sent)
            }
        } finally {
            encoder.close()
            cmds.close()
            while (true) {
                val c = cmds.tryReceive().getOrNull() ?: break
                if (c is Subscribe) closeQuietly(c.out)
            }
            dropSubscribers()
            _stats.value = _stats.value.copy(subscribers = 0)
        }
    }

    private fun handle(c: Cmd, encoder: FrameEncoder) {
        when (c) {
            is Show -> show(c.frame, encoder)
            is Watch -> {
                if (watched == c.on) return
                watched = c.on
                encoder.reset()
                if (c.on) submitLast(encoder) else { width = null; dropSubscribers() }
            }
            is Subscribe -> {
                replaceStreamOf(c.viewer)
                val sub = Subscriber(c.out, c.viewer)
                lastPart?.let { sub.parts.trySend(it) }
                sub.job = writers.launch(write + CoroutineName("prevue-stream-out")) { pump(sub) }
                subscribers += sub
                submitLast(encoder)
            }
            is Unsubscribe -> if (subscribers.remove(c.sub)) drop(c.sub)
            is Viewport -> width = c.width
            is Encoded -> encoder.finished(c.e)?.let { part ->
                lastPart = part
                sent++
                for (s in subscribers) s.parts.trySend(part)
            }
        }
    }

    private fun show(f: LiveFrame?, encoder: FrameEncoder) {
        if (f == null) { last = null; lastPart = null; encoder.reset(); return }
        val gap = f.seq - lastSeq - 1
        lastSeq = f.seq
        last = f
        if (!watched || subscribers.isEmpty()) return
        if (gap > 0) conflated += gap
        encoder.submit(f.image, png = f.rest, width)
    }

    private fun submitLast(encoder: FrameEncoder) {
        if (watched && subscribers.isNotEmpty()) last?.let { encoder.submit(it.image, png = true, width) }
    }

    private suspend fun pump(sub: Subscriber) {
        try {
            sub.out.write("--$BOUNDARY\r\n$PART_HEAD".toByteArray(UTF_8))
            sub.out.flush()
            for (p in sub.parts) {
                sub.out.write(p.bytes)
                sub.out.write("\r\n--$BOUNDARY\r\n$PART_HEAD".toByteArray(UTF_8))
                sub.out.flush()
            }
        } catch (e: Exception) {
            if (e is CancellationException) throw e
            cmds.trySend(Unsubscribe(sub))
        } finally {
            closeQuietly(sub.out)
        }
    }

    private fun replaceStreamOf(viewer: String?) {
        if (viewer == null) return
        val it = subscribers.iterator()
        while (it.hasNext()) it.next().takeIf { s -> s.viewer == viewer }?.let { s -> it.remove(); drop(s) }
    }

    private fun dropSubscribers() {
        for (s in subscribers) drop(s)
        subscribers.clear()
        lastPart = null
    }

    private fun drop(s: Subscriber) {
        s.parts.close()
        s.job.cancel()
        writers.launch(write, CoroutineStart.ATOMIC) { closeQuietly(s.out) }
    }

    private fun closeQuietly(out: OutputStream) {
        runCatching { out.close() }.onFailure { if (it !is IOException) log("구독 연결을 닫지 못했다: $it") }
    }

    companion object {
        const val BOUNDARY = "prevueframe"
        const val PART_HEAD = "Content-Type: image/jpeg\r\n\r\n"
    }
}
