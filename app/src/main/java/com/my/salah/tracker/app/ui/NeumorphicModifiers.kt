package com.my.salah.tracker.app.ui

import android.graphics.BlurMaskFilter
import android.graphics.Path
import android.graphics.RectF
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.interaction.collectIsPressedAsState
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.composed
import androidx.compose.ui.draw.drawBehind
import androidx.compose.ui.draw.drawWithContent
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.drawscope.drawIntoCanvas
import androidx.compose.ui.graphics.nativeCanvas
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalDensity
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Color utility extensions for dynamic Neumorphic shadow derivation.
 */
fun Color.lighten(factor: Float = 0.35f): Color {
    val r = red + (1f - red) * factor
    val g = green + (1f - green) * factor
    val b = blue + (1f - blue) * factor
    return Color(r.coerceIn(0f, 1f), g.coerceIn(0f, 1f), b.coerceIn(0f, 1f), alpha)
}

fun Color.darken(factor: Float = 0.35f): Color {
    val r = red * (1f - factor)
    val g = green * (1f - factor)
    val b = blue * (1f - factor)
    return Color(r.coerceIn(0f, 1f), g.coerceIn(0f, 1f), b.coerceIn(0f, 1f), alpha)
}

/**
 * Renders Dual Soft UI / Neumorphic Outer Shadows (Light Top-Left + Dark Bottom-Right).
 */
fun Modifier.neumorphicOuter(
    lightShadowColor: Color = Color(0xFFFFFFFF).copy(alpha = 0.85f),
    darkShadowColor: Color = Color(0xFF9EA3A8).copy(alpha = 0.55f),
    shadowBlur: Dp = 6.dp,
    offsetX: Dp = 3.dp,
    offsetY: Dp = 3.dp,
    cornerRadius: Dp = 14.dp
): Modifier = composed {
    val density = LocalDensity.current
    val blurPx = with(density) { shadowBlur.toPx() }.coerceAtLeast(1f)
    val offXPx = with(density) { offsetX.toPx() }
    val offsetYPx = with(density) { offsetY.toPx() }
    val cornerPx = with(density) { cornerRadius.toPx() }

    this.drawBehind {
        drawIntoCanvas { canvas ->
            val nativeCanvas = canvas.nativeCanvas
            val paint = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
                style = android.graphics.Paint.Style.FILL
            }

            val w = size.width
            val h = size.height

            // 1. Dark Shadow (Bottom-Right)
            paint.color = darkShadowColor.toArgb()
            paint.maskFilter = BlurMaskFilter(blurPx, BlurMaskFilter.Blur.NORMAL)
            nativeCanvas.drawRoundRect(
                offXPx,
                offsetYPx,
                w + offXPx,
                h + offsetYPx,
                cornerPx,
                cornerPx,
                paint
            )

            // 2. Light Highlight (Top-Left)
            paint.color = lightShadowColor.toArgb()
            paint.maskFilter = BlurMaskFilter(blurPx, BlurMaskFilter.Blur.NORMAL)
            nativeCanvas.drawRoundRect(
                -offXPx,
                -offsetYPx,
                w - offXPx,
                h - offsetYPx,
                cornerPx,
                cornerPx,
                paint
            )
        }
    }
}

/**
 * Renders True Inner / Inset Shadow (Recessed sunken canyon / slot).
 */
fun Modifier.neumorphicInner(
    darkShadowColor: Color = Color(0xB3000000),
    lightShadowColor: Color = Color(0x26FFFFFF),
    depth: Dp = 2.5.dp,
    blur: Dp = 3.dp,
    cornerRadius: Dp = 14.dp
): Modifier = composed {
    val density = LocalDensity.current
    val depthPx = with(density) { depth.toPx() }.coerceAtLeast(1f)
    val blurPx = with(density) { blur.toPx() }.coerceAtLeast(1f)
    val cornerPx = with(density) { cornerRadius.toPx() }

    this.drawWithContent {
        drawIntoCanvas { canvas ->
            val nativeCanvas = canvas.nativeCanvas
            val saveCount = nativeCanvas.save()

            val rect = RectF(0f, 0f, size.width, size.height)
            val path = Path().apply {
                addRoundRect(rect, cornerPx, cornerPx, Path.Direction.CW)
            }
            nativeCanvas.clipPath(path)

            // 1. Inset Dark Upper Shadow (Deep recessed Top-Left cavity)
            if (darkShadowColor != Color.Transparent) {
                val paintDark = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
                    style = android.graphics.Paint.Style.STROKE
                    strokeWidth = depthPx * 4f
                    color = darkShadowColor.toArgb()
                    maskFilter = BlurMaskFilter(blurPx, BlurMaskFilter.Blur.NORMAL)
                }
                val darkRect = RectF(-depthPx * 0.5f, -depthPx * 0.5f, size.width + depthPx * 3.5f, size.height + depthPx * 3.5f)
                nativeCanvas.drawRoundRect(darkRect, cornerPx, cornerPx, paintDark)
            }

            // 2. Inset Light Bottom Rim Highlight (Subtle upward bounce)
            if (lightShadowColor != Color.Transparent) {
                val paintLight = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
                    style = android.graphics.Paint.Style.STROKE
                    strokeWidth = depthPx * 2f
                    color = lightShadowColor.toArgb()
                    maskFilter = BlurMaskFilter(blurPx * 0.8f, BlurMaskFilter.Blur.NORMAL)
                }
                val lightRect = RectF(-depthPx * 3.5f, -depthPx * 3.5f, size.width + depthPx * 0.5f, size.height + depthPx * 0.5f)
                nativeCanvas.drawRoundRect(lightRect, cornerPx, cornerPx, paintLight)
            }

            nativeCanvas.restoreToCount(saveCount)
        }
        drawContent()
    }
}

