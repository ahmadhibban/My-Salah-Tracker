import re
fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# পজিশনগুলো নিচে নামানোর জন্য ভ্যালু পরিবর্তন
code = code.replace('float boxTop = h * 0.03f;', 'float boxTop = h * 0.05f;')
code = code.replace('float circleY = btnY + (h * 0.18f);', 'float circleY = btnY + (h * 0.22f);')
code = code.replace('float beadY = circleY + radius + (h * 0.09f);', 'float beadY = circleY + radius + (h * 0.12f);')
code = code.replace('float totalBoxY = beadY + (h * 0.07f);', 'float totalBoxY = beadY + (h * 0.10f);')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Success: Positions adjusted for part 1!")
