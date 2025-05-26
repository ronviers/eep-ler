package com.example.eepler // This must match the directory structure and build.gradle.kts

import androidx.compose.material3.MaterialTheme // For basic theming
import androidx.compose.material3.Surface       // A surface container
import androidx.compose.material3.Text          // To display text
import androidx.compose.runtime.Composable     // Marks a function as a Composable UI element
import androidx.compose.ui.window.Window
import androidx.compose.ui.window.application
import androidx.compose.runtime.* // Import remember and mutableStateOf

// import com.example.eepler.App // Import if needed

fun main() = application {
    var isDarkTheme by remember { mutableStateOf(false) } // Default to light, or use isSystemInDarkTheme() here if you want to try auto again

    Window(onCloseRequest = ::exitApplication, title = "EEP-LER UI") {
        App( // Pass the state and toggle function to the App composable
            useDarkTheme = isDarkTheme,
            onThemeToggle = { isDarkTheme = !isDarkTheme }
        )
    }
}
