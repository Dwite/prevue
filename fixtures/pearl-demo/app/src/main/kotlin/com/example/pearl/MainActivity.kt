package com.example.pearl

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import com.example.pearl.ui.home.HomeScreen
import com.example.pearl.ui.theme.PearlTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            PearlTheme {
                HomeScreen()
            }
        }
    }
}
