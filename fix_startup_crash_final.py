import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# জোর করে টেক্সট বানানোর ফালতু কোড পাল্টে, সেফটি চেক (instanceof) ফিরিয়ে আনা হচ্ছে
bad_set = "((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(settingsBtn);"
safe_set = "if(settingsBtn instanceof TextView) ((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(settingsBtn);"
content = content.replace(bad_set, safe_set)

bad_per = "((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(periodBtn);"
safe_per = "if(periodBtn instanceof TextView) ((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(periodBtn);"
content = content.replace(bad_per, safe_per)

bad_off = "((TextView)offBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(offBtn);"
safe_off = "if(offBtn instanceof TextView) ((TextView)offBtn).setTextColor(android.graphics.Color.WHITE); rightHeader.addView(offBtn);"
content = content.replace(bad_off, safe_off)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Crash FIXED! Safe type checking restored for top icons.")
