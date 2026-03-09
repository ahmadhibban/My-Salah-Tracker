import re

# 1. Fix StatsHelper (Monthly Chart Overlap Fix)
sh = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
try:
    with open(sh, 'r', encoding='utf-8') as f: c = f.read()
    c = re.sub(r'fE\.add\(new com\.github\.mikephil\.charting\.data\.BarEntry\([^,]+,\s*fVal\)\);', 'fE.add(new com.github.mikephil.charting.data.BarEntry(i-0.2f, fVal));', c)
    with open(sh, 'w', encoding='utf-8') as f: f.write(c)
except Exception as e: print("StatsHelper error:", e)

# 2. Fix MainActivity Tabs Alignment & Arabic Font
ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
try:
    with open(ma, 'r', encoding='utf-8') as f: c = f.read()
    
    # Setup Arabic Font globally
    if 'private android.graphics.Typeface arabicFont;' not in c:
        c = c.replace('private android.graphics.Typeface[] appFonts = new android.graphics.Typeface[2];', 'private android.graphics.Typeface[] appFonts = new android.graphics.Typeface[2];\n    private android.graphics.Typeface arabicFont;')
    if 'arabicFont = android.graphics.Typeface.createFromAsset' not in c:
        c = c.replace('appFonts[1] = android.graphics.Typeface.DEFAULT_BOLD;', 'appFonts[1] = android.graphics.Typeface.DEFAULT_BOLD;\n        try { arabicFont = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf"); } catch(Exception e) { arabicFont = android.graphics.Typeface.DEFAULT; }')
    
    # Apply to Ayat of the day
    c = c.replace('aAr.setTypeface(appFonts[1]);', 'aAr.setTypeface(arabicFont != null ? arabicFont : appFonts[1]);')

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

    new_nav = """private void setupBottomNav() {
        bottomNav.removeAllViews();
        bottomNav.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, (int)(65*DENSITY)));
        String[] titles = {lang.get("Salah"), lang.get("Fasting"), lang.get("Quran"), lang.get("Zikr"), lang.get("Stats")};
        String[] icons = {"img_tab_salah", "img_habit_roza", "img_habit_quran", "img_habit_zikr", "img_tab_stats"};
        bottomNav.setWeightSum(5f);
        for(int i=0; i<5; i++) {
            final int idx = i; boolean isActive = (currentTab == i);
            android.widget.LinearLayout tab = new android.widget.LinearLayout(this); tab.setOrientation(android.widget.LinearLayout.VERTICAL); tab.setGravity(android.view.Gravity.CENTER);
            tab.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -1, 1f));
            android.view.View icon = ui.getRoundImage(icons[i], 0, android.graphics.Color.TRANSPARENT, isActive ? colorAccent : themeColors[3]);
            android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(24*DENSITY), (int)(24*DENSITY)); icLp.setMargins(0,0,0,(int)(4*DENSITY)); icon.setLayoutParams(icLp);
            android.widget.TextView tv = new android.widget.TextView(this); tv.setText(titles[i]); tv.setTextSize(10.5f); tv.setLines(1); tv.setEllipsize(android.text.TextUtils.TruncateAt.END); tv.setTypeface(isActive ? appFonts[1] : appFonts[0]); tv.setTextColor(isActive ? colorAccent : themeColors[3]); tv.setGravity(android.view.Gravity.CENTER);
            tab.addView(icon); tab.addView(tv);
            tab.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); switchTab(idx); });
            bottomNav.addView(tab);
        }
    }"""
    
    c = replace_method(c, "private void setupBottomNav()", new_nav)
    
    with open(ma, 'w', encoding='utf-8') as f: f.write(c)
    print("✅ Tabs perfectly aligned, Arabic Font prepared, and Monthly Chart fixed!")
except Exception as e:
    print("MainActivity error:", e)
