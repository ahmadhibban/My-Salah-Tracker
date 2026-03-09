import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# Fix the missing parenthesis ')' for setOnTouchListener
code = re.sub(r'\}\s*;\s*LinearLayout root = new LinearLayout\(ctx\);', r'});\n\n        LinearLayout root = new LinearLayout(ctx);', code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Missing ')' error fixed!")
