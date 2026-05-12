package com.tardis.psychicpaper.ui

import androidx.compose.animation.animateColorAsState
import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.graphicsLayer
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.tardis.psychicpaper.model.DocumentLayout
import com.tardis.psychicpaper.model.DocumentType
import com.tardis.psychicpaper.model.Identity

@Composable
fun DocumentCard(
    documentType: DocumentType,
    identity: Identity,
    modifier: Modifier = Modifier,
) {
    val animPrimary by animateColorAsState(
        targetValue = documentType.primaryColor,
        animationSpec = tween(500),
        label = "primary",
    )
    val animAccent by animateColorAsState(
        targetValue = documentType.accentColor,
        animationSpec = tween(500),
        label = "accent",
    )
    val animBg by animateColorAsState(
        targetValue = documentType.backgroundColor,
        animationSpec = tween(500),
        label = "card-bg",
    )
    val animTextPrimary by animateColorAsState(
        targetValue = documentType.textPrimary,
        animationSpec = tween(500),
        label = "text-primary",
    )
    val animTextSecondary by animateColorAsState(
        targetValue = documentType.textSecondary,
        animationSpec = tween(500),
        label = "text-secondary",
    )

    // Subtle rotation on morph
    val rotation by animateFloatAsState(
        targetValue = 0f,
        animationSpec = tween(600),
        label = "rotation",
    )

    val cornerRadius = when (documentType.layout) {
        DocumentLayout.BADGE -> 20.dp
        DocumentLayout.TICKET -> 16.dp
        DocumentLayout.CARD -> 14.dp
        DocumentLayout.FULL -> 12.dp
    }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .graphicsLayer { rotationY = rotation }
            .animateContentSize(animationSpec = tween(500))
            .clip(RoundedCornerShape(cornerRadius))
            .background(
                Brush.verticalGradient(
                    colors = listOf(
                        animBg,
                        animPrimary.copy(alpha = 0.15f),
                    )
                )
            )
            .border(
                width = 1.dp,
                color = animPrimary.copy(alpha = 0.4f),
                shape = RoundedCornerShape(cornerRadius),
            )
            .padding(1.dp),
    ) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(24.dp),
        ) {
            when (documentType.layout) {
                DocumentLayout.BADGE -> BadgeLayout(documentType, identity, animPrimary, animAccent, animTextPrimary, animTextSecondary)
                DocumentLayout.TICKET -> TicketLayout(documentType, identity, animPrimary, animAccent, animTextPrimary, animTextSecondary)
                DocumentLayout.CARD -> CardLayout(documentType, identity, animPrimary, animAccent, animTextPrimary, animTextSecondary)
                DocumentLayout.FULL -> FullLayout(documentType, identity, animPrimary, animAccent, animTextPrimary, animTextSecondary)
            }
        }
    }
}

// ---------------------------------------------------------------------------
// Badge layout (press pass, security badge, conference badge)
// ---------------------------------------------------------------------------

