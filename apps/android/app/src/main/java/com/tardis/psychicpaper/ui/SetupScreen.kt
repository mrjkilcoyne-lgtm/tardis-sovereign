package com.tardis.psychicpaper.ui

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.tardis.psychicpaper.model.Identity

@Composable
fun SetupScreen(onComplete: (Identity) -> Unit) {
    var name by remember { mutableStateOf("") }
    var organisation by remember { mutableStateOf("") }
    var title by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .statusBarsPadding()
            .padding(horizontal = 24.dp, vertical = 32.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        Spacer(modifier = Modifier.height(48.dp))

        Text(
            text = "Psychic Paper",
            style = MaterialTheme.typography.headlineLarge,
            color = Color.White,
            fontWeight = FontWeight.Bold,
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = "Set up your base identity. This will appear\non every credential you generate.",
            style = MaterialTheme.typography.bodyMedium,
            color = Color.White.copy(alpha = 0.5f),
        )

        Spacer(modifier = Modifier.height(40.dp))

        val fieldColors = OutlinedTextFieldDefaults.colors(
            focusedTextColor = Color.White,
            unfocusedTextColor = Color.White,
            cursorColor = MaterialTheme.colorScheme.secondary,
            focusedBorderColor = MaterialTheme.colorScheme.secondary,
            unfocusedBorderColor = Color.White.copy(alpha = 0.2f),
            focusedLabelColor = MaterialTheme.colorScheme.secondary,
            unfocusedLabelColor = Color.White.copy(alpha = 0.5f),
        )

        OutlinedTextField(
            value = name,
            onValueChange = { name = it },
            label = { Text("Your Name") },
            modifier = Modifier.fillMaxWidth(),
            colors = fieldColors,
            shape = RoundedCornerShape(14.dp),
            singleLine = true,
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = title,
            onValueChange = { title = it },
            label = { Text("Title / Role") },
            modifier = Modifier.fillMaxWidth(),
            colors = fieldColors,
            shape = RoundedCornerShape(14.dp),
            singleLine = true,
        )

        Spacer(modifier = Modifier.height(16.dp))

        OutlinedTextField(
            value = organisation,
            onValueChange = { organisation = it },
            label = { Text("Organisation") },
            modifier = Modifier.fillMaxWidth(),
            colors = fieldColors,
            shape = RoundedCornerShape(14.dp),
            singleLine = true,
        )

        Spacer(modifier = Modifier.height(32.dp))

        Button(
            onClick = {
                onComplete(
                    Identity(
                        name = name.trim(),
                        organisation = organisation.trim(),
                        title = title.trim(),
                    )
                )
            },
            enabled = name.isNotBlank(),
            modifier = Modifier
                .fillMaxWidth()
                .height(52.dp),
            shape = RoundedCornerShape(14.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = MaterialTheme.colorScheme.secondary,
                contentColor = Color.Black,
                disabledContainerColor = Color.White.copy(alpha = 0.1f),
                disabledContentColor = Color.White.copy(alpha = 0.3f),
            ),
        ) {
            Text(
                text = "Activate Psychic Paper",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = "Name is required. Other fields are optional.",
            style = MaterialTheme.typography.labelSmall,
            color = Color.White.copy(alpha = 0.3f),
        )
    }
}
