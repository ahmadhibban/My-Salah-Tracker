package com.my.salah.tracker.app.ui

import androidx.compose.animation.animateContentSize
import androidx.compose.animation.core.animateDpAsState
import androidx.compose.animation.core.tween
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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import java.text.SimpleDateFormat
import java.util.*

@Composable
fun NeumorphicHeaderRow(
    selectedDate: Date,
    streakDays: Int,
    isLoggedIn: Boolean,
    onDateClick: () -> Unit,
    onAuthClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val sdf = remember { SimpleDateFormat("EEE, MMM dd, yyyy", Locale.US) }
    val formattedDate = remember(selectedDate) { sdf.format(selectedDate) }

    Row(
        modifier = modifier
            .fillMaxWidth()
            .height(45.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.spacedBy(8.dp)
    ) {
        // 1. English Date Badge (Flex 1.4)
        Box(
            modifier = Modifier
                .weight(1.4f)
                .fillMaxHeight()
                .stacked3DBevel(
                    bevelColor = Color(0xFF181C1E),
                    ambientShadowColor = Color(0x4D000000),
                    cornerRadius = 14.dp,
                    layers = 2
                )
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = onDateClick
                )
                .clip(RoundedCornerShape(14.dp))
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFF3A4750), Color(0xFF28313B)),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.linearGradient(listOf(Color(0x59FFFFFF), Color(0x1AFFFFFF), Color.Transparent)),
                    shape = RoundedCornerShape(14.dp)
                ),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = formattedDate,
                style = androidx.compose.ui.text.TextStyle(
                    fontFamily = PlusJakartaFontFamily,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.ExtraBold,
                    color = Color.White
                )
            )
        }

        // 2. Streak Badge (Flex 0.8)
        Box(
            modifier = Modifier
                .weight(0.85f)
                .fillMaxHeight()
                .stacked3DBevel(
                    bevelColor = Color(0xFF0D1C33),
                    ambientShadowColor = Color(0x4D000000),
                    cornerRadius = 14.dp,
                    layers = 2
                )
                .clip(RoundedCornerShape(14.dp))
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFF1A6D96), Color(0xFF0D415C)),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.linearGradient(listOf(Color(0x66FFFFFF), Color(0x20FFFFFF), Color.Transparent)),
                    shape = RoundedCornerShape(14.dp)
                ),
            contentAlignment = Alignment.Center
        ) {
            Text(
                text = "$streakDays Days",
                style = androidx.compose.ui.text.TextStyle(
                    fontFamily = PlusJakartaFontFamily,
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Black,
                    color = Color.White,
                    shadow = androidx.compose.ui.graphics.Shadow(
                        color = Color(0x99000000),
                        offset = Offset(0f, 3f),
                        blurRadius = 4f
                    )
                )
            )
        }

        // 3. Circular Auth / Profile Button (42dp)
        Box(
            modifier = Modifier
                .size(42.dp)
                .stacked3DBevel(
                    bevelColor = Color(0xFF97A0A5),
                    ambientShadowColor = Color(0x33000000),
                    cornerRadius = 21.dp,
                    layers = 2
                )
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = onAuthClick
                )
                .clip(CircleShape)
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFFFFFFFF), Color(0xFFE8E8E8)),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.linearGradient(listOf(Color.White, Color(0x66FFFFFF), Color.Transparent)),
                    shape = CircleShape
                ),
            contentAlignment = Alignment.Center
        ) {
            EngravedUserIcon(size = 20.dp, isLoggedIn = isLoggedIn)
        }
    }
}

