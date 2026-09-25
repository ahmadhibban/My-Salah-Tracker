package com.my.salah.tracker.app.ui

import android.graphics.BlurMaskFilter
import androidx.compose.animation.core.animateFloatAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.res.ResourcesCompat
import com.my.salah.tracker.app.R

data class PrayerPalette(
    val id: String,
    val name: String,
    val type: String, // "extras" or "sunnah"
    val gradStart: Color,
    val gradEnd: Color,
    val baseDarkBevel: Color
)

val PrayerPalettes = listOf(
    PrayerPalette("fajr", "Fajr", "extras", Color(0xFF7C988F), Color(0xFF5C7B71), Color(0xFF405C53)),
    PrayerPalette("dhuhr", "Dhuhr", "extras", Color(0xFFC2A882), Color(0xFFA38760), Color(0xFF82663F)),
    PrayerPalette("asr", "Asr", "sunnah", Color(0xFF7A8EAA), Color(0xFF5B6F8C), Color(0xFF42536B)),
    PrayerPalette("maghrib", "Maghrib", "extras", Color(0xFFB5848C), Color(0xFF94646B), Color(0xFF73464C)),
    PrayerPalette("isha", "Isha", "sunnah", Color(0xFF6B5551), Color(0xFF4D3A37), Color(0xFF2E1F1C)),
    PrayerPalette("witr", "Witr", "sunnah", Color(0xFF485A6C), Color(0xFF2E3D4C), Color(0xFF1A2530))
)

@Composable
fun NeumorphicPrayerCard(
    palette: PrayerPalette,
    isCompleted: Boolean,
    isJamaat: Boolean,
    subText: String,
    isSubCompleted: Boolean,
    onJamaatToggle: () -> Unit,
    onSubClick: () -> Unit,
    onCheckToggle: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    val cornerRadius = 16.dp
    val shape = RoundedCornerShape(cornerRadius)

    Box(
        modifier = modifier
            .fillMaxWidth()
            .defaultMinSize(minHeight = 44.dp)
            .neumorphic3DCard(
                bevelColor = palette.baseDarkBevel,
                ambientShadowColor = Color(0x33000000),
                cornerRadius = cornerRadius,
                layers = 3,
                topSheenAlpha = 0.45f
            )
            .clip(shape)
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(palette.gradStart, palette.gradEnd),
                    start = Offset(0f, 0f),
                    end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                )
            )
    ) {
        // 1. Organic Marble Veins (Authentic Stone Finish)
        PrayerCardMarbleVeins(prayerId = palette.id, modifier = Modifier.fillMaxSize())

        // 2. Card Content Row
        Row(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 14.dp),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            // Left: Recessed Icon & 3D Prayer Name
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Sunken Icon Slot (30x30 with deep debossed inset shadow and dual-edge rim)
                Box(
                    modifier = Modifier
                        .size(30.dp)
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0x40000000))
                        .neumorphicInner(
                            darkShadowColor = Color(0xD9000000),
                            lightShadowColor = Color(0x4DFFFFFF),
                            depth = 2.5.dp,
                            blur = 3.dp,
                            cornerRadius = 8.dp
                        )
                        .border(
                            1.dp,
                            Brush.verticalGradient(listOf(Color(0x66000000), Color(0x33FFFFFF))),
                            RoundedCornerShape(8.dp)
                        ),
                    contentAlignment = Alignment.Center
                ) {
                    PrayerVectorIcon(prayerId = palette.id, size = 18.dp)
                }

                // Razor-Sharp 3D Metallic Extruded Name
                ExtrudedComposeText(text = palette.name)
            }

            // Right: Jamaat Pill, Sunnah Pill, 3D Lava Checkbox
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                // Jamaat Pill
                NeumorphicPillButton(
                    text = "Jamaat",
                    isActive = isJamaat,
                    activeGradient = listOf(Color(0xFF2B6CB0), Color(0xFF142C4C)),
                    activeTextColor = Color(0xFFBEE3F8),
                    bevelColor = Color(0xFF081524),
                    onClick = onJamaatToggle
                )

                // Sunnah / Extras Pill
                NeumorphicPillButton(
                    text = subText,
                    isActive = isSubCompleted,
                    activeGradient = listOf(Color(0xFF2F855A), Color(0xFF133824)),
                    activeTextColor = Color(0xFF9AE6B4),
                    bevelColor = Color(0xFF0A1F13),
                    onClick = onSubClick
                )

                // 3D Lava Checkbox (Sunken concave socket when unchecked, glowing emerald dome when checked)
                NeumorphicLavaCheckbox(
                    isChecked = isCompleted,
                    onToggle = onCheckToggle
                )
            }
        }
    }
}

