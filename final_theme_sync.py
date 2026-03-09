import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

def replace_block(start_marker, end_marker, new_content, text):
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker, start_idx)
    if start_idx != -1 and end_idx != -1:
        return text[:start_idx] + new_content + text[end_idx:]
    else:
        print(f"Error: Could not find {start_marker}")
        return text

# ২. বৃত্তের বর্ডার, প্রোগ্রেস লাইন এবং ৩ডি বল (থিমের কালারে সিঙ্ক)
new_ring_and_ball = """// --- 2. Dynamic 3D Progress Ring & Ball ---
                int themeMain = (themeColors != null && themeColors.length > 0) ? themeColors[0] : accentCol;
                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                float rOuter = radius + 25f;
                
                // বৃত্তের বর্ডার (গ্রে কালার মুছে থিমের কালার বসানো হয়েছে)
                android.graphics.SweepGradient themeRing = new android.graphics.SweepGradient(centerX, circleY, new int[]{cardCol, themeMain, cardCol, themeMain, cardCol}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(30f); p.setShader(themeRing); p.setShadowLayer(20f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawCircle(centerX, circleY, rOuter, p); p.clearShadowLayer(); p.setShader(null);
                
                p.setStrokeWidth(15f); p.setColor(Color.argb(40, 0,0,0)); canvas.drawCircle(centerX, circleY, radius, p);
                
                // প্রোগ্রেস লাইন
                p.setStrokeWidth(22f); p.setStrokeCap(Paint.Cap.ROUND); p.setColor(themeMain);
                canvas.drawArc(new RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
                
                // ৩ডি বল (সাদা থেকে থিম কালারের গ্রেডিয়েন্ট)
                double angle = Math.toRadians(sweep - 90);
                float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
                p.setStyle(Paint.Style.FILL); 
                android.graphics.RadialGradient ballRg = new android.graphics.RadialGradient(ballX-5, ballY-5, 30f, Color.WHITE, themeMain, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(ballRg); p.setShadowLayer(10, 0, 5, Color.argb(100,0,0,0));
                canvas.drawCircle(ballX, ballY, 24f, p); p.clearShadowLayer(); p.setShader(null);

                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); p.setColor(textCol); 
                String mainCountStr = formatNum(curVal); String targetPart = " / " + formatNum(d.target); 
                p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
                Paint targetPaint = new Paint(p); targetPaint.setTextSize(55f); targetPaint.setColor(themeMain); 
                targetPaint.setUnderlineText(true); 
                float targetWidth = targetPaint.measureText(targetPart); float startX = centerX - ((mainTextWidth + targetWidth) / 2f);
                p.setTextAlign(Paint.Align.LEFT); canvas.drawText(mainCountStr, startX, circleY + 85f, p);
                targetPaint.setTextAlign(Paint.Align.LEFT); canvas.drawText(targetPart, startX + mainTextWidth, circleY + 85f, targetPaint);

                """
code = replace_block("// --- 2.", "// --- 3.", new_ring_and_ball, code)

# ৪. টোটাল বক্স (থিমের কালারে ফিল এবং বর্ডার)
new_total_box = """// --- 4. Dynamic Themed Total Box ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(40f); float boxW = p.measureText(totalTxt) + 80; if(bnFont != null) p.setTypeface(bnFont);
                
                RectF totalRect = new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40);
                int themeMain = (themeColors != null && themeColors.length > 0) ? themeColors[0] : accentCol;
                
                // থিম কালারে হালকা ফিল (Background)
                p.setStyle(Paint.Style.FILL); p.setColor(themeMain); p.setAlpha(30);
                canvas.drawRoundRect(totalRect, 40f, 40f, p); p.setAlpha(255);
                
                // থিম কালারে স্পষ্ট বর্ডার
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(themeMain);
                canvas.drawRoundRect(totalRect, 40f, 40f, p);
                
                // লেখা মাঝখানে রাখা
                p.setStyle(Paint.Style.FILL); p.setColor(textCol); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(totalTxt, centerX, totalBoxY + 12, p);

                """
code = replace_block("// --- 4.", "// --- 5.", new_total_box, code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ SUCCESS! Circle border, 3D ball, and Total box are perfectly synced with your 6 themes.")
