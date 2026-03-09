import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. ৩ডি থিম কালারগুলো আবার ফিরিয়ে আনা
new_themes = """    final int[][] beadThemes = {
        {Color.parseColor("#111111"), Color.parseColor("#666666")}, 
        {Color.parseColor("#E0E0E0"), Color.parseColor("#FFFFFF")}, 
        {Color.parseColor("#D4AF37"), Color.parseColor("#FFF5C3")}, 
        {Color.parseColor("#B87333"), Color.parseColor("#F5DEB3")}, 
        {Color.parseColor("#5C4033"), Color.parseColor("#8B5A2B")}, 
        {Color.parseColor("#2E8B57"), Color.parseColor("#8FBC8F")}  
    };"""
import re
code = re.sub(r'final int\[\]\[\] beadThemes = \{.*?\};', new_themes, code, flags=re.DOTALL)

# ২. ড্রয়িং লজিক আপডেট (গোছানো পজিশন + প্রিমিয়াম ৩ডি)
new_draw = """            @Override protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                float w = getWidth(), h = getHeight(), centerX = w / 2.0f;
                Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
                int idx = currentIdx[0]; if (idx >= tasbihList.size()) idx = 0;
                TasbihData d = tasbihList.get(idx); int curVal = individualCounts[idx];

                // --- সালাহ পেইজের মতো গোছানো পজিশন ---
                float boxTop = h * 0.03f, boxHeight = h * 0.17f;
                float iconY = boxTop + boxHeight + (h * 0.08f);
                float circleY = iconY + (h * 0.16f), radius = w * 0.30f;
                float beadY = circleY + radius + (h * 0.12f);
                float totalBoxY = beadY + (h * 0.08f);
                float themeY = h - (h * 0.05f);

                // --- 1. Premium 3D Golden Dua Box ---
                RectF boxRect = new RectF(40, boxTop, w - 40, boxTop + boxHeight);
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(
                    40, boxTop, w-40, boxTop+boxHeight, 
                    new int[]{0xFFE6C27A, 0xFFB8860B, 0xFFFFD700, 0xFF8B6508}, 
                    new float[]{0f, 0.3f, 0.7f, 1f}, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(lg); p.setShadowLayer(25f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawRoundRect(boxRect, 30f, 30f, p); p.clearShadowLayer(); p.setShader(null);
                
                // ইনার বর্ডার (দোয়ার বক্সের সৌন্দর্য বাড়াতে)
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(Color.parseColor("#FFF8DC"));
                canvas.drawRoundRect(new RectF(48, boxTop+8, w-48, boxTop+boxHeight-8), 24f, 24f, p); p.setStyle(Paint.Style.FILL);

                TextPaint tp = new TextPaint(Paint.ANTI_ALIAS_FLAG);
                if(arabicFont != null) tp.setTypeface(arabicFont); 
                tp.setColor(Color.WHITE); tp.setShadowLayer(8f, 0f, 4f, Color.argb(180, 0,0,0));
                int layoutWidth = (int)(w - 100); float autoFontSize = 95f; android.text.StaticLayout sl;
                while (true) {
                    tp.setTextSize(autoFontSize);
                    sl = new android.text.StaticLayout(d.arabic, tp, layoutWidth, android.text.Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false);
                    if (sl.getHeight() <= (boxHeight - 40f) || autoFontSize <= 35f) break; autoFontSize -= 2f; 
                }
                canvas.save(); canvas.translate(centerX - (layoutWidth / 2f), boxTop + (boxHeight - sl.getHeight()) / 2f);
                sl.draw(canvas); canvas.restore(); tp.clearShadowLayer();

                p.setColor(themeColors != null ? themeColors[3] : Color.GRAY); p.setTextSize(30f); p.setTextAlign(Paint.Align.CENTER);
                if(bnFont != null) p.setTypeface(bnFont);
                canvas.drawText(isBn ? "দোয়া পরিবর্তন করতে সোয়াইপ, সেটিংসে যেতে ক্লিক করুন" : "Swipe to change, Tap for settings", centerX, boxTop + boxHeight + 45f, p);

                // --- 2. 3D Icons ---
                float sideMargin = w * 0.16f; float[] iconXs = {sideMargin, w - sideMargin};
                String[] icons = {"↻", (isSoundOn[0] ? "🔊" : "🔇")};
                int[][] iconColors = {{0xFFA8E6CF, 0xFF3B8E63}, {0xFFFFA07A, 0xFF8B4513}}; 

                for(int i=0; i<2; i++) {
                    p.setStyle(Paint.Style.FILL);
                    android.graphics.RadialGradient iRg = new android.graphics.RadialGradient(iconXs[i]-10, iconY-10, 80f, iconColors[i][0], iconColors[i][1], android.graphics.Shader.TileMode.CLAMP);
                    p.setShader(iRg); p.setShadowLayer(15, 0, 10, Color.argb(100,0,0,0));
                    canvas.drawCircle(iconXs[i], iconY, 65f, p); p.clearShadowLayer(); p.setShader(null);
                    
                    p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(6f); p.setColor(Color.parseColor("#B8860B"));
                    canvas.drawCircle(iconXs[i], iconY, 60f, p); p.setStyle(Paint.Style.FILL);
                    
                    p.setColor(Color.WHITE); p.setTextAlign(Paint.Align.CENTER); p.setTextSize(i==0?80f:60f); p.setShadowLayer(5,0,2,Color.BLACK);
                    canvas.drawText(icons[i], iconXs[i], iconY + (i==0?25f:20f), p); p.clearShadowLayer();
                }

                // --- 3. 3D Progress Ring & Ball ---
                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                float rOuter = radius + 25f;
                android.graphics.SweepGradient silver = new android.graphics.SweepGradient(centerX, circleY, new int[]{0xFFE0E0E0, 0xFF888888, 0xFFFFFFFF, 0xFF555555, 0xFFE0E0E0}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(30f); p.setShader(silver); p.setShadowLayer(20f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawCircle(centerX, circleY, rOuter, p); p.clearShadowLayer(); p.setShader(null);
                
                p.setStrokeWidth(15f); p.setColor(Color.parseColor("#E0E0E0")); canvas.drawCircle(centerX, circleY, radius, p);
                
                p.setStrokeWidth(22f); p.setStrokeCap(Paint.Cap.ROUND); p.setColor(Color.parseColor("#FFD700"));
                canvas.drawArc(new RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
                
                // 3D Progress Thumb Ball
                double angle = Math.toRadians(sweep - 90);
                float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
                p.setStyle(Paint.Style.FILL); 
                android.graphics.RadialGradient ballRg = new android.graphics.RadialGradient(ballX-8, ballY-8, 35f, 0xFFFFF8DC, 0xFFB8860B, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(ballRg); p.setShadowLayer(15, 0, 8, Color.argb(150,0,0,0));
                canvas.drawCircle(ballX, ballY, 28f, p); p.clearShadowLayer(); p.setShader(null);

                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); p.setColor(themeColors != null ? themeColors[2] : Color.BLACK); 
                String mainCountStr = formatNum(curVal); String targetPart = " / " + formatNum(d.target); 
                p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
                Paint targetPaint = new Paint(p); targetPaint.setTextSize(48f); targetPaint.setColor(themeColors != null ? themeColors[3] : Color.parseColor("#7F8C8D")); 
                float targetWidth = targetPaint.measureText(targetPart); float startX = centerX - ((mainTextWidth + targetWidth) / 2f);
                p.setTextAlign(Paint.Align.LEFT); canvas.drawText(mainCountStr, startX, circleY + 85f, p);
                targetPaint.setTextAlign(Paint.Align.LEFT); canvas.drawText(targetPart, startX + mainTextWidth, circleY + 85f, targetPaint);

                // --- 4. Authentic 3D Beads ---
                float bRad = 45f, spc = bRad * 2 + 10f;
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(8f); p.setColor(Color.parseColor("#C19A6B"));
                p.setShadowLayer(5, 0, 5, Color.argb(100,0,0,0)); canvas.drawLine(0, beadY, w, beadY, p); p.clearShadowLayer();
                
                float bOffset = beadDragOffset % spc;
                for(int i = -10; i <= 10; i++) {
                    float bx = centerX + (i * spc) + bOffset;
                    if (bx > centerX - 140f && bx < centerX + 140f) continue;
                    
                    p.setStyle(Paint.Style.FILL);
                    android.graphics.RadialGradient woodRg = new android.graphics.RadialGradient(bx - 12f, beadY - 12f, bRad * 1.5f, new int[]{beadThemes[currentBeadTheme][1], beadThemes[currentBeadTheme][0], Color.BLACK}, new float[]{0f, 0.6f, 1f}, android.graphics.Shader.TileMode.CLAMP);
                    p.setShader(woodRg); p.setShadowLayer(20f, 5f, 10f, Color.argb(150, 0, 0, 0)); 
                    canvas.drawCircle(bx, beadY, bRad, p); p.clearShadowLayer(); p.setShader(null);
                    
                    p.setColor(Color.argb(160, 255, 255, 255)); canvas.drawOval(new RectF(bx - 18f, beadY - 35f, bx + 8f, beadY - 12f), p);
                    p.setColor(Color.argb(50, 255, 255, 255)); canvas.drawOval(new RectF(bx - 10f, beadY + 15f, bx + 20f, beadY + 30f), p);
                }
                
                p.setStyle(Paint.Style.FILL); p.setColor(themeColors != null ? themeColors[3] : Color.parseColor("#9E9E9E")); 
                p.setTextSize(26f); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(isBn ? "দানা সোয়াইপ করুন" : "Drag beads to count", centerX, beadY - 75f, p);

                // --- 5. Total/Loop Box ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(40f); float boxW = p.measureText(totalTxt) + 80; if(bnFont != null) p.setTypeface(bnFont);
                android.graphics.LinearGradient badgeLg = new android.graphics.LinearGradient(centerX-boxW/2, totalBoxY-40, centerX+boxW/2, totalBoxY+40, new int[]{0xFFE8DDB5, 0xFFFDFBF7, 0xFFD4C39B}, null, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(badgeLg); p.setShadowLayer(10f, 0, 5f, Color.argb(80, 0, 0, 0));
                canvas.drawRoundRect(new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40), 30f, 30f, p);
                p.clearShadowLayer(); p.setShader(null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(3f); p.setColor(Color.parseColor("#B8860B"));
                canvas.drawRoundRect(new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40), 30f, 30f, p);
                p.setStyle(Paint.Style.FILL); p.setColor(Color.parseColor("#3E2723")); canvas.drawText(totalTxt, centerX, totalBoxY + 12, p);

                // --- 6. 3D Theme Selector ---
                float themeSpacing = w / 7f, themeRadius = 30f;
                for(int i = 0; i < beadThemes.length; i++) {
                    float tx = themeSpacing * (i + 1); p.setStyle(Paint.Style.FILL);
                    android.graphics.RadialGradient trg = new android.graphics.RadialGradient(tx - 10f, themeY - 10f, themeRadius*1.5f, new int[]{beadThemes[i][1], beadThemes[i][0], Color.BLACK}, new float[]{0f, 0.7f, 1f}, android.graphics.Shader.TileMode.CLAMP);
                    p.setShader(trg);
                    if (currentBeadTheme == i) p.setShadowLayer(15f, 0f, 0f, Color.parseColor("#FFD700")); else p.setShadowLayer(8f, 2f, 5f, Color.argb(100,0,0,0));
                    canvas.drawCircle(tx, themeY, themeRadius, p); p.clearShadowLayer(); p.setShader(null);
                    p.setColor(Color.argb(120, 255, 255, 255)); canvas.drawOval(new RectF(tx-12, themeY-20, tx+5, themeY-8), p);
                    if (currentBeadTheme == i) { p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(Color.parseColor("#FFD700")); canvas.drawCircle(tx, themeY, themeRadius + 10f, p); }
                }"""

parts1 = code.split("@Override protected void onDraw(Canvas canvas) {")
if len(parts1) == 2:
    parts2 = parts1[1].split("        };\n\n        circleView.setOnTouchListener")
    if len(parts2) == 2:
        final_code = parts1[0] + new_draw + "\n        };\n\n        circleView.setOnTouchListener" + parts2[1]
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(final_code)
        print("✅ Success: Premium 3D design restored with perfect structured layout!")
    else:
        print("Error: Could not find touch listener split.")
else:
    print("Error: Could not find onDraw start.")
