import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. ভুল জায়গায় থাকা সেই কালপ্রিট কোড ব্লকটি পুরোপুরি মুছে ফেলা হচ্ছে
content = re.sub(r'try\s*\{[^}]*dynCol[^}]*catch\s*\(Exception e\)\s*\{\}', '', content)

# ২. থিম বাটনের কালার সেফ জায়গায় বসানো হচ্ছে
content = re.sub(r'(applyCssToView\(\s*themeToggleBtn[^;]+;)', r'\1 if(themeToggleBtn instanceof TextView) ((TextView)themeToggleBtn).setTextColor(isDarkTheme ? android.graphics.Color.parseColor("#1E88E5") : android.graphics.Color.parseColor("#F59E0B"));', content)

# ৩. সেটিং, পিরিয়ড এবং অফলাইন বাটনের কালার একদম পারফেক্ট জায়গায় (যেখানে বাটনগুলো ১০০% তৈরি হয়ে গেছে) বসানো হচ্ছে
content = re.sub(r'(rightHeader\.addView\(settingsBtn\);)', r'if(settingsBtn instanceof TextView) ((TextView)settingsBtn).setTextColor(android.graphics.Color.WHITE); \1', content)
content = re.sub(r'(rightHeader\.addView\(periodBtn\);)', r'if(periodBtn instanceof TextView) ((TextView)periodBtn).setTextColor(android.graphics.Color.WHITE); \1', content)
content = re.sub(r'(rightHeader\.addView\(offBtn\);)', r'if(offBtn instanceof TextView) ((TextView)offBtn).setTextColor(android.graphics.Color.WHITE); \1', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Scope Errors FIXED! Button colors applied safely.")
