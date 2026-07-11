# Agent Context & Architecture Guide

## Overview
This application has recently undergone a major architectural rewrite. It has been modernized from an older stack (RxJava, MvRx, Epoxy/Groupie, XML layouts) to a modern, fully-Compose Android architecture.

## Tech Stack
- **UI Toolkit:** Jetpack Compose (Material 3)
- **Navigation:** Jetpack Navigation Compose
- **Dependency Injection:** Dagger Hilt (`@HiltAndroidApp`, `@AndroidEntryPoint`, `@HiltViewModel`)
- **Async/Threading:** Kotlin Coroutines and StateFlow (RxJava has been completely removed)
- **Database:** Room (migrated to KSP)
- **Parcelization:** `kotlin-parcelize` (replacing deprecated `kotlin-android-extensions`)

## Project Structure
- `app/`: Contains the main application module, Jetpack Compose UI screens (`com.bernaferrari.changedetection.ui.*`), Hilt dependency injection setup, and Compose Navigation (`NavGraph.kt`, `Screen.kt`).
- `repo/`: Contains the Data Layer (Room Entities like `Site` and `Snap`, DAOs, Data Sources, and Repositories). The data layer now exposes data primarily through `suspend` functions and `Flow`.
- `base/` & `base-android/`: Common utility modules. Note that all legacy UI base classes (BaseMvRxFragment, etc.) have been deleted.
- `diffutils/`: Contains utilities for computing differences between Snap contents.

## Key Changes & Gotchas for Agents
1. **No XML Layouts:** The app uses 100% Jetpack Compose. Do not attempt to use `findViewById`, DataBinding, ViewBinding, or XML layouts. All UI is written in Kotlin.
2. **No RxJava:** Do not use `Observable`, `Single`, `Completable`, etc. Use Coroutines (`suspend`) for one-shot async operations and `Flow` / `StateFlow` for streams of data.
3. **No MvRx or Epoxy:** The previous architecture used Airbnb's MvRx and Epoxy. These have been deleted. Use standard Android `ViewModel` (annotated with `@HiltViewModel`) and Jetpack Compose `LazyColumn` for lists.
4. **Build System:** The project uses KSP instead of KAPT for Dagger Hilt, Room, and Glide. `buildFeatures.compose = true` is enabled, and `buildFeatures.dataBinding` is disabled.

## How to Build and Run
- `./gradlew assembleDebug` to compile the app.
- Tests can be run normally via Gradle. `lintDebug` is known to have some legacy XML warnings from old layout imports in the `base-android` module, but `assembleDebug` and tests should pass.

When implementing new features or fixing bugs, adhere strictly to the new Jetpack Compose and Coroutines/Flow architecture.
