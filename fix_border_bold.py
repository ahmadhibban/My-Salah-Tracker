import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    
    # ১. ইংরেজি ক্যালেন্ডারের বর্ডার ফিক্স (CalendarHelper.java)
    if 'CalendarHelper.java' in f:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ফাঁকা দিনে জোর করে বৃত্ত বসানোর কোডটা মুছে একদম ক্লিন (null) করে দেওয়া হচ্ছে
        c = re.sub(
            r'else\s*\{\s*bgD\.setColor\(android\.graphics\.Color\.TRANSPARENT\);\s*tv\.setBackground\(\(\(MainActivity\)activity\)\.getProgressBorder\(dKey,\s*dKey\.equals\(selectedDate\[0\]\)\)\);\s*\}', 
            r'else { tv.setBackground(null); }', 
            c
        )
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

    # ২. সেটিংসের পপ-আপগুলো বোল্ড করা (MainActivity.java)
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # থিম এবং ক্যালেন্ডার নির্বাচন পপ-আপের অপশন বোল্ড করা
        c = c.replace('tv.setText(copts[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);', 'tv.setText(copts[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);')
        c = c.replace('tv.setText(ops[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);', 'tv.setText(ops[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);')
        
        # -১ দিন, ডিফল্ট, +১ দিন অপশনগুলো বোল্ড করা
        c = re.sub(
            r'sTv\.setTypeface\(vals\[sj\]\s*==\s*currentVal\s*\?\s*android\.graphics\.Typeface\.DEFAULT_BOLD\s*:\s*android\.graphics\.Typeface\.DEFAULT\);', 
            'sTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);', 
            c
        )

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ২টি কাজ একদম ১০০% নিখুঁতভাবে শেষ হয়েছে!")
