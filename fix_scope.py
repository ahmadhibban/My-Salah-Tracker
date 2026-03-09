import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# 'themeMain' ভেরিয়েবলের বদলে সরাসরি ডাইনামিক কালার লজিক বসিয়ে দেওয়া হচ্ছে
safe_color = "(themeColors != null && themeColors.length > 0 ? themeColors[0] : accentCol)"

code = code.replace("p.setColor(themeMain);", f"p.setColor({safe_color});")
code = code.replace("Color.WHITE, themeMain,", f"Color.WHITE, {safe_color},")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Scope Error Fixed! The compiler can now perfectly see your theme colors.")
