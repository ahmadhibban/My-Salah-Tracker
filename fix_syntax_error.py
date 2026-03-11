import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ভুল করে থেকে যাওয়া লেজটুকু কেটে ঠিক করে দেওয়া হচ্ছে
mc = re.sub(r'(ui\.getRoundImage\([^,]+,\s*6,\s*android\.graphics\.Color\.TRANSPARENT,\s*colorAccent\))\s*:[^;]+;', r'\1;', mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✅ Syntax Error (Extra Tail) Fixed Perfectly!")
