import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. Streak Badge-কে পুরোনো ইঞ্জিন থেকে নতুন Pro ইঞ্জিনে আপডেট করা হচ্ছে
content = re.sub(
    r'applyCssToView\(\s*streakBadge\s*,\s*[^,]+,\s*[^,]+,\s*[^,]+,\s*[^)]+\);', 
    r'setProStyle(streakBadge, colorAccent, accShadow, 16f, false, 0, 0, 8);', 
    content
)

# ২. ডুপ্লিকেট ভ্যারিয়েবল (hsv) এর নাম পাল্টে (proHsv) করে দেওয়া হচ্ছে, যাতে কোনো ক্ল্যাশ না হয়
content = content.replace(
    "float[] hsv = new float[3]; android.graphics.Color.colorToHSV(colorAccent, hsv); hsv[2] *= 0.70f;",
    "float[] proHsv = new float[3]; android.graphics.Color.colorToHSV(colorAccent, proHsv); proHsv[2] *= 0.70f;"
)
content = content.replace(
    "int accShadow = android.graphics.Color.HSVToColor(hsv);",
    "int accShadow = android.graphics.Color.HSVToColor(proHsv);"
)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Build Errors FIXED! Badge updated and variable clash resolved.")
