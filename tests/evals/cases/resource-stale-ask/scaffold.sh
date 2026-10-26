#!/bin/bash
# 대상 저장소 흉내 — 화면 파일과 values 하나. 가짜 prevue 는 strings.xml 에 tap_hint 가 생기면 리소스 낡음으로 답한다.
set -e
mkdir -p app/src/main/kotlin app/src/main/res/values
touch gradlew settings.gradle.kts app/build.gradle.kts
cat > app/src/main/res/values/strings.xml <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="welcome">Welcome back</string>
</resources>
XML
cat > app/src/main/kotlin/Screen.kt <<'KT'
package demo

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp

@Composable
fun Greeting(name: String) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Hello $name")
        Text(text = stringResource(R.string.welcome))
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
