pluginManagement {
    repositories {
        google()
        mavenCentral()
        maven("https://maven.pkg.jetbrains.space/public/p/compose/dev")
    }
}

rootProject.name = "eep-ler" // Or a more descriptive name for the whole project

include(":eep-ler-ui")      // Tells Gradle about your new UI module
// If your Python part was also a Gradle module (less common for pure Python), you'd include it here too.