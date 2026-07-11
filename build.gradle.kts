import io.gitlab.arturbosch.detekt.detekt

buildscript {
    repositories {
        google()
        mavenCentral()


    }

    dependencies {
        classpath("com.android.tools.build:gradle:8.2.2")
        classpath("com.google.dagger:hilt-android-gradle-plugin:2.46.1")
        classpath(kotlin("gradle-plugin", version = "1.9.22"))
        classpath("androidx.navigation:navigation-safe-args-gradle-plugin:2.7.7")
        classpath("com.github.ben-manes:gradle-versions-plugin:0.43.0")
    }
}

allprojects {
    repositories {
        google()
        mavenCentral()




    }
}

plugins {
    id("io.gitlab.arturbosch.detekt") version "1.6.0"
}

tasks.register<Delete>("clean").configure {
    delete(rootProject.buildDir)
}

detekt {
    version = "1.6.0"
    input = files("app/")
    config = files("default-detekt-config.yml")
}

subprojects {
    tasks.withType<Javadoc>().configureEach { isEnabled = false }
}
