package com.example.pearl.data

private fun d(id: Int, name: String, kind: Kind, flavor: Flavor, cents: Int, saved: Boolean = false) =
    Drink(id, name, kind, flavor, cents, saved)

val menu: List<Drink> = listOf(
    d(1, "Taro Milk Tea", Kind.MILK_TEA, Flavor.TARO, 550, saved = true),
    d(2, "Thai Milk Tea", Kind.MILK_TEA, Flavor.THAI, 530),
    d(3, "Matcha Latte", Kind.MATCHA, Flavor.MATCHA, 550),
    d(4, "Strawberry Yogurt", Kind.YOGURT, Flavor.STRAWBERRY, 580, saved = true),
    d(5, "Mango Smoothie", Kind.SMOOTHIE, Flavor.MANGO, 620, saved = true),
    d(6, "Brown Sugar Latte", Kind.COFFEE, Flavor.BROWN_SUGAR, 590, saved = true),
    d(7, "Peach Oolong", Kind.FRUIT_TEA, Flavor.PEACH, 520),
    d(8, "Lychee Green Tea", Kind.FRUIT_TEA, Flavor.LYCHEE, 520),
    d(9, "Coconut Coffee", Kind.COFFEE, Flavor.COCONUT, 560),
    d(10, "Matcha Strawberry", Kind.MATCHA, Flavor.STRAWBERRY, 610),
    d(11, "Brown Sugar Milk Tea", Kind.MILK_TEA, Flavor.BROWN_SUGAR, 560),
    d(12, "Passion Fruit Tea", Kind.FRUIT_TEA, Flavor.PASSION, 510),
    d(13, "Taro Smoothie", Kind.SMOOTHIE, Flavor.TARO, 600),
    d(14, "Mango Yogurt", Kind.YOGURT, Flavor.MANGO, 590),
    d(15, "Iced Matcha", Kind.MATCHA, Flavor.MATCHA, 500),
    d(16, "Thai Coffee", Kind.COFFEE, Flavor.THAI, 540),
    d(17, "Coconut Milk Tea", Kind.MILK_TEA, Flavor.COCONUT, 560),
    d(18, "Peach Smoothie", Kind.SMOOTHIE, Flavor.PEACH, 610),
    d(19, "Lychee Yogurt", Kind.YOGURT, Flavor.LYCHEE, 590),
    d(20, "Strawberry Milk Tea", Kind.MILK_TEA, Flavor.STRAWBERRY, 570),
)
