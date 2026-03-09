fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# টাচ লজিক ক্যালকুলেশন ফিক্স (ক্যানভাস ক্যালকুলেশন)
code = code.replace('float circleY = btnY + (h * 0.18f);', 'float circleY = iconY + (h * 0.16f);')
code = code.replace('float totalBoxY = beadY + (h * 0.10f);', 'float totalLineY = beadY - (h * 0.04f);')
code = code.replace('float totalLineY = beadY + (h * 0.10f);', 'float totalLineY = beadY - (h * 0.04f);')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Part 2: Positions successfully adjusted!")
