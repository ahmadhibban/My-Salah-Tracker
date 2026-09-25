package com.my.salah.tracker.app.ui

import android.content.ClipData
import android.content.ClipboardManager
import android.content.Context
import android.content.SharedPreferences
import android.widget.Toast
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.interaction.MutableInteractionSource
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.StrokeJoin
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.Dp
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import androidx.compose.ui.window.DialogProperties
import com.my.salah.tracker.app.FirebaseManager
import com.my.salah.tracker.app.SalahDao
import com.my.salah.tracker.app.SalahRecord
import java.text.SimpleDateFormat
import java.util.*

/**
 * Authentic 3D Neumorphic Dialog Surface matching:
 * background: linear-gradient(145deg, #F9F9F9, #E3E3E3); border-radius: 22px; padding: 24px;
 * box-shadow: 0 20px 45px rgba(0,0,0,0.35), inset 0 2px 5px #FFF;
 * border: 1.5px solid rgba(255,255,255,0.8);
 */
@Composable
fun NeumorphicDialogSurface(
    modifier: Modifier = Modifier,
    onCloseClick: (() -> Unit)? = null,
    customBackground: Brush? = null,
    content: @Composable ColumnScope.() -> Unit
) {
    val bgBrush = customBackground ?: Brush.linearGradient(
        colors = listOf(Color(0xFFF9F9F9), Color(0xFFE3E3E3)),
        start = Offset(0f, 0f),
        end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
    )

    Box(
        modifier = modifier
            .fillMaxWidth()
            .stacked3DBevel(
                bevelColor = Color(0x15000000),
                ambientShadowColor = Color(0x59000000),
                cornerRadius = 22.dp,
                layers = 2
            )
            .clip(RoundedCornerShape(22.dp))
            .background(brush = bgBrush)
            .border(
                width = 1.5.dp,
                brush = Brush.verticalGradient(listOf(Color(0xCCFFFFFF), Color(0x66FFFFFF))),
                shape = RoundedCornerShape(22.dp)
            )
            .padding(22.dp)
    ) {
        // Optional top-right close button (.a-close)
        if (onCloseClick != null) {
            Box(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .size(32.dp)
                    .stacked3DBevel(
                        bevelColor = Color(0xFFBCB4A4),
                        ambientShadowColor = Color(0x1F000000),
                        cornerRadius = 10.dp,
                        layers = 2
                    )
                    .clip(RoundedCornerShape(10.dp))
                    .background(
                        Brush.linearGradient(listOf(Color.White, Color(0xFFDFDBD2)))
                    )
                    .border(1.dp, Color.White, RoundedCornerShape(10.dp))
                    .clickable(
                        interactionSource = remember { MutableInteractionSource() },
                        indication = null,
                        onClick = onCloseClick
                    ),
                contentAlignment = Alignment.Center
            ) {
                DialogCloseVectorIcon(size = 13.dp, color = Color(0xFF6C7A80))
            }
        }

        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            content = content
        )
    }
}

/**
 * 3D Button matching:
 * Primary: linear-gradient(135deg, #4A89DF 0%, #1A4B96 100%), bevel #133366
 * Secondary: linear-gradient(135deg, #FFFFFF 0%, #D4D1C7 100%), bevel #BCB8A7
 * Danger: linear-gradient(135deg, #E74C3C, #B03A2E), bevel #641E16
 */
@Composable
fun NeumorphicDialogButton(
    text: String,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
    isPrimary: Boolean = true,
    isDanger: Boolean = false
) {
    val (gradColors, bevelColor, textColor, topBorderColor) = when {
        isDanger -> Tuple4(
            listOf(Color(0xFFE74C3C), Color(0xFFB03A2E)),
            Color(0xFF641E16),
            Color.White,
            Color(0x4DFFFFFF)
        )
        isPrimary -> Tuple4(
            listOf(Color(0xFF4A89DF), Color(0xFF1A4B96)),
            Color(0xFF133366),
            Color.White,
            Color(0x66FFFFFF)
        )
        else -> Tuple4(
            listOf(Color(0xFFFFFFFF), Color(0xFFD4D1C7)),
            Color(0xFFBCB8A7),
            Color(0xFF444E51),
            Color.White
        )
    }

    Box(
        modifier = modifier
            .fillMaxWidth()
            .height(48.dp)
            .stacked3DBevel(
                bevelColor = bevelColor,
                ambientShadowColor = if (isPrimary || isDanger) Color(0x33000000) else Color(0x20000000),
                cornerRadius = 14.dp,
                layers = 2
            )
            .clip(RoundedCornerShape(14.dp))
            .background(
                brush = Brush.linearGradient(
                    colors = gradColors,
                    start = Offset(0f, 0f),
                    end = Offset(Float.POSITIVE_INFINITY, Float.POSITIVE_INFINITY)
                )
            )
            .border(
                width = 1.dp,
                brush = Brush.verticalGradient(listOf(topBorderColor, Color(0x1AFFFFFF))),
                shape = RoundedCornerShape(14.dp)
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = onClick
            ),
        contentAlignment = Alignment.Center
    ) {
        Text(
            text = text,
            fontSize = 14.sp,
            fontWeight = FontWeight.Black,
            color = textColor,
            letterSpacing = 0.4.sp,
            textAlign = TextAlign.Center,
            modifier = Modifier.padding(horizontal = 8.dp)
        )
    }
}

