package com.example.pearl.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.sp

object PearlColors {
    val canvas = Color(0xFFFAF9F9)
    val sheet = Color(0xFFFFFFFF)
    val muted = Color(0xFFF6F6F5)
    val line = Color(0xFFEFEEEC)
    val forest = Color(0xFF00664F)
    val forestLight = Color(0xFF0B7A5F)
    val green = Color(0xFF4DC591)
    val orange = Color(0xFFFF7648)
    val orangeSoft = Color(0xFFFFEDE6)
    val orangeInk = Color(0xFFB83C14)
    val ink = Color(0xFF212525)
    val subtle = Color(0xFF6F7583)
    val pearl = Color(0xFF3B2622)
    val shadow = Color(0xFF050621)
}

object PearlType {
    val display = TextStyle(fontSize = 44.sp, fontWeight = FontWeight.Medium)
    val title = TextStyle(fontSize = 24.sp, lineHeight = 32.sp, fontWeight = FontWeight.Bold)
    val price = TextStyle(fontSize = 20.sp, fontWeight = FontWeight.SemiBold)
    val card = TextStyle(fontSize = 16.sp, fontWeight = FontWeight.SemiBold)
    val label = TextStyle(fontSize = 14.sp, fontWeight = FontWeight.SemiBold)
    val body = TextStyle(fontSize = 14.sp, fontWeight = FontWeight.Medium)
    val meta = TextStyle(fontSize = 12.sp, fontWeight = FontWeight.Medium)
    val nav = TextStyle(fontSize = 13.sp, fontWeight = FontWeight.SemiBold)
}

@Composable
fun PearlTheme(content: @Composable () -> Unit) {
    val scheme = lightColorScheme(
        primary = PearlColors.orange,
        background = PearlColors.canvas,
        onBackground = PearlColors.ink,
        surface = PearlColors.sheet,
        onSurface = PearlColors.ink,
    )
    MaterialTheme(colorScheme = scheme, content = content)
}
