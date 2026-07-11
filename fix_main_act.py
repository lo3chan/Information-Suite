with open("app/src/main/java/com/bernaferrari/changedetection/MainActivity.kt", "w") as f:
    f.write("""package com.bernaferrari.changedetection

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import dagger.hilt.android.AndroidEntryPoint

@AndroidEntryPoint
class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {

                }
            }
        }
    }

    companion object {
        const val DARKMODE = "dark mode"
        const val LASTCHANGE = "LASTCHANGE"
        const val SITEID = "SITEID"
        const val SNAPID = "SNAPID"
        const val TITLE = "TITLE"
        const val TYPE = "TYPE"
        const val URL = "URL"
        const val TRANSITION = 175L
    }
}
""")
