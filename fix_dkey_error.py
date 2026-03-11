import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# mainLayout-এর ভুল কোডটি সরিয়ে তার আসল কোড (gd) বসিয়ে দেওয়া হচ্ছে
bad_code = "mainLayout.setBackground(getUltimate3DBorder(getProgressBorder(dKey, isSel), 0, true, colorAccent));"
fixed_code = "mainLayout.setBackground(gd);"

content = content.replace(bad_code, fixed_code)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Variable scope error fixed perfectly!")
