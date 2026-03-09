import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# sideMargin ভেরিয়েবলটি onTouch এর ভেতরেও ডিফাইন করে দেওয়া
old_line = 'float btnSp = w / 3;'
new_line = 'float btnSp = w / 3; float sideMargin = 100f;'

if old_line in code and 'float sideMargin = 100f;' not in code.split('public boolean onTouch')[1]:
    # শুধুমাত্র onTouch মেথডের ভেতরের অংশটুকুতে পরিবর্তন করা
    parts = code.split('public boolean onTouch')
    parts[1] = parts[1].replace(old_line, new_line)
    code = 'public boolean onTouch'.join(parts)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: 'sideMargin' variable error fixed!")
