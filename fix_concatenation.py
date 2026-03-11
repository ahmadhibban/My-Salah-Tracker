import os

mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
backup = "all_code.txt"

for r, d, f in os.walk("."):
    if "all_code.txt" in f:
        backup = os.path.join(r, "all_code.txt")
        break

with open(backup, 'r', encoding='utf-8') as f:
    raw = f.read()

# জোড়া লাগা কোডকে আলাদা করার ট্রিক
raw = raw.replace("}package", "}\npackage")
parts = raw.split("package com.my.salah.tracker.app;")

main_code = ""
ui_code = ""

for p in parts:
    if "class MainActivity" in p:
        main_code = "package com.my.salah.tracker.app;" + p
    elif "class UIComponents" in p:
        ui_code = "package com.my.salah.tracker.app;" + p

# ফাইল দুটোকে যার যার জায়গায় আলাদাভাবে সেভ করা
if main_code:
    with open(mf, 'w', encoding='utf-8') as f: f.write(main_code)
if ui_code:
    with open(uf, 'w', encoding='utf-8') as f: f.write(ui_code)

print("✔ FILES SEPARATED PERFECTLY! Ready to Build.")
