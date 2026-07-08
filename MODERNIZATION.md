# Android Modernization Strategy

## Current Architecture Overview
The project currently relies on a slightly outdated, hybrid stack combining modern and deprecated Android technologies.

### Key Components:
- **UI:** A mix of Android View system with layout XMLs. It historically relied heavily on the deprecated `kotlinx.android.synthetic` properties. The current (partially complete) migration is attempting to move this to ViewBinding, but it requires substantial manual refactoring, particularly with fragments sharing name spaces between property delegates (`by BooleanProperty()`) and their synthetic layout IDs.
- **Dependency Injection:** Dagger. Specifically `dagger.android` components (`DaggerFragment`, `DaggerApplication`).
- **Background Tasks:** Androidx WorkManager (`WorkerHelper.kt`, `SyncWorker.kt`)
- **Networking/Data:** JSoup for scraping, OkHttp for requests.
- **Database:** AndroidX Room with RxJava integrations (`SnapsDao.kt` mixes LiveData, RxJava Observables, and standard lists).
- **Asynchrony:** A mix of RxJava (RxRelay, RxKotlin) and Kotlin Coroutines/Flows.
- **Lists/Recyclers:** Heavily dependent on the `groupie` library for declarative UI lists, though the specific components are triggering KAPT code generation issues following the ViewBinding migration.
- **Architecture Pattern:** MVVM using Android's `ViewModel` and `LiveData`, interacting with MVI elements (specifically `MvRx`).

## Core Migration Issues & Lessons Learned
The primary roadblock encountered during the `kotlin-android-extensions` to ViewBinding migration involved **Name Shadowing**.
In fragments like `VisualFragment.kt` and `TextFragment.kt`, the original author used custom property delegates to manage UI state:
```kotlin
var showOriginalAndChanges by BooleanProperty(false)
var sourceView by BooleanProperty(false)
```
These names perfectly shadowed the XML IDs of the UI elements (`@+id/showOriginalAndChanges`, `@+id/sourceView`).

When `kotlinx.android.synthetic` was used, `import kotlinx.android.synthetic.main.diff_text_fragment.*` allowed `sourceView` to refer to the view seamlessly, while the local property delegate managed the state. Once we switch to ViewBinding (`binding.controlBar.sourceView`), automated scripts easily corrupt the file by either renaming the state variables, or creating compiler ambiguities (`Overload resolution ambiguity`) if the UI state variable and the binding view share the same context.

Furthermore, replacing the deprecated `groupie-viewbinding` plugin and standardizing the `Item` implementations to `Item<GroupieViewHolder>` caused `kapt` to fail entirely, masking the true source of the error in Dagger or Groupie annotation processing (`InvocationTargetException (no error message)`).

## Proposed Modernization Strategy (Jetpack Compose & Flow)

To fully modernize this app cleanly without resorting to hacky regex ViewBinding replacements, the following architectural rewrite is recommended:

### 1. UI Layer: Jetpack Compose
- **Replace XML entirely:** The complexity of `TextFragment` and `VisualFragment` handling states like `diff`, `revised`, and `original` toggles is incredibly error-prone in XML. Jetpack Compose's declarative nature fits this perfectly.
- **State Management:** Replace the custom `BooleanProperty` delegates with standard Compose `State` or `MutableStateFlow` in the ViewModel.
- **Remove Groupie:** Jetpack Compose's `LazyColumn` and `LazyRow` completely eliminate the need for third-party RecyclerView abstraction libraries like Groupie or Epoxy.

### 2. Architecture: MVVM with Unidirectional Data Flow (UDF)
- Keep the `ViewModel` but remove MvRx.
- Expose UI state as a single data class via a `StateFlow` from the ViewModel to the Compose UI.
```kotlin
data class DiffUiState(
    val isLoading: Boolean = false,
    val showOriginalAndChanges: Boolean = false,
    val sourceViewActive: Boolean = false,
    val diffActive: Boolean = true,
    // ...
)
```

### 3. Asynchrony: 100% Kotlin Coroutines & Flow
- Remove all RxJava dependencies (`rxRelay`, `rxKotlin`, Room Rx integrations).
- Update Room DAOs to return `Flow<List<Snap>>` instead of `Observable` or `LiveData`.
- Replace `SingleLiveEvent` (used for error toasts/snackbars) with Coroutine `Channel` or `SharedFlow`.

### 4. Dependency Injection: Hilt
- Migrate from raw Dagger (`DaggerFragment`) to Hilt. It significantly reduces boilerplate, especially for ViewModels and Compose integration (`hiltViewModel()`).

### Summary
The app's core value is scraping static sites and diffing them. The current UI logic is deeply entangled with deprecated view-binding synthetics and third-party list adapters. A rewrite of the presentation layer to **Jetpack Compose**, backed by **StateFlows** from the ViewModel, will resolve the name-shadowing issues, eliminate the need for Groupie/Epoxy, drastically reduce code size, and modernize the app to current Android standards.