/**
 * 3D Checkbox matching .chk-3d from index.html:
 * Unchecked: 24x24, r:8px, background rgba(0,0,0,0.06), sunken shadow
 * Checked: linear-gradient(135deg, #159C4C, #0F783A), white check tick
 */
@Composable
fun Neumorphic3DCheckbox(
    isChecked: Boolean,
    onToggle: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .size(24.dp)
            .clip(RoundedCornerShape(8.dp))
            .then(
                if (isChecked) {
                    Modifier
                        .stacked3DBevel(
                            bevelColor = Color(0xFF0A5528),
                            ambientShadowColor = Color(0x4010893E),
                            cornerRadius = 8.dp,
                            layers = 1
                        )
                        .background(
                            Brush.linearGradient(listOf(Color(0xFF159C4C), Color(0xFF0F783A)))
                        )
                        .border(1.dp, Color(0x66FFFFFF), RoundedCornerShape(8.dp))
                } else {
                    Modifier
                        .background(Color(0x0F000000))
                        .border(1.dp, Color(0x1A000000), RoundedCornerShape(8.dp))
                }
            )
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = { onToggle(!isChecked) }
            ),
        contentAlignment = Alignment.Center
    ) {
        if (isChecked) {
            Canvas(modifier = Modifier.size(12.dp)) {
                val tick = androidx.compose.ui.graphics.Path().apply {
                    moveTo(2.5f * (size.width / 12f), 6.5f * (size.height / 12f))
                    lineTo(5.5f * (size.width / 12f), 9.5f * (size.height / 12f))
                    lineTo(10.5f * (size.width / 12f), 3f * (size.height / 12f))
                }
                drawPath(
                    tick,
                    color = Color.White,
                    style = Stroke(width = 2.4f * (size.width / 12f), cap = StrokeCap.Round, join = StrokeJoin.Round)
                )
            }
        }
    }
}

/**
 * 3D Option Row matching .option-3d from index.html:
 * background: linear-gradient(135deg, #FFFFFF 0%, #E8E8E8 100%);
 * box-shadow: 1px 1px 0px #C9C9C9, 2px 2px 0px #C9C9C9, 4px 5px 10px rgba(0,0,0,0.15)
 */
@Composable
fun Neumorphic3DOptionRow(
    label: String,
    isChecked: Boolean,
    onToggle: (Boolean) -> Unit,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp)
            .height(50.dp)
            .stacked3DBevel(
                bevelColor = Color(0xFFC9C9C9),
                ambientShadowColor = Color(0x26000000),
                cornerRadius = 14.dp,
                layers = 2
            )
            .clip(RoundedCornerShape(14.dp))
            .background(
                Brush.linearGradient(listOf(Color(0xFFFFFFFF), Color(0xFFE8E8E8)))
            )
            .border(1.dp, Color.White, RoundedCornerShape(14.dp))
            .clickable(
                interactionSource = remember { MutableInteractionSource() },
                indication = null,
                onClick = { onToggle(!isChecked) }
            )
            .padding(horizontal = 16.dp),
        contentAlignment = Alignment.Center
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            Text(
                text = label,
                fontSize = 13.5.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFF4A5568),
                letterSpacing = 0.5.sp
            )
            Neumorphic3DCheckbox(
                isChecked = isChecked,
                onToggle = onToggle
            )
        }
    }
}

// =========================================================================
// 1. TASBIH LIMIT MODAL (Set Target)
// =========================================================================
@Composable
fun TasbihLimitNeumorphicDialog(
    currentLimit: Int,
    onDismiss: () -> Unit,
    onSave: (Int) -> Unit
) {
    var limitInput by remember { mutableStateOf(currentLimit.toString()) }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 24.dp)) {
            NeumorphicDialogSurface {
                Text(
                    text = "Set Target",
                    fontSize = 19.sp,
                    fontWeight = FontWeight.Black,
                    color = Color(0xFF2D3748)
                )

                Spacer(modifier = Modifier.height(18.dp))

                // Sunken 3D Input (Properly centered, no text clipping)
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(52.dp)
                        .clip(RoundedCornerShape(14.dp))
                        .background(
                            Brush.linearGradient(listOf(Color(0xFFFFFFFF), Color(0xFFE8E8E8)))
                        )
                        .neumorphicInner(
                            darkShadowColor = Color(0x33000000),
                            lightShadowColor = Color.White,
                            depth = 2.dp,
                            blur = 3.dp,
                            cornerRadius = 14.dp
                        )
                        .border(1.dp, Color.White, RoundedCornerShape(14.dp)),
                    contentAlignment = Alignment.Center
                ) {
                    androidx.compose.foundation.text.BasicTextField(
                        value = limitInput,
                        onValueChange = { limitInput = it },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        singleLine = true,
                        cursorBrush = androidx.compose.ui.graphics.SolidColor(Color(0xFF4A5568)),
                        textStyle = androidx.compose.ui.text.TextStyle(
                            fontSize = 22.sp,
                            fontWeight = FontWeight.Black,
                            color = Color(0xFF4A5568),
                            textAlign = TextAlign.Center
                        ),
                        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp)
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))

                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(12.dp)
                ) {
                    NeumorphicDialogButton(
                        text = "Cancel",
                        onClick = onDismiss,
                        isPrimary = false,
                        modifier = Modifier.weight(1f)
                    )
                    NeumorphicDialogButton(
                        text = "Save",
                        onClick = {
                            val num = limitInput.trim().toIntOrNull()
                            if (num != null && num > 0) {
                                onSave(num)
                                onDismiss()
                            }
                        },
                        isPrimary = true,
                        modifier = Modifier.weight(1f)
                    )
                }
            }
        }
    }
}