/**
 * Organic Marble Veins overlay matching the Web Code project.
 */
@Composable
fun PrayerCardMarbleVeins(prayerId: String, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier) {
        val sx = size.width / 400f
        val sy = size.height / 100f

        when (prayerId.lowercase()) {
            "fajr" -> {
                // Vein 1: Smooth white wave
                val p1 = Path().apply {
                    moveTo(-20f * sx, 80f * sy)
                    cubicTo(100f * sx, -20f * sy, 200f * sx, 120f * sy, 420f * sx, 10f * sy)
                }
                drawPath(
                    path = p1,
                    color = Color.White.copy(alpha = 0.08f),
                    style = Stroke(width = 3.5f * sy, cap = StrokeCap.Round)
                )
                // Vein 2: Subtle dark depth line
                val p2 = Path().apply {
                    moveTo(150f * sx, 120f * sy)
                    cubicTo(250f * sx, 40f * sy, 300f * sx, 80f * sy, 400f * sx, -10f * sy)
                }
                drawPath(
                    path = p2,
                    color = Color.Black.copy(alpha = 0.04f),
                    style = Stroke(width = 1.8f * sy, cap = StrokeCap.Round)
                )
            }
            "dhuhr" -> {
                val p1 = Path().apply {
                    moveTo(0f * sx, 100f * sy)
                    cubicTo(100f * sx, 0f * sy, 250f * sx, 100f * sy, 400f * sx, 0f * sy)
                }
                drawPath(
                    path = p1,
                    color = Color(0xFF5A3A1A).copy(alpha = 0.06f),
                    style = Stroke(width = 2.0f * sy, cap = StrokeCap.Round)
                )
                val p2 = Path().apply {
                    moveTo(80f * sx, -20f * sy)
                    cubicTo(180f * sx, 80f * sy, 250f * sx, 20f * sy, 350f * sx, 120f * sy)
                }
                drawPath(
                    path = p2,
                    color = Color.White.copy(alpha = 0.09f),
                    style = Stroke(width = 3.2f * sy, cap = StrokeCap.Round)
                )
            }
            "asr" -> {
                val p1 = Path().apply {
                    moveTo(-50f * sx, 40f * sy)
                    cubicTo(100f * sx, -10f * sy, 200f * sx, 110f * sy, 450f * sx, 30f * sy)
                }
                drawPath(
                    path = p1,
                    color = Color.Black.copy(alpha = 0.04f),
                    style = Stroke(width = 1.8f * sy, cap = StrokeCap.Round)
                )
                val p2 = Path().apply {
                    moveTo(100f * sx, 120f * sy)
                    cubicTo(200f * sx, 20f * sy, 300f * sx, 80f * sy, 400f * sx, -20f * sy)
                }
                drawPath(
                    path = p2,
                    color = Color.White.copy(alpha = 0.09f),
                    style = Stroke(width = 3.5f * sy, cap = StrokeCap.Round)
                )
            }
            "maghrib" -> {
                val p1 = Path().apply {
                    moveTo(-20f * sx, 50f * sy)
                    quadraticBezierTo(150f * sx, 120f * sy, 420f * sx, 20f * sy)
                }
                drawPath(
                    path = p1,
                    color = Color.White.copy(alpha = 0.08f),
                    style = Stroke(width = 3.8f * sy, cap = StrokeCap.Round)
                )
                val p2 = Path().apply {
                    moveTo(50f * sx, 120f * sy)
                    quadraticBezierTo(200f * sx, -20f * sy, 350f * sx, 120f * sy)
                }
                drawPath(
                    path = p2,
                    color = Color(0xFF6B0014).copy(alpha = 0.05f),
                    style = Stroke(width = 2.0f * sy, cap = StrokeCap.Round)
                )
            }
            "isha" -> {
                val p1 = Path().apply {
                    moveTo(-30f * sx, 25f * sy)
                    cubicTo(80f * sx, 85f * sy, 200f * sx, -10f * sy, 430f * sx, 65f * sy)
                }
                drawPath(
                    path = p1,
                    color = Color.White.copy(alpha = 0.06f),
                    style = Stroke(width = 3.0f * sy, cap = StrokeCap.Round)
                )
                val p2 = Path().apply {
                    moveTo(40f * sx, 105f * sy)
                    cubicTo(160f * sx, 25f * sy, 270f * sx, 85f * sy, 420f * sx, 15f * sy)
                }
                drawPath(
                    path = p2,
                    color = Color.White.copy(alpha = 0.06f),
                    style = Stroke(width = 3.0f * sy, cap = StrokeCap.Round)
                )
                val p3 = Path().apply {
                    moveTo(0f * sx, 55f * sy)
                    cubicTo(130f * sx, 15f * sy, 240f * sx, 105f * sy, 400f * sx, 35f * sy)
                }
                drawPath(
                    path = p3,
                    color = Color.Black.copy(alpha = 0.06f),
                    style = Stroke(width = 2.0f * sy, cap = StrokeCap.Round)
                )
            }
            "witr" -> {
                val p1 = Path().apply {
                    moveTo(-20f * sx, 100f * sy)
                    cubicTo(150f * sx, -40f * sy, 250f * sx, 120f * sy, 420f * sx, 20f * sy)
                }
                drawPath(
                    path = p1,
                    color = Color.Black.copy(alpha = 0.04f),
                    style = Stroke(width = 1.8f * sy, cap = StrokeCap.Round)
                )
                val p2 = Path().apply {
                    moveTo(100f * sx, 120f * sy)
                    cubicTo(250f * sx, 20f * sy, 300f * sx, 80f * sy, 450f * sx, -20f * sy)
                }
                drawPath(
                    path = p2,
                    color = Color.White.copy(alpha = 0.08f),
                    style = Stroke(width = 3.5f * sy, cap = StrokeCap.Round)
                )
            }
        }
    }
}

