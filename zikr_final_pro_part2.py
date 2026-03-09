import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# টাচ পজিশন আপডেট (আইকন এবং ড্র্যাগিং এরিয়া)
code = re.sub(r'float btnY = \(h \* 0\.03f\) \+ boxHeight \+ \(h \* 0\.08f\);', 'float iconY = (h * 0.03f) + boxHeight + (h * 0.08f);', code)
code = re.sub(r'float circleY = btnY \+ \(h \* 0\.18f\);', 'float circleY = iconY + (h * 0.15f);', code)
code = re.sub(r'float totalLineY = circleY \+ radius \+ \(h \* 0\.05f\);', 'float totalLineY = circleY + radius + (h * 0.05f);', code)
code = re.sub(r'float beadY = circleY \+ radius \+ \(h \* 0\.09f\);', 'float beadY = totalLineY + (h * 0.08f);', code)

# আইকন টাচ এরিয়া ফিক্স
old_touch = 'if (Math.abs(y - btnY) < 100) {.*?if (Math.abs(x - btnSp \* 1) < 90)'
new_touch = 'if (Math.abs(y - iconY) < 100) {\n                        if (Math.abs(x - sideMargin) < 90)'
code = re.sub(old_touch, new_touch, code, flags=re.DOTALL)
code = code.replace('else if (Math.abs(x - btnSp * 2) < 90)', 'else if (Math.abs(x - (w - sideMargin)) < 90)')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Part 2: Touch positions fixed!")
