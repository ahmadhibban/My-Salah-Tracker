import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ZikrCanvasView ক্লাসটি পুরোপুরি আপনার ডিজাইন অনুযায়ী রি-রাইট করা
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
            float w = getWidth(), h = getHeight(), centerX = w / 2.0f;
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx = zikrMan.currentIdx; ZikrManager.TasbihData d = zikrMan.tasbihList.get(idx); 
            int curVal = zikrMan.indCounts[idx];

            // --- 1. Top Icons (Exactly as in image) ---
            float iconY = 100f; float marginSide = 80f;
            p.setAlpha(255);
            if(resetBmp != null) canvas.drawBitmap(resetBmp, null, new android.graphics.RectF(marginSide-45f, iconY-45f, marginSide+45f, iconY+45f), p);
            else { p.setColor(themeColors[1]); canvas.drawCircle(marginSide, iconY, 65f, p); p.setColor(themeColors[3]); p.setTextSize(55f); p.setTextAlign(android.graphics.Paint.Align.CENTER); canvas.drawText("↺", marginSide, iconY+20f, p); }
            
            android.graphics.Bitmap sBmp = zikrMan.soundOn ? soundOnBmp : soundOffBmp;
            if(sBmp != null) canvas.drawBitmap(sBmp, null, new android.graphics.RectF(w-marginSide-45f, iconY-45f, w-marginSide+45f, iconY+45f), p);
            else { p.setColor(themeColors[1]); canvas.drawCircle(w-marginSide, iconY, 65f, p); p.setColor(zikrMan.soundOn ? colorAccent : themeColors[3]); p.setTextSize(55f); canvas.drawText(zikrMan.soundOn?"🔊":"🔇", w-marginSide, iconY+20f, p); }

            // --- 2. Arabic Box (Wide & Professional) ---
            float boxTop = 220f, boxHeight = 380f;
            p.setColor(themeColors[1]); p.setShadowLayer(25, 0, 12, android.graphics.Color.parseColor("#12000000"));
            canvas.drawRoundRect(new android.graphics.RectF(40f, boxTop, w-40f, boxTop+boxHeight), 45f, 45f, p); p.clearShadowLayer();
            
            // Smart Font Scaling to keep text in SINGLE LINE
            android.text.TextPaint tp = new android.text.TextPaint(p); tp.setTypeface(getArabicFont()); tp.setColor(themeColors[2]);
            int layoutW = (int)(w - 140); float fontSize = 105f; android.text.StaticLayout sl;
            while (true) { 
                tp.setTextSize(fontSize); sl = new android.text.StaticLayout(d.arabic, tp, layoutW, android.text.Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false); 
                if (sl.getLineCount() == 1 || fontSize <= 35f) break; fontSize -= 2f; 
            }
            canvas.save(); canvas.translate(centerX - (layoutW/2f), boxTop + (boxHeight - sl.getHeight())/2f); sl.draw(canvas); canvas.restore();

            p.setColor(themeColors[3]); p.setTextSize(34f); p.setTypeface(appFonts[0]); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            canvas.drawText(lang.get("Tap box to change Dua or Target"), centerX, boxTop + boxHeight + 75f, p);

            // --- 3. Main Progress Circle (Large Spacing) ---
            float circleY = boxTop + boxHeight + 520f; float radius = w * 0.38f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(48f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            p.setColor(themeColors[4]); canvas.drawCircle(centerX, circleY, radius, p);
            p.setColor(colorAccent); float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
            canvas.drawArc(new android.graphics.RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);

            // Dynamic Glowing Ball
            double rad = Math.toRadians(sweep - 90); float bX = (float)(centerX + radius * Math.cos(rad)), bY = (float)(circleY + radius * Math.sin(rad));
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(40, 0, 0, colorAccent); p.setColor(colorAccent); canvas.drawCircle(bX, bY, 36f, p); p.clearShadowLayer();
            p.setColor(android.graphics.Color.WHITE); canvas.drawCircle(bX, bY, 14f, p);

            // --- 4. Count & Target (Perfectly Centered) ---
            p.setTypeface(appFonts[1]); p.setColor(themeColors[2]); 
            String mStr = isBn ? toBengali(curVal) : String.valueOf(curVal);
            String tStr = (d.target > 0) ? (" / " + (isBn ? toBengali(d.target) : String.valueOf(d.target))) : "";
            float mSize = 270f; p.setTextSize(mSize); float mW = p.measureText(mStr);
            android.graphics.Paint tp2 = new android.graphics.Paint(p); tp2.setTextSize(65f); tp2.setColor(themeColors[3]); tp2.setTypeface(appFonts[0]); float tW = tp2.measureText(tStr);
            
            while(mW + tW > radius * 1.7f) { mSize -= 5f; p.setTextSize(mSize); tp2.setTextSize(mSize*0.25f); mW = p.measureText(mStr); tW = tp2.measureText(tStr); }
            float startXText = centerX - (mW + tW)/2f; float txtY = circleY + (mSize/3.2f);
            p.setTextAlign(android.graphics.Paint.Align.LEFT); canvas.drawText(mStr, startXText, txtY, p);
            canvas.drawText(targetStr(d, isBn), startXText + mW, txtY, tp2);

            // --- 5. Bottom Buttons (Symmetrical) ---
            float bY = circleY + radius + 160f; float mX = centerX - radius + 30f, sX = centerX + radius - 30f;
            drawBtn(canvas, mX, bY, "-", android.graphics.Color.parseColor("#EF4444"), 110f);
            drawBtn(canvas, sX, bY, isBn?toBengali(zikrMan.indRounds[idx]):String.valueOf(zikrMan.indRounds[idx]), colorAccent, 70f);
            p.setColor(themeColors[3]); p.setTextSize(34f); p.setTypeface(appFonts[0]); canvas.drawText(lang.get("Rounds"), sX, bY+135f, p);

            // --- 6. Total Card (Premium Look) ---
            String totTxt = lang.get("Total") + ": " + (isBn ? toBengali(zikrMan.indTotals[idx]) : zikrMan.indTotals[idx]);
            p.setTextSize(46f); p.setTypeface(appFonts[1]); float tWBox = p.measureText(totTxt) + 100f;
            p.setColor(themeColors[1]); p.setShadowLayer(15, 0, 8, android.graphics.Color.parseColor("#15000000"));
            canvas.drawRoundRect(new android.graphics.RectF(centerX-tWBox/2, bY+230f, centerX+tWBox/2, bY+330f), 35f, 35f, p); p.clearShadowLayer();
            p.setColor(themeColors[2]); canvas.drawText(totTxt, centerX, bY+298f, p);
        }

        private String targetStr(ZikrManager.TasbihData d, boolean bn) { return d.target > 0 ? (" / " + (bn ? toBengali(d.target) : d.target)) : ""; }

        private void drawBtn(android.graphics.Canvas cv, float x, float y, String txt, int color, float size) {
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            p.setColor(themeColors[1]); p.setShadowLayer(18, 0, 10, android.graphics.Color.parseColor("#1A000000")); cv.drawCircle(x, y, 90f, p); p.clearShadowLayer();
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(themeColors[4]); cv.drawCircle(x, y, 90f, p);
            p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(color); p.setTextSize(size); p.setTypeface(appFonts[1]); p.setTextAlign(android.graphics.Paint.Align.CENTER); cv.drawText(txt, x, y + size/3.2f, p);
        }

        @Override public boolean onTouchEvent(android.view.MotionEvent event) {
            float x = event.getX(), y = event.getY(), w = getWidth(), centerX = w / 2f;
            float boxTop = 220f, boxBottom = boxTop + 380f, circleY = boxBottom + 520f, radius = w * 0.38f; 
            float btnY = circleY + radius + 160f, mX = centerX - radius + 30f, sideMargin = 80f; int idx = zikrMan.currentIdx;
            if (event.getAction() == android.view.MotionEvent.ACTION_DOWN) { startX = x; startY = y; return true; }
            if (event.getAction() == android.view.MotionEvent.ACTION_UP) {
                if (y < 180f) {
                    if (x < 180f) { performHapticFeedback(1); showResetDialog(idx); return true; }
                    if (x > w - 180f) { performHapticFeedback(1); zikrMan.soundOn = !zikrMan.soundOn; zikrMan.save(); invalidate(); return true; }
                }
                if (x > 40f && x < w - 40f && y > boxTop && y < boxBottom) { performHapticFeedback(1); showZikrList(); return true; }
                if (Math.abs(x - mX) < 110 && Math.abs(y - btnY) < 110) { performHapticFeedback(1); if(zikrMan.indCounts[idx]>0){ zikrMan.indCounts[idx]--; zikrMan.indTotals[idx]--; zikrMan.save(); invalidate(); } return true; }
                double dC = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - circleY, 2));
                if (dC <= radius + 60) { performHapticFeedback(1); zikrMan.indCounts[idx]++; zikrMan.indTotals[idx]++; if(zikrMan.soundOn && zikrMan.toneGen != null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50); if(zikrMan.tasbihList.get(idx).target > 0 && zikrMan.indCounts[idx] >= zikrMan.tasbihList.get(idx).target) { zikrMan.indCounts[idx] = 0; zikrMan.indRounds[idx]++; performHapticFeedback(0); } zikrMan.save(); invalidate(); return true; }
                float deltaX = x - startX; if(Math.abs(deltaX) > 150) { if(deltaX < 0) zikrMan.currentIdx = (zikrMan.currentIdx + 1)%zikrMan.tasbihList.size(); else zikrMan.currentIdx = (zikrMan.currentIdx - 1 + zikrMan.tasbihList.size())%zikrMan.tasbihList.size(); zikrMan.save(); invalidate(); return true; }
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
            android.widget.Button btn = new android.widget.Button(getContext()); btn.setText("+ Add New"); btn.setBackgroundColor(themeColors[1]); btn.setTextColor(themeColors[2]); root.addView(btnAdd(d)); d.setContentView(root); d.show();
        }

        private void editTarget(int idx, android.widget.TextView tv) {
            final android.widget.EditText et = new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(idx).target));
            new android.app.AlertDialog.Builder(getContext()).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK", (di, wi) -> { if(!et.getText().toString().isEmpty()){ int n = Integer.parseInt(et.getText().toString()); zikrMan.tasbihList.get(idx).target = n; tv.setText(String.valueOf(n)); zikrMan.prefs.edit().putInt("target_"+idx, n).apply(); invalidate(); } }).show();
        }

        private android.widget.Button btnAdd(android.app.Dialog d) {
            android.widget.Button b = new android.widget.Button(getContext()); b.setText("+ Add New"); b.setAllCaps(false); b.setBackgroundColor(themeColors[1]); b.setTextColor(themeColors[2]);
            b.setOnClickListener(v -> { 
                android.widget.LinearLayout l = new android.widget.LinearLayout(getContext()); l.setOrientation(1); l.setPadding(50,20,50,20);
                final android.widget.EditText eD = new android.widget.EditText(getContext()); eD.setHint("Arabic Dua"); final android.widget.EditText eT = new android.widget.EditText(getContext()); eT.setHint("Target"); eT.setInputType(2);
                l.addView(eD); l.addView(eT); new android.app.AlertDialog.Builder(getContext()).setTitle("Add").setView(l).setPositiveButton("OK", (di, wi) -> { if(!eD.getText().toString().isEmpty()){ zikrMan.tasbihList.add(new ZikrManager.TasbihData(eD.getText().toString(), Integer.parseInt(eT.getText().toString().isEmpty()?"0":eT.getText().toString()))); zikrMan.save(); invalidate(); d.dismiss(); } }).show();
            }); return b;
        }
    }
"""
c = c[:start_idx] + new_canvas + c[end_idx:]

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Zikr Masterpiece RESTORED with precise spacing and single-line Arabic scaling!")
