package com.my.salah.tracker.app.ui

import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.size
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.*
import androidx.compose.ui.graphics.drawscope.DrawScope
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.graphics.drawscope.scale
import androidx.compose.ui.graphics.drawscope.translate
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp

/**
 * Metallic Silver/White linear gradient matching ${PremiumLight} from ui-components.js
 */
val PremiumSilverBrush = Brush.linearGradient(
    colors = listOf(Color(0xFFFFFFFF), Color(0xFFE2E8F0)),
    start = Offset(0f, 0f),
    end = Offset(24f, 24f)
)

/**
 * 1. FAJR ICON: 4-pointed Starburst Constellation
 * Matching SVG: M12 1L13.5 8.5L21 10L13.5 11.5L12 19L10.5 11.5L3 10L10.5 8.5Z ...
 */
@Composable
fun FajrVectorIcon(size: Dp = 18.dp, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f

        // Shadow
        val shadowOffset = Offset(0f, 2f * sy)

        // Main star
        val mainStar = Path().apply {
            moveTo(12f * sx, 1f * sy)
            lineTo(13.5f * sx, 8.5f * sy)
            lineTo(21f * sx, 10f * sy)
            lineTo(13.5f * sx, 11.5f * sy)
            lineTo(12f * sx, 19f * sy)
            lineTo(10.5f * sx, 11.5f * sy)
            lineTo(3f * sx, 10f * sy)
            lineTo(10.5f * sx, 8.5f * sy)
            close()
        }

        // Small top-left star
        val starTL = Path().apply {
            moveTo(5f * sx, 4f * sy)
            lineTo(5.5f * sx, 5.5f * sy)
            lineTo(7f * sx, 6f * sy)
            lineTo(5.5f * sx, 6.5f * sy)
            lineTo(5f * sx, 8f * sy)
            lineTo(4.5f * sx, 6.5f * sy)
            lineTo(3f * sx, 6f * sy)
            lineTo(4.5f * sx, 5.5f * sy)
            close()
        }

        // Small bottom-right star
        val starBR = Path().apply {
            moveTo(19f * sx, 16f * sy)
            lineTo(19.5f * sx, 17.5f * sy)
            lineTo(21f * sx, 18f * sy)
            lineTo(19.5f * sx, 18.5f * sy)
            lineTo(19f * sx, 20f * sy)
            lineTo(18.5f * sx, 18.5f * sy)
            lineTo(17f * sx, 18f * sy)
            lineTo(18.5f * sx, 17.5f * sy)
            close()
        }

        // Draw Shadows
        translate(shadowOffset.x, shadowOffset.y) {
            drawPath(mainStar, color = Color(0x66000000))
            drawPath(starTL, color = Color(0x66000000))
            drawPath(starBR, color = Color(0x66000000))
        }

        // Draw Metallic Paths
        drawPath(mainStar, brush = PremiumSilverBrush)
        drawPath(starTL, brush = PremiumSilverBrush)
        drawPath(starBR, brush = PremiumSilverBrush)
    }
}

/**
 * 2. DHUHR ICON: Geometric Sun with 8 Triangular Sunburst Rays
 */
