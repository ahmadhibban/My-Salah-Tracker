import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'CalendarHelper.java' in f:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ফাঁকা থাকলে বর্ডার (Background) রিমুভ করা
        c = re.sub(r'bgD\.setColor\(\s*(?:android\.graphics\.)?Color\.TRANSPARENT\s*\);\s*tv\.setBackground\(bgD\);', r'tv.setBackground(null);', c)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ইংরেজি ক্যালেন্ডারের বর্ডার পারফেক্টলি রিমুভ করা হয়েছে!")
