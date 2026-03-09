import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# circleView এর মিসিং '};' ঠিক করা
code = re.sub(r'\}\s*circleView\.setOnTouchListener', '};\n        circleView.setOnTouchListener', code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Missing bracket and semicolon fixed!")
