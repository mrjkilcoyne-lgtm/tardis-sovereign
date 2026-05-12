package com.tardis.psychicpaper

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.Crossfade
import androidx.compose.animation.core.tween
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import com.tardis.psychicpaper.model.Identity
import com.tardis.psychicpaper.ui.PaperScreen
import com.tardis.psychicpaper.ui.SetupScreen
import com.tardis.psychicpaper.ui.theme.PsychicPaperTheme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            PsychicPaperTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    var setupDone by remember {
                        mutableStateOf(Identity.hasCompletedSetup(this@MainActivity))
                    }

                    Crossfade(
                        targetState = setupDone,
                        animationSpec = tween(400),
                        label = "screen-switch",
                    ) { done ->
                        if (done) {
                            val identity = Identity.load(this@MainActivity)
                            PaperScreen(identity = identity)
                        } else {
                            SetupScreen(
                                onComplete = { identity ->
                                    Identity.save(this@MainActivity, identity)
                                    setupDone = true
                                },
                            )
                        }
                    }
                }
            }
        }
    }
}
