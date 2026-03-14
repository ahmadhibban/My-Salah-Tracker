import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'AppConstants.java' in f:
        p = os.path.join(r, 'AppConstants.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ভেঙে যাওয়া স্ট্রিংগুলো ঠিক করে জাভার সঠিক \n ফরম্যাটে বসানো হচ্ছে
        bn_fixed = '''public static final String[] EXTRA_PRAYERS_BN = {
        "ফজরের সুন্নত\\n(পূর্বে)", "ইশরাক", "চাশত", 
        "যোহরের সুন্নত\\n(পূর্বে)", "যোহরের সুন্নত\\n(পরে)", 
        "আসরের সুন্নত\\n(পূর্বে)", 
        "মাগরিবের সুন্নত\\n(পরে)", "আওয়াবীন", 
        "এশার সুন্নত\\n(পরে)", "তাহাজ্জুদ"
    };'''
        en_fixed = '''public static final String[] EXTRA_PRAYERS_EN = {
        "Sunnah\\n(Before Fajr)", "Ishraq", "Chasht", 
        "Sunnah\\n(Before Dhuhr)", "Sunnah\\n(After Dhuhr)", 
        "Sunnah\\n(Before Asr)", 
        "Sunnah\\n(After Maghrib)", "Awabeen", 
        "Sunnah\\n(After Isha)", "Tahajjud"
    };'''
        
        c = re.sub(r'public static final String\[\]\s*EXTRA_PRAYERS_BN\s*=\s*\{.*?\};', bn_fixed, c, flags=re.DOTALL)
        c = re.sub(r'public static final String\[\]\s*EXTRA_PRAYERS_EN\s*=\s*\{.*?\};', en_fixed, c, flags=re.DOTALL)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ AppConstants.java এর এরর সফলভাবে ফিক্স করা হয়েছে!")