/**
 * Renders authentic 3D Neumorphic Card:
 * - Ambient soft drop shadow (high blur, soft low opacity)
 * - Hard stacked bevel layers (1px, 2px, 3px) with concentric smooth curved corners
 * - Top-left outer highlight border (1.5px solid white)
 * - Top-left inner sheen (simulating inset 2px 3px 5px rgba(255, 255, 255, 0.4))
 */
fun Modifier.neumorphic3DCard(
    bevelColor: Color,
    ambientShadowColor: Color = Color(0x33000000),
    cornerRadius: Dp = 16.dp,
    layers: Int = 3,
    topSheenAlpha: Float = 0.45f
): Modifier = composed {
    val density = LocalDensity.current
    val cornerPx = with(density) { cornerRadius.toPx() }
    val ambientBlurPx = with(density) { 14.dp.toPx() }.coerceAtLeast(1f)
    val ambientOffX = with(density) { 3.dp.toPx() }
    val ambientOffY = with(density) { 5.dp.toPx() }

    this
        .drawBehind {
            drawIntoCanvas { canvas ->
                val nativeCanvas = canvas.nativeCanvas
                val paint = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)

                // 1. Ambient soft drop shadow (Bottom-Right)
                paint.color = ambientShadowColor.toArgb()
                paint.maskFilter = BlurMaskFilter(ambientBlurPx, BlurMaskFilter.Blur.NORMAL)
                nativeCanvas.drawRoundRect(
                    ambientOffX,
                    ambientOffY,
                    size.width + ambientOffX,
                    size.height + ambientOffY,
                    cornerPx + with(density) { 1.5.dp.toPx() },
                    cornerPx + with(density) { 1.5.dp.toPx() },
                    paint
                )

                // 2. Hard stacked bevel layers with concentric rounded corners
                paint.maskFilter = null
                paint.color = bevelColor.toArgb()
                for (i in layers downTo 1) {
                    val off = with(density) { (i * 0.8f).dp.toPx() }
                    nativeCanvas.drawRoundRect(
                        off * 0.3f,
                        off * 0.3f,
                        size.width + off,
                        size.height + off,
                        cornerPx + off * 0.5f,
                        cornerPx + off * 0.5f,
                        paint
                    )
                }
            }
        }
        .drawWithContent {
            drawContent()
            drawIntoCanvas { canvas ->
                val nativeCanvas = canvas.nativeCanvas
                val saveCount = nativeCanvas.save()

                val rect = RectF(0f, 0f, size.width, size.height)
                val path = Path().apply {
                    addRoundRect(rect, cornerPx, cornerPx, Path.Direction.CW)
                }
                nativeCanvas.clipPath(path)

                // Top-Left inner specular light reflection
                val paintSheen = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
                    style = android.graphics.Paint.Style.STROKE
                    strokeWidth = with(density) { 2.2.dp.toPx() }
                    color = Color.White.copy(alpha = topSheenAlpha).toArgb()
                    maskFilter = BlurMaskFilter(with(density) { 2.5.dp.toPx() }, BlurMaskFilter.Blur.NORMAL)
                }
                val sheenRect = RectF(0f, 0f, size.width, size.height)
                nativeCanvas.drawRoundRect(sheenRect, cornerPx, cornerPx, paintSheen)

                // Top & Left crisp rim border
                val paintRim = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG).apply {
                    style = android.graphics.Paint.Style.STROKE
                    strokeWidth = with(density) { 1.2.dp.toPx() }
                    shader = android.graphics.LinearGradient(
                        0f, 0f, size.width, size.height,
                        Color.White.copy(alpha = 0.55f).toArgb(),
                        Color.Transparent.toArgb(),
                        android.graphics.Shader.TileMode.CLAMP
                    )
                }
                nativeCanvas.drawRoundRect(rect, cornerPx, cornerPx, paintRim)

                nativeCanvas.restoreToCount(saveCount)
            }
        }
}

