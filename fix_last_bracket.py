import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# '};' কে '});' দিয়ে রিপ্লেস করা হচ্ছে
old_text = "        };\n\n        LinearLayout root"
new_text = "        });\n\n        LinearLayout root"

code = code.replace(old_text, new_text)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Missing ')' has been fixed perfectly!")
