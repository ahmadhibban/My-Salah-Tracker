import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# আরবী ফন্টের নাম ফিক্স
code = re.sub(r'Typeface\.createFromAsset\(ctx\.getAssets\(\), "fonts/.*?"\)', 
              'Typeface.createFromAsset(ctx.getAssets(), "fonts/Al_majeed_quranic_font_shiped.ttf")', code)

# ৩ডি ড্রয়িং এবং পজিশন ক্যালকুলেশন আপডেট
new_draw_logic = """
            @Override protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                float w = getWidth(), h = getHeight(), centerX = w / 2.0f;
                Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
                int idx = currentIdx[0]; if (idx >= tasbihList.size()) idx = 0;
                TasbihData d = tasbihList.get(idx); int curVal = individualCounts[idx];

                float boxTop = h * 0.03f, boxHeight = h * 0.18f;
                float iconY = boxTop + boxHeight + (h * 0.08f);
                float circleY = iconY + (h * 0.15f), radius = w * 0.33f;
                float totalLineY = circleY + radius + (h * 0.05f); // সুতোর উপরে টোটাল
                float beadY = totalLineY + (h * 0.08f); // দানা একটু নিচে
                float themeY = h - (h * 0.06f);

                // --- 1. Dua Box (Salah Style) ---
                int hour = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY);
                boolean isDayTime = (hour >= 6 && hour < 18);
                int[] pColors = isDayTime ? new int[]{Color.parseColor("#FF9500"), Color.parseColor("#FFCC00")}
                                          : new int[]{Color.parseColor("#1A2980"), Color.parseColor("#26D0CE")};
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(40, boxTop, w - 40, boxTop + boxHeight, pColors[0], pColors[1], Shader.TileMode.CLAMP);
                p.setShader(lg); canvas.drawRoundRect(new RectF(40, boxTop, w - 40, boxTop + boxHeight), 40f, 40f, p);
                p.setShader(null);

                TextPaint tp = new TextPaint(Paint.ANTI_ALIAS_FLAG);
                if(arabicFont != null) tp.setTypeface(arabicFont); tp.setColor(Color.WHITE);
                int layoutWidth = (int)(w - 120); float autoFontSize = 95f; StaticLayout sl;
                while (true) {
                    tp.setTextSize(autoFontSize);
                    sl = new StaticLayout(d.arabic, tp, layoutWidth, Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false);
                    if (sl.getHeight() <= (boxHeight - 40f) || autoFontSize <= 35f) break;
                    autoFontSize -= 2f; 
                }
                canvas.save(); canvas.translate(centerX - (layoutWidth / 2f), boxTop + (boxHeight - sl.getHeight()) / 2f);
                sl.draw(canvas); canvas.restore();

                // --- 2. Side Icons (Reset & Sound) ---
                float sideMargin = 100f;
                String[] icons = {"↻", (isSoundOn[0] ? "🔊" : "🔇")};
                float[] iconXs = {sideMargin, w - sideMargin};
                for(int i=0; i<2; i++) {
                    p.setStyle(Paint.Style.FILL); p.setColor(themeColors != null ? themeColors[1] : Color.WHITE);
                    p.setShadowLayer(15, 0, 8, Color.LTGRAY);
                    canvas.drawCircle(iconXs[i], iconY, 70f, p); p.clearShadowLayer();
                    p.setColor(i==0 ? Color.parseColor("#2E7D32") : Color.parseColor("#E65100"));
                    p.setTextAlign(Paint.Align.CENTER); p.setTextSize(i==0?90f:65f);
                    canvas.drawText(icons[i], iconXs[i], iconY + (i==0?30f:22f), p);
                }

                // --- 3. Counter Circle ---
                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(50f); p.setStrokeCap(Paint.Cap.ROUND);
                p.setColor(themeColors != null ? themeColors[4] : Color.LTGRAY); canvas.drawCircle(centerX, circleY, radius, p);
                p.setColor(colorAccent); canvas.drawArc(new RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
                
                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); p.setColor(themeColors != null ? themeColors[2] : Color.BLACK); 
                String cStr = formatNum(curVal); p.setTextSize(260f); canvas.drawText(cStr, centerX - (p.measureText(cStr)/2f), circleY + 85f, p);

                // --- 4. Total/Round (Above the Beads) ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(38f); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(totalTxt, centerX, totalLineY, p);

                // --- 5. Ultra 3D Beads ---
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(Color.LTGRAY);
                canvas.drawLine(0, beadY, w, beadY, p);
                float bRad = 45f, spc = bRad * 2 + 15f;
                float bOffset = beadDragOffset % spc;
                for(int i = -8; i <= 8; i++) {
                    float bx = centerX + (i * spc) + bOffset;
                    if (bx > centerX - 120f && bx < centerX + 120f) continue;
                    p.setStyle(Paint.Style.FILL);
                    RadialGradient rg = new RadialGradient(bx - 12f, beadY - 12f, bRad * 1.3f, new int[]{beadThemes[currentBeadTheme][1], beadThemes[currentBeadTheme][0], Color.BLACK}, new float[]{0f, 0.7f, 1f}, Shader.TileMode.CLAMP);
                    p.setShader(rg); canvas.drawCircle(bx, beadY, bRad, p); p.setShader(null);
                    p.setColor(Color.argb(180, 255, 255, 255)); canvas.drawOval(new RectF(bx-20, beadY-30, bx+5, beadY-10), p); // Gloss
                }
"""
code = re.sub(r'@Override protected void onDraw\(Canvas canvas\) \{.*?// --- 6\. Bead Theme Selector ---', new_draw_logic, code, flags=re.DOTALL)
with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Part 1: Icons, Font and Pushing logic updated!")
