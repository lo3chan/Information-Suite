with open("diffutils/build.gradle.kts", "w") as f:
    f.write("""import org.jetbrains.kotlin.config.KotlinCompilerVersion

plugins {
    id("com.android.library")
    id("kotlin-android")
}

android {
    namespace = "com.bernaferrari.diffutils"

    compileSdk = 34

    defaultConfig {
        minSdk = 21
    }

    buildTypes {
        named("release") {
            isMinifyEnabled = true
            setProguardFiles(
                listOf(
                    getDefaultProguardFile("proguard-android-optimize.txt"),
                    file("proguard-rules.pro")
                )
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {
    implementation(kotlin("stdlib", KotlinCompilerVersion.VERSION))
}""")

with open("repo/build.gradle", "w") as f:
    f.write("""import com.bernaferrari.buildsrc.Android
import com.bernaferrari.buildsrc.Libs2

apply plugin: 'com.android.library'
apply plugin: 'kotlin-android'
apply plugin: 'com.google.devtools.ksp'

android {
    namespace "com.bernaferrari.repo"

    compileSdk 34

    defaultConfig {
        minSdkVersion Android.minSdk
        targetSdkVersion 34
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
    kotlinOptions {
        jvmTarget = "11"
    }
}

dependencies {

    // Kotlin
    implementation Libs2.Kotlin.stdlib
    implementation Libs2.Coroutines.core
    implementation Libs2.Coroutines.android

    // Room
    implementation Libs2.AndroidX.Room.runtime
    implementation Libs2.AndroidX.Room.roomktx
    implementation Libs2.AndroidX.Room.rxjava2
    ksp Libs2.AndroidX.Room.compiler

    // Paging
    implementation Libs2.AndroidX.Paging.common
    implementation Libs2.AndroidX.Paging.rxjava2

    // LiveData
    implementation Libs2.AndroidX.Lifecycle.liveDataKtx
    implementation Libs2.AndroidX.Lifecycle.viewModel

    // Logs
    implementation Libs2.logger

    // Parsing
    implementation Libs2.jsoup
}""")

with open("base-android/build.gradle", "w") as f:
    f.write("""import com.bernaferrari.buildsrc.Libs2
import com.bernaferrari.buildsrc.Android

apply from: '../core_dependencies.gradle'
apply plugin: 'com.android.library'
apply plugin: 'kotlin-android'

android {
    namespace "com.bernaferrari.ui"
    compileSdk 34

    defaultConfig {
        minSdkVersion Android.minSdk
        targetSdkVersion 34
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
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
}""")
