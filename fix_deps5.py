import re

filepath = "app/build.gradle.kts"
with open(filepath, 'r') as f:
    content = f.read()

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