@Composable
fun DhuhrVectorIcon(size: Dp = 18.dp, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f

        val center = Offset(12f * sx, 12f * sy)
        val radius = 5f * sx

        // 8 Rays
        val rays = Path().apply {
            // N & S
            moveTo(12f * sx, 1f * sy); lineTo(14f * sx, 5f * sy); lineTo(10f * sx, 5f * sy); close()
            moveTo(12f * sx, 23f * sy); lineTo(14f * sx, 19f * sy); lineTo(10f * sx, 19f * sy); close()
            // W & E
            moveTo(1f * sx, 12f * sy); lineTo(5f * sx, 10f * sy); lineTo(5f * sx, 14f * sy); close()
            moveTo(23f * sx, 12f * sy); lineTo(19f * sx, 10f * sy); lineTo(19f * sx, 14f * sy); close()
            // Diagonals
            moveTo(4.22f * sx, 4.22f * sy); lineTo(8.46f * sx, 5.64f * sy); lineTo(5.64f * sx, 8.46f * sy); close()
            moveTo(19.78f * sx, 19.78f * sy); lineTo(15.54f * sx, 18.36f * sy); lineTo(18.36f * sx, 15.54f * sy); close()
            moveTo(4.22f * sx, 19.78f * sy); lineTo(5.64f * sx, 15.54f * sy); lineTo(8.46f * sx, 18.36f * sy); close()
            moveTo(19.78f * sx, 4.22f * sy); lineTo(18.36f * sx, 8.46f * sy); lineTo(15.54f * sx, 5.64f * sy); close()
        }

        // Shadows
        drawCircle(color = Color(0x66000000), radius = radius, center = center + Offset(0f, 2f * sy))
        translate(0f, 2f * sy) {
            drawPath(rays, color = Color(0x66000000))
        }

        // Sun
        drawCircle(brush = PremiumSilverBrush, radius = radius, center = center)
        drawPath(rays, brush = PremiumSilverBrush)
    }
}

/**
 * 3. ASR ICON: Geometric Cloud Outline
 */
@Composable
fun AsrVectorIcon(size: Dp = 18.dp, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.2f * sx

        val cloud = Path().apply {
            moveTo(17.5f * sx, 19f * sy)
            cubicTo(19.98f * sx, 19f * sy, 22f * sx, 16.98f * sy, 22f * sx, 14.5f * sy)
            cubicTo(22f * sx, 12.18f * sy, 20.25f * sx, 10.28f * sy, 18f * sx, 10.05f * sy)
            cubicTo(17.43f * sx, 7.2f * sy, 15.1f * sx, 5f * sy, 12.25f * sx, 5f * sy)
            cubicTo(9.36f * sx, 5f * sy, 6.94f * sx, 7.04f * sy, 6.36f * sx, 9.8f * sy)
            cubicTo(3.89f * sx, 10.1f * sy, 2f * sx, 12.19f * sy, 2f * sx, 14.75f * sy)
            cubicTo(2f * sx, 17.37f * sy, 4.13f * sx, 19f * sy, 6.75f * sx, 19f * sy)
            lineTo(17.5f * sx, 19f * sy)
            close()
        }

        // Shadow
        translate(0f, 2f * sy) {
            drawPath(cloud, color = Color(0x66000000), style = Stroke(width = strokeW, cap = StrokeCap.Round))
        }
        // Metallic Stroke
        drawPath(cloud, brush = PremiumSilverBrush, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}

/**
 * 4. MAGHRIB ICON: Sun Setting on Horizon Waves
 */
@Composable
fun MaghribVectorIcon(size: Dp = 18.dp, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f

        val halfSun = Path().apply {
            moveTo(5f * sx, 12f * sy)
            arcTo(
                rect = androidx.compose.ui.geometry.Rect(5f * sx, 5f * sy, 19f * sx, 19f * sy),
                startAngleDegrees = 180f,
                sweepAngleDegrees = 180f,
                forceMoveTo = false
            )
            close()
        }

        val line1 = Path().apply {
            addRect(androidx.compose.ui.geometry.Rect(2f * sx, 14f * sy, 22f * sx, 16f * sy))
        }
        val line2 = Path().apply {
            addRect(androidx.compose.ui.geometry.Rect(4f * sx, 18f * sy, 20f * sx, 20f * sy))
        }

        // Shadows
        val sh = Offset(0f, 2f * sy)
        translate(sh.x, sh.y) {
            drawPath(halfSun, color = Color(0x66000000))
            drawPath(line1, color = Color(0x66000000))
            drawPath(line2, color = Color(0x66000000))
        }

        // Paths
        drawPath(halfSun, brush = PremiumSilverBrush)
        drawPath(line1, brush = PremiumSilverBrush)
        drawPath(line2, brush = PremiumSilverBrush)
    }
}

