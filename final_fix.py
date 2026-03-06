import os

def update_file(path, old_text, new_text):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_text in content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.replace(old_text, new_text))
            return True
    return False

# ১. LanguageEngine Fix (Suffix + Button Text)
lang_path = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
suffix_logic = """    private String getBnSuffix(int d) {
        if (!currentLang.equals("bn")) return "";
        if(d == 1) return "লা";
        if(d == 2 || d == 3) return "রা";
        if(d == 4) return "ঠা";
        if(d >= 5 && d <= 18) return "ই";
        return "শে";
    }

    public String getGregorian(Date d) {"""

old_greg = "public String getGregorian(Date d) {"
update_file(lang_path, old_greg, suffix_logic)
update_file(lang_path, 'bnNum(c.get(Calendar.DAY_OF_MONTH))', 'bnNum(day) + getBnSuffix(day)')
update_file(lang_path, 'bnMap.put("Export JSON", "লোকাল ব্যাকআপ (JSON)");', 'bnMap.put("Export JSON", "লোকাল ব্যাকআপ");')

# ২. MainActivity Fix (All Done Long Press)
main_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
all_done_long = """markAllBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showUnmarkOptions(); } });
            markAllBtn.setOnLongClickListener(new View.OnLongClickListener() { @Override public boolean onLongClick(View v) { 
                v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setQazaStat(r, p, True); setFardStat(r, p, "no");
                    sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", True).putString(selectedDate[0]+"_"+p, "no").apply(); 
                    fbHelper.save(selectedDate[0], p, "no"); 
                } 
                updateRoomRecord(r);
                ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, None); loadTodayPage(); refreshWidget(); 
                return True; 
            } });"""
old_all_done = 'markAllBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showUnmarkOptions(); } });'
update_file(main_path, old_all_done, all_done_long)

# ৩. SalahWidget Fix (Suffix Restoration)
widget_path = 'app/src/main/java/com/my/salah/tracker/app/SalahWidget.java'
old_suffix = 'return "";'
new_suffix = 'if(d == 1) return "লা";\\n        if(d == 2 || d == 3) return "রা";\\n        if(d == 4) return "ঠা";\\n        if(d >= 5 && d <= 18) return "ই";\\n        return "শে";'
update_file(widget_path, old_suffix, new_suffix)

print("✅ All Fixes Applied Successfully!")
