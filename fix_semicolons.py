import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# যেখানে সেমিকোলন (;) মুছে গেছে, সেখানে অটোমেটিকভাবে সেমিকোলন বসিয়ে দেওয়া হচ্ছে
content = re.sub(r'([^\s;{}])(\s+GradientDrawable\s+gd\s*=)', r'\1;\2', content)
content = re.sub(r'([^\s;{}])(\s+Calendar\s+cal\s*=)', r'\1;\2', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Semicolon errors fixed perfectly!")