/**
 * 5. ISHA ICON: Crescent Moon + Sparkle Star (Exact SVG Path Matching Web)
 */
@Composable
fun IshaVectorIcon(size: Dp = 18.dp, modifier: Modifier = Modifier) {
    val ishaMoonPath = remember {
        val androidPath = androidx.core.graphics.PathParser.createPathFromPathData(
            "M 21 12.79 A 9 9 0 1 1 11.21 3 A 7 7 0 0 0 21 12.79 Z"
        )
        androidPath.asComposePath()
    }
    val ishaStarPath = remember {
        val androidPath = androidx.core.graphics.PathParser.createPathFromPathData(
            "M 18 4 L 18.5 5.5 L 20 6 L 18.5 6.5 L 18 8 L 17.5 6.5 L 16 6 L 17.5 5.5 Z"
        )
        androidPath.asComposePath()
    }

    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f

        // Scale to 24x24 viewBox
        scale(scaleX = sx, scaleY = sy, pivot = Offset.Zero) {
            translate(0f, 2f) {
                drawPath(ishaMoonPath, color = Color(0x66000000))
                drawPath(ishaStarPath, color = Color(0x66000000))
            }
            drawPath(ishaMoonPath, brush = PremiumSilverBrush)
            drawPath(ishaStarPath, brush = PremiumSilverBrush)
        }
    }
}

/**
 * 6. WITR ICON: Candle with Flame & Base
 */
@Composable
fun WitrVectorIcon(size: Dp = 18.dp, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f

        val candle = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(10f * sx, 11f * sy, 14f * sx, 21f * sy),
                    radiusX = 1f * sx,
                    radiusY = 1f * sy
                )
            )
        }

        val flame = Path().apply {
            moveTo(12f * sx, 2f * sy)
            cubicTo(10.5f * sx, 4.5f * sy, 9f * sx, 6.5f * sy, 12f * sx, 9f * sy)
            cubicTo(15f * sx, 6.5f * sy, 13.5f * sx, 4.5f * sy, 12f * sx, 2f * sy)
            close()
        }

        val base = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(7f * sx, 21f * sy, 17f * sx, 23f * sy),
                    radiusX = 1f * sx,
                    radiusY = 1f * sy
                )
            )
        }

        val sh = Offset(0f, 2f * sy)
        translate(sh.x, sh.y) {
            drawPath(candle, color = Color(0x66000000))
            drawPath(flame, color = Color(0x66000000))
            drawPath(base, color = Color(0x66000000))
        }

        drawPath(candle, brush = PremiumSilverBrush)
        drawPath(flame, brush = PremiumSilverBrush)
        drawPath(base, brush = PremiumSilverBrush)
        drawLine(
            brush = PremiumSilverBrush,
            start = Offset(12f * sx, 9f * sy),
            end = Offset(12f * sx, 11f * sy),
            strokeWidth = 2f * sx
        )
    }
}

/**
 * Universal Prayer Icon Dispatcher
 */
@Composable
fun PrayerVectorIcon(prayerId: String, size: Dp = 18.dp, modifier: Modifier = Modifier) {
    when (prayerId.lowercase()) {
        "fajr" -> FajrVectorIcon(size, modifier)
        "dhuhr" -> DhuhrVectorIcon(size, modifier)
        "asr" -> AsrVectorIcon(size, modifier)
        "maghrib" -> MaghribVectorIcon(size, modifier)
        "isha" -> IshaVectorIcon(size, modifier)
        "witr" -> WitrVectorIcon(size, modifier)
    }
}

/**
 * HEADER: Engraved User Avatar Icon
 */
