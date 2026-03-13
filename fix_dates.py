import os, re
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        c = re.sub(r'dEn\.setTextSize\(\s*\d+\s*\);', 'dEn.setTextSize(14);', c)
        c = re.sub(r'dBn\.setTextSize\(\s*\d+\s*\);', 'dBn.setTextSize(14);', c)
        c = re.sub(r'dHijri\.setTextSize\(\s*\d+\s*\);', 'dHijri.setTextSize(14);', c)
        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ১. সব তারিখের সাইজ সমান করা হয়েছে!")
        break