@Composable
private fun BadgeLayout(
    type: DocumentType,
    identity: Identity,
    primary: Color,
    accent: Color,
    textPrimary: Color,
    textSecondary: Color,
) {
    Column(
        modifier = Modifier.fillMaxWidth(),
        horizontalAlignment = Alignment.CenterHorizontally,
    ) {
        // Issuer header
        Text(
            text = type.issuer,
            style = MaterialTheme.typography.labelSmall,
            color = accent,
            letterSpacing = 2.sp,
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Photo placeholder
        Box(
            modifier = Modifier
                .size(72.dp)
                .clip(CircleShape)
                .background(primary.copy(alpha = 0.3f))
                .border(2.dp, accent.copy(alpha = 0.5f), CircleShape),
            contentAlignment = Alignment.Center,
        ) {
            Text(
                text = identity.name.take(1).uppercase(),
                style = MaterialTheme.typography.headlineMedium,
                color = textPrimary,
                fontWeight = FontWeight.Bold,
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Name
        Text(
            text = identity.name.uppercase().ifBlank { "JOHN SMITH" },
            style = MaterialTheme.typography.headlineMedium,
            color = textPrimary,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center,
        )

        if (identity.title.isNotBlank()) {
            Text(
                text = identity.title,
                style = MaterialTheme.typography.bodyMedium,
                color = textSecondary,
            )
        }

        Spacer(modifier = Modifier.height(20.dp))

        HorizontalDivider(color = primary.copy(alpha = 0.3f))

        Spacer(modifier = Modifier.height(16.dp))

        // Fields in two-column grid
        FieldGrid(
            fields = type.fields,
            identity = identity,
            textPrimary = textPrimary,
            textSecondary = textSecondary,
            accent = accent,
        )
    }
}

// ---------------------------------------------------------------------------
// Ticket layout (event ticket, boarding pass)
// ---------------------------------------------------------------------------

@Composable
private fun TicketLayout(
    type: DocumentType,
    identity: Identity,
    primary: Color,
    accent: Color,
    textPrimary: Color,
    textSecondary: Color,
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        // Header bar
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = type.issuer,
                style = MaterialTheme.typography.labelSmall,
                color = accent,
                letterSpacing = 2.sp,
            )
            Text(
                text = type.icon,
                fontSize = 24.sp,
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Name large
        Text(
            text = identity.name.uppercase().ifBlank { "JOHN SMITH" },
            style = MaterialTheme.typography.headlineLarge,
            color = textPrimary,
            fontWeight = FontWeight.Bold,
        )

        Spacer(modifier = Modifier.height(4.dp))

        if (identity.organisation.isNotBlank()) {
            Text(
                text = identity.organisation,
                style = MaterialTheme.typography.bodyMedium,
                color = textSecondary,
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        // Dashed divider effect
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(1.dp)
                .drawBehind {
                    val dashWidth = 8.dp.toPx()
                    val gapWidth = 6.dp.toPx()
                    var x = 0f
                    while (x < size.width) {
                        drawLine(
                            color = primary.copy(alpha = 0.5f),
                            start = Offset(x, 0f),
                            end = Offset((x + dashWidth).coerceAtMost(size.width), 0f),
                            strokeWidth = 1.dp.toPx(),
                        )
                        x += dashWidth + gapWidth
                    }
                }
        )

        Spacer(modifier = Modifier.height(16.dp))

        FieldGrid(
            fields = type.fields,
            identity = identity,
            textPrimary = textPrimary,
            textSecondary = textSecondary,
            accent = accent,
        )
    }
}

// ---------------------------------------------------------------------------
// Card layout (driving licence, membership, transport pass)
// ---------------------------------------------------------------------------

@Composable
private fun CardLayout(
    type: DocumentType,
    identity: Identity,
    primary: Color,
    accent: Color,
    textPrimary: Color,
    textSecondary: Color,
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        // Header
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Box(
                modifier = Modifier
                    .size(40.dp)
                    .clip(RoundedCornerShape(8.dp))
                    .background(primary.copy(alpha = 0.3f)),
                contentAlignment = Alignment.Center,
            ) {
                Text(text = type.icon, fontSize = 20.sp)
            }

            Spacer(modifier = Modifier.width(12.dp))

            Column {
                Text(
                    text = type.displayName.uppercase(),
                    style = MaterialTheme.typography.labelSmall,
                    color = accent,
                    letterSpacing = 1.5.sp,
                )
                Text(
                    text = type.issuer,
                    style = MaterialTheme.typography.labelSmall,
                    color = textSecondary.copy(alpha = 0.5f),
                    fontSize = 9.sp,
                )
            }
        }

        Spacer(modifier = Modifier.height(20.dp))

        // Name
        Text(
            text = identity.name.uppercase().ifBlank { "JOHN SMITH" },
            style = MaterialTheme.typography.headlineMedium,
            color = textPrimary,
            fontWeight = FontWeight.Bold,
        )

        Spacer(modifier = Modifier.height(16.dp))

        HorizontalDivider(color = primary.copy(alpha = 0.2f))

        Spacer(modifier = Modifier.height(16.dp))

        FieldGrid(
            fields = type.fields,
            identity = identity,
            textPrimary = textPrimary,
            textSecondary = textSecondary,
            accent = accent,
        )
    }
}

// ---------------------------------------------------------------------------
// Full layout (permit, invitation)
// ---------------------------------------------------------------------------

@Composable
private fun FullLayout(
    type: DocumentType,
    identity: Identity,
    primary: Color,
    accent: Color,
    textPrimary: Color,
    textSecondary: Color,
) {
    Column(modifier = Modifier.fillMaxWidth()) {
        // Centered header
        Text(
            text = type.icon,
            fontSize = 32.sp,
            modifier = Modifier.align(Alignment.CenterHorizontally),
        )

        Spacer(modifier = Modifier.height(8.dp))

        Text(
            text = type.issuer,
            style = MaterialTheme.typography.labelSmall,
            color = accent,
            letterSpacing = 3.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth(),
        )

        Spacer(modifier = Modifier.height(16.dp))

        Text(
            text = identity.name.ifBlank { "John Smith" },
            style = MaterialTheme.typography.headlineLarge,
            color = textPrimary,
            fontWeight = FontWeight.Bold,
            textAlign = TextAlign.Center,
            modifier = Modifier.fillMaxWidth(),
        )

        if (identity.title.isNotBlank()) {
            Text(
                text = identity.title,
                style = MaterialTheme.typography.bodyMedium,
                color = textSecondary,
                textAlign = TextAlign.Center,
                modifier = Modifier.fillMaxWidth(),
            )
        }

        Spacer(modifier = Modifier.height(20.dp))

        HorizontalDivider(color = primary.copy(alpha = 0.3f))

        Spacer(modifier = Modifier.height(16.dp))

        // Full-width fields (single column)
        type.fields.forEach { label ->
            FieldItem(
                label = label,
                value = fieldPlaceholder(label, identity),
                textPrimary = textPrimary,
                textSecondary = textSecondary,
            )
            Spacer(modifier = Modifier.height(12.dp))
        }
    }
}

// ---------------------------------------------------------------------------
// Shared helpers
// ---------------------------------------------------------------------------

@Composable
private fun FieldGrid(
    fields: List<String>,
    identity: Identity,
    textPrimary: Color,
    textSecondary: Color,
    accent: Color,
) {
    val pairs = fields.chunked(2)
    pairs.forEach { row ->
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp),
        ) {
            row.forEach { label ->
                Column(modifier = Modifier.weight(1f)) {
                    FieldItem(
                        label = label,
                        value = fieldPlaceholder(label, identity),
                        textPrimary = textPrimary,
                        textSecondary = textSecondary,
                    )
                }
            }
            // Fill empty space if odd number
            if (row.size == 1) {
                Spacer(modifier = Modifier.weight(1f))
            }
        }
        Spacer(modifier = Modifier.height(12.dp))
    }
}

