#!/usr/bin/env python3
# README 맨 위 숏폼 WebP 를 녹화 한 판과 그 판의 에이전트 세션 로그로 굽는다.
#   python3 fixtures/pearl-demo/edit.py <녹화.mp4> <세션.jsonl> <출력.webp>
# 판마다 아래 표(PROMPT_AT · HOOK · STORY · DONE_AT)를 다시 잡는다 — 시각은 모두 녹화 기준 초다.
# 필요: ffmpeg · img2webp · rsvg-convert (이 ffmpeg 에는 drawtext 가 없어 글자는 SVG 로 그려 겹친다)
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime

W, H, FPS = 1600, 1004, 15
SRC_W, SRC_H = 3024, 1898
QUALITY, BUDGET = (65, 60, 55), 9 * 1048576

# 프롬프트를 보낸 순간 — 시계의 0, 세션 로그 시각을 녹화 시각으로 옮기는 기준
PROMPT_AT = 11.7

# (시작, 끝, 출력 초) — 출력 초가 원본 길이보다 길면 마지막 프레임을 그만큼 멈춘다(그동안 시계도 멈춘다).
# 컷마다 확대 배율이 바뀌면 어디를 볼지 흐려져 화면은 늘 창 전체다
HOOK = [(322.0, 322.8, 0.8), (334.0, 334.8, 0.8), (346.0, 346.6, 0.6), (374.0, 375.0, 1.0)]
STORY = [
    (3.0, 11.7, 1.5), (11.7, 14.0, 1.0),
    (14.0, 110.5, 1.5), (110.5, 112.5, 2.0),
    (112.5, 142.8, 1.0), (142.8, 144.8, 2.0), (144.8, 236.0, 1.2),
    (236.0, 282.8, 0.8), (282.8, 284.8, 2.0), (284.8, 319.3, 1.0),
    (319.3, 320.8, 1.5), (320.8, 329.7, 0.2), (329.7, 331.2, 1.5), (331.2, 342.0, 0.2),
    (342.0, 343.5, 1.5), (343.5, 354.0, 0.2), (354.0, 355.5, 1.5), (355.5, 366.3, 0.2),
    (366.3, 368.8, 4.0),
]
FADE = 0.3

# 단계마다 목표 문장과 끝났을 때 문장, 그리고 끝난 녹화 시각(에이전트가 다음 조각으로 넘어간다고 말한 순간)
GOALS = [
    "Read the design and plan the Home screen",
    "Draw the cup \u2014 straw, ice and pearls",
    "Build the drink card \u2014 flavor color, cup, name, price",
    "Assemble the screen \u2014 header, picks, chips, grid, nav",
    "Check it on phone, foldable and tablet",
]
DONE = ["Design read \u2014 three pieces planned", "Cup matches the design", "Drink card matches the design",
        "Home screen matches the design", "Works on every screen"]
DONE_AT = [99.2, 114.8, 188.4, 315.2, 368.8]
HOOK_LINE = "Built from one prompt \u2014 now on every screen"

DEVICES = {"s26": "Galaxy S26", "duo": "iPhone Duo", "tablet": "Pixel Tablet", "pixel9": "Pixel 9", "fold8": "Galaxy Z Fold8"}
SANS = "Helvetica Neue, Helvetica, Arial, sans-serif"
INK, SUB, ORANGE, BODY = "#1D1B19", "#6E6A64", "#D97757", "#C15F3C"
THOUGHT_MIN = round(2.0 * FPS)
CROSS = 4