/**
 * Renders Sunken Pill (when idle/alone) vs Embossed 3D Glowing Pill (when active/completed).
 */
@Composable
fun NeumorphicPillButton(
    text: String,
    isActive: Boolean,
    activeGradient: List<Color>,
    activeTextColor: Color,
    bevelColor: Color,
    onClick: () -> Unit
) {
    val pillShape = RoundedCornerShape(20.dp)

    Box(
        modifier = Modifier
            .height(26.dp)
            .then(
                if (isActive) {
                    Modifier
                        .stacked3DBevel(
                            bevelColor = bevelColor,
                            ambientShadowColor = Color(0x99000000),
                            cornerRadius = 20.dp,
                            layers = 3,
                            hasTopHighlight = true
                        )
                        .clip(pillShape)
                        .background(
                            Brush.verticalGradient(activeGradient)
                        )
                        .border(
                            1.2.dp,
                            Brush.verticalGradient(listOf(Color(0xE6FFFFFF), Color(0x26FFFFFF))),
                            pillShape
                        )
                } else {
                    Modifier
                        .stacked3DBevel(
                            bevelColor = Color(0x66000000),
                            ambientShadowColor = Color(0x4D000000),
                            cornerRadius = 20.dp,
                            layers = 1,
                            hasTopHighlight = true
                        )
                        .clip(pillShape)
                        .background(
                            Brush.verticalGradient(listOf(Color(0x2EFFFFFF), Color(0x40000000)))
                        )
                        .border(
                            1.dp,
                            Brush.verticalGradient(listOf(Color(0x80FFFFFF), Color(0x20FFFFFF))),
                            pillShape
                        )
                }
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            )
            .padding(horizontal = 11.dp),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = text,
            fontFamily = PlusJakartaFontFamily,
            fontSize = 11.5.sp,
            fontWeight = FontWeight.ExtraBold,
            color = if (isActive) activeTextColor else Color(0xFFF1F5F9),
            style = androidx.compose.ui.text.TextStyle(
                shadow = androidx.compose.ui.graphics.Shadow(
                    color = Color(0xCC000000),
                    offset = Offset(1f, 1.5f),
                    blurRadius = 2.5f
                )
            )
        )
    }
}

