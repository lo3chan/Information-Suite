import re

def main():
    # Upgrade gradle
    filepath = "gradle/wrapper/gradle-wrapper.properties"
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('gradle-7.5.1-all.zip', 'gradle-8.5-all.zip')
    content = content.replace('gradle-7.5.1-bin.zip', 'gradle-8.5-bin.zip')

    with open(filepath, 'w') as f:
        f.write(content)


    # Root build.gradle.kts
    filepath = "build.gradle.kts"
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('jcenter()', '')
    content = content.replace('maven("https://jitpack.io")', '')
    content = content.replace('classpath("com.android.tools.build:gradle:7.3.1")', 'classpath("com.android.tools.build:gradle:8.2.2")\n        classpath("com.google.dagger:hilt-android-gradle-plugin:2.46.1")')
    content = content.replace('classpath("androidx.navigation:navigation-safe-args-gradle-plugin:2.2.1")', 'classpath("androidx.navigation:navigation-safe-args-gradle-plugin:2.7.7")')

    with open(filepath, 'w') as f:
        f.write(content)

    # settings.gradle.kts
    filepath = "settings.gradle.kts"
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace('jcenter()', '')

    with open(filepath, 'w') as f:
        f.write(content)

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

    # app/build.gradle.kts
    filepath = "app/build.gradle.kts"
    with open(filepath, 'r') as f:
        content = f.read()

    content = content.replace("import com.bernaferrari.buildsrc.Libs2", "import com.bernaferrari.buildsrc.Libs2\nimport com.bernaferrari.buildsrc.Android")

    # Remove plugins
    content = re.sub(r'id\("kotlin-android-extensions"\)\n', '', content)

    # Add plugins
    content = re.sub(r'id\("kotlin-kapt"\)\n', 'id("kotlin-kapt")\n    id("dagger.hilt.android.plugin")\n', content)

    # Remove androidExtensions block
    content = re.sub(r'androidExtensions\s*\{\s*isExperimental\s*=\s*true\s*\}\n', '', content)

    # Replace SDKs
    content = content.replace('compileSdkVersion(33)', 'compileSdk = Android.compileSdk\n    namespace = "com.bernaferrari.changedetection"')
    content = content.replace('minSdkVersion(21)', 'minSdk = Android.minSdk')
    content = content.replace('targetSdkVersion(33)', 'targetSdk = Android.targetSdk')

    # Add compose block to android
    compose_block = """
    buildFeatures {
        compose = true
        viewBinding = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.4.7"
    }
"""
    content = content.replace("    buildFeatures.dataBinding = true\n", compose_block)

    # Change JVM targets
    content = content.replace('JavaVersion.VERSION_1_8', 'JavaVersion.VERSION_11')
    content = content.replace('jvmTarget = "1.8"', 'jvmTarget = "11"')

    # Remove bad dependencies
    bad_deps = [
        "Libs2.Epoxy.epoxy", "Libs2.Epoxy.dataBinding", "Libs2.Epoxy.paging", "Libs2.Epoxy.processor",
        "Libs2.MvRx.main",
        "Libs2.Dagger.dagger", "Libs2.Dagger.compiler", "Libs2.Dagger.androidSupport", "Libs2.Dagger.androidProcessor",
        "Libs2.AssistedInject.annotationDagger2", "Libs2.AssistedInject.processorDagger2",
        "Libs2.AndroidX.Navigation.navigationUi", "Libs2.AndroidX.Navigation.navigationFragment",
        "Libs2.RxJava.rxJava", "Libs2.RxJava.rxAndroid", "Libs2.RxJava.rxKotlin", "Libs2.RxJava.rxRelay", "Libs2.RxJava.rxkPrefs",
        "Libs2.alerter", "Libs2.Komprehensions.rxJava",
        '"com.xwray:groupie:$groupie"',
        '"com.yarolegovich:discrete-scrollview:1.4.9"',
        '"com.xwray:groupie-kotlin-android-extensions:$groupie"',
        "val groupie = \"2.4.0\"",
        "Libs2.notify",
        '"com.github.daniel-stoneuk:material-about-library:2.4.2"',
        '"com.davemorrissey.labs:subsampling-scale-image-view:3.10.0"'
    ]
    for bad in bad_deps:
        content = re.sub(r'.*?'+re.escape(bad)+r'.*\n', '', content)

    # Add new dependencies
    new_deps = """
    // Compose
    implementation(platform(Libs2.Compose.bom))
    implementation(Libs2.Compose.ui)
    implementation(Libs2.Compose.material3)
    implementation(Libs2.Compose.uiToolingPreview)
    debugImplementation(Libs2.Compose.uiTooling)
    implementation(Libs2.Compose.activity)
    implementation(Libs2.Compose.navigation)
    implementation(Libs2.Compose.hiltNavigation)
    implementation(Libs2.Compose.foundation)

    // Hilt
    implementation(Libs2.Hilt.android)
    kapt(Libs2.Hilt.compiler)
"""
    content = content.replace("    // Kotlin\n", new_deps + "\n    // Kotlin\n")

    with open(filepath, 'w') as f:
        f.write(content)

    # fix core dependencies
    with open("core_dependencies.gradle", "r") as f:
        content = f.read()

    # Change JVM targets
    content = content.replace('targetCompatibility 1.8', 'targetCompatibility = JavaVersion.VERSION_11')
    content = content.replace('sourceCompatibility 1.8', 'sourceCompatibility = JavaVersion.VERSION_11')

    bad = [
        "Libs2.Epoxy.epoxy", "Libs2.Epoxy.dataBinding", "Libs2.MvRx.main",
        "Libs2.Dagger.dagger", "Libs2.Dagger.androidSupport"
    ]
    for b in bad:
        content = re.sub(r'.*?'+re.escape(b)+r'.*\n', '', content)

    with open("core_dependencies.gradle", "w") as f:
        f.write(content)

    # base/build.gradle
    with open("base/build.gradle", "w") as f:
        f.write('''apply from: '../core_dependencies.gradle'

android {
    namespace "com.bernaferrari.base"
    kotlinOptions {
        jvmTarget = "11"
    }
}
''')

    # base-android/build.gradle
    with open("base-android/build.gradle", "w") as f:
        f.write('''import com.bernaferrari.buildsrc.Libs2
import com.bernaferrari.buildsrc.Android

apply from: '../core_dependencies.gradle'
apply plugin: 'com.android.library'
apply plugin: 'kotlin-android'
apply plugin: 'kotlin-kapt'

android {
    namespace "com.bernaferrari.ui"
    compileSdkVersion Android.compileSdk

    defaultConfig {
        minSdkVersion Android.minSdk
        targetSdkVersion Android.targetSdk
    }

    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {

    implementation project(':base')

    // Google
    implementation Libs2.AndroidX.Lifecycle.liveDataKtx
    implementation Libs2.AndroidX.Lifecycle.viewModel
}
''')

    # repo/build.gradle
    with open("repo/build.gradle", "r") as f:
        content = f.read()

    content = content.replace("androidExtensions {\n    experimental = true\n}", "")
    content = content.replace("apply plugin: 'kotlin-android-extensions'", "")

    content = re.sub(r'android\s*\{', 'android {\n    namespace "com.bernaferrari.repo"\n    kotlinOptions {\n        jvmTarget = "11"\n    }\n', content)

    with open("repo/build.gradle", "w") as f:
        f.write(content)

    # diffutils/build.gradle.kts
    with open("diffutils/build.gradle.kts", "r") as f:
        content = f.read()

    content = re.sub(r'android\s*\{', 'android {\n    namespace = "com.bernaferrari.diffutils"\n    kotlinOptions {\n        jvmTarget = "11"\n    }\n', content)
    content = content.replace('JavaVersion.VERSION_1_8', 'JavaVersion.VERSION_11')
    content = content.replace('jvmTarget = "1.8"', 'jvmTarget = "11"')

    with open("diffutils/build.gradle.kts", "w") as f:
        f.write(content)

    # Base fix
    with open("base/src/main/java/com/bernaferrari/base/misc/OtherExt.kt", "r") as f:
        content = f.read()

    content = content.replace("import androidx.lifecycle.ViewModelProviders", "import androidx.lifecycle.ViewModelProvider")
    content = content.replace("ViewModelProviders.of(this)", "ViewModelProvider(this)")

    with open("base/src/main/java/com/bernaferrari/base/misc/OtherExt.kt", "w") as f:
        f.write(content)

    # Delete bad files
    import os
    for root, dirs, files in os.walk("."):
        if "legacy_archive" in root:
            continue
        for file in files:
            if file == "AndroidManifest.xml":
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    content = f.read()
                content = re.sub(r'package="[^"]+"', '', content)
                with open(filepath, 'w') as f:
                    f.write(content)
            elif file.endswith(".kt") or file.endswith(".java"):
                filepath = os.path.join(root, file)
                with open(filepath, "r") as f:
                    content = f.read()

                if "com.airbnb.epoxy" in content or "com.airbnb.mvrx" in content or "dagger.android" in content:
                    os.remove(filepath)
            elif file.endswith(".xml") and "layout" in root:
                filepath = os.path.join(root, file)
                os.remove(filepath)

if __name__ == "__main__":
    main()
