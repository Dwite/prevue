import org.jetbrains.kotlin.gradle.dsl.JvmTarget

// 순수 Kotlin 모듈 — 프리뷰가 없는 모듈이 그래프에 섞인다.
plugins {
    alias(libs.plugins.kotlin.jvm)
}

java {
    sourceCompatibility = JavaVersion.VERSION_11
    targetCompatibility = JavaVersion.VERSION_11
}

kotlin {
    compilerOptions { jvmTarget.set(JvmTarget.JVM_11) }
}
