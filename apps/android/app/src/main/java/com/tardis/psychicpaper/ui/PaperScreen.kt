package com.tardis.psychicpaper.ui

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Search
import androidx.compose.material3.FilterChip
import androidx.compose.material3.FilterChipDefaults
import androidx.compose.material3.Icon
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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.tardis.psychicpaper.model.ContextDetector
import com.tardis.psychicpaper.model.DocumentType
import com.tardis.psychicpaper.model.Identity

@Composable
fun PaperScreen(identity: Identity) {
    var situationText by remember { mutableStateOf("") }
    var selectedType by remember { mutableStateOf(DocumentType.DEFAULT) }
    var manualOverride by remember { mutableStateOf(false) }

    val activeType = if (manualOverride) {
        selectedType
    } else if (situationText.isNotBlank()) {
        ContextDetector.detect(situationText)
    } else {
        selectedType
    }

    val animatedBg by animateColorAsState(
        targetValue = activeType.backgroundColor,
        animationSpec = tween(600),
        label = "bg-color",
    )

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.verticalGradient(
                    colors = listOf(animatedBg, Color(0xFF0A0A0A)),
                    startY = 0f,
                    endY = 1200f,
                )
            )
    ) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .statusBarsPadding()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 20.dp, vertical = 16.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
        ) {
            // Title
            Text(
                text = "Psychic Paper",
                style = MaterialTheme.typography.headlineLarge,
                color = Color.White,
                fontWeight = FontWeight.Bold,
            )

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = "It shows them whatever I want them to see.",
                style = MaterialTheme.typography.bodyMedium,
                color = Color.White.copy(alpha = 0.5f),
            )

            Spacer(modifier = Modifier.height(20.dp))

            // Situation input
            OutlinedTextField(
                value = situationText,
                onValueChange = {
                    situationText = it
                    manualOverride = false
                },
                modifier = Modifier.fillMaxWidth(),
                placeholder = {
                    Text(
                        "Describe the situation...",
                        color = Color.White.copy(alpha = 0.4f),
                    )
                },
                leadingIcon = {
                    Icon(
                        Icons.Default.Search,
                        contentDescription = null,
                        tint = Color.White.copy(alpha = 0.5f),
                    )
                },
                colors = OutlinedTextFieldDefaults.colors(
                    focusedTextColor = Color.White,
                    unfocusedTextColor = Color.White,
                    cursorColor = activeType.accentColor,
                    focusedBorderColor = activeType.primaryColor,
                    unfocusedBorderColor = Color.White.copy(alpha = 0.2f),
                ),
                shape = RoundedCornerShape(14.dp),
                singleLine = true,
            )

            Spacer(modifier = Modifier.height(16.dp))

            // Quick-select pills
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .horizontalScroll(rememberScrollState()),
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                DocumentType.entries.forEach { type ->
                    FilterChip(
                        selected = activeType == type,
                        onClick = {
                            selectedType = type
                            manualOverride = true
                        },
                        label = {
                            Text(
                                text = "${type.icon} ${type.displayName}",
                                style = MaterialTheme.typography.labelLarge,
                            )
                        },
                        colors = FilterChipDefaults.filterChipColors(
                            containerColor = Color.White.copy(alpha = 0.06f),
                            labelColor = Color.White.copy(alpha = 0.7f),
                            selectedContainerColor = type.primaryColor.copy(alpha = 0.3f),
                            selectedLabelColor = Color.White,
                        ),
                        border = FilterChipDefaults.filterChipBorder(
                            borderColor = Color.White.copy(alpha = 0.1f),
                            selectedBorderColor = type.primaryColor,
                            enabled = true,
                            selected = activeType == type,
                        ),
                    )
                }
            }

            Spacer(modifier = Modifier.height(28.dp))

            // The morphing document card
            DocumentCard(
                documentType = activeType,
                identity = identity,
            )

            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
