with open("base/build.gradle", "w") as f:
    f.write("""apply from: '../core_dependencies.gradle'

android {
    namespace "com.bernaferrari.base"
    compileSdk 34
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }
}
""")