// =========================================================================
// 2. MARK / UNMARK OPTIONS MODAL
// =========================================================================
@Composable
fun MarkOptionsNeumorphicDialog(
    isMark: Boolean,
    onDismiss: () -> Unit,
    onExecute: (scope: String) -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 20.dp)) {
            NeumorphicDialogSurface {
                Text(
                    text = if (isMark) "Mark Prayers" else "Unmark Prayers",
                    fontSize = 19.sp,
                    fontWeight = FontWeight.Black,
                    color = Color(0xFF2D3748)
                )

                Spacer(modifier = Modifier.height(18.dp))

                NeumorphicDialogButton(
                    text = if (isMark) "MARK FARZ ONLY" else "UNMARK FARZ ONLY",
                    onClick = {
                        onDismiss()
                        onExecute("farz")
                    },
                    isPrimary = true
                )

                Spacer(modifier = Modifier.height(12.dp))

                NeumorphicDialogButton(
                    text = if (isMark) "MARK FARZ + SUNNAH (ALL)" else "UNMARK FARZ + SUNNAH (ALL)",
                    onClick = {
                        onDismiss()
                        onExecute("all")
                    },
                    isPrimary = true
                )

                Spacer(modifier = Modifier.height(14.dp))

                NeumorphicDialogButton(
                    text = "Cancel",
                    onClick = onDismiss,
                    isPrimary = false
                )
            }
        }
    }
}

// =========================================================================
// 3. FUTURE DATE WARNING MODAL
// =========================================================================
@Composable
fun FutureDateWarningNeumorphicDialog(
    onDismiss: () -> Unit
) {
    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 20.dp)) {
            NeumorphicDialogSurface {
                // Sunken circular coin
                Box(
                    modifier = Modifier
                        .size(50.dp)
                        .clip(CircleShape)
                        .background(Color(0x0D000000))
                        .border(1.dp, Color(0x1A000000), CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    AlertCircleVectorIcon(size = 24.dp, color = Color(0xFF6C7A80))
                }

                Spacer(modifier = Modifier.height(14.dp))

                Text(
                    text = "Future Date!",
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Black,
                    color = Color(0xFF2D3748)
                )

                Spacer(modifier = Modifier.height(8.dp))

                Text(
                    text = "You cannot track prayers for a future date. Please focus on today.",
                    fontSize = 13.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF6C7A80),
                    textAlign = TextAlign.Center,
                    lineHeight = 18.sp
                )

                Spacer(modifier = Modifier.height(20.dp))

                NeumorphicDialogButton(
                    text = "Okay",
                    onClick = onDismiss,
                    isPrimary = true
                )
            }
        }
    }
}

