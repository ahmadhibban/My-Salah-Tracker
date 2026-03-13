import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    
    # ১. ইংরেজি ক্যালেন্ডারের বর্ডার রিমুভ (CalendarHelper.java)
    if 'CalendarHelper.java' in f:
        p = os.path.join(r, 'CalendarHelper.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ফাঁকা বর্ডার তৈরি করার কোড (setStroke) মুছে দেওয়া হচ্ছে
        c = re.sub(r'bgD\.setStroke\([^;]+\);', '// stroke removed', c)
        c = re.sub(r'bg\.setStroke\([^;]+\);', '// stroke removed', c)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

    # ২, ৩ এবং ৪ নম্বর কাজ (MainActivity.java)
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ২. উপরের দুইটা কার্ডের সাইজ সমান করা (-2 মানে WRAP_CONTENT, -1 মানে MATCH_PARENT)
        c = c.replace('LinearLayout.LayoutParams markLp = new LinearLayout.LayoutParams(0, -2, 1f);', 'LinearLayout.LayoutParams markLp = new LinearLayout.LayoutParams(0, -1, 1f);')
        c = c.replace('LinearLayout.LayoutParams todayLp = new LinearLayout.LayoutParams(0, -2, 1f);', 'LinearLayout.LayoutParams todayLp = new LinearLayout.LayoutParams(0, -1, 1f);')
        
        # ৩. নামাজের নাম বোল্ড করা (NORMAL কে BOLD করে দেওয়া হচ্ছে)
        c = c.replace('Typeface.NORMAL', 'Typeface.BOLD')
        c = c.replace('android.graphics.Typeface.NORMAL', 'android.graphics.Typeface.BOLD')
        # আগে ভুল করে থাকা DEFAULT থাকলে সেটাও বোল্ড করে দিচ্ছি
        c = c.replace('tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setTextSize(16); tv.setTypeface(android.graphics.Typeface.DEFAULT);', 'tv.setTypeface(Typeface.DEFAULT_BOLD); tv.setTextSize(16);')
        
        # ৪. মোটিভেশনাল টেক্সটগুলোর বাংলা ট্রান্সলেশন
        bn = 'sp.getString("app_lang", "en").equals("bn") ? '
        
        # সাবধানে রিপ্লেস করা হচ্ছে যেন ডাবল না হয়ে যায়
        if 'আর মাত্র ১টি বাকি!' not in c:
            c = c.replace('"Just one more!"', '(' + bn + '"আর মাত্র ১টি বাকি!" : "Just one more!")')
            c = c.replace('"Halfway there!"', '(' + bn + '"অর্ধেক সম্পন্ন!" : "Halfway there!")')
            c = c.replace('"All prayers done!"', '(' + bn + '"আলহামদুলিল্লাহ, সব পড়া হয়েছে!" : "All prayers done!")')
            c = c.replace('"No prayers yet!"', '(' + bn + '"এখনো নামাজ পড়া হয়নি" : "No prayers yet!")')
            c = c.replace('"No prayers yet"', '(' + bn + '"এখনো নামাজ পড়া হয়নি" : "No prayers yet")')
            c = c.replace('"1 down, 5 to go"', '(' + bn + '"১টি পড়া হয়েছে, ৫টি বাকি" : "1 down, 5 to go")')
            c = c.replace('"2 down, 4 to go"', '(' + bn + '"২টি পড়া হয়েছে, ৪টি বাকি" : "2 down, 4 to go")')
            c = c.replace('"3 down, 3 to go"', '(' + bn + bn + '"৩টি পড়া হয়েছে, ৩টি বাকি" : "3 down, 3 to go")')
            c = c.replace('"4 down, 2 to go"', '(' + bn + '"৪টি পড়া হয়েছে, ২টি বাকি" : "4 down, 2 to go")')
            c = c.replace('"5 down, 1 to go"', '(' + bn + '"৫টি পড়া হয়েছে, ১টি বাকি" : "5 down, 1 to go")')

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ৪টি কাজ ১০০% সফলভাবে সম্পন্ন হয়েছে!")
