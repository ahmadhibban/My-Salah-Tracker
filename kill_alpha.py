import os
for r, d, f in os.walk('.'):
    if 'build' in r: continue
    for fname in ['MainActivity.java', 'CalendarHelper.java']:
        if fname in f:
            p = os.path.join(r, fname)
            with open(p, 'r', encoding='utf-8') as file: 
                c = file.read()
            
            # সোজাসুজি ক্ষতিকর কোড ডিলিট (কোনো জটিল লজিক নেই)
            c = c.replace('dt.setAlpha(0.4f);', '')
            c = c.replace('tv.setAlpha(0.4f);', '')
            c = c.replace('dTv.setAlpha(0.4f);', '')
            
            with open(p, 'w', encoding='utf-8') as file: 
                file.write(c)

print("✅ ইনভিজিবল ব্যাকগ্রাউন্ড চিরতরে মুছে ফেলা হয়েছে!")
