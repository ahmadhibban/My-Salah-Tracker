import re
path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f: mc = f.read()

# আমার আগের পণ্ডিতি করে বসানো ভুল কোডগুলো সমূলে মুছে ফেলা হচ্ছে
mc = re.sub(r'// Safe Text Color Fixer.*?\}\);', '', mc, flags=re.DOTALL)
mc = re.sub(r'getWindow\(\)\.getDecorView\(\)\.post\(\(\)\s*->\s*\{\s*try\s*\{[^}]*java\.util\.Stack<android\.view\.View> stack = new java\.util\.Stack<>\(\);[\s\S]*?catch\s*\(Exception e\)\s*\{\}\s*\}\);', '', mc)

with open(path, "w", encoding="utf-8") as f: f.write(mc)
print("✅ ৩. সাদা হয়ে যাওয়া লেখার সমস্যা দূর করা হয়েছে!")
