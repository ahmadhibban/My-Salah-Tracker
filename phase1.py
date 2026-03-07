import os

def replace_in_file(path, old, new):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f: content = f.read()
        if old in content:
            with open(path, 'w', encoding='utf-8') as f: f.write(content.replace(old, new))
            return True
    return False

# 1. MainActivity: Nav Bar Fix & Smooth Theme Transition
m_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
o_nav = 'getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_HIDE_NAVIGATION | View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY | View.SYSTEM_UI_FLAG_LAYOUT_STABLE);'
n_nav = 'getWindow().getDecorView().setSystemUiVisibility(View.SYSTEM_UI_FLAG_LAYOUT_STABLE | View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN);\n            if (Build.VERSION.SDK_INT >= 21) { getWindow().setStatusBarColor(Color.TRANSPARENT); getWindow().setNavigationBarColor(themeColors[0]); }'
replace_in_file(m_path, o_nav, n_nav)

o_theme = 'sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); recreate();'
n_theme = 'sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); finish(); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out); startActivity(getIntent());'
replace_in_file(m_path, o_theme, n_theme)

# 2. UIComponents: Add Touch/Click Feedback Engine
u_path = 'app/src/main/java/com/my/salah/tracker/app/UIComponents.java'
o_cf = 'public void hideLoadingBanner(final FrameLayout root) {'
n_cf = 'public void addClickFeedback(final View v) { v.setOnTouchListener(new View.OnTouchListener() { @Override public boolean onTouch(View view, android.view.MotionEvent event) { switch (event.getAction()) { case android.view.MotionEvent.ACTION_DOWN: view.animate().scaleX(0.92f).scaleY(0.92f).alpha(0.7f).setDuration(100).start(); break; case android.view.MotionEvent.ACTION_UP: case android.view.MotionEvent.ACTION_CANCEL: view.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(100).start(); break; } return false; } }); }\n\n    public void hideLoadingBanner(final FrameLayout root) {'
replace_in_file(u_path, o_cf, n_cf)

# 3. BackupHelper: Human Readable File Name & Language Fix
b_path = 'app/src/main/java/com/my/salah/tracker/app/BackupHelper.java'
o_bn = 'File f = new File(dir, "Salah_Backup_" + System.currentTimeMillis() + ".json");'
n_bn = 'String dStr = new SimpleDateFormat("dd_MMM_yyyy", Locale.US).format(new Date());\n            File f = new File(dir, "Salah_Backup_" + dStr + "_" + (System.currentTimeMillis()%1000) + ".json");'
replace_in_file(b_path, o_bn, n_bn)

o_lang = 'String syncText = lastSyncTime == 0 ?\n        "Never synced" : "Last synced: " + new SimpleDateFormat("dd MMM, hh:mm a", Locale.US).format(new Date(lastSyncTime));\n        if(lang.get("Fajr").equals("ফজর")) { syncText = lastSyncTime == 0 ? "কখনো সিঙ্ক করা হয়নি" : "শেষ সিঙ্ক: " + lang.bnNum(new SimpleDateFormat("dd MMM, hh:mm a", Locale.US).format(new Date(lastSyncTime)));\n        }'
n_lang = 'String syncText = lastSyncTime == 0 ? lang.get("Never synced") : lang.get("Last synced") + ": " + (lang.get("Fajr").equals("ফজর") ? lang.bnNum(new SimpleDateFormat("dd MMM, hh:mm a", Locale.US).format(new Date(lastSyncTime))) : new SimpleDateFormat("dd MMM, hh:mm a", Locale.US).format(new Date(lastSyncTime)));'
replace_in_file(b_path, o_lang, n_lang)

# 4. LanguageEngine: Add missing Bangla words
l_path = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
o_map = 'bnMap.put("You\'ve completed all prayers for this day.\\nMay Allah accept it.", "এই দিনের সব নামাজ সম্পন্ন হয়েছে।\\nআল্লাহ কবুল করুন।");'
n_map = o_map + '\n        bnMap.put("Never synced", "কখনো সিঙ্ক করা হয়নি"); bnMap.put("Last synced", "শেষ সিঙ্ক"); bnMap.put("Skip", "এড়িয়ে যান");'
replace_in_file(l_path, o_map, n_map)

# 5. OnboardingHelper: Add "Skip" Button
o_path = 'app/src/main/java/com/my/salah/tracker/app/OnboardingHelper.java'
o_skip = 'main.addView(iconContainer); main.addView(title); main.addView(desc); main.addView(nextBtn); overlay.addView(main); root.addView(overlay);'
n_skip = 'main.addView(iconContainer); main.addView(title); main.addView(desc); main.addView(nextBtn); overlay.addView(main); root.addView(overlay);\n        TextView skipBtn = new TextView(activity); skipBtn.setText(lang.get("Skip")); skipBtn.setTextColor(themeColors[3]); skipBtn.setTextSize(14); skipBtn.setTypeface(Typeface.DEFAULT_BOLD); skipBtn.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));\n        FrameLayout.LayoutParams skipLp = new FrameLayout.LayoutParams(-2, -2); skipLp.gravity = Gravity.TOP | Gravity.END; skipLp.setMargins(0, (int)(30*DENSITY), 0, 0); overlay.addView(skipBtn, skipLp);\n        skipBtn.setOnClickListener(v -> { sp.edit().putBoolean("is_first_run_tutorial", false).apply(); overlay.animate().alpha(0f).setDuration(300).withEndAction(() -> root.removeView(overlay)).start(); });'
replace_in_file(o_path, o_skip, n_skip)

print("✅ Phase 1: Core UX & Bug Fixes Applied Successfully!")
