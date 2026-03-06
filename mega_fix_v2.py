import os

def fix_file(path, old, new):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old in content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.replace(old, new))
            return True
    return False

# ১. ১০০ বছরের সীমা (MainActivity.java)
m_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
old_p = 'selectedCalArr[0].add(Calendar.DATE, -7);'
new_p = 'Calendar cL = (Calendar) selectedCalArr[0].clone(); cL.add(Calendar.DATE, -7); if(cL.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { selectedCalArr[0].add(Calendar.DATE, -7); }'
fix_file(m_path, old_p, new_p)

# ২. ক্যালেন্ডার হাইলাইট ও ফন্ট (CalendarHelper.java)
c_path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
# হাইলাইট লজিক আপডেট
old_h = 'tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : ui.getRainbowBorder(dKey, 3)));'
new_h = """SalahRecord dR = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey);
                    boolean isD = (dR != null && dR.fajr.equals("yes") && dR.dhuhr.equals("yes") && dR.asr.equals("yes") && dR.maghrib.equals("yes") && dR.isha.equals("yes"));
                    if(isD && !isFuture) { bgD.setColor(colorAccent & 0x30FFFFFF); tv.setBackground(bgD); }
                    else { tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : ui.getRainbowBorder(dKey, 3))); }"""
fix_file(c_path, old_h, new_h)

print("✅ All Target Fixes Applied!")
