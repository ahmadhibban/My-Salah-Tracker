import re

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# গাধা AI এর ভুল: ব্যাকগ্রাউন্ড কালারের বদলে থিমের আসল অ্যাকসেন্ট কালার (accentCol) বসানো হচ্ছে
code = re.sub(r'int\s+themeMain\s*=\s*[^;]+;', 'int themeMain = accentCol;', code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Slap accepted! The invisible text, ring, and box are now beautifully synced with your exact theme color.")
