package com.my.salah.tracker.app.ui

import android.content.Context
import android.media.AudioAttributes
import android.media.MediaPlayer
import android.os.Build
import android.os.VibrationEffect
import android.os.Vibrator
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
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.net.URLEncoder
import kotlin.math.cos
import kotlin.math.sin

data class TasbihDua(
    val arabic: String,
    val pronounce: String,
    val meaning: String,
    val defaultLimit: Int
)

val DefaultTasbihDuas = listOf(
    TasbihDua("سُبْحَانَ اللّٰهِ", "Subhan Allah", "Glory be to Allah", 33),
    TasbihDua("الْحَمْدُ لِلّٰهِ", "Alhamdulillah", "All praise is due to Allah", 33),
    TasbihDua("اللّٰهُ أَكْبَرُ", "Allahu Akbar", "Allah is the Greatest", 34),
    TasbihDua("لَا إِلٰهَ إِلَّا اللّٰهُ", "La ilaha illallah", "There is no deity but Allah", 100),
    TasbihDua("أَسْتَغْفِرُ اللّٰهَ", "Astaghfirullah", "I seek forgiveness from Allah", 100),
    TasbihDua("سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ", "Subhan Allahi wa bihamdihi", "Glory & praise be to Allah", 100),
    TasbihDua("سُبْحَانَ اللّٰهِ الْعَظِيمِ", "Subhan Allahil Azeem", "Glory to Allah, The Supreme", 100)
)

