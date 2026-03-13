import os
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        # বঙ্গাব্দ যুক্ত করা
        c = c.replace('return dayStr + suf + " " + bMs[bM] + ", " + yearStr;', 'return dayStr + suf + " " + bMs[bM] + ", " + yearStr + (isBn ? " বঙ্গাব্দ" : " BS");')
        # বাংলা ক্যালেন্ডার বোল্ড করা
        c = c.replace('dt.setTypeface(android.graphics.Typeface.DEFAULT);', 'dt.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);')
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

    if 'CalendarHelper.java' in f and 'build' not in r:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        # ইংরেজি ক্যালেন্ডার বোল্ড করা
        c = c.replace('dt.setTypeface(Typeface.DEFAULT);', 'dt.setTypeface(Typeface.DEFAULT_BOLD);')
        c = c.replace('dTv.setTypeface(Typeface.DEFAULT);', 'dTv.setTypeface(Typeface.DEFAULT_BOLD);')
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ২. 'বঙ্গাব্দ' যুক্ত করা হয়েছে এবং ক্যালেন্ডারের সংখ্যা বোল্ড করা হয়েছে!")
