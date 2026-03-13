import os
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        c = c.replace('yearChip.setText(yrStr + (isBn ? " বঙ্গাব্দ ▼" : " BS ▼"));', 'yearChip.setText(yrStr);')
        c = c.replace('yearChip.setText(yrStr + (isBn ? " বঙ্গাব্দ" : " BS"));', 'yearChip.setText(yrStr);')
        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ২. সালের পাশের অতিরিক্ত লেখা মুছে ফেলা হয়েছে!")
        break