@Composable
fun UltraTasbihNeumorphicCard(
    onOpenLimitDialog: (currentLimit: Int, onSave: (Int) -> Unit) -> Unit,
    modifier: Modifier = Modifier
) {
    val context = LocalContext.current
    val sp = remember { context.getSharedPreferences("tasbih_prefs", Context.MODE_PRIVATE) }
    val vibrator = remember { context.getSystemService(Context.VIBRATOR_SERVICE) as? Vibrator }

    var currentDuaIndex by remember {
        mutableIntStateOf(sp.getInt("current_dua_idx", 0).coerceIn(0, DefaultTasbihDuas.size - 1))
    }
    var currentCount by remember {
        mutableIntStateOf(sp.getInt("count_$currentDuaIndex", 0))
    }
    var currentLimit by remember {
        mutableIntStateOf(sp.getInt("limit_$currentDuaIndex", DefaultTasbihDuas[currentDuaIndex].defaultLimit))
    }

    val currentDua = DefaultTasbihDuas[currentDuaIndex]

    // Vibration helper
    val triggerVibrate = { durationMs: Long ->
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vibrator?.vibrate(VibrationEffect.createOneShot(durationMs, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                vibrator?.vibrate(durationMs)
            }
        } catch (_: Exception) {}
    }

    // Audio helper
    var mediaPlayer by remember { mutableStateOf<MediaPlayer?>(null) }
    DisposableEffect(Unit) {
        onDispose {
            mediaPlayer?.release()
            mediaPlayer = null
        }
    }

    val playAudio = {
        try {
            mediaPlayer?.release()
            val text = currentDua.arabic
            val encoded = URLEncoder.encode(text, "UTF-8")
            val url = "https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=ar&q=$encoded"
            val mp = MediaPlayer().apply {
                setAudioAttributes(
                    AudioAttributes.Builder()
                        .setContentType(AudioAttributes.CONTENT_TYPE_SPEECH)
                        .setUsage(AudioAttributes.USAGE_MEDIA)
                        .build()
                )
                setDataSource(url)
                prepareAsync()
                setOnPreparedListener { start() }
            }
            mediaPlayer = mp
        } catch (_: Exception) {}
    }

    // Actions
    val increment: () -> Unit = {
        if (currentCount >= currentLimit) {
            currentCount = 1
            triggerVibrate(80)
        } else {
            currentCount++
            triggerVibrate(30)
        }
        sp.edit().putInt("count_$currentDuaIndex", currentCount).apply()
    }

    val decrement: () -> Unit = {
        if (currentCount > 0) {
            currentCount--
            triggerVibrate(20)
            sp.edit().putInt("count_$currentDuaIndex", currentCount).apply()
        }
    }

    val reset: () -> Unit = {
        currentCount = 0
        triggerVibrate(40)
        sp.edit().putInt("count_$currentDuaIndex", 0).apply()
    }

    val nextDua: () -> Unit = {
        currentDuaIndex = (currentDuaIndex + 1) % DefaultTasbihDuas.size
        sp.edit().putInt("current_dua_idx", currentDuaIndex).apply()
        currentCount = sp.getInt("count_$currentDuaIndex", 0)
        currentLimit = sp.getInt("limit_$currentDuaIndex", DefaultTasbihDuas[currentDuaIndex].defaultLimit)
        triggerVibrate(30)
    }

    val cornerRadius = 20.dp
    val shape = RoundedCornerShape(cornerRadius)

    // Deep Ocean Metallic 3D Card
    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(165.dp)
            .neumorphic3DCard(
                bevelColor = Color(0xFF021A2A),
                ambientShadowColor = Color(0x66032B45),
                cornerRadius = cornerRadius,
                layers = 3,
                topSheenAlpha = 0.4f
            )
            .clip(shape)
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(Color(0xFF0A4F70), Color(0xFF032B45)),
                    start = Offset(0f, 0f),
                    end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                )
            )
            .padding(horizontal = 14.dp, vertical = 8.dp)
    ) {
        // Radial specular sheen on top-right corner
        Canvas(modifier = Modifier.fillMaxSize()) {
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(Color(0x22FFFFFF), Color.Transparent),
                    center = Offset(size.width * 0.85f, size.height * 0.15f),
                    radius = size.width * 0.45f
                ),
                radius = size.width * 0.45f,
                center = Offset(size.width * 0.85f, size.height * 0.15f)
            )
        }

        Row(
            modifier = Modifier.fillMaxSize(),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Left Column: Dua Info & 4 Neumorphic Control Buttons
            Column(
                modifier = Modifier
                    .weight(1.3f)
                    .fillMaxHeight()
                    .padding(top = 10.dp, bottom = 8.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.SpaceBetween
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    modifier = Modifier.padding(top = 4.dp)
                ) {
                    // Arabic Calligraphy with smooth Gaussian blur shadow (Amiri)
                    Text(
                        text = currentDua.arabic,
                        style = androidx.compose.ui.text.TextStyle(
                            fontFamily = AmiriFontFamily,
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFFE2F1F8),
                            shadow = androidx.compose.ui.graphics.Shadow(
                                color = Color(0x99000000),
                                offset = Offset(0f, 4f),
                                blurRadius = 10f
                            )
                        ),
                        maxLines = 1,
                        overflow = TextOverflow.Visible,
                        modifier = Modifier.padding(bottom = 4.dp)
                    )

                    // Divider
                    Box(
                        modifier = Modifier
                            .width(130.dp)
                            .height(1.dp)
                            .background(
                                Brush.horizontalGradient(
                                    listOf(Color.Transparent, Color(0x40FFFFFF), Color.Transparent)
                                )
                            )
                    )

                    Spacer(modifier = Modifier.height(4.dp))

                    // Pronunciation with Neon Glow
                    Text(
                        text = currentDua.pronounce,
                        style = androidx.compose.ui.text.TextStyle(
                            fontFamily = PlusJakartaFontFamily,
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF00FA9A),
                            letterSpacing = 0.5.sp,
                            shadow = androidx.compose.ui.graphics.Shadow(
                                color = Color(0x6600FA9A),
                                blurRadius = 8f
                            )
                        ),
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        textAlign = TextAlign.Center
                    )

                    Spacer(modifier = Modifier.height(2.dp))

                    // Meaning
                    Text(
                        text = currentDua.meaning,
                        fontFamily = PlusJakartaFontFamily,
                        fontSize = 10.5.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFFA4C6DB),
                        maxLines = 2,
                        lineHeight = 12.5.sp,
                        softWrap = true,
                        overflow = TextOverflow.Ellipsis,
                        textAlign = TextAlign.Center
                    )
                }

                // 4 Neumorphic Circular Buttons: Reset, Minus, Audio, Next
                Row(
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    TasbihCircleButton(onClick = { reset() }) {
                        TasbihResetVectorIcon(size = 15.dp, color = Color(0xFF2ECC71))
                    }
                    TasbihCircleButton(onClick = { decrement() }) {
                        TasbihMinusVectorIcon(size = 15.dp, color = Color(0xFFFF6B6B))
                    }
                    TasbihCircleButton(onClick = { playAudio() }) {
                        TasbihAudioVectorIcon(size = 15.dp, color = Color(0xFFFF9F43))
                    }
                    TasbihCircleButton(onClick = { nextDua() }) {
                        TasbihNextVectorIcon(size = 15.dp, color = Color(0xFFA4C6DB))
                    }
                }
            }

                Spacer(modifier = Modifier.width(8.dp))

                // Right Column: Circular 3D Ring Counter & Target Limit Pill
                Column(
                    modifier = Modifier
                        .weight(0.95f)
                        .fillMaxHeight(),
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.Center
                ) {
                    // 3D Ring View
                    TasbihRingComposable(
                        count = currentCount,
                        limit = currentLimit,
                        onClick = increment,
                        modifier = Modifier.size(114.dp)
                    )

                    // Sunken Neumorphic Limit Pill (overlapping circle bottom slightly)
                    Box(
                        modifier = Modifier
                            .offset(y = (-8).dp)
                            .height(24.dp)
                            .clip(RoundedCornerShape(12.dp))
                            .background(
                                Brush.linearGradient(
                                    colors = listOf(Color(0x26FFFFFF), Color(0x40000000))
                                )
                            )
                            .neumorphicInner(
                                darkShadowColor = Color(0x80000000),
                                lightShadowColor = Color(0x33FFFFFF),
                                depth = 1.5.dp,
                                blur = 2.dp,
                                cornerRadius = 12.dp
                            )
                            .border(1.dp, Color(0x33FFFFFF), RoundedCornerShape(12.dp))
                            .clickable {
                                onOpenLimitDialog(currentLimit) { newLimit ->
                                    currentLimit = newLimit
                                    sp.edit().putInt("limit_$currentDuaIndex", newLimit).apply()
                                }
                            }
                            .padding(horizontal = 14.dp),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(
                            text = "/ $currentLimit",
                            style = androidx.compose.ui.text.TextStyle(
                                fontFamily = PlusJakartaFontFamily,
                                fontSize = 13.sp,
                                fontWeight = FontWeight.ExtraBold,
                                color = Color(0xFF8AB4CD),
                                shadow = androidx.compose.ui.graphics.Shadow(
                                    color = Color(0xCC000000),
                                    offset = Offset(1f, 1f),
                                    blurRadius = 3f
                                )
                            )
                        )
                }
            }
        }
    }
}