/**
 * 3D Lava Checkbox: Deep sunken socket with prominent 2px dark border when unchecked,
 * and glowing convex emerald lava dome when checked (matching web code).
 */
@Composable
fun NeumorphicLavaCheckbox(
    isChecked: Boolean,
    onToggle: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    val animProgress by animateFloatAsState(
        targetValue = if (isChecked) 1f else 0f,
        animationSpec = tween(durationMillis = 200),
        label = "lavaScale"
    )

    Box(
        modifier = modifier
            .size(24.dp)
            .clip(CircleShape)
            .background(Color(0x40000000))
            .then(
                if (!isChecked) {
                    Modifier
                        .neumorphicInner(
                            darkShadowColor = Color(0xE6000000),
                            lightShadowColor = Color(0x59FFFFFF),
                            depth = 2.5.dp,
                            blur = 2.5.dp,
                            cornerRadius = 12.dp
                        )
                        .border(
                            1.5.dp,
                            Brush.verticalGradient(listOf(Color(0x80000000), Color(0x4DFFFFFF))),
                            CircleShape
                        )
                } else {
                    Modifier
                }
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = { onToggle(!isChecked) }
            ),
        contentAlignment = Alignment.Center
    ) {
        if (animProgress > 0.05f) {
            Canvas(modifier = Modifier.fillMaxSize()) {
                val cx = size.width / 2f
                val cy = size.height / 2f
                val rLava = (size.minDimension / 2f - 2.dp.toPx()) * animProgress

                // 1. Subtle Green Glow Halo
                drawCircle(
                    color = Color(0x802EEA72),
                    radius = rLava + 3.dp.toPx()
                )

                // 2. Convex 3D Lava Dome (Gradient: #5DF598 to #159C4C)
                drawCircle(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFF5DF598), Color(0xFF159C4C)),
                        start = Offset(cx - rLava, cy - rLava),
                        end = Offset(cx + rLava, cy + rLava)
                    ),
                    radius = rLava,
                    center = Offset(cx, cy)
                )

                // 3. Specular upper-left sheen glint
                drawCircle(
                    brush = Brush.radialGradient(
                        colors = listOf(Color(0xCCFFFFFF), Color.Transparent),
                        center = Offset(cx - rLava * 0.35f, cy - rLava * 0.35f),
                        radius = rLava * 0.7f
                    ),
                    radius = rLava * 0.7f,
                    center = Offset(cx - rLava * 0.35f, cy - rLava * 0.35f)
                )

                // 4. Centered Crisp White Checkmark
                if (animProgress > 0.5f) {
                    val s = animProgress
                    val path = Path().apply {
                        moveTo(cx - 3.2.dp.toPx() * s, cy - 0.2.dp.toPx() * s)
                        lineTo(cx - 0.8.dp.toPx() * s, cy + 2.4.dp.toPx() * s)
                        lineTo(cx + 3.6.dp.toPx() * s, cy - 2.4.dp.toPx() * s)
                    }
                    drawPath(
                        path = path,
                        color = Color.White,
                        style = Stroke(width = 2.2.dp.toPx(), cap = StrokeCap.Round, join = StrokeJoin.Round)
                    )
                }
            }
        }
    }
}

