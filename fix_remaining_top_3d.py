import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. পুরোনো সাধারণ ব্যাকগ্রাউন্ডকে ৩ডি ব্যাকগ্রাউন্ডে রূপান্তর করা হচ্ছে
content = content.replace('dateBtn.setBackground(bg1);', 'dateBtn.setBackground(get3DDrawable(bg1, 16f, false));')
content = content.replace('viewToggle.setBackground(bg2);', 'viewToggle.setBackground(get3DDrawable(bg2, 16f, false));')

# ২. পুরোনো ভুল প্যাডিংগুলো মুছে ফেলা হচ্ছে
content = re.sub(r'dateBtn\.setPadding\([^;]+\);', '', content)
content = re.sub(r'viewToggle\.setPadding\([^;]+\);', '', content)

# ৩. ৩ডি শ্যাডোর (৩.৫ পিক্সেল) সাথে ব্যালেন্স করে টেক্সট একদম মাঝখানে রাখার জন্য নতুন প্যাডিং
content = re.sub(r'(dateBtn\.setBackground\([^;]+\);)', r'\1 dateBtn.setPadding((int)(16*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY), (int)(11.5f*DENSITY));', content)
content = re.sub(r'(viewToggle\.setBackground\([^;]+\);)', r'\1 viewToggle.setPadding((int)(12*DENSITY), (int)(8*DENSITY), (int)(12*DENSITY), (int)(11.5f*DENSITY));', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Remaining top boxes (Date & View Toggle) are now PERFECTLY 3D!")