@Composable
fun NeumorphicWeekDaysRow(
    selectedDate: Date,
    today: Date,
    onDateSelected: (Date) -> Unit,
    onFutureDateAttempt: () -> Unit,
    modifier: Modifier = Modifier
) {
    val sdfKey = remember { SimpleDateFormat("yyyy-MM-dd", Locale.US) }
    val todayKey = remember(today) { sdfKey.format(today) }
    val selectedKey = remember(selectedDate) { sdfKey.format(selectedDate) }

    // Calculate beginning of the week (Sunday based, matching index 0)
    val startOfWeekCal = remember(selectedDate) {
        Calendar.getInstance().apply {
            time = selectedDate
            val dayOffset = if (get(Calendar.DAY_OF_WEEK) == Calendar.SATURDAY) 0 else get(Calendar.DAY_OF_WEEK)
            add(Calendar.DAY_OF_MONTH, -dayOffset)
        }
    }

    val dayNames = arrayOf("S", "S", "M", "T", "W", "T", "F")

    Row(
        modifier = modifier
            .fillMaxWidth()
            .height(42.dp),
        verticalAlignment = Alignment.CenterVertically,
        horizontalArrangement = Arrangement.SpaceBetween
    ) {
        // Left "<" Button (matching web 20x26)
        WeekNavButton(symbol = "<") {
            val prevCal = Calendar.getInstance().apply {
                time = selectedDate
                add(Calendar.DAY_OF_MONTH, -7)
            }
            onDateSelected(prevCal.time)
        }

        // 7 Week Days
        for (i in 0 until 7) {
            val dCal = Calendar.getInstance().apply {
                time = startOfWeekCal.time
                add(Calendar.DAY_OF_MONTH, i)
            }
            val dDate = dCal.time
            val dKey = sdfKey.format(dDate)
            val isSelected = dKey == selectedKey
            val isFuture = dCal.after(Calendar.getInstance().apply { time = today })

            Box(
                modifier = Modifier.weight(1f),
                contentAlignment = Alignment.Center
            ) {
                WeekDayButton(
                    letter = dayNames[i],
                    isSelected = isSelected,
                    onClick = {
                        if (isFuture) {
                            onFutureDateAttempt()
                        } else {
                            onDateSelected(dDate)
                        }
                    }
                )
            }
        }

        // Right ">" Button (matching web 20x26)
        WeekNavButton(symbol = ">") {
            val nextCal = Calendar.getInstance().apply {
                time = selectedDate
                add(Calendar.DAY_OF_MONTH, 7)
            }
            val todayCal = Calendar.getInstance().apply { time = today }
            val nextWeekStart = Calendar.getInstance().apply {
                time = nextCal.time
                val offset = if (get(Calendar.DAY_OF_WEEK) == Calendar.SATURDAY) 0 else get(Calendar.DAY_OF_WEEK)
                add(Calendar.DAY_OF_MONTH, -offset)
                set(Calendar.HOUR_OF_DAY, 0)
                set(Calendar.MINUTE, 0)
                set(Calendar.SECOND, 0)
                set(Calendar.MILLISECOND, 0)
            }
            val todayWeekStart = Calendar.getInstance().apply {
                time = todayCal.time
                val offset = if (get(Calendar.DAY_OF_WEEK) == Calendar.SATURDAY) 0 else get(Calendar.DAY_OF_WEEK)
                add(Calendar.DAY_OF_MONTH, -offset)
                set(Calendar.HOUR_OF_DAY, 0)
                set(Calendar.MINUTE, 0)
                set(Calendar.SECOND, 0)
                set(Calendar.MILLISECOND, 0)
            }

            if (nextWeekStart.after(todayWeekStart)) {
                onFutureDateAttempt()
            } else {
                val finalDate = if (nextCal.after(todayCal)) today else nextCal.time
                onDateSelected(finalDate)
            }
        }
    }
}

@Composable
private fun WeekNavButton(
    symbol: String,
    onClick: () -> Unit
) {
    Box(
        modifier = Modifier
            .width(20.dp)
            .height(26.dp)
            .stacked3DBevel(
                bevelColor = Color(0xFFBCB4A4),
                ambientShadowColor = Color(0x1F000000),
                cornerRadius = 6.dp,
                layers = 1
            )
            .clip(RoundedCornerShape(6.dp))
            .background(
                brush = Brush.linearGradient(
                    colors = listOf(Color(0xFFFFFFFF), Color(0xFFDFDBD2)),
                    start = Offset(0f, 0f),
                    end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                )
            )
            .border(
                1.dp,
                Brush.linearGradient(listOf(Color.White, Color.Transparent)),
                RoundedCornerShape(6.dp)
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            ),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = symbol,
            style = androidx.compose.ui.text.TextStyle(
                fontFamily = PlusJakartaFontFamily,
                fontSize = 11.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFF5C5547),
                shadow = androidx.compose.ui.graphics.Shadow(
                    color = Color.White,
                    offset = Offset(1f, 1f),
                    blurRadius = 1f
                )
            )
        )
    }
}

