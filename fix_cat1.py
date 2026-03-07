import os, re

# 1. LanguageEngine: Better translations and offline count
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
if os.path.exists(le):
    c = open(le).read()
    c = c.replace('bnMap.put("Network Error", "নেটওয়ার্ক এরর");', 'bnMap.put("Network Error", "ইন্টারনেট কানেকশন নেই");')
    if '"items waiting to sync."' not in c:
        c = c.replace('bnMap.put("Delete", "মুছে ফেলুন");', 'bnMap.put("Delete", "মুছে ফেলুন");\n        bnMap.put("items waiting to sync.", "টি ডেটা সিঙ্কের অপেক্ষায় আছে।");')
    open(le, 'w').write(c)

# 2. MainActivity: Animations, Offline Count, Success Sequence Once
ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
if os.path.exists(ma):
    c = open(ma).read()
    
    # Offline count logic
    old_off = 'ui.showSmartBanner(root, lang.get("Offline Data"), lang.get("Data will sync when internet is available."), "img_offline_warning", colorAccent, null);'
    new_off = 'String[] items = sp.getString("offline_q", "").split(","); int count = 0; for(String it : items) if(!it.trim().isEmpty()) count++; ui.showSmartBanner(root, lang.get("Offline Data"), count + " " + lang.get("items waiting to sync."), "img_offline_warning", colorAccent, null);'
    c = c.replace(old_off, new_off)

    # Fade-in animation for cards
    if 'cardsContainer.setAlpha(0f)' not in c:
        c = c.replace('contentArea.addView(cardsContainer);', 'cardsContainer.setAlpha(0f); cardsContainer.animate().alpha(1f).setDuration(400).start(); contentArea.addView(cardsContainer);')

    # Success sequence once a day
    old_seq = 'private void showSuccessSequence() {'
    new_seq = 'private void showSuccessSequence() {\n        if(sp.getBoolean(selectedDate[0] + "_success_shown", false)) return;\n        sp.edit().putBoolean(selectedDate[0] + "_success_shown", true).apply();'
    if '_success_shown' not in c:
        c = c.replace(old_seq, new_seq)

    open(ma, 'w').write(c)

# 3. StatsHelper: RAM Optimization (RGB_565)
sh = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(sh):
    c = open(sh).read()
    c = c.replace('android.graphics.Bitmap.Config.ARGB_8888', 'android.graphics.Bitmap.Config.RGB_565')
    open(sh, 'w').write(c)

# 4. CalendarHelper: Fat Finger Fix (Increase Touch Target)
ch = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
if os.path.exists(ch):
    c = open(ch).read()
    c = re.sub(r'tv\.setPadding\(\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\)\);', r'tv.setPadding((int)(2*DENSITY), (int)(18*DENSITY), (int)(2*DENSITY), (int)(18*DENSITY));', c)
    c = re.sub(r'dTv\.setPadding\(\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\)\);', r'dTv.setPadding((int)(2*DENSITY), (int)(18*DENSITY), (int)(2*DENSITY), (int)(18*DENSITY));', c)
    open(ch, 'w').write(c)

print("✅ Category 1 UI/UX Updates Applied Successfully! YOU CAN BUILD NOW.")
