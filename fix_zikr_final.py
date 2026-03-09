import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# onTouch মেথডের ভেতরে sideMargin ভেরিয়েবলটি ইনজেক্ট করা
if 'public boolean onTouch(final View v, MotionEvent event) {' in code:
    old_line = 'float x = event.getX(), y = event.getY(), w = v.getWidth(), h = v.getHeight(), centerX = w / 2.0f;'
    new_line = old_line + ' float sideMargin = 100f;'
    
    if 'float sideMargin = 100f;' not in code.split('public boolean onTouch')[1].split('if (event.getAction()')[0]:
        code = code.replace(old_line, new_line)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: 'sideMargin' variable scope error fixed!")
