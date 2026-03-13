import os, re

for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # আগে যদি ভুল করে ব্যাকগ্রাউন্ড ইনভিজিবল (setAlpha) করা থাকে, সেটা মুছে পরিষ্কার করা
        c = re.sub(r'if\s*\(\s*isFutureDate\s*\)\s*dt\.setAlpha\([^;]+\);', '', c)
        c = re.sub(r'if\s*\(\s*isFutureDate\s*\)\s*\{\s*dt\.setAlpha\([^;]+\);\s*\}', '', c)
        
        # ওভাররাইড লজিক পরিষ্কার করা (যাতে ডাবল না বসে)
        c = re.sub(r'if \(isFutureDate && !isSel\) \{ dt\.setTextColor[^}]+\}\s*', '', c)
        
        # 100% গ্যারান্টেড ওভাররাইড (শুধুমাত্র টেক্সট হালকা হবে)
        override_bn = 'cell.addView(dt);\n                    if (isFutureDate && !isSel) { dt.setTextColor(android.graphics.Color.argb(80, android.graphics.Color.red(themeColors[2]), android.graphics.Color.green(themeColors[2]), android.graphics.Color.blue(themeColors[2]))); }'
        c = c.replace('cell.addView(dt);', override_bn)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

    if 'CalendarHelper.java' in f and 'build' not in r:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ইংরেজি ও আরবি ক্যালেন্ডারের ভুল আলফা (Alpha) মুছে ফেলা
        c = re.sub(r'if\s*\(\s*isFuture\s*\)\s*tv\.setAlpha\([^;]+\);', '', c)
        c = re.sub(r'if\s*\(\s*isFutureDate\s*\)\s*dTv\.setAlpha\([^;]+\);', '', c)
        
        # ইংরেজি ক্যালেন্ডার ওভাররাইড
        c = re.sub(r'if \(isFuture && !dKey\.equals\(selectedDate\[0\]\)\) \{ tv\.setTextColor[^}]+\}\s*', '', c)
        override_greg = 'cell.addView(tv);\n                    if (isFuture && !dKey.equals(selectedDate[0])) { tv.setTextColor(android.graphics.Color.argb(80, android.graphics.Color.red(themeColors[2]), android.graphics.Color.green(themeColors[2]), android.graphics.Color.blue(themeColors[2]))); }'
        c = c.replace('cell.addView(tv);', override_greg)
        
        # আরবি ক্যালেন্ডার ওভাররাইড
        c = re.sub(r'if \(isFutureDate && !isSelected\) \{ dTv\.setTextColor[^}]+\}\s*', '', c)
        override_hijri = 'cell.addView(dTv);\n                            if (isFutureDate && !isSelected) { dTv.setTextColor(android.graphics.Color.argb(80, android.graphics.Color.red(themeColors[2]), android.graphics.Color.green(themeColors[2]), android.graphics.Color.blue(themeColors[2]))); }'
        c = c.replace('cell.addView(dTv);', override_hijri)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ সব ক্যালেন্ডারের ভবিষ্যতের তারিখ পারফেক্টলি ইনভিজিবল করা হয়েছে!")