@Composable
private fun WeekDayButton(
    letter: String,
    isSelected: Boolean,
    onClick: () -> Unit,
    modifier: Modifier = Modifier
) {
    val w by animateDpAsState(
        targetValue = if (isSelected) 34.dp else 22.dp,
        animationSpec = tween(150),
        label = "dayWidth"
    )
    val h by animateDpAsState(
        targetValue = if (isSelected) 38.dp else 26.dp,
        animationSpec = tween(150),
        label = "dayHeight"
    )

    Box(
        modifier = modifier
            .width(w)
            .height(h)
            .then(
                if (isSelected) {
                    Modifier
                        .stacked3DBevel(
                            bevelColor = Color(0xFF133366),
                            ambientShadowColor = Color(0x4D000000),
                            cornerRadius = 10.dp,
                            layers = 2
                        )
                        .clip(RoundedCornerShape(10.dp))
                        .background(
                            brush = Brush.linearGradient(
                                colors = listOf(Color(0xFF5D9DF5), Color(0xFF224E91)),
                                start = Offset(0f, 0f),
                                end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                            )
                        )
                        .border(
                            1.dp,
                            Brush.linearGradient(listOf(Color(0x80FFFFFF), Color.Transparent)),
                            RoundedCornerShape(10.dp)
                        )
                } else {
                    Modifier
                        .stacked3DBevel(
                            bevelColor = Color(0xFFBCB4A4),
                            ambientShadowColor = Color(0x33000000),
                            cornerRadius = 6.dp,
                            layers = 2
                        )
                        .clip(RoundedCornerShape(6.dp))
                        .background(
                            brush = Brush.linearGradient(
                                colors = listOf(Color(0xFFFFFFFF), Color(0xFFDFDBD2)),
                                start = Offset(0f, 0f),
                                end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                            )
                        )
                        .neumorphicInner(
                            darkShadowColor = Color.Transparent,
                            lightShadowColor = Color(0x99FFFFFF),
                            depth = 1.5.dp,
                            blur = 2.dp,
                            cornerRadius = 6.dp
                        )
                        .border(
                            1.dp,
                            Brush.linearGradient(listOf(Color.White, Color(0xB3FFFFFF), Color.Transparent)),
                            RoundedCornerShape(6.dp)
                        )
                }
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            ),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = letter,
            style = androidx.compose.ui.text.TextStyle(
                fontFamily = PlusJakartaFontFamily,
                fontSize = if (isSelected) 14.sp else 10.sp,
                fontWeight = FontWeight.ExtraBold,
                color = if (isSelected) Color.White else Color(0xFF5C5547),
                shadow = if (isSelected) {
                    androidx.compose.ui.graphics.Shadow(
                        color = Color(0x80000000),
                        offset = Offset(0f, 2f),
                        blurRadius = 4f
                    )
                } else {
                    androidx.compose.ui.graphics.Shadow(
                        color = Color.White,
                        offset = Offset(1f, 1f),
                        blurRadius = 1f
                    )
                }
            )
        )
    }
}

@Composable
fun NeumorphicActionsRow(
    isAllMarked: Boolean,
    isToday: Boolean,
    onMarkToggle: () -> Unit,
    onStatsOrToday: () -> Unit,
    modifier: Modifier = Modifier
) {
    Row(
        modifier = modifier
            .fillMaxWidth()
            .height(38.dp),
        horizontalArrangement = Arrangement.spacedBy(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        // Mark All / Unmark All Button
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .stacked3DBevel(
                    bevelColor = Color(0xFFBCB8A7),
                    ambientShadowColor = Color(0x24000000),
                    cornerRadius = 8.dp,
                    layers = 3
                )
                .clip(RoundedCornerShape(8.dp))
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFFFFFFFF), Color(0xFFE0DED3)),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.linearGradient(
                        listOf(Color(0xE6FFFFFF), Color(0x66FFFFFF), Color.Transparent, Color.Transparent),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    ),
                    shape = RoundedCornerShape(8.dp)
                )
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = onMarkToggle
                ),
            contentAlignment = Alignment.Center
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                if (isAllMarked) {
                    UnmarkAllCrossVectorIcon(size = 14.dp, color = Color(0xFF444E51))
                } else {
                    MarkAllCheckVectorIcon(size = 14.dp, color = Color(0xFF444E51))
                }
                Text(
                    text = if (isAllMarked) "Unmark All" else "Mark All",
                    style = androidx.compose.ui.text.TextStyle(
                        fontFamily = PlusJakartaFontFamily,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color(0xFF444E51),
                        shadow = androidx.compose.ui.graphics.Shadow(
                            color = Color.White,
                            offset = Offset(1f, 1f),
                            blurRadius = 1f
                        )
                    )
                )
            }
        }

        // Statistics / Today Button
        Box(
            modifier = Modifier
                .weight(1f)
                .fillMaxHeight()
                .stacked3DBevel(
                    bevelColor = Color(0xFFBCB8A7),
                    ambientShadowColor = Color(0x24000000),
                    cornerRadius = 8.dp,
                    layers = 3
                )
                .clip(RoundedCornerShape(8.dp))
                .background(
                    brush = Brush.linearGradient(
                        colors = listOf(Color(0xFFFFFFFF), Color(0xFFE0DED3)),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    )
                )
                .border(
                    width = 1.dp,
                    brush = Brush.linearGradient(
                        listOf(Color(0xE6FFFFFF), Color(0x66FFFFFF), Color.Transparent, Color.Transparent),
                        start = Offset(0f, 0f),
                        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                    ),
                    shape = RoundedCornerShape(8.dp)
                )
                .clickable(
                    interactionSource = remember { MutableInteractionSource() },
                    indication = null,
                    onClick = onStatsOrToday
                ),
            contentAlignment = Alignment.Center
        ) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(6.dp)
            ) {
                if (isToday) {
                    StatisticsChartVectorIcon(size = 14.dp, color = Color(0xFF444E51))
                } else {
                    TodayCalendarVectorIcon(size = 14.dp, color = Color(0xFF444E51))
                }
                Text(
                    text = if (isToday) "Statistics" else "Today",
                    style = androidx.compose.ui.text.TextStyle(
                        fontFamily = PlusJakartaFontFamily,
                        fontSize = 12.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color(0xFF444E51),
                        shadow = androidx.compose.ui.graphics.Shadow(
                            color = Color.White,
                            offset = Offset(1f, 1f),
                            blurRadius = 1f
                        )
                    )
                )
            }
        }
    }
}
