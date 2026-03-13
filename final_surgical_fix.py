import os, re

for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ১. শুধুমাত্র Mark All এবং Today কার্ডের উচ্চতা সমান করা (-2 থেকে -1)
        c = re.sub(r'(LayoutParams\s*markLp\s*=\s*new\s*(?:android\.widget\.)?LinearLayout\.LayoutParams\(\s*0\s*,\s*)-2(\s*,\s*1[fF]\s*\);)', r'\g<1>-1\g<2>', c)
        c = re.sub(r'(LayoutParams\s*todayLp\s*=\s*new\s*(?:android\.widget\.)?LinearLayout\.LayoutParams\(\s*0\s*,\s*)-2(\s*,\s*1[fF]\s*\);)', r'\g<1>-1\g<2>', c)
        
        # ২. নামাজের নাম ও সেটিংসের পপ-আপ বোল্ড করা
        c = re.sub(r'tv\.setTypeface\([^;]+\);', '', c)
        c = re.sub(r'sTv\.setTypeface\([^;]+\);', '', c)
        c = c.replace('tv.setTextSize(16);', 'tv.setTextSize(16); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);')
        c = c.replace('sTv.setTextSize(16);', 'sTv.setTextSize(16); sTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);')
        
        # ৩. বাংলা ক্যালেন্ডারের ভবিষ্যতের তারিখের লেখা হালকা করা (ব্যাকগ্রাউন্ড অক্ষত থাকবে)
        c = re.sub(r'if\s*\(\s*isFutureDate\s*\)\s*dt\.setAlpha\([^;]+\);', '', c)
        c = re.sub(r'if\(isFutureDate\s*&&\s*!isSel\)\s*\{\s*dt\.[^}]+\}\s*', '', c)
        c = c.replace('cell.addView(dt);', 'if(isFutureDate && !isSel) { dt.setTextColor(themeColors[2]); dt.setAlpha(0.4f); }\n                    cell.addView(dt);')

        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ১. মেইন পেজ, কার্ড, বোল্ড ফন্ট এবং বাংলা ক্যালেন্ডার ফিক্সড!")

    if 'CalendarHelper.java' in f and 'build' not in r:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ৪. ইংরেজি ও আরবি ক্যালেন্ডারের ভবিষ্যতের তারিখ হালকা করা
        c = re.sub(r'if\s*\(\s*isFuture\s*\)\s*tv\.setAlpha\([^;]+\);', '', c)
        c = re.sub(r'if\s*\(\s*isFutureDate\s*\)\s*dTv\.setAlpha\([^;]+\);', '', c)
        c = re.sub(r'if\(isFuture\)\s*\{\s*tv\.[^}]+\}\s*', '', c)
        c = re.sub(r'if\(isFutureDate\)\s*\{\s*dTv\.[^}]+\}\s*', '', c)
        
        c = c.replace('cell.addView(tv);', 'if(isFuture) { tv.setTextColor(themeColors[2]); tv.setAlpha(0.4f); }\n                    cell.addView(tv);')
        c = c.replace('cell.addView(dTv);', 'if(isFutureDate) { dTv.setTextColor(themeColors[2]); dTv.setAlpha(0.4f); }\n                            cell.addView(dTv);')

        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ২. ইংরেজি ও আরবি ক্যালেন্ডারের তারিখ ফিক্সড!")

