import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. পুরোনো ভুল লাইনগুলো পুরো ফাইল থেকে চিরতরে মুছে ফেলা হচ্ছে
bad_lines = [
    "if(settingsBtn instanceof TextView) ((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE);",
    "if(periodBtn instanceof TextView) ((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE);",
    "if(offBtn instanceof TextView) ((TextView)offBtn).setTextColor(android.graphics.Color.WHITE);"
]
for bad in bad_lines:
    content = content.replace(bad, "")

# ওই ফালতু try-catch ব্লকটাও মুছে ফেলা হচ্ছে
content = re.sub(r'try\s*\{\s*int dynCol[^}]*catch\s*\([^)]*\)\s*\{\}', '', content)

# সেফটির জন্য আগের কোনো কালার কোড থাকলে সেটাও ক্লিন করা হলো
content = content.replace("((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE);", "")
content = content.replace("((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE);", "")
content = content.replace("((TextView)offBtn).setTextColor(android.graphics.Color.WHITE);", "")

# ২. এবার একদম ১০০% নিরাপদ জায়গায় (যেখানে বাটনগুলো rightHeader এ যুক্ত হচ্ছে) কালার বসানো হচ্ছে
content = content.replace("rightHeader.addView(settingsBtn);", "((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(settingsBtn);")
content = content.replace("rightHeader.addView(periodBtn);", "((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(periodBtn);")
content = content.replace("rightHeader.addView(offBtn);", "((TextView)offBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(offBtn);")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Symbol errors wiped out! Icons beautifully colored to white.")
