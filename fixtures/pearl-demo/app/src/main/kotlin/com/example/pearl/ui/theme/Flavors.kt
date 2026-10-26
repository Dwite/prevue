package com.example.pearl.ui.theme

import androidx.compose.ui.graphics.Color
import com.example.pearl.data.Drink
import com.example.pearl.data.Flavor
import com.example.pearl.data.Kind

data class FlavorColors(val card: Color, val blob: Color, val liquid: Color, val top: Color, val onCard: Color)

private val light = Color(0xFFFFFFFF)
private val dark = Color(0xFF212525)

val Flavor.colors: FlavorColors
    get() = when (this) {
        Flavor.TARO -> FlavorColors(Color(0xFF8F98FF), Color(0xFF5A63D8), Color(0xFFD9D2FF), Color(0xFFF4F1FF), light)
        Flavor.THAI -> FlavorColors(Color(0xFFFF7648), Color(0xFFFFC278), Color(0xFFFFB37A), Color(0xFFFFE7D2), light)
        Flavor.MATCHA -> FlavorColors(Color(0xFF4DC591), Color(0xFF00664F), Color(0xFF9BE3B8), Color(0xFFE4F7EA), dark)
        Flavor.STRAWBERRY -> FlavorColors(Color(0xFFFF8FA3), Color(0xFFFFC2CC), Color(0xFFFFD3DA), Color(0xFFFFF0F3), dark)
        Flavor.MANGO -> FlavorColors(Color(0xFFFFC278), Color(0xFFFF9F45), Color(0xFFFFE08A), Color(0xFFFFF5D6), dark)
        Flavor.BROWN_SUGAR -> FlavorColors(Color(0xFFC98B5E), Color(0xFFA86B43), Color(0xFF8A5A3C), Color(0xFFF3E6DA), light)
        Flavor.PEACH -> FlavorColors(Color(0xFFFFB199), Color(0xFFFF8A6B), Color(0xFFFFD6C7), Color(0xFFFFF1EB), dark)
        Flavor.LYCHEE -> FlavorColors(Color(0xFFF2B5D4), Color(0xFFE48DB8), Color(0xFFFBE3EE), Color(0xFFFFF7FA), dark)
        Flavor.PASSION -> FlavorColors(Color(0xFFFFD25E), Color(0xFFFFB347), Color(0xFFFFE9A6), Color(0xFFFFF8E0), dark)
        Flavor.COCONUT -> FlavorColors(Color(0xFFB8C7D9), Color(0xFF8FA3BD), Color(0xFFEDF1F6), Color(0xFFFFFFFF), dark)
    }

val Drink.colors: FlavorColors get() = flavor.colors

val Kind.label: String
    get() = when (this) {
        Kind.FRUIT_TEA -> "Fruit tea"
        Kind.MILK_TEA -> "Milk tea"
        Kind.MATCHA -> "Matcha"
        Kind.COFFEE -> "Coffee"
        Kind.SMOOTHIE -> "Smoothie"
        Kind.YOGURT -> "Yogurt"
    }

fun price(cents: Int): String = "$%d.%02d".format(cents / 100, cents % 100)