@Composable
fun EngravedUserIcon(size: Dp = 20.dp, isLoggedIn: Boolean = false, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        val head = Offset(12f * sx, 7f * sy)
        val headRadius = 4f * sx

        val body = Path().apply {
            moveTo(20f * sx, 21f * sy)
            lineTo(20f * sx, 19f * sy)
            cubicTo(20f * sx, 16.79f * sy, 18.21f * sx, 15f * sy, 16f * sx, 15f * sy)
            lineTo(8f * sx, 15f * sy)
            cubicTo(5.79f * sx, 15f * sy, 4f * sx, 16.79f * sy, 4f * sx, 19f * sy)
            lineTo(4f * sx, 21f * sy)
        }

        // Engraved 1px White Bottom/Right Highlight
        drawCircle(color = Color.White, radius = headRadius, center = head + Offset(1f, 1f), style = Stroke(width = strokeW))
        translate(1f, 1f) {
            drawPath(body, color = Color.White, style = Stroke(width = strokeW, cap = StrokeCap.Round))
        }

        // Main Stroke
        val mainColor = if (isLoggedIn) Color(0xFF159C4C) else Color(0xFF6C7A80)
        drawCircle(color = mainColor, radius = headRadius, center = head, style = Stroke(width = strokeW))
        drawPath(body, color = mainColor, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))

        if (isLoggedIn) {
            // Check badge
            drawCircle(color = Color(0xFF159C4C), radius = 5f * sx, center = Offset(19f * sx, 19f * sy))
            val chk = Path().apply {
                moveTo(17f * sx, 19f * sy)
                lineTo(18.5f * sx, 20.5f * sy)
                lineTo(21f * sx, 17.5f * sy)
            }
            drawPath(chk, color = Color.White, style = Stroke(width = 2f * sx, cap = StrokeCap.Round))
        }
    }
}

/**
 * TASBIH: Circular Vector Icons (Reset, Minus, Audio, Next)
 */
@Composable
fun TasbihResetVectorIcon(size: Dp = 15.dp, color: Color = Color(0xFF2ECC71), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        val p = Path().apply {
            moveTo(21.5f * sx, 2f * sy)
            lineTo(21.5f * sx, 8f * sy)
            lineTo(15.5f * sx, 8f * sy)
            moveTo(21.34f * sx, 15.57f * sy)
            arcTo(
                rect = androidx.compose.ui.geometry.Rect(2f * sx, 2f * sy, 22f * sx, 22f * sy),
                startAngleDegrees = 20f,
                sweepAngleDegrees = -300f,
                forceMoveTo = false
            )
        }
        drawPath(p, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}

@Composable
fun TasbihMinusVectorIcon(size: Dp = 15.dp, color: Color = Color(0xFFFF6B6B), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        drawLine(
            color = color,
            start = Offset(5f * sx, 12f * sy),
            end = Offset(19f * sx, 12f * sy),
            strokeWidth = 2.8f * sx,
            cap = StrokeCap.Round
        )
    }
}

@Composable
fun TasbihAudioVectorIcon(size: Dp = 15.dp, color: Color = Color(0xFFFF9F43), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        val speaker = Path().apply {
            moveTo(11f * sx, 5f * sy)
            lineTo(6f * sx, 9f * sy)
            lineTo(2f * sx, 9f * sy)
            lineTo(2f * sx, 15f * sy)
            lineTo(6f * sx, 15f * sy)
            lineTo(11f * sx, 19f * sy)
            close()
        }
        drawPath(speaker, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))

        // Soundwaves
        val wave1 = Path().apply {
            arcTo(
                rect = androidx.compose.ui.geometry.Rect(7f * sx, 7f * sy, 17f * sx, 17f * sy),
                startAngleDegrees = -45f,
                sweepAngleDegrees = 90f,
                forceMoveTo = true
            )
        }
        val wave2 = Path().apply {
            arcTo(
                rect = androidx.compose.ui.geometry.Rect(4f * sx, 4f * sy, 20f * sx, 20f * sy),
                startAngleDegrees = -45f,
                sweepAngleDegrees = 90f,
                forceMoveTo = true
            )
        }
        drawPath(wave1, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round))
        drawPath(wave2, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round))
    }
}

