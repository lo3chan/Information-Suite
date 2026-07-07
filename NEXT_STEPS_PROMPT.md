# Comprehensive Modernization Prompt for Jules

## Context & Current State
You are taking over the modernization of an Android application. The previous agent performed a comprehensive codebase analysis and discovered that a simple 1:1 migration to ViewBinding is impossible due to severe Name Shadowing (the original architecture uses custom property delegates like `var sourceView by BooleanProperty()` that share exact names with XML layout IDs).

Furthermore, the project cannot currently compile because several legacy UI libraries (`com.xwray:groupie:2.4.0`, `com.tapadoo.android:alerter:4.0.3`, `com.yarolegovich:discrete-scrollview:1.4.9`) were hosted on JCenter/Bintray, which have been sunset. The artifacts are unresolvable.

The CI/CD pipeline (GitHub Actions for APK deployment) and a modernization blueprint (`MODERNIZATION.md`) have already been added to the repository.

## Your Goal: Architectural Rewrite
Your objective is to execute the architectural rewrite outlined in `MODERNIZATION.md`. Do not attempt to fix the legacy dependencies or migrate to ViewBinding. You must completely replace the UI layer with **Jetpack Compose**.

### Key Technologies to Implement:
*   **UI:** Jetpack Compose (replaces XML layouts, `Groupie`, and `Alerter`).
*   **Architecture:** MVVM with Unidirectional Data Flow (UDF).
*   **State Management:** Kotlin `StateFlow` and pure Coroutines (replaces RxJava and MvRx).
*   **Dependency Injection:** Hilt (replaces the raw Dagger setup).

### Execution Steps:
1.  **Dependency Overhaul:** Open `build.gradle.kts` and `app/build.gradle.kts`. Remove all legacy dependencies: `groupie`, `groupie-kotlin-android-extensions`, `alerter`, `discrete-scrollview`, `mvrx`, and `rxjava`.
2.  **Add Compose & Hilt:** Add the dependencies for Jetpack Compose, Compose Navigation, Hilt, and Coroutines. Ensure you configure the Compose compiler and Hilt Gradle plugins correctly.
3.  **UI Rewrite (Iterative):**
    *   Start by deleting the XML layouts in `base-android/src/main/res/layout`.
    *   Delete the Groupie items (`MainCardItem`, `RowItem`, etc.) and the complex Fragment delegates (`TextFragment`, `VisualFragment`).
    *   Implement the core UI components as Composable functions. Start with the main list view (previously handled by Groupie and DiscreteScrollView) using `LazyColumn` or `LazyRow`.
4.  **State Management Rewrite:** Replace MvRx State classes with standard Kotlin Data Classes. Expose state from ViewModels using `MutableStateFlow` and collect them in Compose using `collectAsState()`.
5.  **Remove KAPT/Kotlin-Android-Extensions:** Remove `apply plugin: 'kotlin-android-extensions'` as it is deprecated and breaks the build. If Hilt requires annotation processing, use KSP instead of KAPT where possible, or ensure KAPT is configured strictly for Hilt.

### Warnings:
*   Do not waste time trying to make the legacy code compile. The Bintray repositories are dead.
*   Focus on ripping out the old UI layer and replacing it directly with Compose.

Good luck!
