import os

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    
    # CalendarHelper.java ফাইলে ইংরেজি ক্যালেন্ডারের সংখ্যা বোল্ড করা
    if 'CalendarHelper.java' in f:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # তারিখের টেক্সট ভিউতে Bold ফন্ট যুক্ত করা হচ্ছে
        c = c.replace('tv.setTextSize(13); tv.setGravity(Gravity.CENTER);', 'tv.setTextSize(13); tv.setGravity(Gravity.CENTER); tv.setTypeface(Typeface.DEFAULT_BOLD);')
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ইংরেজি ক্যালেন্ডারের সংখ্যাগুলো পারফেক্টলি বোল্ড করা হয়েছে!")
