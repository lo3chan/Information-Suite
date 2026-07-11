import com.bernaferrari.buildsrc.Libs2
import java.io.FileInputStream
import java.util.*

plugins {
    id("com.android.application")
    id("kotlin-android")
    id("kotlin-parcelize")
    id("com.google.devtools.ksp") version "1.9.22-1.0.16"
    id("com.github.ben-manes.versions")
}


android {
    namespace = "com.bernaferrari.changedetection"

    compileSdk = 34

    defaultConfig {
        applicationId = "com.bernaferrari.changedetection"
        minSdkVersion(21)
        targetSdkVersion(33)
        versionCode = 34
        versionName = "2.31"
        multiDexEnabled = true
    }

    signingConfigs {
        register("release") {
            val keystorePropertiesFile = file("../ci-dummies/upload-keystore.properties")

            if (!keystorePropertiesFile.exists()) {
                logger.warn("Release builds may not work: signing config not found.")
                return@register
            }

            val keystoreProperties = Properties()
            keystoreProperties.load(FileInputStream(keystorePropertiesFile))

            keyAlias = keystoreProperties["keyAlias"] as String
            keyPassword = keystoreProperties["keyPassword"] as String
            storeFile = file(keystoreProperties["storeFile"] as String)
            storePassword = keystoreProperties["storePassword"] as String
        }
    }

    lintOptions.isAbortOnError = false
    buildFeatures.compose = true
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.10"
    }


    buildTypes {
        named("release") {
            isDebuggable = false
            isMinifyEnabled = true
            isShrinkResources = true

            setProguardFiles(
                listOf(
                    getDefaultProguardFile("proguard-android.txt"),
                    file("proguard-rules.pro")
                )
            )
            val keystorePropertiesFile = file("../ci-dummies/upload-keystore.properties")
            if (keystorePropertiesFile.exists()) {
                signingConfig = signingConfigs.getByName("release")
            }
        }
    }

    kotlinOptions.jvmTarget = "1.8"

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_1_8
        targetCompatibility = JavaVersion.VERSION_1_8
    }
}

dependencies {

    implementation(project(":base"))
    implementation(project(":base-android"))

    implementation(project(":diffutils"))
    implementation(project(":repo"))


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
    ksp(Libs2.Hilt.compiler)

    // Kotlin
    implementation(Libs2.Kotlin.stdlib)
    implementation(Libs2.Coroutines.core)
    implementation(Libs2.Coroutines.rx2)
    implementation(Libs2.Coroutines.android)

    // Epoxy

    // MvRx

    // Glide
    implementation(Libs2.Glide.glide)

    // Dagger




    // AndroidX
    implementation(Libs2.Google.material)
    implementation(Libs2.AndroidX.coreKtx)
    implementation(Libs2.AndroidX.constraintlayout)
    implementation(Libs2.AndroidX.appcompat)
    implementation(Libs2.AndroidX.recyclerview)

    implementation(Libs2.AndroidX.Lifecycle.liveDataKtx)
    implementation(Libs2.AndroidX.Lifecycle.viewModel)


    annotationProcessor(Libs2.AndroidX.Room.compiler)
    ksp(Libs2.AndroidX.Room.compiler)
    implementation(Libs2.AndroidX.Room.runtime)
    implementation(Libs2.AndroidX.Room.roomktx)
    implementation(Libs2.AndroidX.Work.runtimeKtx)
    implementation(Libs2.AndroidX.Work.rxJava)
    implementation(Libs2.AndroidX.Paging.runtimeKtx)
    implementation(Libs2.AndroidX.browser)

    // Logging
    implementation(Libs2.logger)

    // RX

    // Glide
    implementation(Libs2.Glide.glide)
    ksp(Libs2.Glide.compiler)

    // Others
    implementation(Libs2.jsoup)
    implementation(Libs2.MaterialDialogs.core)
    implementation(Libs2.MaterialDialogs.input)
    implementation(Libs2.MaterialDialogs.bottomsheets)

    // UI


    debugImplementation(Libs2.LeakCanary.no_op)
    debugImplementation(Libs2.LeakCanary.no_op)
    releaseImplementation(Libs2.LeakCanary.no_op)


    // Iconics
    implementation("com.mikepenz:iconics-core:3.1.0@aar")
    implementation("com.mikepenz:community-material-typeface:2.0.46.1@aar")
    implementation("com.mikepenz:google-material-typeface:3.0.1.2.original@aar")

    // About


    // RecyclerView

    // Internal
    implementation(Libs2.stetho)
    implementation(Libs2.okHttp)
    implementation(Libs2.okio)
    implementation("org.apache.commons:commons-text:1.8")


    // Others
    implementation(Libs2.threeTenAndroid)
    implementation(Libs2.timeAgo)
    testImplementation(Libs2.junit)
}