// =========================================================================
// 4. 3D CALENDAR MONTH MODAL
// =========================================================================
@Composable
fun CalendarNeumorphicDialog(
    selectedDate: Date,
    today: Date,
    onDismiss: () -> Unit,
    onDateSelected: (Date) -> Unit,
    onFutureDateAttempt: () -> Unit
) {
    var viewMonthCal by remember { mutableStateOf(Calendar.getInstance().apply { time = selectedDate }) }
    val todayCal = remember { Calendar.getInstance().apply { time = today } }

    val monthName = remember(viewMonthCal) {
        SimpleDateFormat("MMMM yyyy", Locale.US).format(viewMonthCal.time)
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 20.dp)) {
            NeumorphicDialogSurface(
                customBackground = Brush.linearGradient(
                    listOf(Color(0xFFF8F6F1), Color(0xFFE2DFD6))
                )
            ) {
                // Month Header Row: < Month Year >
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .stacked3DBevel(
                                bevelColor = Color(0xFFC9C5BC),
                                ambientShadowColor = Color(0x20000000),
                                cornerRadius = 10.dp,
                                layers = 1
                            )
                            .clip(RoundedCornerShape(10.dp))
                            .background(
                                Brush.linearGradient(listOf(Color.White, Color(0xFFE2DFD6)))
                            )
                            .border(1.dp, Color.White, RoundedCornerShape(10.dp))
                            .clickable(
                                interactionSource = remember { MutableInteractionSource() },
                                indication = null,
                                onClick = {
                                    val c = Calendar.getInstance().apply {
                                        time = viewMonthCal.time
                                        add(Calendar.MONTH, -1)
                                    }
                                    viewMonthCal = c
                                }
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Text("<", fontSize = 15.sp, fontWeight = FontWeight.Black, color = Color(0xFF444E51))
                    }

                    Text(
                        text = monthName,
                        fontSize = 17.sp,
                        fontWeight = FontWeight.Black,
                        color = Color(0xFF444E51)
                    )

                    Box(
                        modifier = Modifier
                            .size(36.dp)
                            .stacked3DBevel(
                                bevelColor = Color(0xFFC9C5BC),
                                ambientShadowColor = Color(0x20000000),
                                cornerRadius = 10.dp,
                                layers = 1
                            )
                            .clip(RoundedCornerShape(10.dp))
                            .background(
                                Brush.linearGradient(listOf(Color.White, Color(0xFFE2DFD6)))
                            )
                            .border(1.dp, Color.White, RoundedCornerShape(10.dp))
                            .clickable(
                                interactionSource = remember { MutableInteractionSource() },
                                indication = null,
                                onClick = {
                                    val c = Calendar.getInstance().apply {
                                        time = viewMonthCal.time
                                        add(Calendar.MONTH, 1)
                                    }
                                    val tm = c.get(Calendar.YEAR) * 12 + c.get(Calendar.MONTH)
                                    val cm = todayCal.get(Calendar.YEAR) * 12 + todayCal.get(Calendar.MONTH)
                                    if (tm > cm) {
                                        onFutureDateAttempt()
                                    } else {
                                        viewMonthCal = c
                                    }
                                }
                            ),
                        contentAlignment = Alignment.Center
                    ) {
                        Text(">", fontSize = 15.sp, fontWeight = FontWeight.Black, color = Color(0xFF444E51))
                    }
                }

                Spacer(modifier = Modifier.height(15.dp))

                // Days grid: S M T W T F S
                val daysLabels = listOf("S", "M", "T", "W", "T", "F", "S")
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceAround
                ) {
                    daysLabels.forEach {
                        Text(
                            text = it,
                            fontSize = 12.sp,
                            fontWeight = FontWeight.Black,
                            color = Color(0xFF8C9496),
                            modifier = Modifier.weight(1f),
                            textAlign = TextAlign.Center
                        )
                    }
                }

                Spacer(modifier = Modifier.height(8.dp))

                // Build month grid days
                val tempCal = Calendar.getInstance().apply {
                    time = viewMonthCal.time
                    set(Calendar.DAY_OF_MONTH, 1)
                }
                val firstDayOfWeek = tempCal.get(Calendar.DAY_OF_WEEK) - 1
                val daysInMonth = tempCal.getActualMaximum(Calendar.DAY_OF_MONTH)
                val totalCells = firstDayOfWeek + daysInMonth
                val totalRows = (totalCells + 6) / 7

                val sdfKey = SimpleDateFormat("yyyy-MM-dd", Locale.US)
                val selectedKey = sdfKey.format(selectedDate)

                for (r in 0 until totalRows) {
                    Row(
                        modifier = Modifier.fillMaxWidth().padding(vertical = 3.dp),
                        horizontalArrangement = Arrangement.SpaceAround
                    ) {
                        for (c in 0 until 7) {
                            val cellIndex = r * 7 + c
                            if (cellIndex < firstDayOfWeek || cellIndex >= totalCells) {
                                Spacer(modifier = Modifier.weight(1f).height(36.dp))
                            } else {
                                val dayNum = cellIndex - firstDayOfWeek + 1
                                val dCal = Calendar.getInstance().apply {
                                    time = viewMonthCal.time
                                    set(Calendar.DAY_OF_MONTH, dayNum)
                                }
                                val isSelected = sdfKey.format(dCal.time) == selectedKey
                                val isFuture = dCal.after(todayCal)

                                Box(
                                    modifier = Modifier
                                        .weight(1f)
                                        .height(36.dp)
                                        .padding(2.dp)
                                        .stacked3DBevel(
                                            bevelColor = if (isSelected) Color(0xFF133366) else Color(0xFFC9C5BC),
                                            ambientShadowColor = if (isSelected) Color(0x401A4B96) else Color(0x1A000000),
                                            cornerRadius = 8.dp,
                                            layers = 1
                                        )
                                        .clip(RoundedCornerShape(8.dp))
                                        .background(
                                            if (isSelected) {
                                                Brush.linearGradient(listOf(Color(0xFF5D9DF5), Color(0xFF224E91)))
                                            } else {
                                                Brush.linearGradient(listOf(Color.White, Color(0xFFF0EFEB)))
                                            }
                                        )
                                        .border(
                                            1.dp,
                                            if (isSelected) Color(0x66FFFFFF) else Color.White,
                                            RoundedCornerShape(8.dp)
                                        )
                                        .clickable(
                                            interactionSource = remember { MutableInteractionSource() },
                                            indication = null
                                        ) {
                                            if (isFuture) {
                                                onFutureDateAttempt()
                                            } else {
                                                onDateSelected(dCal.time)
                                                onDismiss()
                                            }
                                        },
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = dayNum.toString(),
                                        fontSize = 13.5.sp,
                                        fontWeight = FontWeight.ExtraBold,
                                        color = when {
                                            isSelected -> Color.White
                                            isFuture -> Color(0xFFA0AAB0)
                                            else -> Color(0xFF444E51)
                                        }
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(16.dp))

                NeumorphicDialogButton(
                    text = "Close",
                    onClick = onDismiss,
                    isPrimary = false
                )
            }
        }
    }
}

