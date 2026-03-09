import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. থিম কালার আপডেট (আসল পাথর ও কাঠের রঙের জন্য)
new_themes = """final int[][] beadThemes = {
        {Color.parseColor("#111111"), Color.parseColor("#666666")}, // Black Agate
        {Color.parseColor("#E0E0E0"), Color.parseColor("#FFFFFF")}, // Pearl
        {Color.parseColor("#D4AF37"), Color.parseColor("#FFF5C3")}, // Gold
        {Color.parseColor("#B87333"), Color.parseColor("#F5DEB3")}, // Amber / Tiger Eye
        {Color.parseColor("#5C4033"), Color.parseColor("#8B5A2B")}, // Dark Wood
        {Color.parseColor("#2E8B57"), Color.parseColor("#8FBC8F")}  // Jade / Green
    };"""

theme_start = code.find("final int[][] beadThemes = {")
theme_end = code.find("};", theme_start) + 2
if theme_start != -1:
    code = code[:theme_start] + new_themes + code[theme_end:]

# ২. সম্পূর্ণ নতুন আল্ট্রা ৩ডি ড্রয়িং লজিক
new_draw = """@Override protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                float w = getWidth(), h = getHeight(), centerX = w / 2.0f;
                Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
                int idx = currentIdx[0]; if (idx >= tasbihList.size()) idx = 0;
                TasbihData d = tasbihList.get(idx); int curVal = individualCounts[idx];

                float boxTop = h * 0.04f, boxHeight = h * 0.17f;
                float iconY = boxTop + boxHeight + (h * 0.07f);
                float circleY = iconY + (h * 0.17f), radius = w * 0.28f;
                float totalLineY = circleY + radius + (h * 0.09f);
                float beadY = totalLineY + (h * 0.08f);
                float themeY = h - (h * 0.06f);

                // --- Background Texture (Cream/Paper) ---
                p.setStyle(Paint.Style.FILL);
                RadialGradient bgRg = new RadialGradient(centerX, h/2, h, Color.parseColor("#FDFCF0"), Color.parseColor("#E8E0D0"), Shader.TileMode.CLAMP);
                p.setShader(bgRg); canvas.drawRect(0, 0, w, h, p); p.setShader(null);

                // --- 1. Golden Embossed Dua Box ---
                RectF boxRect = new RectF(40, boxTop, w - 40, boxTop + boxHeight);
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(40, boxTop, w-40, boxTop+boxHeight, new int[]{0xFFE6C27A, 0xFFB8860B, 0xFFFFD700, 0xFF8B6508}, new float[]{0f, 0.3f, 0.7f, 1f}, Shader.TileMode.CLAMP);
                p.setShader(lg); p.setShadowLayer(25f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawRoundRect(boxRect, 35f, 35f, p); p.clearShadowLayer(); p.setShader(null);
                
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(Color.parseColor("#FFF8DC"));
                canvas.drawRoundRect(new RectF(48, boxTop+8, w-48, boxTop+boxHeight-8), 28f, 28f, p); p.setStyle(Paint.Style.FILL);

                TextPaint tp = new TextPaint(Paint.ANTI_ALIAS_FLAG);
                if(arabicFont != null) tp.setTypeface(arabicFont); 
                tp.setColor(Color.WHITE); tp.setShadowLayer(8f, 0f, 4f, Color.argb(180, 0,0,0));
                int layoutWidth = (int)(w - 120); float autoFontSize = 95f; StaticLayout sl;
                while (true) {
                    tp.setTextSize(autoFontSize);
                    sl = new StaticLayout(d.arabic, tp, layoutWidth, Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false);
                    if (sl.getHeight() <= (boxHeight - 40f) || autoFontSize <= 35f) break; autoFontSize -= 2f; 
                }
                canvas.save(); canvas.translate(centerX - (layoutWidth / 2f), boxTop + (boxHeight - sl.getHeight()) / 2f);
                sl.draw(canvas); canvas.restore(); tp.clearShadowLayer();

                // --- 2. Side Icons (Jade & Bronze) ---
                float sideMargin = w * 0.16f; float[] iconXs = {sideMargin, w - sideMargin};
                String[] icons = {"↻", (isSoundOn[0] ? "🔊" : "🔇")};
                int[][] iconColors = {{0xFFA8E6CF, 0xFF3B8E63}, {0xFFFFA07A, 0xFF8B4513}}; 
                for(int i=0; i<2; i++) {
                    p.setStyle(Paint.Style.FILL);
                    RadialGradient iRg = new RadialGradient(iconXs[i]-10, iconY-10, 80f, iconColors[i][0], iconColors[i][1], Shader.TileMode.CLAMP);
                    p.setShader(iRg); p.setShadowLayer(15, 0, 10, Color.argb(120,0,0,0));
                    canvas.drawCircle(iconXs[i], iconY, 70f, p); p.clearShadowLayer(); p.setShader(null);
                    p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(6f); p.setColor(Color.parseColor("#B8860B"));
                    canvas.drawCircle(iconXs[i], iconY, 65f, p); p.setStyle(Paint.Style.FILL);
                    p.setColor(Color.WHITE); p.setTextAlign(Paint.Align.CENTER); p.setTextSize(i==0?80f:60f); p.setShadowLayer(5,0,2,Color.BLACK);
                    canvas.drawText(icons[i], iconXs[i], iconY + (i==0?25f:20f), p); p.clearShadowLayer();
                }

                // --- 3. Multi-layer Realistic Ring ---
                float rOuter = radius + 55f;
                android.graphics.SweepGradient silver = new android.graphics.SweepGradient(centerX, circleY, new int[]{0xFFE0E0E0, 0xFF888888, 0xFFFFFFFF, 0xFF555555, 0xFFE0E0E0}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(50f); p.setShader(silver); p.setShadowLayer(30f, 0, 20f, Color.argb(160,0,0,0));
                canvas.drawCircle(centerX, circleY, rOuter, p); p.clearShadowLayer();
                
                float rInner = radius + 10f;
                android.graphics.SweepGradient bronze = new android.graphics.SweepGradient(centerX, circleY, new int[]{0xFFFFD700, 0xFF8B6508, 0xFFFFF8DC, 0xFF8B4513, 0xFFFFD700}, null);
                p.setStrokeWidth(35f); p.setShader(bronze); canvas.drawCircle(centerX, circleY, rInner, p); p.setShader(null);
                
                p.setStyle(Paint.Style.FILL); RadialGradient centerRg = new RadialGradient(centerX, circleY, radius, 0xFFFFFFFF, 0xFFF5F5DC, Shader.TileMode.CLAMP);
                p.setShader(centerRg); canvas.drawCircle(centerX, circleY, radius, p); p.setShader(null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(15f); p.setColor(Color.argb(40,0,0,0)); canvas.drawCircle(centerX, circleY, radius-7f, p);

                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(25f); p.setStrokeCap(Paint.Cap.ROUND);
                p.setColor(Color.parseColor("#FFD700")); p.setShadowLayer(20, 0, 0, Color.parseColor("#FF8C00"));
                canvas.drawArc(new RectF(centerX-rInner, circleY-rInner, centerX+rInner, circleY+rInner), -90, sweep, false, p); p.clearShadowLayer();
                
                // Gems on Silver Ring
                for(int angle=0; angle<360; angle+=90) {
                    float gx = centerX + rOuter * (float)Math.cos(Math.toRadians(angle)), gy = circleY + rOuter * (float)Math.sin(Math.toRadians(angle));
                    p.setStyle(Paint.Style.FILL); RadialGradient gemRg = new RadialGradient(gx-5, gy-5, 25f, 0xFFE0FFFF, 0xFF4682B4, Shader.TileMode.CLAMP);
                    p.setShader(gemRg); p.setShadowLayer(10,0,5,Color.BLACK); canvas.drawCircle(gx, gy, 20f, p); p.clearShadowLayer(); 
                    p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f); p.setShader(silver); canvas.drawCircle(gx, gy, 20f, p); p.setShader(null);
                }

                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); 
                p.setColor(Color.parseColor("#2C3E50")); p.setShadowLayer(4, 2, 2, Color.LTGRAY);
                String mainCountStr = formatNum(curVal); String targetPart = " / " + formatNum(d.target); 
                p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
                Paint targetPaint = new Paint(p); targetPaint.setTextSize(48f); targetPaint.setColor(Color.parseColor("#7F8C8D")); 
                float targetWidth = targetPaint.measureText(targetPart); float startX = centerX - ((mainTextWidth + targetWidth) / 2f);
                p.setTextAlign(Paint.Align.LEFT); canvas.drawText(mainCountStr, startX, circleY + 85f, p);
                targetPaint.setTextAlign(Paint.Align.LEFT); canvas.drawText(targetPart, startX + mainTextWidth, circleY + 100f, targetPaint);
                p.clearShadowLayer(); targetPaint.clearShadowLayer();

                // --- 4. Total/Loop Metallic Badge ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(42f); float boxW = p.measureText(totalTxt) + 100;
                android.graphics.LinearGradient badgeLg = new android.graphics.LinearGradient(centerX-boxW/2, totalLineY-45, centerX+boxW/2, totalLineY+45, new int[]{0xFFE8DDB5, 0xFFFDFBF7, 0xFFD4C39B}, null, Shader.TileMode.CLAMP);
                p.setShader(badgeLg); p.setShadowLayer(15, 0, 8, Color.argb(100,0,0,0));
                canvas.drawRoundRect(new RectF(centerX - boxW/2, totalLineY - 35, centerX + boxW/2, totalLineY + 15), 25f, 25f, p);
                p.clearShadowLayer(); p.setShader(null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(3f); p.setColor(Color.parseColor("#B8860B"));
                canvas.drawRoundRect(new RectF(centerX - boxW/2, totalLineY - 35, centerX + boxW/2, totalLineY + 15), 25f, 25f, p);
                p.setStyle(Paint.Style.FILL); p.setColor(Color.parseColor("#3E2723")); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(totalTxt, centerX, totalLineY - 2, p);

                // --- 5. Ultra Realistic Beads ---
                float bRad = 48f, spc = bRad * 2 + 10f;
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(12f); p.setColor(Color.parseColor("#C19A6B"));
                p.setShadowLayer(10, 0, 5, Color.argb(100,0,0,0)); canvas.drawLine(0, beadY, w, beadY, p); p.clearShadowLayer();
                
                float bOffset = beadDragOffset % spc;
                for(int i = -10; i <= 10; i++) {
                    float bx = centerX + (i * spc) + bOffset;
                    if (bx > centerX - 140f && bx < centerX + 140f) continue; 
                    p.setStyle(Paint.Style.FILL);
                    RadialGradient woodRg = new RadialGradient(bx - 15f, beadY - 15f, bRad * 1.5f, new int[]{beadThemes[currentBeadTheme][1], beadThemes[currentBeadTheme][0], Color.BLACK}, new float[]{0f, 0.6f, 1f}, Shader.TileMode.CLAMP);
                    p.setShader(woodRg); p.setShadowLayer(25f, 5f, 15f, Color.argb(180, 0, 0, 0)); canvas.drawCircle(bx, beadY, bRad, p); p.clearShadowLayer(); p.setShader(null);
                    
                    android.graphics.LinearGradient goldRing = new android.graphics.LinearGradient(bx-bRad, beadY, bx+bRad, beadY, new int[]{0xFF8B6508, 0xFFFFD700, 0xFF8B6508}, null, Shader.TileMode.CLAMP);
                    p.setShader(goldRing); canvas.drawRect(bx-bRad+4f, beadY-8f, bx+bRad-4f, beadY+8f, p); p.setShader(null);
                    
                    p.setColor(Color.argb(160, 255, 255, 255)); canvas.drawOval(new RectF(bx - 20f, beadY - 38f, bx + 10f, beadY - 15f), p);
                    p.setColor(Color.argb(50, 255, 255, 255)); canvas.drawOval(new RectF(bx - 10f, beadY + 20f, bx + 25f, beadY + 35f), p);
                }

                // --- 6. Bead Theme Selector ---
                float themeSpacing = w / 7f, themeRadius = 35f;
                for(int i = 0; i < beadThemes.length; i++) {
                    float tx = themeSpacing * (i + 1); p.setStyle(Paint.Style.FILL);
                    RadialGradient trg = new RadialGradient(tx - 10f, themeY - 10f, themeRadius*1.5f, new int[]{beadThemes[i][1], beadThemes[i][0], Color.BLACK}, new float[]{0f, 0.7f, 1f}, Shader.TileMode.CLAMP);
                    p.setShader(trg);
                    if (currentBeadTheme == i) p.setShadowLayer(25f, 0f, 0f, Color.parseColor("#FFD700")); else p.setShadowLayer(10f, 2f, 8f, Color.argb(150,0,0,0));
                    canvas.drawCircle(tx, themeY, themeRadius, p); p.clearShadowLayer(); p.setShader(null);
                    p.setColor(Color.argb(120, 255, 255, 255)); canvas.drawOval(new RectF(tx-15, themeY-25, tx+5, themeY-8), p);
                    if (currentBeadTheme == i) { p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(Color.parseColor("#FFD700")); canvas.drawCircle(tx, themeY, themeRadius + 12f, p); }
                }
                
                // গাইড টেক্সট
                p.setStyle(Paint.Style.FILL); p.setTextSize(26f); p.setColor(Color.parseColor("#8D6E63")); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(isBn ? "দানা সোয়াইপ করুন" : "Drag beads to count", centerX, beadY - 80f, p);
            }
"""

draw_start = code.find("@Override protected void onDraw(Canvas canvas) {")
draw_end = code.find("circleView.setOnTouchListener", draw_start)
if draw_start != -1 and draw_end != -1:
    code = code[:draw_start] + new_draw + "\n        " + code[draw_end:]

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Ultra Realistic 3D Java Canvas applied!")
