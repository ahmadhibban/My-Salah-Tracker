import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. ফন্ট নাম ঠিক করা (ছোট হাতের)
code = re.sub(r'Typeface\.createFromAsset\(ctx\.getAssets\(\), "fonts/.*?"\)', 
              'Typeface.createFromAsset(ctx.getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf")', code)

# ২. সম্পূর্ণ ডিজাইনের ড্রয়িং কোড রিপ্লেস
new_drawing = """
            @Override protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                float w = getWidth(), h = getHeight(), centerX = w / 2.0f;
                Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
                int idx = currentIdx[0]; if (idx >= tasbihList.size()) idx = 0;
                TasbihData d = tasbihList.get(idx); int curVal = individualCounts[idx];

                float boxTop = h * 0.04f, boxHeight = h * 0.17f;
                float iconY = boxTop + boxHeight + (h * 0.08f);
                float circleY = iconY + (h * 0.16f), radius = w * 0.31f;
                float beadY = circleY + radius + (h * 0.12f);
                float totalLineY = beadY - (h * 0.04f); // সুতোর ঠিক উপরে
                float themeY = h - (h * 0.06f);

                // --- Background Paper Texture ---
                p.setStyle(Paint.Style.FILL);
                RadialGradient bgRg = new RadialGradient(centerX, h/2, h, Color.parseColor("#FDFCF0"), Color.parseColor("#E8E0D0"), Shader.TileMode.CLAMP);
                p.setShader(bgRg); canvas.drawRect(0, 0, w, h, p); p.setShader(null);

                // --- 1. Dua Box (Golden Embossed - ছবির মতো) ---
                RectF boxRect = new RectF(40, boxTop, w - 40, boxTop + boxHeight);
                
                // ছবির মতো গোল্ডেন গ্র্যাডিয়েন্ট
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(40, boxTop, w-40, boxTop+boxHeight, new int[]{0xFFE6C27A, 0xFFB8860B, 0xFFFFD700, 0xFF8B6508}, new float[]{0f, 0.3f, 0.7f, 1f}, Shader.TileMode.CLAMP);
                p.setShader(lg); p.setShadowLayer(25f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawRoundRect(boxRect, 35f, 35f, p); p.clearShadowLayer(); p.setShader(null);
                
                // দোয়ার টেক্সটের ওপরে একটি গোল্ডেন লাইন (ছবির মতো)
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

                // --- 2. Side Icons (Edges - Jade & Bronze) ---
                float sideMargin = w * 0.16f; float[] iconXs = {sideMargin, w - sideMargin};
                String[] icons = {"↻", (isSoundOn[0] ? "🔊" : "🔇")};
                
                // ছবির মতো Jade এবং Bronze কালার
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

                // --- 3. Multi-layer Metallic Ring ( ছবির মতো রৌপ্য ও সোনা) ---
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
                
                // Gems
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

                // --- 4. Total/Round (Above the Beads) ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(38f); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(totalTxt, centerX, totalLineY, p);

                // --- 5. Ultra Realistic Beads ---
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(12f); p.setColor(Color.parseColor("#C19A6B"));
                canvas.drawLine(0, beadY, w, beadY, p);
                float bRad = 45f, spc = bRad * 2 + 15f;
                float bOffset = beadDragOffset % spc;
                for(int i = -8; i <= 8; i++) {
                    float bx = centerX + (i * spc) + bOffset;
                    if (bx > centerX - 120f && bx < centerX + 120f) continue; 
                    p.setStyle(Paint.Style.FILL);
                    RadialGradient woodRg = new RadialGradient(bx - 12f, beadY - 12f, bRad * 1.5f, new int[]{beadThemes[currentBeadTheme][1], beadThemes[currentBeadTheme][0], Color.BLACK}, new float[]{0f, 0.7f, 1f}, Shader.TileMode.CLAMP);
                    p.setShader(woodRg); p.setShadowLayer(25f, 5f, 15f, Color.argb(180, 0, 0, 0)); canvas.drawCircle(bx, beadY, bRad, p); p.clearShadowLayer(); p.setShader(null);
                    
                    p.setColor(Color.argb(160, 255, 255, 255)); canvas.drawOval(new RectF(bx - 20f, beadY - 35f, bx + 5f, beadY - 10f), p);
                }
"""

code = re.sub(r'@Override protected void onDraw\(Canvas canvas\) \{.*?p\.setTextAlign\(Paint\.Align\.CENTER\);.*?canvas\.drawText\(.*?centerX, beadY - 80f, p\);', 
              new_drawing, code, flags=re.DOTALL)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Part 1: Final Ultra 3D Design applied!")
