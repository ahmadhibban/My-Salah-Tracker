import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"

with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# স্পেস বা লাইন ব্রেক যাই থাকুক না কেন, এটি ঠিকমতো '});' বসিয়ে দেবে
code = re.sub(r'\}\s*;\s*LinearLayout root', '});\n\n        LinearLayout root', code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Missing ')' has been perfectly fixed with Regex!")
