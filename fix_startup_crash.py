import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ক্র্যাশ করা ফোরগ্রাউন্ড লাইনটি খুঁজে মুছে ফেলা হচ্ছে
buggy_pattern = r'if\s*\(android\.os\.Build\.VERSION\.SDK_INT\s*>=\s*23\)\s*card\.setForeground\([^;]+\);'
new_content = re.sub(buggy_pattern, '/* Foreground ripple removed to fix startup crash */', content)

if new_content != content:
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Startup CRASH fixed! The invalid drawable line has been permanently removed.")
else:
    print("Could not find the buggy line. Maybe it's already removed?")