// =========================================================================
// 5. SUNNAH / EXTRAS CHECKLIST MODAL
// =========================================================================
@Composable
fun SunnahExtrasNeumorphicDialog(
    prayerId: String,
    prayerName: String,
    prayerType: String,
    dateKey: String,
    sp: SharedPreferences,
    fbManager: FirebaseManager? = null,
    onDismiss: () -> Unit,
    onDone: () -> Unit
) {
    val items = remember {
        if (prayerType == "sunnah") {
            listOf(
                prayerId to "PERFORM SUNNAH"
            )
        } else {
            when (prayerId) {
                "fajr" -> listOf(
                    "sunnah_before" to "SUNNAH (BEFORE FAJR)",
                    "ishraq" to "ISHRAQ PRAYER",
                    "chasht" to "CHASHT (DUHA) PRAYER"
                )
                "dhuhr" -> listOf(
                    "sunnah_before" to "SUNNAH (4 RAK'AH BEFORE)",
                    "sunnah_after" to "SUNNAH (2 RAK'AH AFTER)"
                )
                "maghrib" -> listOf(
                    "sunnah_after" to "SUNNAH (2 RAK'AH AFTER)",
                    "awabin" to "AWABIN PRAYER"
                )
                else -> emptyList()
            }
        }
    }

    val checkedStates = remember {
        mutableStateMapOf<String, Boolean>().apply {
            items.forEach { (subKey, _) ->
                this[subKey] = sp.getBoolean("${dateKey}_${prayerId}_${subKey}", false)
            }
        }
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 20.dp)) {
            NeumorphicDialogSurface {
                Text(
                    text = "$prayerName " + if (prayerType == "sunnah") "Sunnah" else "Extras",
                    fontSize = 19.sp,
                    fontWeight = FontWeight.Black,
                    color = Color(0xFF2D3748)
                )

                Spacer(modifier = Modifier.height(18.dp))

                items.forEach { (subKey, label) ->
                    val isChecked = checkedStates[subKey] == true

                    Neumorphic3DOptionRow(
                        label = label,
                        isChecked = isChecked,
                        onToggle = { nextVal ->
                            checkedStates[subKey] = nextVal
                            sp.edit().putBoolean("${dateKey}_${prayerId}_${subKey}", nextVal).apply()
                            fbManager?.save(dateKey, "${prayerId}_${subKey}", if (nextVal) "yes" else "no")
                        }
                    )
                }

                Spacer(modifier = Modifier.height(20.dp))

                NeumorphicDialogButton(
                    text = "Save & Close",
                    onClick = {
                        onDismiss()
                        onDone()
                    },
                    isPrimary = true
                )
            }
        }
    }
}

