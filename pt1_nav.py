import os, re
# 1. Language Engine
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
c = open(le).read()
if '"Habits"' not in c:
    c = c.replace('bnMap.put("Settings & Options", "সেটিংস এবং অপশন");', 'bnMap.put("Settings & Options", "সেটিংস এবং অপশন");\n        bnMap.put("Salah", "নামাজ"); bnMap.put("Stats", "রিপোর্ট"); bnMap.put("Habits", "আমল"); bnMap.put("Daily Habits", "দৈনিক আমল"); bnMap.put("Fasting (Roza)", "রোজা"); bnMap.put("Quran Recitation", "কুরআন তিলাওয়াত"); bnMap.put("Daily Zikr", "জিকির ও তাসবীহ"); bnMap.put("Ayat of the Day", "আজকের আয়াত"); bnMap.put("Pages/Surah", "পৃষ্ঠা বা সূরা"); bnMap.put("Not Fasting", "রাখিনি"); bnMap.put("Fard", "ফরজ"); bnMap.put("Nafl", "নফল"); bnMap.put("Qaza", "কাজা"); bnMap.put("Reset", "রিসেট");')
    open(le, 'w').write(c)

# 2. MainActivity Settings Menu Fix (Remove Stats)
ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()
c = re.sub(r'mr\.addImg\("Advanced Statistics".*?\n', '', c)

# 3. Add Global Variables for Tabs
v_old = 'private android.widget.LinearLayout contentArea;'
v_new = 'private android.widget.LinearLayout contentArea;\n    private android.widget.FrameLayout fragmentContainer;\n    private android.widget.LinearLayout bottomNav;\n    private int currentTab = 0;'
if 'fragmentContainer' not in c: c = c.replace(v_old, v_new)

open(ma, 'w').write(c)
print("✅ Part 1 Done! Variables and Languages ready.")
