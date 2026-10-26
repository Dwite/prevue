#!/bin/bash
# 대상 저장소 흉내 — Compose 화면 파일 하나. 가짜 prevue 는 이 파일을 읽지 않지만 에이전트가 읽고 고친다.
set -e
mkdir -p app/src/main/kotlin
touch gradlew settings.gradle.kts app/build.gradle.kts
cat > app/src/main/kotlin/Screen.kt <<'KT'
package demo

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

@Composable
fun Greeting(name: String) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Hello $name")
        Text(text = "Welcome back")
    }
}

@Preview(device = "id:pixel_5")
@Preview(device = "id:pixel_tablet")
@Composable
fun GreetingPreview() = Greeting("Android")

@Preview(device = "id:pixel_5", uiMode = 0x20)
@Preview(device = "id:pixel_tablet", uiMode = 0x20)
@Composable
fun GreetingDarkPreview() = Greeting("Android")
KT
