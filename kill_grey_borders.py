import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# মেইন কালপ্রিট: themeColors[4] (ছাই রঙের বর্ডার)!
# এটিকে পাল্টে নিচের কার্ডের মতো একদম TRANSPARENT (স্বচ্ছ) করে দেওয়া হচ্ছে।
content = re.sub(r'setStroke\(\(int\)\(1f\s*\*\s*DENSITY\),\s*themeColors\[4\]\)', 'setStroke((int)(1f*DENSITY), android.graphics.Color.TRANSPARENT)', content)

# অ্যারো বাটনগুলোর জন্য এক্সট্রা সেফটি
content = re.sub(r'navBg2\.setStroke\([^;]+\);', 'navBg2.setStroke((int)(1f*DENSITY), android.graphics.Color.TRANSPARENT);', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Grey borders KILLED! Top elements now flawlessly match the 3D cards.")
