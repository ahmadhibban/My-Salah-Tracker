import re
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
c = open(le).read()
c = c.replace('bnMap.put("Fasting (Roza)", "রোজা");', 'bnMap.put("Fasting", "রোজা"); bnMap.put("Quran", "কুরআন"); bnMap.put("Zikr", "জিকির"); bnMap.put("Save", "সেভ করুন");')
if '"Fasting"' not in c:
    c = c.replace('bnMap.put("Settings & Options", "সেটিংস এবং অপশন");', 'bnMap.put("Settings & Options", "সেটিংস এবং অপশন");\n        bnMap.put("Fasting", "রোজা"); bnMap.put("Quran", "কুরআন"); bnMap.put("Zikr", "জিকির"); bnMap.put("Save", "সেভ করুন");')
open(le, 'w').write(c)

ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()

def replace_method(text, method_sig, new_code):
    idx = text.find(method_sig)
    if idx == -1: return text
    start = text.find('{', idx)
    count = 1
    i = start + 1
    while i < len(text) and count > 0:
        if text[i] == '{': count += 1
        elif text[i] == '}': count -= 1
        i += 1
    return text[:idx] + new_code + text[i:]

c = replace_method(c, "private void setupBottomNav()", "private void setupBottomNav() { \n// TBD\n")
c = replace_method(c, "private void switchTab(int index)", "private void switchTab(int index) { \n// TBD\n")
c = replace_method(c, "private void loadHabitsTab()", "")
c = replace_method(c, "private void showHabitInput(String id, String title, android.widget.TextView valTv)", "")

c = c.replace("private void setupBottomNav() { \n// TBD\n", "")
c = c.replace("private void switchTab(int index) { \n// TBD\n", "")