def run(*cmd):
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def first_sentence(text, limit=78):
    t = re.sub(r"[*`_]", "", text.strip().split("\n")[0])
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    t = m.group(1) if m else t
    if len(t) > limit:
        t = t[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"
    return t


def action(name, inp):
    name_of = lambda p: os.path.basename(p or "")
    if name == "Artifact":
        return "look", "Reading the design"
    if name == "Write":
        return "type", f"Writing {name_of(inp.get('file_path'))}"
    if name == "Edit":
        return "type", f"Fixing {name_of(inp.get('file_path'))}"
    if name == "Read":
        p = inp.get("file_path", "")
        return ("look", "Looking at the render") if p.endswith(".png") else ("look", f"Reading {name_of(p)}")
    if name == "Bash":
        cmd = inp.get("command", "")
        dev = re.search(r"--device\s+(\w+)", cmd)
        if dev:
            d = DEVICES.get(dev.group(1), dev.group(1))
            return "look", f"Checking {d}" + (" · folded" if "--folded" in cmd else "")
        if re.search(r"prevue\S*\s+(show|wait|start|reload|render|card)\b", cmd):
            return "draw", "Rendering it in Prevue"
        if ".kt" in cmd and (">>" in cmd or "> " in cmd):
            return "type", "Editing the code"
    return None


def caption_events(log):
    rows = [json.loads(l) for l in open(log) if l.strip()]
    t0 = None
    out = []
    for r in rows:
        if "timestamp" not in r:
            continue
        t = datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00"))
        msg = r.get("message") or {}
        content = msg.get("content")
        if t0 is None:
            if r.get("type") == "user" and isinstance(content, str):
                t0 = t
            continue
        if r.get("type") != "assistant" or not isinstance(content, list):
            continue
        at = (t - t0).total_seconds() + PROMPT_AT
        for c in content:
            if c.get("type") == "text" and c["text"].strip():
                out.append((at, "think", first_sentence(c["text"])))
            elif c.get("type") == "tool_use":
                a = action(c["name"], c.get("input") or {})
                if a:
                    out.append((at, *a))
    return out


# Claude Code 마스코트 — 원본 도트 비율(몸통 130x72, 팔 20x20, 눈 8x20, 다리 8x24). 생각 · 타이핑 · 보기를 프레임 f 로 돌린다
def mascot(kind, f, x, y, k):
    r = lambda rx, ry, w, h, c, extra="": f'<rect x="{x + rx * k:.1f}" y="{y + ry * k:.1f}" width="{w * k:.1f}" height="{h * k:.1f}" fill="{c}"{extra}/>'
    circ = lambda cx, cy, rr, extra: f'<circle cx="{x + cx * k:.1f}" cy="{y + cy * k:.1f}" r="{rr * k:.1f}" {extra}/>'
    out = r(20, 10, 130, 72, BODY) + "".join(r(lx, 82, 8, 24, BODY) for lx in (30, 42, 120, 132))
    if kind == "think":
        # 오른팔을 턱에, 눈은 위로, 생각 풍선의 점이 하나씩 찬다
        out += r(0, 50, 20, 20, BODY) + r(150, 30, 20, 20, BODY) + r(140, 40, 12, 12, BODY)
        out += r(44, 21, 8, 16, "#111") + r(124, 21, 8, 16, "#111")
        out += circ(166, 2, 4, 'fill="#fff" stroke="#CFC9C0" stroke-width="1.2"') + circ(178, -10, 6, 'fill="#fff" stroke="#CFC9C0" stroke-width="1.2"')
        out += r(176, -46, 66, 30, "#fff", ' rx="8" stroke="#CFC9C0" stroke-width="1.2"')
        out += "".join(circ(193 + i * 16, -31, 4, f'fill="{SUB}"') for i in range(f % 3 + 1))
    elif kind == "type":
        # 몸 앞 키보드 — 두 팔이 번갈아 누르고 누른 키가 빛난다, 눈은 아래로
        down = f % 2
        out += r(0, 56 + (8 if down else 0), 20, 20, BODY) + r(150, 56 + (0 if down else 8), 20, 20, BODY)
        out += r(40, 37, 8, 16, "#111") + r(120, 37, 8, 16, "#111")
        out += r(4, 84, 162, 22, "#3B3A38", ' rx="3"')
        for row in range(2):
            for c in range(9):
                lit = (row == down and c == (2 if down else 6))
                out += r(10 + c * 17.5, 88 + row * 9, 14, 6, ORANGE if lit else "#8A8680", ' rx="1"')
    else:
        # 돋보기를 들고 좌우로 훑는다 — 눈이 돋보기를 따라간다
        side = 1 if f % 2 else -1
        out += r(0, 50, 20, 20, BODY) + r(150, 40, 20, 20, BODY)
        out += r(44 + 4 * side, 29, 8, 20, "#111") + r(124 + 4 * side, 29, 8, 20, "#111")
        lx = 196 + 10 * side
        out += f'<line x1="{x + 168 * k:.1f}" y1="{y + 50 * k:.1f}" x2="{x + (lx - 10) * k:.1f}" y2="{y + 30 * k:.1f}" stroke="#6E6A64" stroke-width="{6 * k:.1f}" stroke-linecap="round"/>'
        out += circ(lx, 18, 16, f'fill="#fff" fill-opacity=".55" stroke="#6E6A64" stroke-width="{5 * k:.1f}"')
    return out


def popup_svg(step, done, now_fill, line, checked, pop, thought, alpha, kind, a, rise, op=1.0):
    w, h = 1024, 132
    x, y = (W - w) / 2, H - h - 34 + rise
    tx = x + 150
    segs = ""
    for i in range(len(GOALS)):
        sx = tx + 108 + i * 34
        segs += f'<rect x="{sx}" y="{y + 25}" width="30" height="5" rx="2.5" fill="{INK}" fill-opacity=".14"/>'
        f = 1.0 if i < done else (now_fill if i == done else 0.0)
        if f > 0:
            segs += f'<rect x="{sx}" y="{y + 25}" width="{30 * f:.1f}" height="5" rx="2.5" fill="{ORANGE}"/>'
    check = ""
    lx = tx
    if checked:
        cx, cy = tx + 13, y + 64
        check = (f'<g transform="translate({cx} {cy}) scale({pop:.2f})"><circle r="13" fill="{ORANGE}"/>'
                 f'<path d="M-6 0 L-2 4.5 L6.5 -5" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>')
        lx = tx + 36
    return (f'<g opacity="{op:.2f}"><defs><filter id="sh" x="-10%" y="-30%" width="120%" height="180%"><feDropShadow dx="0" dy="10" stdDeviation="16" flood-color="#000" flood-opacity=".35"/></filter></defs>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#fff" fill-opacity=".95" filter="url(#sh)"/>'
            + mascot(kind, a, x + 22, y + 46, 0.5)
            + f'<text x="{tx}" y="{y + 32}" font-family="{SANS}" font-size="15" font-weight="bold" letter-spacing="1" fill="{SUB}">STEP {step + 1} OF {len(GOALS)}</text>'
            + segs + check
            + f'<text x="{lx}" y="{y + 72}" font-family="{SANS}" font-size="27" font-weight="bold" fill="{INK}">{esc(line)}</text>'
            + (f'<text x="{tx}" y="{y + 108}" font-family="{SANS}" font-size="20" fill="{SUB}" fill-opacity="{alpha:.2f}">\u201c{esc(thought)}\u201d</text>' if thought else "") + "</g>")


def clock_svg(clock):
    if clock is None:
        return ""
    m, s = divmod(int(clock), 60)
    return (f'<rect x="{W - 176}" y="{24}" width="152" height="54" rx="16" fill="#fff" fill-opacity=".95"/>'
            f'<text x="{W - 158}" y="{58}" font-family="{SANS}" font-size="14" fill="{SUB}">real time</text>'
            f'<text x="{W - 40}" y="{60}" text-anchor="end" font-family="{SANS}" font-size="24" font-weight="bold" fill="{INK}">{m}:{s:02d}</text>')


def cut(src, tmp, n, start, end, secs):
    span = end - start
    count = max(1, round(secs * FPS))
    moved = max(1, round(span * FPS)) if secs >= span else count
    seg = os.path.join(tmp, f"seg{n:03d}")
    os.mkdir(seg)
    speed = span / (moved / FPS)
    run("ffmpeg", "-v", "error", "-ss", f"{start}", "-t", f"{span}", "-i", src,
        "-vf", f"setpts=PTS/{speed},fps={FPS},scale={W}:{H}:flags=lanczos",
        "-frames:v", str(moved), os.path.join(seg, "%04d.png"))
    got = sorted(os.listdir(seg))
    return [(os.path.join(seg, got[min(i, len(got) - 1)]), start + min(i, moved - 1) * speed / FPS) for i in range(count)]


def main(src, log, out):
    events = caption_events(log)
    tmp = tempfile.mkdtemp(prefix="pearl-edit-")
    try:
        frames = []
        for n, c in enumerate(HOOK):
            frames += [(f, t, "hook") for f, t in cut(src, tmp, n, *c)]
        for n, c in enumerate(STORY):
            frames += [(f, t, "story") for f, t in cut(src, tmp, 100 + n, *c)]
        # 끝에서 처음으로 — 마지막 프레임과 첫 프레임을 섞어 루프 이음새를 감춘다
        last, first = frames[-1][0], frames[0][0]
        k = round(FADE * FPS)
        for i in range(1, k + 1):
            f = os.path.join(tmp, f"fade{i}.png")
            run("ffmpeg", "-v", "error", "-i", last, "-i", first, "-filter_complex",
                f"blend=all_expr='A*(1-{i / (k + 1)})+B*{i / (k + 1)}'", "-frames:v", "1", f)
            frames.append((f, None, "fade"))

        final = os.path.join(tmp, "final")
        os.mkdir(final)
        thoughts = [(t, text) for t, kind, text in events if kind == "think"]
        acts = [(t, kind) for t, kind, _ in events if kind != "think"]
        story_start = next(i for i, fr in enumerate(frames) if fr[2] == "story")
        starts = [PROMPT_AT] + DONE_AT[:-1]
        shown, held, prev, fade_in, done_seen, cache = None, THOUGHT_MIN, None, CROSS, {}, {}
        for i, (f, t, part) in enumerate(frames):
            a = (i // 4) % 2
            # 맨 앞 미리보기가 끝나면 팝업이 내려가며 사라지고, 본편은 1단계부터 새로 올라온다 — 되감지 않는다
            enter = i if part == "hook" else (i - story_start if part == "story" else 99)
            leave = story_start - i if part == "hook" else 99
            op = min(1.0, (enter + 1) / 3, leave / 3)
            rise = round((1 - op) * 18)
            if part == "story":
                done = sum(1 for d in DONE_AT if t >= d)
                step = min(done, len(GOALS) - 1)
                now_fill = 0.0 if done >= len(GOALS) else min(1.0, max(0.0, (t - starts[done]) / (DONE_AT[done] - starts[done])))
                # 막 끝난 단계는 0.8초 동안 체크와 끝 문장을 보인다
                for j in range(done):
                    done_seen.setdefault(j, i)
                last = max((j for j in range(done) if i - done_seen.get(j, -99) < round(0.8 * FPS)), default=None)
                if last is not None:
                    step, line, checked = last, DONE[last], True
                    pop = [0.0, 0.6, 1.2, 1.08, 1.0][min(4, i - done_seen[last])]
                else:
                    line, checked, pop = GOALS[step], done >= len(GOALS), 1.0
                    if checked:
                        line = DONE[-1]
                latest = next((x for x in reversed(thoughts) if x[0] <= t), None)
                if latest and latest[1] != shown and held >= THOUGHT_MIN:
                    shown, held, fade_in = latest[1], 0, 0
                held += 1
                fade_in += 1
                alpha = min(1.0, fade_in / CROSS)
                act = next((k for tt, k in reversed(acts) if tt <= t), "look")
                kind = "think" if latest and t - latest[0] < 1.5 else ("type" if act == "type" else "look")
                clock = t - PROMPT_AT if t >= PROMPT_AT else None
                svg_body = popup_svg(step, done, now_fill, line, checked, pop, shown, alpha, kind, i // 4, rise, op) + clock_svg(clock)
            else:
                svg_body = popup_svg(len(GOALS) - 1, len(GOALS), 1.0, HOOK_LINE, True, 1.0, None, 1.0, "look", i // 4, rise, op)
            svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{svg_body}</svg>'
            if svg not in cache:
                p = os.path.join(tmp, f"ov{len(cache)}")
                with open(p + ".svg", "w") as fh:
                    fh.write(svg)
                run("rsvg-convert", "-o", p + ".png", p + ".svg")
                cache[svg] = p + ".png"
            run("ffmpeg", "-v", "error", "-i", f, "-i", cache[svg], "-filter_complex", "overlay",
                "-frames:v", "1", os.path.join(final, f"{i:04d}.png"))

        names = [os.path.join(final, x) for x in sorted(os.listdir(final))]
        # 손실 애니메이션은 투명으로 비운 자리의 RGB 를 바꾸면 앞 프레임이 잔상으로 남는다 — -exact
        for q in QUALITY:
            run("img2webp", "-loop", "0", "-lossy", "-q", str(q), "-m", "6", "-exact", "-d", str(round(1000 / FPS)), *names, "-o", out)
            if os.path.getsize(out) <= BUDGET:
                break
        print(f"{out}  {len(names)}프레임 {len(names) / FPS:.1f}초 q{q} {os.path.getsize(out) / 1048576:.2f}MB")
        # WebP 프레임은 바뀐 조각만 담아 눈으로 보기 어렵다 — 검토용으로 다 그린 프레임을 남긴다
        keep = os.environ.get("PEARL_EDIT_FRAMES")
        if keep:
            shutil.copytree(final, keep, dirs_exist_ok=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit("python3 fixtures/pearl-demo/edit.py <녹화.mp4> <세션.jsonl> <출력.webp>")
    main(*sys.argv[1:])