/**
 * Full Interactive Neumorphic Button:
 * Automatically transitions from Floating (Outer Shadow) when idle
 * to Sunken (Inner Shadow + 1.5dp displacement) when pressed.
 */
fun Modifier.neumorphicClickable(
    cornerRadius: Dp = 12.dp,
    lightShadowColor: Color = Color(0xFFFFFFFF).copy(alpha = 0.9f),
    darkShadowColor: Color = Color(0xFFB0AFA6).copy(alpha = 0.6f),
    onClick: () -> Unit
): Modifier = composed {
    val interactionSource = remember { MutableInteractionSource() }
    val isPressed by interactionSource.collectIsPressedAsState()

    val translationY by animateDpAsState(
        targetValue = if (isPressed) 1.5.dp else 0.dp,
        animationSpec = tween(durationMillis = 80),
        label = "translationY"
    )

    this
        .clickable(
            interactionSource = interactionSource,
            indication = null,
            onClick = onClick
        )
        .then(
            if (isPressed) {
                Modifier.neumorphicInner(
                    darkShadowColor = Color(0x66000000),
                    lightShadowColor = Color(0x66FFFFFF),
                    depth = 2.5.dp,
                    blur = 3.dp,
                    cornerRadius = cornerRadius
                )
            } else {
                Modifier.neumorphicOuter(
                    lightShadowColor = lightShadowColor,
                    darkShadowColor = darkShadowColor,
                    shadowBlur = 5.dp,
                    offsetX = 2.5.dp,
                    offsetY = 3.dp,
                    cornerRadius = cornerRadius
                )
            }
        )
}

/**
 * Renders authentic CSS-style stacked hard bevel layers + ambient blurred shadow:
 * 1px 1px 0px var(--e3), 2px 2px 0px var(--e3), 3px 3px 0px var(--e3), 4px 4px 0px var(--e3), 6px 8px 15px rgba(0,0,0,0.2)
 */
fun Modifier.stacked3DBevel(
    bevelColor: Color,
    ambientShadowColor: Color = Color(0x24000000),
    cornerRadius: Dp = 14.dp,
    layers: Int = 2,
    hasTopHighlight: Boolean = false
): Modifier = composed {
    val density = LocalDensity.current
    val cornerPx = with(density) { cornerRadius.toPx() }
    val ambientBlurPx = with(density) { 15.dp.toPx() }.coerceAtLeast(1f)
    val highlightBlurPx = with(density) { 8.dp.toPx() }.coerceAtLeast(1f)
    val ambientOffX = with(density) { 4.dp.toPx() }
    val ambientOffY = with(density) { 6.dp.toPx() }
    val highlightOff = with(density) { 2.dp.toPx() }

    this.drawBehind {
        drawIntoCanvas { canvas ->
            val nativeCanvas = canvas.nativeCanvas
            val paint = android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)

            // 0. Soft White Highlight (Top-Left) only if requested
            if (hasTopHighlight) {
                paint.color = Color(0x99FFFFFF).toArgb()
                paint.maskFilter = BlurMaskFilter(highlightBlurPx, BlurMaskFilter.Blur.NORMAL)
                nativeCanvas.drawRoundRect(
                    -highlightOff,
                    -highlightOff,
                    size.width - highlightOff,
                    size.height - highlightOff,
                    cornerPx,
                    cornerPx,
                    paint
                )
            }

            // 1. Ambient soft drop shadow (Bottom-Right, high blur, soft low opacity)
            paint.color = ambientShadowColor.toArgb()
            paint.maskFilter = BlurMaskFilter(ambientBlurPx, BlurMaskFilter.Blur.NORMAL)
            nativeCanvas.drawRoundRect(
                ambientOffX,
                ambientOffY,
                size.width + ambientOffX,
                size.height + ambientOffY,
                cornerPx,
                cornerPx,
                paint
            )

            // 2. Subtle hard stacked bevel layers
            paint.maskFilter = null
            paint.color = bevelColor.toArgb()
            for (i in layers downTo 1) {
                val off = with(density) { i.dp.toPx() }
                nativeCanvas.drawRoundRect(
                    off,
                    off,
                    size.width + off,
                    size.height + off,
                    cornerPx + off * 0.5f,
                    cornerPx + off * 0.5f,
                    paint
                )
            }
        }
    }
}
