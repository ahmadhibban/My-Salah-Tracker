import os, re

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if not os.path.exists(mf):
    for r, d, f in os.walk("."):
        if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")

with open(mf, 'r', encoding='utf-8') as f: mc = f.read()

# ডুপ্লিকেট pmTheme ফিক্স
s1 = r'int\s+pmTheme\s*=\s*isDarkTheme\s*\?\s*android\.graphics\.Color\.parseColor\("#1A2980"\)\s*:\s*android\.graphics\.Color\.parseColor\("#FF9500"\);'
mc = re.sub(f'({s1})(.*?)({s1})', r'\1\2', mc, flags=re.DOTALL)

# ডুপ্লিকেট pm ফিক্স
s2 = r'int\s+pm\s*=\s*isDayTime\s*\?\s*android\.graphics\.Color\.parseColor\("#FF9500"\)\s*:\s*android\.graphics\.Color\.parseColor\("#1A2980"\);'
mc = re.sub(f'({s2})(.*?)({s2})', r'\1\2', mc, flags=re.DOTALL)

# ডুপ্লিকেট cM ফিক্স
s3 = r'int\s+cM\s*=\s*stat\.equals\("excused"\)\s*\?\s*\(isDarkTheme\s*\?\s*android\.graphics\.Color\.parseColor\("#1A1115"\)\s*:\s*android\.graphics\.Color\.parseColor\("#FCE4EC"\)\)\s*:\s*themeColors\[1\];'
mc = re.sub(f'({s3})(.*?)({s3})', r'\1\2', mc, flags=re.DOTALL)

with open(mf, 'w', encoding='utf-8') as f: f.write(mc)
print("✔ Duplicate Variables Fixed Successfully!")
