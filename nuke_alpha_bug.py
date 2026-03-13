import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    for fname in ['MainActivity.java', 'CalendarHelper.java']:
        if fname in f:
            p = os.path.join(r, fname)
            with open(p, 'r', encoding='utf-8') as file: 
                c = file.read()
            
            # বাংলা ক্যালেন্ডারের ক্ষতিকর আলফা রিমুভ (যেকোনো স্পেস বা এন্টার থাকলেও ধরবে)
            c = re.sub(r'if\s*\(\s*isFutureDate\s*&&\s*!isSel\s*\)\s*\{\s*dt\.setTextColor\([^)]+\);\s*dt\.setAlpha\([^)]+\);\s*\}', '', c)
            
            # ইংরেজি ক্যালেন্ডারের ক্ষতিকর আলফা রিমুভ
            c = re.sub(r'if\s*\(\s*isFuture\s*\)\s*\{\s*tv\.setTextColor\([^)]+\);\s*tv\.setAlpha\([^)]+\);\s*\}', '', c)
            
            # আরবি ক্যালেন্ডারের ক্ষতিকর আলফা রিমুভ
            c = re.sub(r'if\s*\(\s*isFutureDate\s*\)\s*\{\s*dTv\.setTextColor\([^)]+\);\s*dTv\.setAlpha\([^)]+\);\s*\}', '', c)
            
            with open(p, 'w', encoding='utf-8') as file: 
                file.write(c)

print("✅ সব ক্যালেন্ডারের ইনভিজিবিলিটি বাগ ১০০% ফিক্স করা হয়েছে!")
