import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# ১. switchTab আপডেট করা যাতে জিকির পেজে ScrollView ঝামেলা না করে (Canvas এর জন্য ফুল স্ক্রিন লাগে)
old_switch = """private void switchTab(int index) {
        currentTab = index; setupBottomNav(); fragmentContainer.removeAllViews();
        android.widget.ScrollView sv = new android.widget.ScrollView(this); sv.setFillViewport(true); sv.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
        contentArea = new android.widget.LinearLayout(this); contentArea.setOrientation(android.widget.LinearLayout.VERTICAL); sv.addView(contentArea, new android.widget.FrameLayout.LayoutParams(-1, -1));
        fragmentContainer.addView(sv);
        if(index == 0) loadTodayPageCore();
        else if(index == 1) loadRozaTab();
        else if(index == 2) loadQuranTab();
        else if(index == 3) loadZikrTab();
        else if(index == 4) loadStatsTab();
    }"""

new_switch = """private void switchTab(int index) {
        currentTab = index; setupBottomNav(); fragmentContainer.removeAllViews();
        contentArea = new android.widget.LinearLayout(this); contentArea.setOrientation(android.widget.LinearLayout.VERTICAL);
        if(index == 3) {
            contentArea.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
            fragmentContainer.addView(contentArea);
        } else {
            android.widget.ScrollView sv = new android.widget.ScrollView(this); sv.setFillViewport(true); sv.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
            sv.addView(contentArea, new android.widget.FrameLayout.LayoutParams(-1, -1));
            fragmentContainer.addView(sv);
        }
        if(index == 0) loadTodayPageCore();
        else if(index == 1) loadRozaTab();
        else if(index == 2) loadQuranTab();
        else if(index == 3) loadZikrTab();
        else if(index == 4) loadStatsTab();
    }"""
if 'if(index == 3) {' not in c:
    c = c.replace(old_switch, new_switch)

# ২. পুরনো ফালতু জিকির পেজ মুছে ফেলা
def wipe_method(text, method_name):
    while True:
        idx = text.find(method_name)
        if idx == -1: break
        start = text.find('{', idx)
        if start == -1: break
        count = 1; i = start + 1
        while i < len(text) and count > 0:
            if text[i] == '{': count += 1
            elif text[i] == '}': count -= 1
            i += 1
        text = text[:idx] + text[i:]
    return text

c = wipe_method(c, "private void loadZikrTab()")

