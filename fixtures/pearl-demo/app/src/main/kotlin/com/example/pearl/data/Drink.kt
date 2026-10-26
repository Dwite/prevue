package com.example.pearl.data

enum class Kind { FRUIT_TEA, MILK_TEA, MATCHA, COFFEE, SMOOTHIE, YOGURT }

enum class Flavor { TARO, THAI, MATCHA, STRAWBERRY, MANGO, BROWN_SUGAR, PEACH, LYCHEE, PASSION, COCONUT }

data class Drink(
    val id: Int,
    val name: String,
    val kind: Kind,
    val flavor: Flavor,
    val cents: Int,
    val saved: Boolean = false,
)