/**
 * Razor-Sharp 3D Extruded Text using Native Paint rendering:
 * Perfectly reproduces CSS:
 * text-shadow: 0px 1px 0px rgba(0,0,0,0.8), 0px 2px 0px #64748B, 0px 3px 0px #475569, 0px 4px 0px #334155, 0px 6px 5px rgba(0,0,0,0.6);
 * with ZERO subpixel blurring or double-edge artifacts!
 */
@Composable
fun ExtrudedComposeText(
    text: String,
    modifier: Modifier = Modifier,
    fontSizeSp: Float = 16.5f
) {
    val context = LocalContext.current
    val density = LocalDensity.current

    val typeface = remember {
        try {
            ResourcesCompat.getFont(context, R.font.outfit_black)
                ?: ResourcesCompat.getFont(context, R.font.outfit_bold)
                ?: android.graphics.Typeface.DEFAULT_BOLD
        } catch (_: Exception) {
            android.graphics.Typeface.DEFAULT_BOLD
        }
    }

    val textSizePx = with(density) { fontSizeSp.sp.toPx() }
    val shadowBlurPx = with(density) { 3.dp.toPx() }
    val off1 = with(density) { 0.4.dp.toPx() }
    val off2 = with(density) { 0.8.dp.toPx() }
    val off3 = with(density) { 1.3.dp.toPx() }
    val off4 = with(density) { 1.8.dp.toPx() }
    val offShadow = with(density) { 2.6.dp.toPx() }

    val paint = remember(typeface, textSizePx) {
        android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
            this.typeface = typeface
            this.textSize = textSizePx
            this.letterSpacing = 0.03f
        }
    }

    val textWidth = remember(text, paint) { paint.measureText(text) }
    val fontMetrics = remember(paint) { paint.fontMetrics }
    val textHeight = remember(fontMetrics) { fontMetrics.bottom - fontMetrics.top + offShadow + 4f }
    val textBaseline = remember(fontMetrics) { -fontMetrics.top }

    Canvas(
        modifier = modifier
            .width(with(density) { (textWidth + 4f).toDp() })
            .height(with(density) { textHeight.toDp() })
    ) {
        drawIntoCanvas { canvas ->
            val nativeCanvas = canvas.nativeCanvas

            // 1. Ambient blurred drop shadow: 0px 6px 5px rgba(0,0,0,0.6)
            paint.maskFilter = BlurMaskFilter(shadowBlurPx, BlurMaskFilter.Blur.NORMAL)
            paint.color = android.graphics.Color.argb(153, 0, 0, 0)
            nativeCanvas.drawText(text, 0f, textBaseline + offShadow, paint)

            paint.maskFilter = null

            // 2. Bevel layer 4: #334155
            paint.color = android.graphics.Color.rgb(0x33, 0x41, 0x55)
            nativeCanvas.drawText(text, 0f, textBaseline + off4, paint)

            // 3. Bevel layer 3: #475569
            paint.color = android.graphics.Color.rgb(0x47, 0x55, 0x69)
            nativeCanvas.drawText(text, 0f, textBaseline + off3, paint)

            // 4. Bevel layer 2: #64748B
            paint.color = android.graphics.Color.rgb(0x64, 0x74, 0x8B)
            nativeCanvas.drawText(text, 0f, textBaseline + off2, paint)

            // 5. Bevel layer 1: rgba(0,0,0,0.8)
            paint.color = android.graphics.Color.argb(204, 0, 0, 0)
            nativeCanvas.drawText(text, 0f, textBaseline + off1, paint)

            // 6. Foreground crisp text: #F8FAFC
            paint.color = android.graphics.Color.rgb(0xF8, 0xFA, 0xFC)
            nativeCanvas.drawText(text, 0f, textBaseline, paint)
        }
    }
}