@Composable
private fun FieldItem(
    label: String,
    value: String,
    textPrimary: Color,
    textSecondary: Color,
) {
    Column {
        Text(
            text = label,
            style = MaterialTheme.typography.labelSmall,
            color = textSecondary,
            letterSpacing = 1.sp,
        )
        Spacer(modifier = Modifier.height(2.dp))
        Text(
            text = value,
            style = MaterialTheme.typography.bodyLarge,
            color = textPrimary,
            fontWeight = FontWeight.Medium,
        )
    }
}

/**
 * Generates placeholder values for fields based on the user's identity.
 * In a real build, these would come from user input or generation logic.
 */
private fun fieldPlaceholder(label: String, identity: Identity): String {
    val upper = label.uppercase()
    return when {
        upper.contains("NAME") || upper == "PASSENGER" || upper == "HOLDER" ||
            upper == "ATTENDEE" || upper == "MEMBER" || upper == "GUEST" -> identity.name.ifBlank { "John Smith" }
        upper.contains("TITLE") || upper == "ROLE" -> identity.title.ifBlank { "Authorised Personnel" }
        upper.contains("COMPANY") || upper.contains("ORGANISATION") ||
            upper.contains("OUTLET") || upper == "FACILITY" -> identity.organisation.ifBlank { "TARDIS Corp" }
        upper.contains("NO.") || upper == "REF" || upper == "SERIAL" -> "PP-${(1000..9999).random()}"
        upper.contains("DATE") || upper == "ISSUED" || upper.contains("FROM") ||
            upper == "BOARDING" -> "2026-04-04"
        upper.contains("EXPIRES") || upper.contains("VALID") || upper.contains("TO") -> "2027-04-04"
        upper == "CLASS" -> "A/B"
        upper == "CLEARANCE" -> "LEVEL 5"
        upper == "ACCESS LEVEL" -> "ALL AREAS"
        upper == "TIER" -> "GOLD"
        upper == "ZONE" -> "1 - 6"
        upper == "GATE" -> "42"
        upper == "SEAT" -> "14A"
        upper == "FLIGHT" -> "TB 963"
        upper == "SINCE" -> "2019"
        upper == "PASS TYPE" -> "UNLIMITED"
        upper == "PERMIT TYPE" -> "GENERAL ACCESS"
        upper.contains("ISSUED BY") -> "The Authority"
        upper == "HOST" -> "The Doctor"
        upper == "TIME" -> "19:00"
        upper == "VENUE" -> "The Great Hall"
        upper == "EVENT" -> "Special Occasion"
        upper == "CONFERENCE" -> "TARDISConf 2026"
        upper == "DRESS CODE" -> "Black Tie"
        upper == "DATE OF BIRTH" -> "1963-11-23"
        upper == "CONDITIONS" -> "No restrictions"
        else -> "---"
    }
}
