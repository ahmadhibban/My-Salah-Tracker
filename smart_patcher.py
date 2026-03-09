import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

def replace_block(start_marker, end_marker, new_content, text):
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker, start_idx)
    if start_idx != -1 and end_idx != -1:
        return text[:start_idx] + new_content + text[end_idx:]
    return text

# ১. সালাহ ট্যাবের মতো ডে/নাইট দোয়ার বক্স
new_box = """// --- 1. Salah Tab Style Day/Night Dua Box ---
                RectF boxRect = new RectF(40, boxTop, w - 40, boxTop + boxHeight);
                int hour = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY);
                boolean isDayTime = (hour >= 6 && hour < 18);
                int[] cardColors = isDayTime ? new int[]{Color.parseColor("#FFB75E"), Color.parseColor("#ED8F03")} 
                                             : new int[]{Color.parseColor("#00C9FF"), Color.parseColor("#1A2980")};
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(
                    40, boxTop, w-40, boxTop+boxHeight, cardColors[0], cardColors[1], android.graphics.Shader.TileMode.CLAMP);
                p.setShader(lg); p.setShadowLayer(15f, 0, 10f, Color.argb(60, 0, 0, 0));
                canvas.drawRoundRect(boxRect, 50f, 50f, p); p.clearShadowLayer(); p.setShader(null);

                TextPaint tp = new TextPaint(Paint.ANTI_ALIAS_FLAG);
                if(arabicFont != null) tp.setTypeface(arabicFont); 
                tp.setColor(Color.WHITE); tp.setShadowLayer(5f, 0f, 2f, Color.argb(150, 0,0,0));
                int layoutWidth = (int)(w - 100); 
                if (layoutWidth > 0) {
                    float autoFontSize = 95f; android.text.StaticLayout sl;
                    while (true) {
                        tp.setTextSize(autoFontSize);
                        sl = new android.text.StaticLayout(d.arabic, tp, layoutWidth, android.text.Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false);
                        if (sl.getHeight() <= (boxHeight - 40f) || autoFontSize <= 35f) break; autoFontSize -= 2f; 
                    }
                    canvas.save(); canvas.translate(centerX - (layoutWidth / 2f), boxTop + (boxHeight - sl.getHeight()) / 2f);
                    sl.draw(canvas); canvas.restore(); tp.clearShadowLayer();
                }

                """
code = replace_block("// --- 1.", "// --- 2.", new_box, code)

# ২. প্রোগ্রেস লাইন এবং ৩ডি বল থিমের কালারে ফিল করা
new_ring = """// --- 2. Dynamic 3D Progress Ring & Ball ---
                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                float rOuter = radius + 25f;
                
                android.graphics.SweepGradient metallic = new android.graphics.SweepGradient(centerX, circleY, new int[]{cardCol, Color.GRAY, cardCol, Color.LTGRAY, cardCol}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(30f); p.setShader(metallic); p.setShadowLayer(20f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawCircle(centerX, circleY, rOuter, p); p.clearShadowLayer(); p.setShader(null);
                
                p.setStrokeWidth(15f); p.setColor(Color.argb(40, 0,0,0)); canvas.drawCircle(centerX, circleY, radius, p);
                
                // প্রোগ্রেস লাইন থিমের অ্যাকসেন্ট কালারে
                p.setStrokeWidth(22f); p.setStrokeCap(Paint.Cap.ROUND); p.setColor(accentCol);
                canvas.drawArc(new RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
                
                // ৩ডি বল থিমের অ্যাকসেন্ট কালারে
                double angle = Math.toRadians(sweep - 90);
                float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
                p.setStyle(Paint.Style.FILL); 
                android.graphics.RadialGradient ballRg = new android.graphics.RadialGradient(ballX-5, ballY-5, 30f, Color.WHITE, accentCol, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(ballRg); p.setShadowLayer(10, 0, 5, Color.argb(100,0,0,0));
                canvas.drawCircle(ballX, ballY, 24f, p); p.clearShadowLayer(); p.setShader(null);

                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); p.setColor(textCol); 
                String mainCountStr = formatNum(curVal); String targetPart = " / " + formatNum(d.target); 
                p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
                Paint targetPaint = new Paint(p); targetPaint.setTextSize(55f); targetPaint.setColor(accentCol); 
                targetPaint.setUnderlineText(true); 
                float targetWidth = targetPaint.measureText(targetPart); float startX = centerX - ((mainTextWidth + targetWidth) / 2f);
                p.setTextAlign(Paint.Align.LEFT); canvas.drawText(mainCountStr, startX, circleY + 85f, p);
                targetPaint.setTextAlign(Paint.Align.LEFT); canvas.drawText(targetPart, startX + mainTextWidth, circleY + 85f, targetPaint);

                """
code = replace_block("// --- 2.", "// --- 3.", new_ring, code)

# ৩. টোটাল/লুপ বক্সে থিম কালারের চিকন বর্ডার
new_total = """// --- 4. Dynamic Themed Total Box ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(40f); float boxW = p.measureText(totalTxt) + 80; if(bnFont != null) p.setTypeface(bnFont);
                
                RectF totalRect = new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40);
                
                // ব্যাকগ্রাউন্ড
                p.setStyle(Paint.Style.FILL); p.setColor(cardCol);
                p.setShadowLayer(8f, 0, 4f, Color.argb(40, 0, 0, 0));
                canvas.drawRoundRect(totalRect, 40f, 40f, p); p.clearShadowLayer();
                
                // চিকন বর্ডার (থিমের অ্যাকসেন্ট কালারে)
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(3f); p.setColor(accentCol);
                canvas.drawRoundRect(totalRect, 40f, 40f, p);
                
                // মাঝখানে টেক্সট
                p.setStyle(Paint.Style.FILL); p.setColor(textCol); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(totalTxt, centerX, totalBoxY + 12, p);

                """
code = replace_block("// --- 4.", "// --- 5.", new_total, code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Magic executed! All layout updates applied flawlessly.")
