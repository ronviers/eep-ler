plugins {
    kotlin("multiplatform") version "1.9.23" // Or the latest stable Kotlin version
    id("org.jetbrains.compose") version "1.6.1" // Or the latest stable Compose version
}

kotlin {
    jvm("desktop") { // Target for desktop application
        compilations.all {
            kotlinOptions.jvmTarget = "11" // Or a newer LTS version like "17"
        }
    }
    // Add js(IR) or other targets later if needed

    sourceSets {
        val commonMain by getting {
            dependencies {
                implementation(compose.runtime)
                implementation(compose.foundation)
                implementation(compose.material3) // For Material Design 3
                implementation(compose.ui)
                // Ktor and Serialization will be added here later
            }
        }
        val desktopMain by getting {
            dependencies {
                implementation(compose.desktop.currentOs)
            }
        }
    }
}

compose.desktop {
    application {
        mainClass = "com.example.eepler.MainKt" // We'll create this file next
        nativeDistributions {
            targetFormats(org.jetbrains.compose.desktop.application.dsl.TargetFormat.Dmg, org.jetbrains.compose.desktop.application.dsl.TargetFormat.Msi, org.jetbrains.compose.desktop.application.dsl.TargetFormat.Deb)
            packageName = "EEP-LER"
            packageVersion = "1.0.0"
        }
    }
}