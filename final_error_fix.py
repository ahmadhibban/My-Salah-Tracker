import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if not os.path.exists(mf):
    for r, d, f in os.walk("."):
        if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ১. getUltra3D এর মিসিং প্যারামিটার (radius) ফিক্স করা
mc = re.sub(r'getUltra3D\((.*?), (.*?), 3f\)\); streakBadge', r'getUltra3D(\1, \2, 20f*DENSITY, 3f)); streakBadge', mc)
mc = re.sub(r'getUltra3D\((.*?), (.*?), isSel \? 0f : 3f\)\); t\.setPadding', r'getUltra3D(\1, \2, 8f*DENSITY, isSel ? 0f : 3f)); t.setPadding', mc)
mc = re.sub(r'getUltra3D\((.*?), (.*?), 5f\)\); markAllBtn', r'getUltra3D(\1, \2, 12f*DENSITY, 5f)); markAllBtn', mc)
mc = re.sub(r'getUltra3D\((.*?), (.*?), 5f\)\); todayBtn', r'getUltra3D(\1, \2, 12f*DENSITY, 5f)); todayBtn', mc)
mc = re.sub(r'getUltra3D\(cM, (.*?), 6f\)\); card', r'getUltra3D(cM, \1, 14f*DENSITY, 6f)); card', mc)

# ২. ডুপ্লিকেট tSur এবং tShd ফিক্স করা
s_dup = r'int\s+tSur\s*=\s*isDayTime\s*\?\s*android\.graphics\.Color\.parseColor\("#FF9500"\)\s*:\s*android\.graphics\.Color\.parseColor\("#1A2980"\);\s*int\s+tShd\s*=\s*isDayTime\s*\?\s*android\.graphics\.Color\.parseColor\("#C77600"\)\s*:\s*android\.graphics\.Color\.parseColor\("#0F184A"\);'
mc = re.sub(f'({s_dup})(.*?)({s_dup})', r'\1\2', mc, flags=re.DOTALL)

# ৩. accShd স্কোপ ফিক্স (sunnahBtn এর জন্য)
mc = mc.replace('int sShd = doneSunnahs > 0 ? accShd :', 'int _rX = android.graphics.Color.red(colorAccent); int _gX = android.graphics.Color.green(colorAccent); int _bX = android.graphics.Color.blue(colorAccent); int accShdTemp = isDarkTheme ? android.graphics.Color.rgb((int)(_rX*0.4f), (int)(_gX*0.4f), (int)(_bX*0.4f)) : android.graphics.Color.argb(100, _rX, _gX, _bX); int sShd = doneSunnahs > 0 ? accShdTemp :')

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)
print("✔ COMPILATION ERRORS FIXED! Ready to Build.")