/**
 * Circular Neumorphic button for Reset, Minus, Audio, Next with Vector Icon support.
 */
@Composable
fun TasbihCircleButton(
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    content: @Composable () -> Unit
) {
    Box(
        modifier = modifier
            .size(30.dp)
            .neumorphicOuter(
                lightShadowColor = Color(0x1AFFFFFF),
                darkShadowColor = Color(0x40000000),
                shadowBlur = 3.dp,
                offsetX = 1.dp,
                offsetY = 1.dp,
                cornerRadius = 15.dp
            )
            .clip(CircleShape)
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(Color(0x2BFFFFFF), Color(0x05FFFFFF)),
                    start = Offset(0f, 0f),
                    end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                )
            )
            .border(1.dp, Color(0x33FFFFFF), CircleShape)
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            ),
        contentAlignment = Alignment.Center
    ) {
        content()
    }
}

/**
 * 3D Ring Canvas:
 * Recessed circular canyon + background track + neon green arc + multi-stop radial specular glass marble + 3D extruded count.
 */
@Composable
fun TasbihRingComposable(
    count: Int,
    limit: Int,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val progress = (count.toFloat() / limit.coerceAtLeast(1)).coerceIn(0f, 1f)
    val animProgress by animateFloatAsState(
        targetValue = progress,
        animationSpec = tween(durationMillis = 200),
        label = "ringProgress"
    )

    Box(
        modifier = modifier
            .background(Color(0x4D0A3C57), CircleShape)
            .neumorphicOuter(
                lightShadowColor = Color(0x0FFFFFFF),
                darkShadowColor = Color(0x66000000),
                shadowBlur = 8.dp,
                offsetX = 3.dp,
                offsetY = 3.dp,
                cornerRadius = 58.dp
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            ),
        contentAlignment = Alignment.Center
    ) {
        Canvas(modifier = Modifier.fillMaxSize()) {
            val cx = size.width / 2f
            val cy = size.height / 2f
            val ringRadius = (size.minDimension / 2f) - 12.dp.toPx()

            // 1. Background translucent track line (matching web's stroke: rgba(255,255,255,0.08))
            drawCircle(
                color = Color(0x1AFFFFFF),
                radius = ringRadius,
                center = Offset(cx, cy),
                style = Stroke(width = 8.dp.toPx())
            )

            // 2. Thick Glowing Neon Progress Arc (matching web's stroke: #00fa9a; stroke-width: 8)
            val sweepAngle = animProgress * 360f
            if (sweepAngle > 0.5f) {
                // A. Wide soft neon halo (simulating filter: drop-shadow(0 0 6px #00fa9a))
                drawArc(
                    color = Color(0x3300FA9A),
                    startAngle = -90f,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = Offset(cx - ringRadius, cy - ringRadius),
                    size = Size(ringRadius * 2f, ringRadius * 2f),
                    style = Stroke(width = 15.dp.toPx(), cap = StrokeCap.Round)
                )

                // B. Medium vibrant green aura
                drawArc(
                    color = Color(0x7700FA9A),
                    startAngle = -90f,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = Offset(cx - ringRadius, cy - ringRadius),
                    size = Size(ringRadius * 2f, ringRadius * 2f),
                    style = Stroke(width = 10.dp.toPx(), cap = StrokeCap.Round)
                )

                // C. Solid emerald core arc (matching web stroke-width 8)
                drawArc(
                    color = Color(0xFF00FA9A),
                    startAngle = -90f,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = Offset(cx - ringRadius, cy - ringRadius),
                    size = Size(ringRadius * 2f, ringRadius * 2f),
                    style = Stroke(width = 7.5.dp.toPx(), cap = StrokeCap.Round)
                )

                // D. Specular center streak
                drawArc(
                    color = Color(0x80E6FFF7),
                    startAngle = -90f,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = Offset(cx - ringRadius, cy - ringRadius),
                    size = Size(ringRadius * 2f, ringRadius * 2f),
                    style = Stroke(width = 2.dp.toPx(), cap = StrokeCap.Round)
                )
            }

            // 3. Large 3D Specular Glass Marble Bead (Matching web exactly, self-contained with no outer bleed)
            val angleRad = Math.toRadians((sweepAngle - 90.0))
            val dotX = cx + (ringRadius * cos(angleRad)).toFloat()
            val dotY = cy + (ringRadius * sin(angleRad)).toFloat()
            val marbleR = 12.dp.toPx() // 24dp diameter, fits completely inside container

            // A. Concentric Multi-Stop Radial Gradient Sphere (3D Glass Marble)
            drawCircle(
                brush = Brush.radialGradient(
                    colorStops = arrayOf(
                        0.00f to Color(0xFFFFFFFF), // 0% specular white glint at 35% 35%
                        0.15f to Color(0xFFE6FFFF), // 15% ice cyan
                        0.38f to Color(0xFF80E5FF), // 38% vivid sky blue
                        0.62f to Color(0xFF0099CC), // 62% electric ocean
                        0.85f to Color(0xFF004D66), // 85% deep teal
                        1.00f to Color(0xFF001A22)  // 100% dark 3D base
                    ),
                    center = Offset(dotX - marbleR * 0.30f, dotY - marbleR * 0.30f),
                    radius = marbleR * 1.35f
                ),
                radius = marbleR,
                center = Offset(dotX, dotY)
            )

            // C. Inset Specular Top-Left Highlight (matching web's inset 3px 3px 8px rgba(255,255,255,0.9))
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(Color(0xF5FFFFFF), Color(0x55FFFFFF), Color.Transparent),
                    center = Offset(dotX - marbleR * 0.35f, dotY - marbleR * 0.35f),
                    radius = marbleR * 0.60f
                ),
                radius = marbleR * 0.60f,
                center = Offset(dotX - marbleR * 0.35f, dotY - marbleR * 0.35f)
            )

            // D. Inset Bottom-Right Shadow (matching web's inset -3px -3px 8px rgba(0,0,0,0.8))
            drawCircle(
                brush = Brush.radialGradient(
                    colors = listOf(Color(0x99000D18), Color(0x33000D18), Color.Transparent),
                    center = Offset(dotX + marbleR * 0.40f, dotY + marbleR * 0.40f),
                    radius = marbleR * 0.75f
                ),
                radius = marbleR * 0.75f,
                center = Offset(dotX + marbleR * 0.40f, dotY + marbleR * 0.40f)
            )
            // NO dark outer stroke: Pure realistic glass marble bead
        }

        // Center Extruded Count with real Gaussian blur shadow
        Text(
            text = count.toString(),
            style = androidx.compose.ui.text.TextStyle(
                fontFamily = OutfitFontFamily,
                fontSize = 34.sp,
                fontWeight = FontWeight.Black,
                color = Color.White,
                shadow = androidx.compose.ui.graphics.Shadow(
                    color = Color(0xB3000000),
                    offset = Offset(0f, 5f),
                    blurRadius = 10f
                )
            )
        )
    }
}