methods = """
    private void setupBottomNav() {
        bottomNav.removeAllViews();
        String[] titles = {lang.get("Salah"), lang.get("Fasting"), lang.get("Quran"), lang.get("Zikr"), lang.get("Stats")};
        String[] icons = {"img_tab_salah", "img_habit_roza", "img_habit_quran", "img_habit_zikr", "img_tab_stats"};
        bottomNav.setWeightSum(5f);
        for(int i=0; i<5; i++) {
            final int idx = i; boolean isActive = (currentTab == i);
            android.widget.LinearLayout tab = new android.widget.LinearLayout(this); tab.setOrientation(android.widget.LinearLayout.VERTICAL); tab.setGravity(android.view.Gravity.CENTER);
            tab.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -1, 1f));
            tab.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
            android.view.View icon = ui.getRoundImage(icons[i], 0, android.graphics.Color.TRANSPARENT, isActive ? colorAccent : themeColors[3]);
            android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(22*DENSITY), (int)(22*DENSITY)); icLp.setMargins(0,0,0,(int)(4*DENSITY)); icon.setLayoutParams(icLp);
            android.widget.TextView tv = new android.widget.TextView(this); tv.setText(titles[i]); tv.setTextSize(10); tv.setSingleLine(true); tv.setTypeface(isActive ? appFonts[1] : appFonts[0]); tv.setTextColor(isActive ? colorAccent : themeColors[3]); tv.setGravity(android.view.Gravity.CENTER);
            tab.addView(icon); tab.addView(tv);
            tab.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); switchTab(idx); });
            bottomNav.addView(tab);
        }
    }

    private void switchTab(int index) {
        currentTab = index; setupBottomNav(); fragmentContainer.removeAllViews();
        android.widget.ScrollView sv = new android.widget.ScrollView(this); sv.setFillViewport(true); sv.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
        contentArea = new android.widget.LinearLayout(this); contentArea.setOrientation(android.widget.LinearLayout.VERTICAL); sv.addView(contentArea, new android.widget.FrameLayout.LayoutParams(-1, -1));
        fragmentContainer.addView(sv);
        if(index == 0) loadTodayPageCore();
        else if(index == 1) loadRozaTab();
        else if(index == 2) loadQuranTab();
        else if(index == 3) loadZikrTab();
        else if(index == 4) loadStatsTab();
    }

    private void loadRozaTab() {
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Fasting")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        String currentRoza = sp.getString(selectedDate[0]+"_roza", lang.get("Not Fasting"));
        String[] opts = {lang.get("Fard"), lang.get("Nafl"), lang.get("Qaza"), lang.get("Not Fasting")};
        for(String opt : opts) {
            boolean isSel = opt.equals(currentRoza);
            android.widget.TextView b = new android.widget.TextView(this); b.setText(opt); b.setTextColor(isSel ? android.graphics.Color.WHITE : themeColors[2]); b.setTextSize(16); b.setGravity(android.view.Gravity.CENTER); b.setPadding(0,(int)(18*DENSITY),0,(int)(18*DENSITY)); b.setTypeface(isSel ? appFonts[1] : appFonts[0]);
            android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(isSel ? colorAccent : themeColors[1]); bg.setCornerRadius(20f*DENSITY); if(!isSel) bg.setStroke((int)(1.5f*DENSITY), themeColors[4]); b.setBackground(bg);
            android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams(-1, -2); lp.setMargins(0,0,0,(int)(15*DENSITY)); b.setLayoutParams(lp);
            b.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); sp.edit().putString(selectedDate[0]+"_roza", opt).apply(); loadRozaTab(); }); contentArea.addView(b);
        }
    }

    private void loadQuranTab() {
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Quran")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        android.widget.LinearLayout ayatCard = new android.widget.LinearLayout(this); ayatCard.setOrientation(android.widget.LinearLayout.VERTICAL); ayatCard.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable aBg = new android.graphics.drawable.GradientDrawable(android.graphics.drawable.GradientDrawable.Orientation.TL_BR, new int[]{colorAccent, android.graphics.Color.parseColor("#1A2980")}); aBg.setCornerRadius(25f*DENSITY); ayatCard.setBackground(aBg);
        android.widget.LinearLayout.LayoutParams aLp = new android.widget.LinearLayout.LayoutParams(-1, -2); aLp.setMargins(0,0,0,(int)(25*DENSITY)); ayatCard.setLayoutParams(aLp);
        android.widget.TextView aTitle = new android.widget.TextView(this); aTitle.setText("✨ " + lang.get("Ayat of the Day")); aTitle.setTextColor(android.graphics.Color.WHITE); aTitle.setTextSize(14); aTitle.setTypeface(appFonts[1]); aTitle.setAlpha(0.8f); aTitle.setPadding(0,0,0,(int)(15*DENSITY)); ayatCard.addView(aTitle);
        String[] ar = {"فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ", "فَاذْكُرُونِي أَذْكُرْكُمْ"}; String[] bn = {"নিশ্চয়ই কষ্টের সাথেই রয়েছে স্বস্তি। (৯৪:৫)", "তোমরা যেখানেই থাকো না কেন, তিনি তোমাদের সাথেই আছেন। (৫৭:৪)", "তোমরা আমাকে স্মরণ করো, আমিও তোমাদের স্মরণ করব। (২:১৫২)"};
        int rIdx = java.util.Calendar.getInstance().get(java.util.Calendar.DAY_OF_YEAR) % ar.length;
        android.widget.TextView aAr = new android.widget.TextView(this); aAr.setText(ar[rIdx]); aAr.setTextColor(android.graphics.Color.WHITE); aAr.setTextSize(26); aAr.setTypeface(appFonts[1]); aAr.setGravity(android.view.Gravity.CENTER); aAr.setPadding(0,0,0,(int)(10*DENSITY)); ayatCard.addView(aAr);
        android.widget.TextView aBn = new android.widget.TextView(this); aBn.setText(bn[rIdx]); aBn.setTextColor(android.graphics.Color.WHITE); aBn.setTextSize(14); aBn.setTypeface(appFonts[0]); aBn.setGravity(android.view.Gravity.CENTER); ayatCard.addView(aBn);
        contentArea.addView(ayatCard);
        android.widget.TextView tT = new android.widget.TextView(this); tT.setText(lang.get("Pages/Surah")); tT.setTextColor(themeColors[3]); tT.setTextSize(14); tT.setPadding(0,0,0,(int)(10*DENSITY)); contentArea.addView(tT);
        final android.widget.EditText et = new android.widget.EditText(this); et.setText(sp.getString(selectedDate[0]+"_quran", "")); et.setHint(lang.get("Pages/Surah")); et.setTextColor(themeColors[2]); et.setHintTextColor(themeColors[3]);
        android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setColor(themeColors[1]); ibg.setStroke((int)(1.5f*DENSITY), themeColors[4]); ibg.setCornerRadius(20f*DENSITY); et.setBackground(ibg); et.setPadding((int)(20*DENSITY),(int)(18*DENSITY),(int)(20*DENSITY),(int)(18*DENSITY));
        contentArea.addView(et, new android.widget.LinearLayout.LayoutParams(-1, -2));
        android.widget.Button btn = new android.widget.Button(this); btn.setText(lang.get("Save")); btn.setTextColor(android.graphics.Color.WHITE); android.graphics.drawable.GradientDrawable bbg = new android.graphics.drawable.GradientDrawable(); bbg.setColor(colorAccent); bbg.setCornerRadius(20f*DENSITY); btn.setBackground(bbg); btn.setAllCaps(false);
        android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, (int)(55*DENSITY)); blp.setMargins(0,(int)(15*DENSITY),0,0); contentArea.addView(btn, blp);
        btn.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); String txt = et.getText().toString().trim(); sp.edit().putString(selectedDate[0]+"_quran", txt).apply(); ui.showSmartBanner((android.widget.FrameLayout)findViewById(android.R.id.content), lang.get("Success"), lang.get("Progress updated."), "img_tick", colorAccent, null); });
    }

    private void loadZikrTab() {
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Zikr")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        android.widget.LinearLayout card = new android.widget.LinearLayout(this); card.setOrientation(android.widget.LinearLayout.VERTICAL); card.setGravity(android.view.Gravity.CENTER); card.setPadding((int)(20*DENSITY), (int)(60*DENSITY), (int)(20*DENSITY), (int)(60*DENSITY));
        android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(themeColors[1]); cBg.setCornerRadius(40f*DENSITY); cBg.setStroke((int)(1.5f*DENSITY), colorAccent); card.setBackground(cBg); card.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, -2));
        android.widget.TextView tv = new android.widget.TextView(this); tv.setText(lang.get("Tap anywhere to count")); tv.setTextColor(themeColors[3]); tv.setTypeface(appFonts[0]); tv.setTextSize(16); card.addView(tv);
        final android.widget.TextView countTv = new android.widget.TextView(this); countTv.setText(lang.bnNum(sp.getInt(selectedDate[0]+"_zikr", 0))); countTv.setTextColor(colorAccent); countTv.setTypeface(appFonts[1]); countTv.setTextSize(80); countTv.setPadding(0,(int)(20*DENSITY),0,(int)(20*DENSITY)); card.addView(countTv);
        android.widget.TextView tv2 = new android.widget.TextView(this); tv2.setText(lang.get("Long press to reset")); tv2.setTextColor(themeColors[3]); tv2.setTypeface(appFonts[0]); tv2.setTextSize(12); tv2.setAlpha(0.6f); card.addView(tv2);
        card.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); int c = sp.getInt(selectedDate[0]+"_zikr", 0) + 1; sp.edit().putInt(selectedDate[0]+"_zikr", c).apply(); countTv.setText(lang.bnNum(c)); countTv.animate().scaleX(1.1f).scaleY(1.1f).setDuration(50).withEndAction(()->countTv.animate().scaleX(1f).scaleY(1f).setDuration(150).start()).start(); });
        card.setOnLongClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); sp.edit().putInt(selectedDate[0]+"_zikr", 0).apply(); countTv.setText(lang.bnNum(0)); return true; });
        contentArea.addView(card);
    }
"""

c = c.rstrip()
if c.endswith('}'): c = c[:-1].rstrip()
c += "\n" + methods + "\n}\n"
open(ma, 'w').write(c)
print("✅ PERFECT WHATSAPP-STYLE 5 TABS CREATED!")
