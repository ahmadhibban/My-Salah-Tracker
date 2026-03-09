import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file: c = file.read()

# 1. Update Languages
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
try:
    with open(le, 'r', encoding='utf-8') as l_file: lc = l_file.read()
    if '"Round"' not in lc:
        lc = lc.replace('bnMap.put("Reset", "রিসেট");', 'bnMap.put("Reset", "রিসেট"); bnMap.put("Round", "রাউন্ড");')
        open(le, 'w', encoding='utf-8').write(lc)
except: pass

# 2. Add beadTheme to ZikrManager
old_z = r'boolean soundOn = true; android\.media\.ToneGenerator toneGen; android\.content\.SharedPreferences prefs;'
new_z = r'boolean soundOn = true; int beadTheme = 0; android.media.ToneGenerator toneGen; android.content.SharedPreferences prefs;'
c = re.sub(old_z, new_z, c)

old_init = r'soundOn = prefs\.getBoolean\("sound_on", true\);'
new_init = r'soundOn = prefs.getBoolean("sound_on", true); beadTheme = prefs.getInt("bead_theme", 0);'
c = re.sub(old_init, new_init, c)

old_save = r'putBoolean\("sound_on", soundOn\)\.apply\(\);'
new_save = r'putBoolean("sound_on", soundOn).putInt("bead_theme", beadTheme).apply();'
c = re.sub(old_save, new_save, c)

with open(f, 'w', encoding='utf-8') as file: file.write(c)
print("✅ Part 1: Zikr Memory & Language Updated!")