@Composable
fun TasbihNextVectorIcon(size: Dp = 15.dp, color: Color = Color(0xFFA4C6DB), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.8f * sx

        val p = Path().apply {
            moveTo(9f * sx, 18f * sy)
            lineTo(15f * sx, 12f * sy)
            lineTo(9f * sx, 6f * sy)
        }
        drawPath(p, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}

/**
 * ACTION ROW: Engraved Icons (Mark All, Unmark All, Statistics, Today)
 */
@Composable
fun MarkAllCheckVectorIcon(size: Dp = 14.dp, color: Color = Color(0xFF444E51), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 3f * sx

        val arc = Path().apply {
            arcTo(
                rect = androidx.compose.ui.geometry.Rect(3f * sx, 3f * sy, 21f * sx, 21f * sy),
                startAngleDegrees = 300f,
                sweepAngleDegrees = 300f,
                forceMoveTo = false
            )
        }
        val check = Path().apply {
            moveTo(22f * sx, 4f * sy)
            lineTo(12f * sx, 14f * sy)
            lineTo(8f * sx, 10f * sy)
        }

        // White 1px engraved bottom-right shadow
        translate(1f, 1f) {
            drawPath(arc, color = Color.White, style = Stroke(width = strokeW))
            drawPath(check, color = Color.White, style = Stroke(width = strokeW, cap = StrokeCap.Round))
        }

        // Main Icon
        drawPath(arc, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round))
        drawPath(check, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}

@Composable
fun UnmarkAllCrossVectorIcon(size: Dp = 14.dp, color: Color = Color(0xFF444E51), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 3f * sx

        val center = Offset(12f * sx, 12f * sy)
        val r = 10f * sx

        // White 1px engraved
        drawCircle(color = Color.White, radius = r, center = center + Offset(1f, 1f), style = Stroke(width = strokeW))
        drawLine(color = Color.White, start = Offset(15f * sx + 1f, 9f * sy + 1f), end = Offset(9f * sx + 1f, 15f * sy + 1f), strokeWidth = strokeW, cap = StrokeCap.Round)
        drawLine(color = Color.White, start = Offset(9f * sx + 1f, 9f * sy + 1f), end = Offset(15f * sx + 1f, 15f * sy + 1f), strokeWidth = strokeW, cap = StrokeCap.Round)

        // Main
        drawCircle(color = color, radius = r, center = center, style = Stroke(width = strokeW))
        drawLine(color = color, start = Offset(15f * sx, 9f * sy), end = Offset(9f * sx, 15f * sy), strokeWidth = strokeW, cap = StrokeCap.Round)
        drawLine(color = color, start = Offset(9f * sx, 9f * sy), end = Offset(15f * sx, 15f * sy), strokeWidth = strokeW, cap = StrokeCap.Round)
    }
}

@Composable
fun StatisticsChartVectorIcon(size: Dp = 14.dp, color: Color = Color(0xFF444E51), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        // White 1px engraved
        val sh = Offset(1f, 1f)
        drawLine(Color.White, Offset(18f * sx, 10f * sy) + sh, Offset(18f * sx, 20f * sy) + sh, strokeW, StrokeCap.Round)
        drawLine(Color.White, Offset(12f * sx, 4f * sy) + sh, Offset(12f * sx, 20f * sy) + sh, strokeW, StrokeCap.Round)
        drawLine(Color.White, Offset(6f * sx, 14f * sy) + sh, Offset(6f * sx, 20f * sy) + sh, strokeW, StrokeCap.Round)

        // Main
        drawLine(color, Offset(18f * sx, 10f * sy), Offset(18f * sx, 20f * sy), strokeW, StrokeCap.Round)
        drawLine(color, Offset(12f * sx, 4f * sy), Offset(12f * sx, 20f * sy), strokeW, StrokeCap.Round)
        drawLine(color, Offset(6f * sx, 14f * sy), Offset(6f * sx, 20f * sy), strokeW, StrokeCap.Round)
    }
}

