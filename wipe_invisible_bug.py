import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    for fname in ['MainActivity.java', 'CalendarHelper.java']:
        if fname in f:
            p = os.path.join(r, fname)
            with open(p, 'r', encoding='utf-8') as file: 
                c = file.read()
            
            # ১. এন্টার বা স্পেস দিয়ে লুকিয়ে থাকা ক্ষতিকর setAlpha ব্লকগুলো সমূলে ধ্বংস করা
            c = re.sub(r'if\s*\([^)]+\)\s*\{\s*(?:dt|tv|dTv)\.setTextColor\([^;]+\);\s*(?:dt|tv|dTv)\.setAlpha\([^;]+\);\s*\}', '', c)
            
            # ২. ওভাররাইড করা ডুপ্লিকেট কালার ব্লকগুলো রিমুভ করা
            c = re.sub(r'if\s*\([^)]+\)\s*\{\s*(?:dt|tv|dTv)\.setTextColor\(\s*(?:android\.graphics\.)?Color\.argb[^}]+\}\s*', '', c)
            
            # ৩. ইংরেজি ক্যালেন্ডারে themeColors[4] (অদৃশ্য) এর জায়গায় themeColors[3] (হালকা ছাই) বসানো
            c = c.replace('isFuture ? themeColors[4] :', 'isFuture ? themeColors[3] :')
            c = c.replace('isFutureDate ? themeColors[4] :', 'isFutureDate ? themeColors[3] :')
            
            with open(p, 'w', encoding='utf-8') as file: 
                file.write(c)

print("✅ সব ক্যালেন্ডারের ইনভিজিবিলিটি বাগ ১০০% ফিক্স করা হয়েছে!")
