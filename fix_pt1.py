import re
f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file: c = file.read()

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

garbage = ["private void setupBottomNav", "private void switchTab", "private void loadHabitsTab", "private void showHabitInput", "private void loadRozaTab", "private void loadQuranTab", "private void loadZikrTab", "private void loadStatsTab", "private android.graphics.Typeface getArabicFont", "private android.graphics.drawable.GradientDrawable getRdRect", "static class ZikrManager", "private void loadTodayPage() {", "private ZikrManager zikrMan ="]
for g in garbage: c = wipe_method(c, g)
c = c.replace('private ZikrManager zikrMan = null;', '')

new_base = """
    private void loadTodayPage() { if(fragmentContainer != null) switchTab(currentTab); else loadTodayPageCore(); }
    private android.graphics.Typeface _arabicFontObj = null;
    private android.graphics.Typeface getArabicFont() { if (_arabicFontObj == null) { try { _arabicFontObj = android.graphics.Typeface.createFromAsset(getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf"); } catch (Exception e) { _arabicFontObj = appFonts[1]; } } return _arabicFontObj; }
    private void setupBottomNav() { bottomNav.removeAllViews(); bottomNav.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, (int)(65*DENSITY))); bottomNav.setPadding(0, (int)(5*DENSITY), 0, (int)(5*DENSITY)); String[] titles = {lang.get("Salah"), lang.get("Fasting"), lang.get("Quran"), lang.get("Zikr"), lang.get("Stats")}; String[] icons = {"img_tab_salah", "img_habit_roza", "img_habit_quran", "img_habit_zikr", "img_tab_stats"}; bottomNav.setWeightSum(5f); for(int i=0; i<5; i++) { final int idx = i; boolean isActive = (currentTab == i); android.widget.LinearLayout tab = new android.widget.LinearLayout(this); tab.setOrientation(android.widget.LinearLayout.VERTICAL); tab.setGravity(android.view.Gravity.CENTER); tab.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -1, 1f)); android.view.View icon = ui.getRoundImage(icons[i], 0, android.graphics.Color.TRANSPARENT, isActive ? colorAccent : themeColors[3]); android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(24*DENSITY), (int)(24*DENSITY)); icLp.setMargins(0,0,0,(int)(3*DENSITY)); icon.setLayoutParams(icLp); android.widget.TextView tv = new android.widget.TextView(this); tv.setText(titles[i]); tv.setTextSize(10.5f); tv.setLines(1); tv.setTypeface(isActive ? appFonts[1] : appFonts[0]); tv.setTextColor(isActive ? colorAccent : themeColors[3]); tv.setGravity(android.view.Gravity.CENTER); tab.addView(icon); tab.addView(tv); tab.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); switchTab(idx); }); bottomNav.addView(tab); } }
    private void switchTab(int index) { currentTab = index; setupBottomNav(); fragmentContainer.removeAllViews(); android.widget.ScrollView sv = new android.widget.ScrollView(this); sv.setFillViewport(true); sv.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER); contentArea = new android.widget.LinearLayout(this); contentArea.setOrientation(android.widget.LinearLayout.VERTICAL); sv.addView(contentArea, new android.widget.FrameLayout.LayoutParams(-1, -1)); fragmentContainer.addView(sv); if(index == 0) loadTodayPageCore(); else if(index == 1) loadRozaTab(); else if(index == 2) loadQuranTab(); else if(index == 3) loadZikrTab(); else if(index == 4) loadStatsTab(); }
"""
c = c.rstrip()
if c.endswith('}'): c = c[:-1].rstrip()
c += "\n" + new_base + "\n}\n"
with open(f, 'w', encoding='utf-8') as file: file.write(c)
print("✅ Part 1 Done: Cleanup & Base Navigation injected.")