@Composable
fun TodayCalendarVectorIcon(size: Dp = 14.dp, color: Color = Color(0xFF444E51), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        val box = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(3f * sx, 4f * sy, 21f * sx, 20f * sy),
                    radiusX = 3f * sx,
                    radiusY = 3f * sy
                )
            )
        }

        // White 1px engraved
        val sh = Offset(1f, 1f)
        translate(sh.x, sh.y) {
            drawPath(box, color = Color.White, style = Stroke(strokeW))
        }
        drawLine(Color.White, Offset(3f * sx, 9f * sy) + sh, Offset(21f * sx, 9f * sy) + sh, strokeW)
        drawLine(Color.White, Offset(8f * sx, 2f * sy) + sh, Offset(8f * sx, 6f * sy) + sh, strokeW, StrokeCap.Round)
        drawLine(Color.White, Offset(16f * sx, 2f * sy) + sh, Offset(16f * sx, 6f * sy) + sh, strokeW, StrokeCap.Round)

        // Main
        drawPath(box, color = color, style = Stroke(strokeW))
        drawLine(color, Offset(3f * sx, 9f * sy), Offset(21f * sx, 9f * sy), strokeW)
        drawLine(color, Offset(8f * sx, 2f * sy), Offset(8f * sx, 6f * sy), strokeW, StrokeCap.Round)
        drawLine(color, Offset(16f * sx, 2f * sy), Offset(16f * sx, 6f * sy), strokeW, StrokeCap.Round)
    }
}

/**
 * DIALOG: Alert Circle Vector Icon (Future Date Warning)
 */
@Composable
fun AlertCircleVectorIcon(size: Dp = 24.dp, color: Color = Color(0xFF6C7A80), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        // Circle
        drawCircle(
            color = color,
            radius = 10f * sx,
            center = Offset(12f * sx, 12f * sy),
            style = Stroke(width = strokeW)
        )
        // Line top
        drawLine(
            color = color,
            start = Offset(12f * sx, 8f * sy),
            end = Offset(12f * sx, 12f * sy),
            strokeWidth = strokeW,
            cap = StrokeCap.Round
        )
        // Dot bottom
        drawCircle(
            color = color,
            radius = 1.25f * sx,
            center = Offset(12f * sx, 16f * sy)
        )
    }
}

/**
 * DIALOG: Warning Triangle Vector Icon (Logout Confirm)
 */
@Composable
fun WarningTriangleVectorIcon(size: Dp = 24.dp, color: Color = Color.White, modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        val triangle = Path().apply {
            moveTo(10.29f * sx, 3.86f * sy)
            lineTo(1.82f * sx, 18f * sy)
            cubicTo(1.4f * sx, 18.7f * sy, 1.9f * sx, 21f * sy, 2.7f * sx, 21f * sy)
            lineTo(21.3f * sx, 21f * sy)
            cubicTo(22.1f * sx, 21f * sy, 22.6f * sx, 18.7f * sy, 22.18f * sx, 18f * sy)
            lineTo(13.71f * sx, 3.86f * sy)
            cubicTo(12.9f * sx, 2.5f * sy, 11.1f * sx, 2.5f * sy, 10.29f * sx, 3.86f * sy)
            close()
        }

        drawPath(triangle, color = color, style = Stroke(width = strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
        drawLine(
            color = color,
            start = Offset(12f * sx, 9f * sy),
            end = Offset(12f * sx, 13f * sy),
            strokeWidth = strokeW,
            cap = StrokeCap.Round
        )
        drawCircle(
            color = color,
            radius = 1.25f * sx,
            center = Offset(12f * sx, 17f * sy)
        )
    }
}

/**
 * DIALOG: Bar Chart Vector Icon (Weekly Progress Modal Header)
 */
@Composable
fun DialogBarChartVectorIcon(size: Dp = 20.dp, color: Color = Color(0xFF364455), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f

        val bar1 = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(4f * sx, 13f * sy, 8f * sx, 22f * sy),
                    radiusX = 1.5f * sx,
                    radiusY = 1.5f * sy
                )
            )
        }
        val bar2 = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(10f * sx, 8f * sy, 14f * sx, 22f * sy),
                    radiusX = 1.5f * sx,
                    radiusY = 1.5f * sy
                )
            )
        }
        val bar3 = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(16f * sx, 3f * sy, 20f * sx, 22f * sy),
                    radiusX = 1.5f * sx,
                    radiusY = 1.5f * sy
                )
            )
        }

        drawPath(bar1, color = color)
        drawPath(bar2, color = color)
        drawPath(bar3, color = color)
    }
}

