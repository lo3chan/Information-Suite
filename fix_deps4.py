import re

# dependencies.kt
filepath = "buildSrc/src/main/java/com/bernaferrari/buildsrc/dependencies.kt"
with open(filepath, 'r') as f:
    content = f.read()

compose_h = """    object Compose {
    const val version = "1.4.3"
    const val material3Version = "1.1.1"
    const val navigationVersion = "2.7.7"

    val bom = "androidx.compose:compose-bom:2023.06.01"
    val ui = "androidx.compose.ui:ui"
    val material3 = "androidx.compose.material3:material3"
    val uiToolingPreview = "androidx.compose.ui:ui-tooling-preview"
    val uiTooling = "androidx.compose.ui:ui-tooling"
    val navigation = "androidx.navigation:navigation-compose:$navigationVersion"
    val activity = "androidx.activity:activity-compose:1.7.2"
    val hiltNavigation = "androidx.hilt:hilt-navigation-compose:1.0.0"
    val foundation = "androidx.compose.foundation:foundation"
}

object Hilt {
    const val version = "2.46.1"
    val android = "com.google.dagger:hilt-android:$version"
    val compiler = "com.google.dagger:hilt-android-compiler:$version"
}
"""
content = content.replace("    object RxJava {", compose_h + "\n    object RxJava {")
with open(filepath, 'w') as f:
    f.write(content)
