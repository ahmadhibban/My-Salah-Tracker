import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ZikrCanvasView ক্লাসটি পুরোপুরি আপনার চাহিদা অনুযায়ী ফিক্স করা
start_idx = c.find("class ZikrCanvasView")
end_idx = c.find("private void loadZikrTab()")

if start_idx != -1 and end_idx != -1:
    new_canvas = """class ZikrCanvasView extends android.view.View {
        private float startX, startY; 
        private android.graphics.Bitmap resetBmp, soundOnBmp, soundOffBmp;

        public ZikrCanvasView(android.content.Context context) {
            super(context); 
            if(zikrMan == null) { zikrMan = new ZikrManager(); zikrMan.init(context); }
            try {
                resetBmp = loadBmp("img_zikr_reset");
                soundOnBmp = loadBmp("img_zikr_sound_on");
                soundOffBmp = loadBmp("img_zikr_sound_off");
            } catch(Exception e){}
        }

        private android.graphics.Bitmap loadBmp(String name) {
            int id = getResources().getIdentifier(name, "drawable", getContext().getPackageName());
            return id != 0 ? android.graphics.BitmapFactory.decodeResource(getResources(), id) : null;
        }
        
        private String toBengali(int num) { 
            String out = String.valueOf(num); 
            String[] eng = {"0","1","2","3","4","5","6","7","8","9"}, bng = {"০","১","২","৩","৪","৫","৬","৭","৮","৯"}; 
            for(int i=0; i<10; i++) out = out.replace(eng[i], bng[i]); return out; 
        }

        @Override protected void onDraw(android.graphics.Canvas canvas) {
            super.onDraw(canvas); boolean isBn = sp.getString("app_lang","en").equals("bn"); 
            float w = getWidth(), centerX = w / 2.0f;
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx = zikrMan.currentIdx; ZikrManager.TasbihData d = zikrMan.tasbihList.get(idx); 
            int curVal = zikrMan.indCounts[idx];

            // --- 1. Top Icons (At the very corners) ---
            float iconY = 100f; float marginSide = 80f;
            if(resetBmp != null) canvas.drawBitmap(resetBmp, null, new android.graphics.RectF(marginSide-45f, iconY-45f, marginSide+45f, iconY+45f), p);
            else { p.setColor(themeColors[1]); canvas.drawCircle(marginSide, iconY, 60f, p); p.setColor(themeColors[3]); p.setTextSize(50f); p.setTextAlign(android.graphics.Paint.Align.CENTER); canvas.drawText("↺", marginSide, iconY+18f, p); }
            
            android.graphics.Bitmap sBmp = zikrMan.soundOn ? soundOnBmp : soundOffBmp;
            if(sBmp != null) canvas.drawBitmap(sBmp, null, new android.graphics.RectF(w-marginSide-45f, iconY-45f, w-marginSide+45f, iconY+45f), p);
            else { p.setColor(themeColors[1]); canvas.drawCircle(w-marginSide, iconY, 60f, p); p.setColor(zikrMan.soundOn ? colorAccent : themeColors[3]); p.setTextSize(50f); canvas.drawText(zikrMan.soundOn?"🔊":"🔇", w-marginSide, iconY+18f, p); }

            // --- 2. Arabic Box (Single Line Scaling) ---
            float boxTop = 230f, boxHeight = 400f;
            p.setColor(themeColors[1]); p.setShadowLayer(20, 0, 10, android.graphics.Color.parseColor("#12000000"));
            canvas.drawRoundRect(new android.graphics.RectF(50f, boxTop, w-50f, boxTop+boxHeight), 45f, 45f, p); p.clearShadowLayer();
            
            android.text.TextPaint tp = new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layoutW = (int)(w - 180); float fontSize = 100f; android.text.StaticLayout sl;
            while (true) { 
                tp.setTextSize(fontSize); sl = new android.text.StaticLayout(d.arabic, tp, layoutW, android.text.Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false); 
                if (sl.getLineCount() == 1 || fontSize <= 35f) break; fontSize -= 2f; 
            }
            canvas.save(); canvas.translate(centerX - (layoutW/2f), boxTop + (boxHeight - sl.getHeight())/2f); sl.draw(canvas); canvas.restore();

            p.setColor(themeColors[3]); p.setTextSize(32f); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            canvas.drawText(lang.get("Tap box to change Dua or Target"), centerX, boxTop + boxHeight + 70f, p);

            // --- 3. Main Progress Circle (Centered Spacing) ---
            float circleY = boxTop + boxHeight + 500f; float radius = w * 0.38f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(50f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            p.setColor(themeColors[4]); canvas.drawCircle(centerX, circleY, radius, p);
            p.setColor(colorAccent); float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
            canvas.drawArc(new android.graphics.RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);

            // Glowing Ball
            double rad = Math.toRadians(sweep - 90); float ballX = (float)(centerX + radius * Math.cos(rad)), ballY = (float)(circleY + radius * Math.sin(rad));
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(40, 0, 0, colorAccent); p.setColor(colorAccent); canvas.drawCircle(ballX, ballY, 35f, p); p.clearShadowLayer();
            p.setColor(android.graphics.Color.WHITE); canvas.drawCircle(ballX, ballY, 14f, p);

            // --- 4. Count & Target (Centered Together) ---
            p.setTypeface(appFonts[0]); p.setColor(themeColors[2]); 
            String mStr = isBn ? toBengali(curVal) : String.valueOf(curVal);
            String tStr = (d.target > 0) ? (" / " + (isBn ? toBengali(d.target) : String.valueOf(d.target))) : "";
            float mSize = 260f; p.setTextSize(mSize); float mW = p.measureText(mStr);
            android.graphics.Paint tp2 = new android.graphics.Paint(p); tp2.setTextSize(60f); tp2.setColor(themeColors[3]); float tW = tp2.measureText(tStr);
            
            while(mW + tW > radius * 1.6f) { mSize -= 5f; p.setTextSize(mSize); tp2.setTextSize(mSize*0.25f); mW = p.measureText(mStr); tW = tp2.measureText(tStr); }
            float startXT = centerX - (mW + tW)/2f; float txtY = circleY + (mSize/3.5f);
            p.setTextAlign(android.graphics.Paint.Align.LEFT); canvas.drawText(mStr, startXT, txtY, p);
            canvas.drawText(tStr, startXT + mW, txtY, tp2);

            // --- 5. Bottom Buttons (Symmetrical) ---
            float buttonsY = circleY + radius + 150f; float mXPos = centerX - radius + 30f, sXPos = centerX + radius - 30f;
            drawCustomBtn(canvas, mXPos, buttonsY, "-", android.graphics.Color.parseColor("#EF4444"), 100f);
            drawCustomBtn(canvas, sXPos, buttonsY, isBn?toBengali(zikrMan.indRounds[idx]):String.valueOf(zikrMan.indRounds[idx]), colorAccent, 65f);
            p.setColor(themeColors[3]); p.setTextSize(32f); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            canvas.drawText(lang.get("Rounds"), sXPos, buttonsY + 130f, p);

            // --- 6. Total Card (Bottom) ---
            String totT = lang.get("Total") + ": " + (isBn ? toBengali(zikrMan.indTotals[idx]) : zikrMan.indTotals[idx]);
            p.setTextSize(44f); p.setTypeface(appFonts[0]); float tWBox = p.measureText(totT) + 100f;
            p.setColor(themeColors[1]); p.setShadowLayer(15, 0, 8, android.graphics.Color.parseColor("#12000000"));
            canvas.drawRoundRect(new android.graphics.RectF(centerX-tWBox/2, buttonsY+220f, centerX+tWBox/2, buttonsY+320f), 35f, 35f, p); p.clearShadowLayer();
            p.setColor(themeColors[2]); canvas.drawText(totT, centerX, buttonsY+285f, p);
        }

        private void drawCustomBtn(android.graphics.Canvas cv, float x, float y, String txt, int clr, float sz) {
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            p.setColor(themeColors[1]); cv.drawCircle(x, y, 85f, p);
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(themeColors[4]); cv.drawCircle(x, y, 85f, p);
            p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(clr); p.setTextSize(sz); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(txt, x, y + sz/3.5f, p);
        }

        @Override public boolean onTouchEvent(android.view.MotionEvent event) {
            float x = event.getX(), y = event.getY(), w = getWidth(), cX = w / 2f;
            float bT = 230f, bB = bT + 400f, cY = bB + 500f, rad = w * 0.38f; 
            float btY = cY + rad + 150f, mXP = cX - rad + 30f, mS = 80f; int idx = zikrMan.currentIdx;
            if (event.getAction() == android.view.MotionEvent.ACTION_DOWN) { startX = x; startY = y; return true; }
            if (event.getAction() == android.view.MotionEvent.ACTION_UP) {
                if (y < 180f) {
                    if (x < 180f) { performHapticFeedback(1); showResetDialog(idx); return true; }
                    if (x > w - 180f) { performHapticFeedback(1); zikrMan.soundOn = !zikrMan.soundOn; zikrMan.save(); invalidate(); return true; }
                }
                if (x > 50f && x < w - 50f && y > bT && y < bB) { performHapticFeedback(1); showZikrList(); return true; }
                if (Math.abs(x - mXP) < 100 && Math.abs(y - btY) < 100) { performHapticFeedback(1); if(zikrMan.indCounts[idx]>0){ zikrMan.indCounts[idx]--; zikrMan.indTotals[idx]--; zikrMan.save(); invalidate(); } return true; }
                double dC = Math.sqrt(Math.pow(x - cX, 2) + Math.pow(y - cY, 2));
                if (dC <= rad + 60) { performHapticFeedback(1); zikrMan.indCounts[idx]++; zikrMan.indTotals[idx]++; if(zikrMan.soundOn && zikrMan.toneGen != null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50); if(zikrMan.tasbihList.get(idx).target > 0 && zikrMan.indCounts[idx] >= zikrMan.tasbihList.get(idx).target) { zikrMan.indCounts[idx] = 0; zikrMan.indRounds[idx]++; performHapticFeedback(0); } zikrMan.save(); invalidate(); return true; }
                float dX = x - startX; if(Math.abs(dX) > 150) { if(dX < 0) zikrMan.currentIdx = (zikrMan.currentIdx + 1)%zikrMan.tasbihList.size(); else zikrMan.currentIdx = (zikrMan.currentIdx - 1 + zikrMan.tasbihList.size())%zikrMan.tasbihList.size(); zikrMan.save(); invalidate(); return true; }
            } invalidate(); return true;
        }

        private void showResetDialog(int idx) {
            new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Reset")).setMessage(lang.get("Do you want to reset counts for this Dua?")).setPositiveButton(lang.get("Yes"), (di, wi) -> { zikrMan.indCounts[idx] = 0; zikrMan.indTotals[idx] = 0; zikrMan.indRounds[idx] = 0; zikrMan.save(); invalidate(); }).setNegativeButton(lang.get("No"), null).show();
        }

        private void showZikrList() {
            final android.app.Dialog d = new android.app.Dialog(getContext(), android.R.style.Theme_Black_NoTitleBar_Fullscreen);
            android.widget.LinearLayout root = new android.widget.LinearLayout(getContext()); root.setOrientation(1); root.setBackgroundColor(themeColors[0]); root.setPadding(40, 80, 40, 40);
            android.widget.TextView t1 = new android.widget.TextView(getContext()); t1.setText(lang.get("Zikr")); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(1); root.addView(t1);
            android.widget.ScrollView sv = new android.widget.ScrollView(getContext()); android.widget.LinearLayout list = new android.widget.LinearLayout(getContext()); list.setOrientation(1);
            for (int i = 0; i < zikrMan.tasbihList.size(); i++) {
                final int rIdx = i; android.widget.LinearLayout row = new android.widget.LinearLayout(getContext()); row.setPadding(20, 35, 20, 35); row.setGravity(16);
                android.widget.TextView tvD = new android.widget.TextView(getContext()); tvD.setText(zikrMan.tasbihList.get(rIdx).arabic); tvD.setTextColor(themeColors[2]); tvD.setTextSize(26); tvD.setTypeface(getArabicFont()); tvD.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 7.5f));
                tvD.setOnClickListener(v -> { zikrMan.currentIdx = rIdx; zikrMan.save(); invalidate(); d.dismiss(); });
                android.widget.TextView tvT = new android.widget.TextView(getContext()); tvT.setText(String.valueOf(zikrMan.tasbihList.get(rIdx).target)); tvT.setTextColor(colorAccent); tvT.setTextSize(22); tvT.setTypeface(appFonts[1]); tvT.setGravity(1); tvT.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 2.5f));
                tvT.setOnClickListener(v -> { editTarget(rIdx, tvT); }); row.addView(tvD); row.addView(tvT); list.addView(row);
            } sv.addView(list); root.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, 0, 1f));
            android.widget.Button btn = new android.widget.Button(getContext()); btn.setText("+ Add New"); btn.setBackgroundColor(themeColors[1]); btn.setTextColor(themeColors[2]);
            btn.setOnClickListener(v -> { 
                android.widget.LinearLayout l = new android.widget.LinearLayout(getContext()); l.setOrientation(1); l.setPadding(50,20,50,20);
                final android.widget.EditText eD = new android.widget.EditText(getContext()); eD.setHint("Arabic Dua"); final android.widget.EditText eT = new android.widget.EditText(getContext()); eT.setHint("Target"); eT.setInputType(2);
                l.addView(eD); l.addView(eT); new android.app.AlertDialog.Builder(getContext()).setTitle("Add").setView(l).setPositiveButton("OK", (di, wi) -> { if(!eD.getText().toString().isEmpty()){ zikrMan.tasbihList.add(new ZikrManager.TasbihData(eD.getText().toString(), Integer.parseInt(eT.getText().toString().isEmpty()?"0":eT.getText().toString()))); zikrMan.save(); invalidate(); d.dismiss(); } }).show();
            }); root.addView(btn); d.setContentView(root); d.show();
        }

        private void editTarget(int idx, android.widget.TextView tv) {
            final android.widget.EditText et = new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(idx).target));
            new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK", (di, wi) -> { if(!et.getText().toString().isEmpty()){ int n = Integer.parseInt(et.getText().toString()); zikrMan.tasbihList.get(idx).target = n; tv.setText(String.valueOf(n)); zikrMan.prefs.edit().putInt("target_"+idx, n).apply(); invalidate(); } }).show();
        }
    }
"""
    c = c[:start_idx] + new_canvas + c[end_idx:]

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Zikr Masterpiece RESTORED and Duplicate Variable FIXED!")