# ৩. ইউজারের অরিজিনাল ক্যানভাস কোড (ZikrCanvasView) ইনজেক্ট করা
canvas_code = """
    // --- USER'S ORIGINAL MASTERPIECE ZIKR CANVAS ---
    class ZikrCanvasView extends android.view.View {
        private int pressedButton = -1;
        private float startX, startY;
        private android.graphics.Typeface bnFont;

        public ZikrCanvasView(android.content.Context context) {
            super(context);
            bnFont = appFonts[1];
            if(zikrMan == null) { zikrMan = new ZikrManager(); zikrMan.init(context); }
        }

        private String toBengali(int num) {
            String out = String.valueOf(num);
            String[] eng = {"0","1","2","3","4","5","6","7","8","9"}, bng = {"০","১","২","৩","৪","৫","৬","৭","৮","৯"};
            for(int i=0; i<10; i++) out = out.replace(eng[i], bng[i]); return out;
        }

        @Override
        protected void onDraw(android.graphics.Canvas canvas) {
            super.onDraw(canvas);
            float w = getWidth(), centerX = w / 2.0f;
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            int idx = zikrMan.currentIdx;
            if (idx >= zikrMan.tasbihList.size()) idx = 0;
            ZikrManager.TasbihData d = zikrMan.tasbihList.get(idx);
            int curVal = zikrMan.indCounts[idx];

            // --- Arabic Box ---
            android.text.TextPaint tp = new android.text.TextPaint(p);
            tp.setTypeface(getArabicFont()); tp.setColor(android.graphics.Color.BLACK);
            float boxTop = 50f, fixedBoxHeight = 420f, boxBottom = boxTop + fixedBoxHeight;
            int layoutWidth = (int)(w - 200); 
            
            float autoFontSize = 95f; android.text.StaticLayout sl;
            while (true) {
                tp.setTextSize(autoFontSize);
                sl = new android.text.StaticLayout(d.arabic, tp, layoutWidth, android.text.Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false);
                if (sl.getHeight() <= (fixedBoxHeight - 40f) || autoFontSize <= 35f) break;
                autoFontSize -= 2f; 
            }
            p.setColor(android.graphics.Color.parseColor("#CFD8DC")); 
            canvas.drawRoundRect(new android.graphics.RectF(30, boxTop, w - 30, boxBottom), 40f, 40f, p);
            canvas.save();
            canvas.translate(centerX - (layoutWidth / 2f), boxTop + (fixedBoxHeight - sl.getHeight()) / 2f);
            sl.draw(canvas);
            canvas.restore();

            // --- Swipe Text ---
            p.setColor(android.graphics.Color.GRAY); p.setTextSize(32f); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            p.setTypeface(android.graphics.Typeface.DEFAULT);
            canvas.drawText("Swipe left or right to change Dua", centerX, boxBottom + 60f, p);

            // --- 3 Icons ---
            float btnY = boxBottom + 220f; float btnSp = w / 4;
            String[] icons = {"⚙", "↻", (zikrMan.soundOn ? "🔊" : "🔇")};
            int[] ringColors = { android.graphics.Color.parseColor("#455A64"), android.graphics.Color.parseColor("#2E7D32"), android.graphics.Color.parseColor("#E65100") };
            for(int i=0; i<3; i++) {
                float shift = (pressedButton == i) ? 8f : 0f; 
                p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(10f); p.setColor(ringColors[i]);
                canvas.drawCircle(btnSp * (i+1), btnY + shift, 85f, p);
                p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(android.graphics.Color.WHITE);
                if (pressedButton != i) p.setShadowLayer(15, 0, 10, android.graphics.Color.LTGRAY);
                canvas.drawCircle(btnSp * (i+1), btnY + shift, 80f, p); p.clearShadowLayer();
                p.setTextAlign(android.graphics.Paint.Align.CENTER); p.setColor(ringColors[i]); 
                if (i == 0) { p.setTextSize(110f); canvas.drawText(icons[i], btnSp * (i+1), btnY + shift + 38f, p); }
                else if (i == 1) { p.setTextSize(130f); canvas.drawText(icons[i], btnSp * (i+1), btnY + shift + 42f, p); }
                else { p.setTextSize(85f); canvas.drawText(icons[i], btnSp * (i+1), btnY + shift + 30f, p); }
            }

            // --- Main Circle ---
            float circleY = 1320f, radius = w * 0.35f; 
            float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(50f); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            p.setColor(android.graphics.Color.parseColor("#D1DBE0")); canvas.drawCircle(centerX, circleY, radius, p);
            p.setColor(android.graphics.Color.parseColor("#1B5E20")); 
            canvas.drawArc(new android.graphics.RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
            
            // Glowing Ball
            double angle = Math.toRadians(sweep - 90);
            float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
            p.setStyle(android.graphics.Paint.Style.FILL); p.setShadowLayer(35, 0, 0, android.graphics.Color.parseColor("#00FBFF"));
            p.setColor(android.graphics.Color.parseColor("#A3FFFD")); canvas.drawCircle(ballX, ballY, 35f, p); p.clearShadowLayer();
            p.setColor(android.graphics.Color.WHITE); canvas.drawCircle(ballX, ballY, 15f, p);

            // --- Count Text ---
            p.setStyle(android.graphics.Paint.Style.FILL); p.setTypeface(bnFont); p.setColor(android.graphics.Color.BLACK); 
            String mainCountStr = toBengali(curVal); String targetPart = " / " + toBengali(d.target); 
            p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
            android.graphics.Paint targetPaint = new android.graphics.Paint(p); targetPaint.setTextSize(42f); targetPaint.setColor(android.graphics.Color.parseColor("#546E7A")); 
            float targetWidth = targetPaint.measureText(targetPart); float totalWidth = mainTextWidth + targetWidth; 
            float sXText = centerX - (totalWidth / 2f);
            p.setTextAlign(android.graphics.Paint.Align.LEFT); canvas.drawText(mainCountStr, sXText, circleY + 85f, p);
            targetPaint.setTextAlign(android.graphics.Paint.Align.LEFT); canvas.drawText(targetPart, sXText + mainTextWidth, circleY + 100f, targetPaint);
            
            // --- Minus & Round ---
            float sX = centerX + radius + 15, sY = circleY + radius + 140, mX = centerX - radius - 15;
            p.setStyle(android.graphics.Paint.Style.FILL); p.setColor(android.graphics.Color.WHITE); p.setShadowLayer(20, 0, 8, android.graphics.Color.parseColor("#E0E0E0"));
            canvas.drawCircle(mX, sY, 80f, p); canvas.drawCircle(sX, sY, 80f, p); p.clearShadowLayer();
            p.setColor(android.graphics.Color.parseColor("#D32F2F")); p.setTextSize(100f); p.setTextAlign(android.graphics.Paint.Align.CENTER);
            canvas.drawText("-", mX, sY + 30, p);
            p.setColor(android.graphics.Color.parseColor("#37474F")); p.setTextSize(65f); canvas.drawText(toBengali(zikrMan.indRounds[idx]), sX, sY + 22, p);

            // --- Total ---
            String totalTxt = "সর্বমোট: " + toBengali(zikrMan.indTotals[idx]);
            p.setTextSize(42f); float boxW = p.measureText(totalTxt) + 70; p.setColor(android.graphics.Color.parseColor("#CFD8DC"));
            canvas.drawRoundRect(new android.graphics.RectF(centerX - boxW/2, sY + 160, centerX + boxW/2, sY + 255), 25f, 25f, p);
            p.setColor(android.graphics.Color.parseColor("#263238")); canvas.drawText(totalTxt, centerX, sY + 222, p);
        }

        @Override
        public boolean onTouchEvent(android.view.MotionEvent event) {
            float x = event.getX(), y = event.getY();
            float w = getWidth(), centerX = w / 2.0f;
            float boxBottom = 470f; float btnY = boxBottom + 220f, btnSp = w / 4;
            float circleY = 1320f; float radius = w * 0.35f; 
            float sY = circleY + radius + 140; float mX = centerX - radius - 15; 
            int idx = zikrMan.currentIdx;

            if (event.getAction() == android.view.MotionEvent.ACTION_DOWN) {
                startX = x; startY = y;
                for (int i = 0; i < 3; i++) { if (Math.abs(x - btnSp * (i+1)) < 90 && Math.abs(y - btnY) < 90) { pressedButton = i; invalidate(); break; } }
                return true;
            } 
            
            if (event.getAction() == android.view.MotionEvent.ACTION_UP) {
                pressedButton = -1;
                
                // Minus
                if (Math.abs(x - mX) < 95 && Math.abs(y - sY) < 95) {
                    performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                    if (zikrMan.indCounts[idx] > 0) { zikrMan.indCounts[idx]--; if (zikrMan.indTotals[idx] > 0) zikrMan.indTotals[idx]--; zikrMan.save(); invalidate(); } return true;
                }

                // Main Circle
                double distToCenter = Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - circleY, 2));
                if (distToCenter <= radius + 50) {
                    performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                    zikrMan.indCounts[idx]++; zikrMan.indTotals[idx]++;
                    if (zikrMan.soundOn && zikrMan.toneGen != null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50);
                    if (zikrMan.tasbihList.get(idx).target > 0 && zikrMan.indCounts[idx] >= zikrMan.tasbihList.get(idx).target) {
                        zikrMan.indCounts[idx] = 0; zikrMan.indRounds[idx]++; performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS);
                    }
                    zikrMan.save(); invalidate(); return true;
                }

                // Icons
                if (Math.abs(y - btnY) < 110) {
                    if (Math.abs(x - btnSp * 1) < 100) { // Settings
                        performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                        final android.app.Dialog d = new android.app.Dialog(getContext(), android.R.style.Theme_Black_NoTitleBar_Fullscreen);
                        android.widget.LinearLayout root = new android.widget.LinearLayout(getContext()); root.setOrientation(android.widget.LinearLayout.VERTICAL); root.setBackgroundColor(android.graphics.Color.parseColor("#3D301E")); root.setPadding(40, 80, 40, 40);
                        android.widget.TextView t1 = new android.widget.TextView(getContext()); t1.setText("Tasbih Settings"); t1.setTextColor(android.graphics.Color.YELLOW); t1.setTextSize(26); t1.setGravity(android.view.Gravity.CENTER); root.addView(t1);
                        android.widget.TextView t2 = new android.widget.TextView(getContext()); t2.setText("Select Dua or Click Number to Edit Target"); t2.setTextColor(android.graphics.Color.WHITE); t2.setTextSize(14); t2.setGravity(android.view.Gravity.CENTER); t2.setPadding(0, 5, 0, 30); root.addView(t2);
                        android.widget.ScrollView sv = new android.widget.ScrollView(getContext()); android.widget.LinearLayout listBody = new android.widget.LinearLayout(getContext()); listBody.setOrientation(android.widget.LinearLayout.VERTICAL);
                        for (int i = 0; i < zikrMan.tasbihList.size(); i++) {
                            final int rowIdx = i; android.widget.LinearLayout row = new android.widget.LinearLayout(getContext()); row.setPadding(10, 30, 10, 30); row.setWeightSum(10f); row.setGravity(android.view.Gravity.CENTER_VERTICAL);
                            android.widget.TextView tvDua = new android.widget.TextView(getContext()); tvDua.setText(zikrMan.tasbihList.get(rowIdx).arabic); tvDua.setTextColor(android.graphics.Color.WHITE); tvDua.setTextSize(24); tvDua.setGravity(android.view.Gravity.CENTER); tvDua.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 7.5f)); tvDua.setTypeface(getArabicFont());
                            tvDua.setOnClickListener(v2 -> { zikrMan.currentIdx = rowIdx; zikrMan.save(); invalidate(); d.dismiss(); });
                            final android.widget.TextView tvTarg = new android.widget.TextView(getContext()); tvTarg.setText(String.valueOf(zikrMan.tasbihList.get(rowIdx).target)); tvTarg.setTextColor(android.graphics.Color.YELLOW); tvTarg.setTextSize(20); tvTarg.setGravity(android.view.Gravity.CENTER); tvTarg.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 2.5f));
                            tvTarg.setOnClickListener(v3 -> {
                                final android.widget.EditText et = new android.widget.EditText(getContext()); et.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); et.setText(String.valueOf(zikrMan.tasbihList.get(rowIdx).target));
                                new android.app.AlertDialog.Builder(getContext()).setTitle("Edit Target").setView(et).setPositiveButton("OK", (di, wi) -> { if(!et.getText().toString().isEmpty()){ zikrMan.tasbihList.get(rowIdx).target = Integer.parseInt(et.getText().toString()); tvTarg.setText(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+rowIdx, zikrMan.tasbihList.get(rowIdx).target).apply(); invalidate(); } }).show();
                            });
                            row.addView(tvDua); row.addView(tvTarg); listBody.addView(row);
                        }
                        sv.addView(listBody); root.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, 0, 1f));
                        android.widget.Button btnAdd = new android.widget.Button(getContext()); btnAdd.setText("+ Add New Tasbih"); btnAdd.setAllCaps(false); btnAdd.setBackgroundColor(android.graphics.Color.parseColor("#4D3B2A")); btnAdd.setTextColor(android.graphics.Color.WHITE); android.widget.LinearLayout.LayoutParams btnLp = new android.widget.LinearLayout.LayoutParams(-1, -2); btnLp.setMargins(0, 20, 0, 0); btnAdd.setLayoutParams(btnLp);
                        btnAdd.setOnClickListener(v4 -> {
                            android.widget.LinearLayout lay = new android.widget.LinearLayout(getContext()); lay.setOrientation(android.widget.LinearLayout.VERTICAL); lay.setPadding(50, 20, 50, 20);
                            final android.widget.EditText etDua = new android.widget.EditText(getContext()); etDua.setHint("Enter Arabic Dua");
                            final android.widget.EditText etTarget = new android.widget.EditText(getContext()); etTarget.setHint("Target Count"); etTarget.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
                            lay.addView(etDua); lay.addView(etTarget);
                            new android.app.AlertDialog.Builder(getContext()).setTitle("Add New").setView(lay).setPositiveButton("Add", (di, wi) -> { String dText = etDua.getText().toString(); String tText = etTarget.getText().toString(); if(!dText.isEmpty() && !tText.isEmpty()){ zikrMan.tasbihList.add(new ZikrManager.TasbihData(dText, Integer.parseInt(tText))); zikrMan.save(); invalidate(); d.dismiss(); } }).setNegativeButton("Cancel", null).show();
                        });
                        root.addView(btnAdd); d.setContentView(root); d.show(); return true;
                    }
                    else if (Math.abs(x - btnSp * 2) < 100) { // Reset
                        performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                        new android.app.AlertDialog.Builder(getContext()).setTitle("Reset").setMessage("Do you want to reset counts for this Dua?").setPositiveButton("Yes", (dialog, which) -> { zikrMan.indCounts[idx] = 0; zikrMan.indTotals[idx] = 0; zikrMan.indRounds[idx] = 0; zikrMan.save(); invalidate(); }).setNegativeButton("No", null).show(); return true;
                    }
                    else if (Math.abs(x - btnSp * 3) < 100) { // Sound
                        performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); zikrMan.soundOn = !zikrMan.soundOn; zikrMan.save(); invalidate(); return true;
                    }
                }

                // Swipe
                float deltaX = x - startX;
                if (Math.abs(deltaX) > 150) {
                    if (deltaX < 0) zikrMan.currentIdx = (zikrMan.currentIdx + 1) % zikrMan.tasbihList.size();
                    else zikrMan.currentIdx = (zikrMan.currentIdx - 1 + zikrMan.tasbihList.size()) % zikrMan.tasbihList.size();
                    zikrMan.save(); invalidate(); return true;
                }
            }
            invalidate();
            return true;
        }
    }

    private void loadZikrTab() {
        contentArea.removeAllViews();
        contentArea.addView(new ZikrCanvasView(this), new android.widget.LinearLayout.LayoutParams(-1, -1));
    }
"""

c = c.rstrip()
if c.endswith('}'): c = c[:-1].rstrip()
c += "\n" + canvas_code + "\n}\n"

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ YOUR ORIGINAL MASTERPIECE CANVAS IS RESTORED PERFECTLY!")
