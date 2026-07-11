with open("app/src/main/java/com/bernaferrari/changedetection/Injector.kt", "w") as f:
    f.write("""package com.bernaferrari.changedetection

import android.content.Context
import android.content.SharedPreferences
import androidx.room.Room
import com.bernaferrari.changedetection.repo.AppExecutors
import com.bernaferrari.changedetection.repo.source.SitesDataSource
import com.bernaferrari.changedetection.repo.source.SitesRepository
import com.bernaferrari.changedetection.repo.source.SnapsDataSource
import com.bernaferrari.changedetection.repo.source.SnapsRepository
import com.bernaferrari.changedetection.repo.source.local.*
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Named
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModuleAR {

    @Provides
    fun provideContext(@ApplicationContext context: Context): Context = context

    @Provides
    fun sharedPrefs(@ApplicationContext context: Context): SharedPreferences {
        return context.getSharedPreferences("workerPreferences", Context.MODE_PRIVATE)
    }
}

@Module
@InstallIn(SingletonComponent::class)
object SitesRepositoryModule {

    @Provides
    @Singleton
    internal fun provideSitesLocalDataSource(
        dao: SitesDao,
        executors: AppExecutors
    ): SitesDataSource = SitesLocalDataSource(executors, dao)

    @Singleton
    @Provides
    internal fun provideSitesDao(db: ChangeDatabase): SitesDao = db.siteDao()
}

@Module
@InstallIn(SingletonComponent::class)
object SnapsRepositoryModule {

    @Provides
    @Singleton
    internal fun provideSnapsLocalDataSource(
        dao: SnapsDao,
        executors: AppExecutors,
        @ApplicationContext context: Context
    ): SnapsDataSource = SnapsLocalDataSource(executors, dao, context)

    @Singleton
    @Provides
    internal fun provideSnapsDao(db: ChangeDatabase): SnapsDao = db.snapsDao()
}

@Module
@InstallIn(SingletonComponent::class)
object RepositoriesMutualDependenciesModule {

    @Singleton
    @Provides
    internal fun provideDb(@ApplicationContext context: Context): ChangeDatabase {
        return Room.databaseBuilder(
            context,
            ChangeDatabase::class.java,
            "Changes.db"
        )
            .build()
    }

    @Singleton
    @Provides
    internal fun provideAppExecutors(): AppExecutors = AppExecutors()
}

""")
