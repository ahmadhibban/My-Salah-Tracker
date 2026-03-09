f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f).read()

start_idx = c.find("class ZikrCanvasView")
end_idx = c.find("private void loadZikrTab()")

if start_idx != -1 and end_idx != -1:
    new_canvas = """class ZikrCanvasView extends android.view.View {
        private float startX, startY; private android.graphics.Typeface bnFont; private android.graphics.Bitmap resetBmp, soundBmp;
        public ZikrCanvasView(android.content.Context context) {
            super(context); bnFont = appFonts[1]; if(zikrMan == null) { zikrMan = new ZikrManager(); zikrMan.init(context); }
            try {
                int rId = getResources().getIdentifier("img_zikr_reset", "drawable", context.getPackageName());
                if(rId != 0) resetBmp = android.graphics.BitmapFactory.decodeResource(getResources(), rId);
                int sId = getResources().getIdentifier("img_zikr_sound", "drawable", context.getPackageName());
                if(sId != 0) soundBmp = android.graphics.BitmapFactory.decodeResource(getResources(), sId);
            } catch(Exception e){}
        }
        private String toBengali(int num) { String out = String.valueOf(num); String[] eng = {"0","1","2","3","4","5","6","7","8","9"}, bng = {"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; for(int i=0; i<10; i++) out = out.replace(eng[i], bng[i]); return out; }

        @Override protected void onDraw(android.graphics.Canvas canvas) {
            super.onDraw(canvas); boolean isBn = sp.getString("app_lang","en").equals("bn"); float w = getWidth(), centerX = w / 2.0f;
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx = zikrMan.currentIdx; if (idx >= zikrMan.tasbihList.size()) idx = 0;
            ZikrManager.TasbihData d = zikrMan.tasbihList.get(idx); int curVal = zikrMan.indCounts[idx];

            // 1. Top Icons (Corners)
            float topY = 130f, leftX = 120f, rightX = w - 120f;
            if(resetBmp != null) { canvas.drawBitmap(resetBmp, new android.graphics.Rect(0,0,resetBmp.getWidth(), resetBmp.getHeight()), new android.graphics.RectF(leftX-45f, topY-45f, leftX+45f, topY+45f), p); }
            else { p.setColor(themeColors[1]); canvas.drawCircle(leftX, topY, 60f, p); p.setColor(themeColors[3]); p.setTextSize(60f); p.setTextAlign(android.graphics.Paint.Align.CENTER); canvas.drawText("↺", leftX, topY+20f, p); }
            
            p.setAlpha(zikrMan.soundOn ? 255 : 100);
            if(soundBmp != null) { canvas.drawBitmap(soundBmp, new android.graphics.Rect(0,0,soundBmp.getWidth(), soundBmp.getHeight()), new android.graphics.RectF(rightX-45f, topY-45f, rightX+45f, topY+45f), p); }
            else { p.setColor(themeColors[1]); canvas.drawCircle(rightX, topY, 60f, p); p.setColor(themeColors[3]); p.setTextSize(60f); p.setTextAlign(android.graphics.Paint.Align.CENTER); canvas.drawText("🔊", rightX, topY+20f, p); } p.setAlpha(255);

            // 2. Arabic Dua Box (Clickable for Settings)
            float boxTop = 240f, fixedBoxHeight = 350f, boxBottom = boxTop + fixedBoxHeight;
            p.setColor(themeColors[1]); p.setShadowLayer(20, 0, 10, android.graphics.Color.parseColor("#1A000000")); canvas.drawRoundRect(new android.graphics.RectF(140f, boxTop, w - 140f, boxBottom), 40f, 40f, p); p.clearShadowLayer();
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(3f); p.setColor(themeColors[4]); canvas.drawRoundRect(new android.graphics.RectF(140f, boxTop, w - 140f, boxBottom), 40f, 40f, p);
            
            p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(themeColors[3]); p.setTextSize(70f); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            canvas.drawText("❮", 70f, boxTop + 190f, p); canvas.drawText("❯", w - 70f, boxTop + 190f, p);

            android.text.TextPaint tp = new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layoutWidth = (int)(w - 320); float autoFontSize = 95f; android.text.StaticLayout sl;
            while (true) { tp.setTextSize(autoFontSize); sl = new android.text.StaticLayout(d.arabic, tp, layoutWidth, android.text.Layout.Alignment.ALIGN_CENTER, 1.2f, 0.0f, false); if (sl.getHeight() <= (fixedBoxHeight - 50f) || autoFontSize <= 35f) break; autoFontSize -= 2f; }
            canvas.save(); canvas.translate(centerX - (layoutWidth / 2f), boxTop + (fixedBoxHeight - sl.getHeight()) / 2f); sl.draw(canvas); canvas.restore();

            p.setColor(themeColors[3]); p.setTextSize(32f); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            canvas.drawText(lang.get("Tap box to change Dua or Target"), centerX, boxBottom + 65f, p);

            // 3. Main Circle & Glowing Ball
            float circleY = boxBottom + 500f, radius = w * 0.38f; float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(45f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND); p.setColor(themeColors[1]); canvas.drawCircle(centerX, circleY, radius, p);
            p.setColor(colorAccent); canvas.drawArc(new android.graphics.RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
            
            double angle = Math.toRadians(sweep - 90); float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(45, 0, 0, colorAccent); p.setColor(colorAccent); canvas.drawCircle(ballX, ballY, 35f, p); p.clearShadowLayer();
            p.setColor(android.graphics.Color.WHITE); canvas.drawCircle(ballX, ballY, 15f, p);

            // 4. Perfect Centered Number
            p.setStyle(android.graphics.Paint.Style.FILL); p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            String mainCountStr = isBn ? toBengali(curVal) : String.valueOf(curVal); float tSize = 280f; p.setTextSize(tSize);
            while(p.measureText(mainCountStr) > radius * 1.6f) { tSize -= 5f; p.setTextSize(tSize); }
            canvas.drawText(mainCountStr, centerX, circleY + (tSize/3f) - 20f, p);
            
            if(d.target > 0) { p.setTextSize(45f); p.setColor(themeColors[3]); p.setTypeface(appFonts[0]); canvas.drawText((isBn ? "টার্গেট: " + toBengali(d.target) : "Target: " + d.target), centerX, circleY + (tSize/3f) + 50f, p); }

            // 5. Bottom Premium Buttons
            float btnRadius = 85f, sY = circleY + radius + 150f, mX = centerX - radius + 20f, sX = centerX + radius - 20f;
            p.setColor(themeColors[1]); p.setShadowLayer(15, 0, 8, android.graphics.Color.parseColor("#22000000")); canvas.drawCircle(mX, sY, btnRadius, p); p.clearShadowLayer(); p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(themeColors[4]); canvas.drawCircle(mX, sY, btnRadius, p); p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(android.graphics.Color.parseColor("#EF4444")); p.setTextSize(110f); p.setTextAlign(android.graphics.Paint.Align.CENTER); canvas.drawText("-", mX, sY + 35f, p);
            p.setColor(themeColors[1]); p.setShadowLayer(15, 0, 8, android.graphics.Color.parseColor("#22000000")); canvas.drawCircle(sX, sY, btnRadius, p); p.clearShadowLayer(); p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(themeColors[4]); canvas.drawCircle(sX, sY, btnRadius, p); p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(colorAccent); p.setTextSize(65f); p.setTypeface(appFonts[1]); canvas.drawText(isBn ? toBengali(zikrMan.indRounds[idx]) : String.valueOf(zikrMan.indRounds[idx]), sX, sY + 25f, p); p.setTextSize(32f); p.setColor(themeColors[3]); p.setTypeface(appFonts[0]); canvas.drawText(lang.get("Rounds"), sX, sY + 140f, p);

            String totalTxt = lang.get("Total") + ": " + (isBn ? toBengali(zikrMan.indTotals[idx]) : zikrMan.indTotals[idx]); p.setTextSize(45f); p.setTypeface(appFonts[1]); float boxW = p.measureText(totalTxt) + 90f; p.setColor(themeColors[1]); p.setShadowLayer(12, 0, 6, android.graphics.Color.parseColor("#15000000")); canvas.drawRoundRect(new android.graphics.RectF(centerX - boxW/2, sY + 220f, centerX + boxW/2, sY + 315f), 30f, 30f, p); p.clearShadowLayer(); p.setColor(themeColors[2]); canvas.drawText(totalTxt, centerX, sY + 285f, p);
        }

        @Override public boolean onTouchEvent(android.view.MotionEvent event) {
            float x = event.getX(), y = event.getY(), w = getWidth(), centerX = w / 2.0f;
            float boxTop = 240f, boxBottom = boxTop + 350f, circleY = boxBottom + 500f, radius = w * 0.38f; 
            float sY = circleY + radius + 150f, mX = centerX - radius + 20f; int idx = zikrMan.currentIdx;

            if (event.getAction() == android.view.MotionEvent.ACTION_DOWN) { startX = x; startY = y; return true; } 
            if (event.getAction() == android.view.MotionEvent.ACTION_UP) {
                float deltaX = x - startX;
                if (y < 230f) {
                    if (x < 230f) { performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Reset")).setMessage(lang.get("Do you want to reset counts for this Dua?")).setPositiveButton("Yes", (dialog, which) -> { zikrMan.indCounts[idx] = 0; zikrMan.indTotals[idx] = 0; zikrMan.indRounds[idx] = 0; zikrMan.save(); invalidate(); }).setNegativeButton("No", null).show(); return true; }
                    if (x > w - 230f) { performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); zikrMan.soundOn = !zikrMan.soundOn; zikrMan.save(); invalidate(); return true; }
                }
                if (x < 140f && y > boxTop && y < boxBottom) { zikrMan.currentIdx = (zikrMan.currentIdx - 1 + zikrMan.tasbihList.size()) % zikrMan.tasbihList.size(); zikrMan.save(); invalidate(); return true; }
                if (x > w - 140f && y > boxTop && y < boxBottom) { zikrMan.currentIdx = (zikrMan.currentIdx + 1) % zikrMan.tasbihList.size(); zikrMan.save(); invalidate(); return true; }
                if (x > 140f && x < w - 140f && y > boxTop && y < boxBottom && Math.abs(deltaX) < 20f) {
                    performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); final android.app.Dialog d = new android.app.Dialog(getContext(), android.R.style.Theme_Black_NoTitleBar_Fullscreen); android.widget.LinearLayout root = new android.widget.LinearLayout(getContext()); root.setOrientation(android.widget.LinearLayout.VERTICAL); root.setBackgroundColor(themeColors[0]); root.setPadding(40, 80, 40, 40); android.widget.TextView t1 = new android.widget.TextView(getContext()); t1.setText(lang.get("Daily Zikr")); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(android.view.Gravity.CENTER); root.addView(t1); android.widget.TextView t2 = new android.widget.TextView(getContext()); t2.setText(lang.get("Tap box to change Dua or Target")); t2.setTextColor(themeColors[3]); t2.setTextSize(14); t2.setGravity(android.view.Gravity.CENTER); t2.setPadding(0, 5, 0, 30); root.addView(t2); android.widget.ScrollView sv = new android.widget.ScrollView(getContext()); android.widget.LinearLayout listBody = new android.widget.LinearLayout(getContext()); listBody.setOrientation(android.widget.LinearLayout.VERTICAL);
                    for (int i = 0; i < zikrMan.tasbihList.size(); i++) {
                        final int rowIdx = i; android.widget.LinearLayout row = new android.widget.LinearLayout(getContext()); row.setPadding(10, 30, 10, 30); row.setWeightSum(10f); row.setGravity(android.view.Gravity.CENTER_VERTICAL); android.widget.TextView tvDua = new android.widget.TextView(getContext()); tvDua.setText(zikrMan.tasbihList.get(rowIdx).arabic); tvDua.setTextColor(themeColors[2]); tvDua.setTextSize(26); tvDua.setGravity(android.view.Gravity.CENTER); tvDua.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 7.5f)); tvDua.setTypeface(getArabicFont()); tvDua.setOnClickListener(v2 -> { zikrMan.currentIdx = rowIdx; zikrMan.save(); invalidate(); d.dismiss(); }); final android.widget.TextView tvTarg = new android.widget.TextView(getContext()); tvTarg.setText(String.valueOf(zikrMan.tasbihList.get(rowIdx).target)); tvTarg.setTextColor(colorAccent); tvTarg.setTextSize(20); tvTarg.setGravity(android.view.Gravity.CENTER); tvTarg.setTypeface(appFonts[1]); tvTarg.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 2.5f));
                        tvTarg.setOnClickListener(v3 -> { final android.widget.EditText et = new android.widget.EditText(getContext()); et.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); et.setText(String.valueOf(zikrMan.tasbihList.get(rowIdx).target)); new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK", (di, wi) -> { if(!et.getText().toString().isEmpty()){ zikrMan.tasbihList.get(rowIdx).target = Integer.parseInt(et.getText().toString()); tvTarg.setText(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+rowIdx, zikrMan.tasbihList.get(rowIdx).target).apply(); invalidate(); } }).show(); }); row.addView(tvDua); row.addView(tvTarg); listBody.addView(row);
                    } sv.addView(listBody); root.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, 0, 1f)); android.widget.Button btnAdd = new android.widget.Button(getContext()); btnAdd.setText("+ Add New"); btnAdd.setAllCaps(false); btnAdd.setBackgroundColor(themeColors[1]); btnAdd.setTextColor(themeColors[2]); android.widget.LinearLayout.LayoutParams btnLp = new android.widget.LinearLayout.LayoutParams(-1, -2); btnLp.setMargins(0, 20, 0, 0); btnAdd.setLayoutParams(btnLp);
                    btnAdd.setOnClickListener(v4 -> { android.widget.LinearLayout lay = new android.widget.LinearLayout(getContext()); lay.setOrientation(android.widget.LinearLayout.VERTICAL); lay.setPadding(50, 20, 50, 20); final android.widget.EditText etDua = new android.widget.EditText(getContext()); etDua.setHint("Arabic Dua"); final android.widget.EditText etTarget = new android.widget.EditText(getContext()); etTarget.setHint("Target"); etTarget.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); lay.addView(etDua); lay.addView(etTarget); new android.app.AlertDialog.Builder(getContext()).setTitle("Add").setView(lay).setPositiveButton("OK", (di, wi) -> { String dText = etDua.getText().toString(); String tText = etTarget.getText().toString(); if(!dText.isEmpty() && !tText.isEmpty()){ zikrMan.tasbihList.add(new ZikrManager.TasbihData(dText, Integer.parseInt(tText))); zikrMan.save(); invalidate(); d.dismiss(); } }).show(); }); root.addView(btnAdd); d.setContentView(root); d.show(); return true;
                }
                if (Math.abs(deltaX) > 150) { if (deltaX < 0) zikrMan.currentIdx = (zikrMan.currentIdx + 1) % zikrMan.tasbihList.size(); else zikrMan.currentIdx = (zikrMan.currentIdx - 1 + zikrMan.tasbihList.size()) % zikrMan.tasbihList.size(); zikrMan.save(); invalidate(); return true; }
                if (Math.abs(x - mX) < 100 && Math.abs(y - sY) < 100) { performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); if (zikrMan.indCounts[idx] > 0) { zikrMan.indCounts[idx]--; if (zikrMan.indTotals[idx] > 0) zikrMan.indTotals[idx]--; zikrMan.save(); invalidate(); } return true; }
                double distToCenter = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - circleY, 2));
                if (distToCenter <= radius + 50) { performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); zikrMan.indCounts[idx]++; zikrMan.indTotals[idx]++; if (zikrMan.soundOn && zikrMan.toneGen != null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50); if (zikrMan.tasbihList.get(idx).target > 0 && zikrMan.indCounts[idx] >= zikrMan.tasbihList.get(idx).target) { zikrMan.indCounts[idx] = 0; zikrMan.indRounds[idx]++; performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); } zikrMan.save(); invalidate(); return true; }
            } invalidate(); return true;
        }
    }
    """
    c = c[:start_idx] + new_canvas + c[end_idx:]
    open(f, 'w').write(c)
    print("✅ Part 2 Done: MASTERPIECE UI RESTORED PERFECTLY!")
