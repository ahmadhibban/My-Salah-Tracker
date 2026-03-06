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

# ১. MainActivity Fix (All Done Long Press)
main_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
all_done_long = """markAllBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showUnmarkOptions(); } });
            markAllBtn.setOnLongClickListener(new View.OnLongClickListener() { @Override public boolean onLongClick(View v) { 
                v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                for(String p : AppConstants.PRAYERS) { 
                    setQazaStat(r, p, true); setFardStat(r, p, "no");
                    sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", true).putString(selectedDate[0]+"_"+p, "no").apply(); 
                    fbHelper.save(selectedDate[0], p, "no"); 
                } 
                updateRoomRecord(r);
                ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null); loadTodayPage(); refreshWidget(); 
                return true; 
            } });"""
old_all_done = 'markAllBtn.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { showUnmarkOptions(); } });'
m_res = update_file(main_path, old_all_done, all_done_long)

# ২. SalahWidget Fix (Suffix Restoration)
widget_path = 'app/src/main/java/com/my/salah/tracker/app/SalahWidget.java'
new_suffix = """public static String getBnSuffix(int d) {
        if(d == 1) return "লা";
        if(d == 2 || d == 3) return "রা"; 
        if(d == 4) return "ঠা";
        if(d >= 5 && d <= 18) return "ই"; 
        return "শে";
    }"""
old_suffix_err = 'public static String getBnSuffix(int d) {\n        // ✨ ফিক্স: ৫ ই মার্চ এর "ই" বা "শে" মুছে ফেলা হলো!\n        return ""; \n    }'
w_res = update_file(widget_path, old_suffix_err, new_suffix)

if m_res: print("✅ MainActivity Fixed!")
if w_res: print("✅ SalahWidget Fixed!")