// =========================================================================
// 6. WEEKLY PROGRESS / STATISTICS MODAL
// =========================================================================
@Composable
fun WeeklyStatsNeumorphicDialog(
    selectedDate: Date,
    sp: SharedPreferences,
    dao: SalahDao,
    onDismiss: () -> Unit
) {
    val prayers = listOf("fajr", "dhuhr", "asr", "maghrib", "isha", "witr")
    val prayerColors = listOf(
        Brush.linearGradient(listOf(Color(0xFF7C988F), Color(0xFF5C7B71))),
        Brush.linearGradient(listOf(Color(0xFFC2A882), Color(0xFFA38760))),
        Brush.linearGradient(listOf(Color(0xFF7A8EAA), Color(0xFF5B6F8C))),
        Brush.linearGradient(listOf(Color(0xFFB5848C), Color(0xFF94646B))),
        Brush.linearGradient(listOf(Color(0xFF574643), Color(0xFF3D2D2A))),
        Brush.linearGradient(listOf(Color(0xFF3A4A5A), Color(0xFF253140)))
    )

    // Calculate weekly statistics
    val (prayersRatio, jamaatPct, sunnahPct, weekGrid) = remember(selectedDate) {
        val startOfWeek = Calendar.getInstance().apply {
            time = selectedDate
            val dayOffset = if (get(Calendar.DAY_OF_WEEK) == Calendar.SATURDAY) 0 else get(Calendar.DAY_OF_WEEK)
            add(Calendar.DAY_OF_MONTH, -dayOffset)
        }

        var totalPrayers = 0
        var donePrayers = 0
        var doneJamaat = 0
        var doneSunnah = 0
        var totalSunnah = 0
        val todayCal = Calendar.getInstance()

        val daysList = mutableListOf<Triple<String, Boolean, List<Boolean>>>() // label, isToday, pills
        val dayNames = arrayOf("S", "S", "M", "T", "W", "T", "F")
        val sdfKey = SimpleDateFormat("yyyy-MM-dd", Locale.US)
        val todayKey = sdfKey.format(todayCal.time)

        for (i in 0 until 7) {
            val dCal = Calendar.getInstance().apply {
                time = startOfWeek.time
                add(Calendar.DAY_OF_MONTH, i)
            }
            val key = sdfKey.format(dCal.time)
            val record = dao.getRecordByDate(key) ?: SalahRecord(key)
            val isPastOrToday = !dCal.after(todayCal)

            val pills = mutableListOf<Boolean>()
            for (p in prayers) {
                val done = record.getFardStat(p) == "yes"
                val isJ = record.getJamaatStat(p) == "yes"
                if (isPastOrToday) {
                    totalPrayers++
                    if (done) {
                        donePrayers++
                        if (isJ) doneJamaat++
                    }
                }
                pills.add(done)
            }

            if (isPastOrToday) {
                val sunnahKeys = listOf(
                    "fajr_sunnah_before", "fajr_ishraq", "fajr_chasht",
                    "dhuhr_sunnah_before", "dhuhr_sunnah_after",
                    "asr_asr",
                    "maghrib_sunnah_after", "maghrib_awabin",
                    "isha_isha",
                    "witr_witr"
                )
                totalSunnah += sunnahKeys.size
                for (sKey in sunnahKeys) {
                    if (sp.getBoolean("${key}_$sKey", false)) {
                        doneSunnah++
                    }
                }
            }
            daysList.add(Triple(dayNames[i], key == todayKey, pills))
        }

        val jPct = if (donePrayers > 0) (doneJamaat * 100 / donePrayers) else 0
        val sPct = if (totalSunnah > 0) (doneSunnah * 100 / totalSunnah) else 0

        Tuple4("$donePrayers/$totalPrayers", "$jPct%", "$sPct%", daysList)
    }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 20.dp, vertical = 20.dp)) {
            NeumorphicDialogSurface {
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.Center,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    DialogBarChartVectorIcon(size = 20.dp, color = Color(0xFF364455))
                    Spacer(modifier = Modifier.width(8.dp))
                    Text(
                        text = "Weekly Progress",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Black,
                        color = Color(0xFF364455)
                    )
                }

                Spacer(modifier = Modifier.height(18.dp))

                // 3 Top Stats: Prayers, Jamaat, Sunnah (.option-3d)
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    WeeklyStatCard(title = "PRAYERS", value = prayersRatio, valColor = Color(0xFF1C3682), modifier = Modifier.weight(1f))
                    WeeklyStatCard(title = "JAMAAT", value = jamaatPct, valColor = Color(0xFF1C7043), modifier = Modifier.weight(1f))
                    WeeklyStatCard(title = "SUNNAH", value = sunnahPct, valColor = Color(0xFFA13824), modifier = Modifier.weight(1f))
                }

                Spacer(modifier = Modifier.height(18.dp))

                // Sunken tray: background: linear-gradient(135deg, #EAECEF, #F4F6F8); border-radius: 20px
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .clip(RoundedCornerShape(20.dp))
                        .background(
                            Brush.linearGradient(listOf(Color(0xFFEAECEF), Color(0xFFF4F6F8)))
                        )
                        .border(1.dp, Color(0x99FFFFFF), RoundedCornerShape(20.dp))
                        .padding(horizontal = 12.dp, vertical = 18.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween
                    ) {
                        weekGrid.forEach { (dayLetter, isToday, pills) ->
                            Column(
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.spacedBy(6.dp)
                            ) {
                                pills.forEachIndexed { idx, done ->
                                    Box(
                                        modifier = Modifier
                                            .width(24.dp)
                                            .height(12.dp)
                                            .clip(RoundedCornerShape(6.dp))
                                            .then(
                                                if (done) {
                                                    Modifier
                                                        .background(prayerColors[idx])
                                                        .border(1.dp, Color(0x66FFFFFF), RoundedCornerShape(6.dp))
                                                } else {
                                                    Modifier
                                                        .background(Color(0x08000000))
                                                        .border(0.5.dp, Color(0x14000000), RoundedCornerShape(6.dp))
                                                }
                                            )
                                    )
                                }

                                Spacer(modifier = Modifier.height(4.dp))

                                // Day label circle (.stats-day-lbl)
                                Box(
                                    modifier = Modifier
                                        .size(24.dp)
                                        .clip(CircleShape)
                                        .then(
                                            if (isToday) {
                                                Modifier
                                                    .background(
                                                        Brush.linearGradient(listOf(Color(0xFF4A89DF), Color(0xFF1A4B96)))
                                                    )
                                            } else {
                                                Modifier
                                                    .background(
                                                        Brush.linearGradient(listOf(Color(0xFFF9F9F9), Color(0xFFE3E3E3)))
                                                    )
                                                    .border(1.dp, Color.White, CircleShape)
                                            }
                                        ),
                                    contentAlignment = Alignment.Center
                                ) {
                                    Text(
                                        text = dayLetter,
                                        fontSize = 10.sp,
                                        fontWeight = FontWeight.Black,
                                        color = if (isToday) Color.White else Color(0xFF8A9499)
                                    )
                                }
                            }
                        }
                    }
                }

                Spacer(modifier = Modifier.height(20.dp))

                NeumorphicDialogButton(
                    text = "Excellent, Keep It Up!",
                    onClick = onDismiss,
                    isPrimary = true
                )
            }
        }
    }
}