/**
 * DIALOG: Dialog Close Cross Vector Icon
 */
@Composable
fun DialogCloseVectorIcon(size: Dp = 14.dp, color: Color = Color(0xFF6C7A80), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 3f * sx

        // White 1px shadow
        drawLine(Color.White, Offset(18f * sx + 1f, 6f * sy + 1f), Offset(6f * sx + 1f, 18f * sy + 1f), strokeW, StrokeCap.Round)
        drawLine(Color.White, Offset(6f * sx + 1f, 6f * sy + 1f), Offset(18f * sx + 1f, 18f * sy + 1f), strokeW, StrokeCap.Round)

        // Main
        drawLine(color, Offset(18f * sx, 6f * sy), Offset(6f * sx, 18f * sy), strokeW, StrokeCap.Round)
        drawLine(color, Offset(6f * sx, 6f * sy), Offset(18f * sx, 18f * sy), strokeW, StrokeCap.Round)
    }
}

/**
 * DIALOG: Copy Vector Icon
 */
@Composable
fun CopyVectorIcon(size: Dp = 16.dp, color: Color = Color(0xFF3B75C6), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 2.5f * sx

        val mainRect = Path().apply {
            addRoundRect(
                androidx.compose.ui.geometry.RoundRect(
                    rect = androidx.compose.ui.geometry.Rect(9f * sx, 9f * sy, 22f * sx, 22f * sy),
                    radiusX = 2f * sx,
                    radiusY = 2f * sy
                )
            )
        }
        val backShape = Path().apply {
            moveTo(5f * sx, 15f * sy)
            lineTo(4f * sx, 15f * sy)
            cubicTo(2.9f * sx, 15f * sy, 2f * sx, 14.1f * sy, 2f * sx, 13f * sy)
            lineTo(2f * sx, 4f * sy)
            cubicTo(2f * sx, 2.9f * sx, 2.9f * sx, 2f * sy, 4f * sx, 2f * sy)
            lineTo(13f * sx, 2f * sy)
            cubicTo(14.1f * sx, 2f * sy, 15f * sx, 2.9f * sy, 15f * sx, 4f * sy)
            lineTo(15f * sx, 5f * sy)
        }

        drawPath(mainRect, color = color, style = Stroke(strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
        drawPath(backShape, color = color, style = Stroke(strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}

/**
 * DIALOG: Check Vector Icon (Copied)
 */
@Composable
fun CheckVectorIcon(size: Dp = 16.dp, color: Color = Color(0xFF159C4C), modifier: Modifier = Modifier) {
    Canvas(modifier = modifier.size(size)) {
        val sx = this.size.width / 24f
        val sy = this.size.height / 24f
        val strokeW = 3f * sx

        val tick = Path().apply {
            moveTo(20f * sx, 6f * sy)
            lineTo(9f * sx, 17f * sy)
            lineTo(4f * sx, 12f * sy)
        }
        drawPath(tick, color = color, style = Stroke(strokeW, cap = StrokeCap.Round, join = StrokeJoin.Round))
    }
}

