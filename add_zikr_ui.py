import re
f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f).read()

def replace_method(text, method_sig, new_code):
    idx = text.find(method_sig)
    if idx == -1: return text
    start = text.find('{', idx)
    count = 1; i = start + 1
    while i < len(text) and count > 0:
        if text[i] == '{': count += 1
        elif text[i] == '}': count -= 1
        i += 1
    return text[:idx] + new_code + text[i:]

zikr_ui = """private void loadZikrTab() {
        if(zikrMan == null) { zikrMan = new ZikrManager(); zikrMan.init(this); }
        contentArea.setPadding((int)(20*DENSITY), (int)(10*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.LinearLayout header = new android.widget.LinearLayout(this); header.setOrientation(android.widget.LinearLayout.HORIZONTAL); header.setGravity(android.view.Gravity.CENTER_VERTICAL);
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Zikr")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-2,1f)); header.addView(h);
        
        android.view.View btnSet = ui.getRoundImage("img_zikr_settings", 8, themeColors[4], themeColors[3]); android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY)); icLp.setMargins(0,0,(int)(15*DENSITY),0); btnSet.setLayoutParams(icLp); header.addView(btnSet);
        android.view.View btnRes = ui.getRoundImage("img_zikr_reset", 8, themeColors[4], themeColors[3]); btnRes.setLayoutParams(icLp); header.addView(btnRes);
        android.view.View btnSnd = ui.getRoundImage("img_zikr_sound", 8, themeColors[4], zikrMan.soundOn ? colorAccent : themeColors[3]); btnSnd.setLayoutParams(new android.widget.LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY))); header.addView(btnSnd);
        contentArea.addView(header);

        android.widget.LinearLayout duaContainer = new android.widget.LinearLayout(this); duaContainer.setOrientation(android.widget.LinearLayout.HORIZONTAL); duaContainer.setGravity(android.view.Gravity.CENTER_VERTICAL); duaContainer.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY));
        android.widget.TextView btnPrev = new android.widget.TextView(this); btnPrev.setText("❮"); btnPrev.setTextSize(26); btnPrev.setTextColor(themeColors[3]); btnPrev.setPadding((int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY)); duaContainer.addView(btnPrev);
        
        final android.widget.TextView tvDua = new android.widget.TextView(this); tvDua.setTypeface(arabicFont != null ? arabicFont : appFonts[1]); tvDua.setTextColor(themeColors[2]); tvDua.setTextSize(30); tvDua.setGravity(android.view.Gravity.CENTER); tvDua.setLineSpacing(0, 1.2f);
        android.widget.ScrollView svDua = new android.widget.ScrollView(this); svDua.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,(int)(130*DENSITY),1f)); svDua.addView(tvDua);
        android.widget.LinearLayout duaWrap = new android.widget.LinearLayout(this); duaWrap.setGravity(android.view.Gravity.CENTER); duaWrap.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0,-1,1f)); duaWrap.addView(svDua); duaContainer.addView(duaWrap);
        
        android.widget.TextView btnNext = new android.widget.TextView(this); btnNext.setText("❯"); btnNext.setTextSize(26); btnNext.setTextColor(themeColors[3]); btnNext.setPadding((int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY),(int)(10*DENSITY)); duaContainer.addView(btnNext);
        contentArea.addView(duaContainer);

        android.widget.FrameLayout circleWrap = new android.widget.FrameLayout(this); android.widget.LinearLayout.LayoutParams cwLp = new android.widget.LinearLayout.LayoutParams(-1, (int)(290*DENSITY)); cwLp.setMargins(0,0,0,(int)(20*DENSITY)); circleWrap.setLayoutParams(cwLp);
        final android.view.View ring = new android.view.View(this) {
            android.graphics.Paint p = new android.graphics.Paint(android.graphics.Paint.ANTI_ALIAS_FLAG);
            @Override protected void onDraw(android.graphics.Canvas canvas) {
                float w = getWidth(), h = getHeight(); float r = Math.min(w, h)/2f - 25f;
                p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(28f); p.setColor(themeColors[1]); p.setStrokeCap(android.graphics.Paint.Cap.ROUND); canvas.drawCircle(w/2, h/2, r, p);
                ZikrManager.TasbihData d = zikrMan.tasbihList.get(zikrMan.currentIdx);
                if(d.target > 0) {
                    float sweep = ((float)zikrMan.indCounts[zikrMan.currentIdx] / d.target) * 360f;
                    p.setColor(colorAccent); canvas.drawArc(new android.graphics.RectF(w/2-r, h/2-r, w/2+r, h/2+r), -90, sweep, false, p);
                }
            }
        };
        circleWrap.addView(ring, new android.widget.FrameLayout.LayoutParams(-1,-1));
        
        android.widget.LinearLayout centerInfo = new android.widget.LinearLayout(this); centerInfo.setOrientation(android.widget.LinearLayout.VERTICAL); centerInfo.setGravity(android.view.Gravity.CENTER);
        final android.widget.TextView tvCount = new android.widget.TextView(this); tvCount.setTextSize(65); tvCount.setTypeface(appFonts[1]); tvCount.setTextColor(colorAccent); centerInfo.addView(tvCount);
        final android.widget.TextView tvTarget = new android.widget.TextView(this); tvTarget.setTextSize(16); tvTarget.setTypeface(appFonts[0]); tvTarget.setTextColor(themeColors[3]); centerInfo.addView(tvTarget);
        android.widget.FrameLayout.LayoutParams ciLp = new android.widget.FrameLayout.LayoutParams(-2,-2); ciLp.gravity = android.view.Gravity.CENTER; circleWrap.addView(centerInfo, ciLp);
        contentArea.addView(circleWrap);

        android.widget.LinearLayout footer = new android.widget.LinearLayout(this); footer.setOrientation(android.widget.LinearLayout.HORIZONTAL); footer.setGravity(android.view.Gravity.CENTER);
        final android.widget.TextView tvRound = new android.widget.TextView(this); tvRound.setTextSize(14); tvRound.setTypeface(appFonts[1]); tvRound.setTextColor(themeColors[2]); tvRound.setBackground(ui.getRoundRect(themeColors[1], 15f*DENSITY)); tvRound.setPadding((int)(20*DENSITY),(int)(12*DENSITY),(int)(20*DENSITY),(int)(12*DENSITY)); footer.addView(tvRound);
        final android.widget.TextView tvTotal = new android.widget.TextView(this); tvTotal.setTextSize(14); tvTotal.setTypeface(appFonts[1]); tvTotal.setTextColor(themeColors[2]); tvTotal.setBackground(ui.getRoundRect(themeColors[1], 15f*DENSITY)); tvTotal.setPadding((int)(20*DENSITY),(int)(12*DENSITY),(int)(20*DENSITY),(int)(12*DENSITY)); android.widget.LinearLayout.LayoutParams ftLp = new android.widget.LinearLayout.LayoutParams(-2,-2); ftLp.setMargins((int)(15*DENSITY),0,0,0); footer.addView(tvTotal, ftLp);
        contentArea.addView(footer);

        Runnable updateUi = () -> {
            ZikrManager.TasbihData d = zikrMan.tasbihList.get(zikrMan.currentIdx); tvDua.setText(d.arabic); boolean isBn = sp.getString("app_lang","en").equals("bn");
            tvCount.setText(isBn ? lang.bnNum(zikrMan.indCounts[zikrMan.currentIdx]) : String.valueOf(zikrMan.indCounts[zikrMan.currentIdx]));
            tvTarget.setText(d.target > 0 ? (lang.get("Target") + ": " + (isBn ? lang.bnNum(d.target) : d.target)) : "");
            tvRound.setText(lang.get("Rounds") + ": " + (isBn ? lang.bnNum(zikrMan.indRounds[zikrMan.currentIdx]) : zikrMan.indRounds[zikrMan.currentIdx]));
            tvTotal.setText(lang.get("Total") + ": " + (isBn ? lang.bnNum(zikrMan.indTotals[zikrMan.currentIdx]) : zikrMan.indTotals[zikrMan.currentIdx])); ring.invalidate();
        };

        btnPrev.setOnClickListener(v -> { zikrMan.currentIdx = (zikrMan.currentIdx - 1 + zikrMan.tasbihList.size()) % zikrMan.tasbihList.size(); zikrMan.save(); updateUi.run(); });
        btnNext.setOnClickListener(v -> { zikrMan.currentIdx = (zikrMan.currentIdx + 1) % zikrMan.tasbihList.size(); zikrMan.save(); updateUi.run(); });

        circleWrap.setOnClickListener(v -> {
            v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); ZikrManager.TasbihData d = zikrMan.tasbihList.get(zikrMan.currentIdx);
            zikrMan.indCounts[zikrMan.currentIdx]++; zikrMan.indTotals[zikrMan.currentIdx]++;
            if(zikrMan.soundOn && zikrMan.toneGen != null) zikrMan.toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 50);
            if(d.target > 0 && zikrMan.indCounts[zikrMan.currentIdx] >= d.target) { zikrMan.indCounts[zikrMan.currentIdx] = 0; zikrMan.indRounds[zikrMan.currentIdx]++; v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); }
            zikrMan.save(); updateUi.run(); tvCount.animate().scaleX(1.1f).scaleY(1.1f).setDuration(50).withEndAction(()->tvCount.animate().scaleX(1f).scaleY(1f).setDuration(150).start()).start();
        });

        btnSet.setOnClickListener(v -> {
            final android.widget.EditText et = new android.widget.EditText(this); et.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); et.setText(String.valueOf(zikrMan.tasbihList.get(zikrMan.currentIdx).target)); et.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY));
            new android.app.AlertDialog.Builder(this).setTitle(lang.get("Target")).setView(et).setPositiveButton("OK", (d,w)->{ if(!et.getText().toString().isEmpty()){ zikrMan.tasbihList.get(zikrMan.currentIdx).target = Integer.parseInt(et.getText().toString()); zikrMan.prefs.edit().putInt("target_"+zikrMan.currentIdx, zikrMan.tasbihList.get(zikrMan.currentIdx).target).apply(); updateUi.run(); } }).show();
        });
        
        btnRes.setOnClickListener(v -> { zikrMan.indCounts[zikrMan.currentIdx] = 0; zikrMan.indRounds[zikrMan.currentIdx] = 0; zikrMan.indTotals[zikrMan.currentIdx] = 0; zikrMan.save(); updateUi.run(); });
        btnSnd.setOnClickListener(v -> { zikrMan.soundOn = !zikrMan.soundOn; zikrMan.save(); loadZikrTab(); }); updateUi.run();
    }"""

c = replace_method(c, "private void loadZikrTab()", zikr_ui)
open(f, 'w').write(c)
print("✅ Part 2: Premium Zikr UI Built Successfully!")