@Composable
private fun WeeklyStatCard(
    title: String,
    value: String,
    valColor: Color,
    modifier: Modifier = Modifier
) {
    Box(
        modifier = modifier
            .stacked3DBevel(
                bevelColor = Color(0xFFC9C9C9),
                ambientShadowColor = Color(0x1F000000),
                cornerRadius = 14.dp,
                layers = 1
            )
            .clip(RoundedCornerShape(14.dp))
            .background(
                Brush.linearGradient(listOf(Color(0xFFFFFFFF), Color(0xFFE8E8E8)))
            )
            .border(1.dp, Color.White, RoundedCornerShape(14.dp))
            .padding(vertical = 12.dp, horizontal = 4.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            Text(
                text = title,
                fontSize = 9.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color(0xFF8A9499),
                letterSpacing = 0.5.sp
            )
            Spacer(modifier = Modifier.height(4.dp))
            Text(
                text = value,
                fontSize = 18.sp,
                fontWeight = FontWeight.Black,
                color = valColor
            )
        }
    }
}

// =========================================================================
// 7. AUTH / PROFILE MODAL (Matches auth.js 100%)
// =========================================================================
@Composable
fun AuthNeumorphicDialog(
    sp: SharedPreferences,
    fbManager: FirebaseManager,
    onDismiss: () -> Unit,
    onAuthChanged: () -> Unit
) {
    val context = LocalContext.current
    var isLoggedIn by remember { mutableStateOf(sp.getBoolean("is_logged_in", false)) }
    var regEmail by remember { mutableStateOf(sp.getString("user_email", "") ?: "") }

    var authEmail by remember { mutableStateOf("") }
    var emailError by remember { mutableStateOf(false) }
    var isLoading by remember { mutableStateOf(false) }
    var isLogoutConfirmOpen by remember { mutableStateOf(false) }

    Dialog(
        onDismissRequest = onDismiss,
        properties = DialogProperties(usePlatformDefaultWidth = false)
    ) {
        Box(modifier = Modifier.fillMaxWidth().padding(horizontal = 24.dp, vertical = 20.dp)) {
            NeumorphicDialogSurface(
                onCloseClick = if (!isLogoutConfirmOpen) onDismiss else null
            ) {
                if (isLoggedIn) {
                    if (isLogoutConfirmOpen) {
                        // LOGOUT CONFIRMATION STATE
                        Box(
                            modifier = Modifier
                                .size(50.dp)
                                .stacked3DBevel(
                                    bevelColor = Color(0xFF641E16),
                                    ambientShadowColor = Color(0x4D000000),
                                    cornerRadius = 25.dp,
                                    layers = 2
                                )
                                .clip(CircleShape)
                                .background(
                                    Brush.linearGradient(listOf(Color(0xFFE74C3C), Color(0xFFB03A2E)))
                                )
                                .border(1.dp, Color(0x4DFFFFFF), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            WarningTriangleVectorIcon(size = 24.dp, color = Color.White)
                        }

                        Spacer(modifier = Modifier.height(14.dp))

                        Text(
                            text = "Logout?",
                            fontSize = 20.sp,
                            fontWeight = FontWeight.Black,
                            color = Color(0xFF2D3748)
                        )

                        Spacer(modifier = Modifier.height(8.dp))

                        Text(
                            text = "Your local data will be cleared. Restore anytime by logging in.",
                            fontSize = 13.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF6C7A80),
                            textAlign = TextAlign.Center,
                            lineHeight = 18.sp
                        )

                        Spacer(modifier = Modifier.height(22.dp))

                        Row(
                            modifier = Modifier.fillMaxWidth(),
                            horizontalArrangement = Arrangement.spacedBy(10.dp)
                        ) {
                            NeumorphicDialogButton(
                                text = "Cancel",
                                onClick = { isLogoutConfirmOpen = false },
                                isPrimary = false,
                                modifier = Modifier.weight(1f)
                            )
                            NeumorphicDialogButton(
                                text = "Yes, Logout",
                                onClick = {
                                    val editor = sp.edit()
                                    editor.putBoolean("is_logged_in", false)
                                    editor.putString("user_email", "")
                                    editor.putString("user_password", "")
                                    editor.remove("last_sync")
                                    for (k in sp.all.keys) {
                                        if (k.matches(Regex("\\d{4}-\\d{2}-\\d{2}.*"))) {
                                            editor.remove(k)
                                        }
                                    }
                                    editor.apply()
                                    com.my.salah.tracker.app.SalahDatabase.getDatabase(context).clearAllTables()
                                    isLoggedIn = false
                                    regEmail = ""
                                    onAuthChanged()
                                    onDismiss()
                                },
                                isPrimary = false,
                                isDanger = true,
                                modifier = Modifier.weight(1f)
                            )
                        }
                    } else {
                        // LOGGED IN PROFILE VIEW
                        Box(
                            modifier = Modifier
                                .size(55.dp)
                                .stacked3DBevel(
                                    bevelColor = Color(0xFF0F783A),
                                    ambientShadowColor = Color(0x4D159C4C),
                                    cornerRadius = 27.5.dp,
                                    layers = 2
                                )
                                .clip(CircleShape)
                                .background(
                                    Brush.linearGradient(listOf(Color(0xFF159C4C), Color(0xFF0F783A)))
                                )
                                .border(1.dp, Color(0x66FFFFFF), CircleShape),
                            contentAlignment = Alignment.Center
                        ) {
                            EngravedUserIcon(size = 24.dp, isLoggedIn = false)
                        }

                        Spacer(modifier = Modifier.height(12.dp))

                        Text(
                            text = "Profile",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Black,
                            color = Color(0xFF2D3748)
                        )

                        Spacer(modifier = Modifier.height(4.dp))

                        Text(
                            text = regEmail,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Black,
                            color = Color(0xFF4A5568),
                            letterSpacing = 0.5.sp
                        )

                        Spacer(modifier = Modifier.height(18.dp))

                        // Cloud Sync Status Box (.a-sync)
                        Box(
                            modifier = Modifier
                                .fillMaxWidth()
                                .stacked3DBevel(
                                    bevelColor = Color(0xFFC9C9C9),
                                    ambientShadowColor = Color(0x1A000000),
                                    cornerRadius = 16.dp,
                                    layers = 1
                                )
                                .clip(RoundedCornerShape(16.dp))
                                .background(
                                    Brush.linearGradient(listOf(Color.White, Color(0xFFE8E8E8)))
                                )
                                .border(1.dp, Color.White, RoundedCornerShape(16.dp))
                                .padding(14.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                                Row(
                                    verticalAlignment = Alignment.CenterVertically,
                                    horizontalArrangement = Arrangement.Center
                                ) {
                                    Box(
                                        modifier = Modifier
                                            .size(8.dp)
                                            .clip(CircleShape)
                                            .background(Color(0xFF159C4C))
                                    )
                                    Spacer(modifier = Modifier.width(8.dp))
                                    Text(
                                        text = "Cloud Syncing Active",
                                        fontSize = 13.sp,
                                        fontWeight = FontWeight.Black,
                                        color = Color(0xFF4A5568)
                                    )
                                }
                                Spacer(modifier = Modifier.height(4.dp))
                                val time = SimpleDateFormat("hh:mm a", Locale.US).format(Date())
                                Text(
                                    text = "Last Synced: $time",
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFF8A9499)
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(20.dp))

                        NeumorphicDialogButton(
                            text = "Logout",
                            onClick = { isLogoutConfirmOpen = true },
                            isPrimary = false,
                            isDanger = true
                        )
                    }
                } else {
                    // NOT LOGGED IN (Create Account or Login)
                    Box(
                        modifier = Modifier
                            .size(55.dp)
                            .clip(CircleShape)
                            .background(Color(0x0D000000))
                            .border(1.dp, Color(0x1A000000), CircleShape),
                        contentAlignment = Alignment.Center
                    ) {
                        EngravedUserIcon(size = 24.dp, isLoggedIn = false)
                    }

                    Spacer(modifier = Modifier.height(14.dp))

                    Text(
                        text = "Cloud Sync / Login",
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Black,
                        color = Color(0xFF2D3748)
                    )

                    Spacer(modifier = Modifier.height(6.dp))

                    Text(
                        text = "Directly sync and restore all your prayer data with your email.",
                        fontSize = 12.5.sp,
                        fontWeight = FontWeight.Medium,
                        color = Color(0xFF6C7A80),
                        textAlign = TextAlign.Center,
                        lineHeight = 16.sp
                    )

                    Spacer(modifier = Modifier.height(18.dp))

                    // Email Input (.a-input)
                    Box(
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(50.dp)
                            .clip(RoundedCornerShape(14.dp))
                            .background(
                                Brush.linearGradient(listOf(Color.White, Color(0xFFE8E8E8)))
                            )
                            .border(
                                1.dp,
                                if (emailError) Color(0xFFE53E3E) else Color.White,
                                RoundedCornerShape(14.dp)
                            ),
                        contentAlignment = Alignment.CenterStart
                    ) {
                        androidx.compose.foundation.text.BasicTextField(
                            value = authEmail,
                            onValueChange = {
                                authEmail = it
                                emailError = false
                            },
                            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                            singleLine = true,
                            cursorBrush = androidx.compose.ui.graphics.SolidColor(Color(0xFF4A5568)),
                            textStyle = androidx.compose.ui.text.TextStyle(
                                fontSize = 14.5.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFF4A5568)
                            ),
                            modifier = Modifier.fillMaxWidth().padding(horizontal = 14.dp),
                            decorationBox = { innerTextField ->
                                if (authEmail.isEmpty()) {
                                    Text("Enter your email address", fontSize = 14.sp, fontWeight = FontWeight.Bold, color = Color(0xFFA0AAB0))
                                }
                                innerTextField()
                            }
                        )
                    }

                    if (emailError) {
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "Please enter a valid email address",
                            fontSize = 11.5.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFFE53E3E)
                        )
                    }

                    Spacer(modifier = Modifier.height(18.dp))

                    NeumorphicDialogButton(
                        text = if (isLoading) "Syncing Data..." else "Login & Sync",
                        onClick = {
                            val em = authEmail.trim().lowercase(Locale.US)
                            if (android.util.Patterns.EMAIL_ADDRESS.matcher(em).matches()) {
                                isLoading = true
                                emailError = false
                                fbManager.loginWithEmail(em) {
                                    isLoading = false
                                    onAuthChanged()
                                    onDismiss()
                                }
                            } else {
                                emailError = true
                            }
                        },
                        isPrimary = true
                    )
                }
            }
        }
    }
}

private data class Tuple4<A, B, C, D>(val a: A, val b: B, val c: C, val d: D)
