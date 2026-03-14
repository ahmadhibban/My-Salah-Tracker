import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'AppConstants.java' in f:
        p = os.path.join(r, 'AppConstants.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # নতুন ডেটাগুলো AppConstants এ যোগ করা হচ্ছে
        new_constants = '''
    // নতুন ১০টি সুন্নত/নফলের ডিসপ্লে নাম
    public static final String[] EXTRA_PRAYERS_BN = {
        "ফজরের পূর্বের সুন্নত", "ইশরাক", "চাশত", 
        "যোহরের পূর্বের সুন্নত", "যোহরের পরের সুন্নত", 
        "আসরের পূর্বের সুন্নত", 
        "মাগরিবের পরের সুন্নত", "আওয়াবীন", 
        "এশার পরের সুন্নত", "তাহাজ্জুদ"
    };
    public static final String[] EXTRA_PRAYERS_EN = {
        "Sunnah (Before Fajr)", "Ishraq", "Chasht", 
        "Sunnah (Before Dhuhr)", "Sunnah (After Dhuhr)", 
        "Sunnah (Before Asr)", 
        "Sunnah (After Maghrib)", "Awabeen", 
        "Sunnah (After Isha)", "Tahajjud"
    };
    // পুরনো ডেটাবেস Key (যাতে আগের ডেটা না হারায়)
    public static final String[] EXTRA_DB_KEYS = {
        "Fajr_2 Rakat Sunnah (Before)", "Fajr_4 Rakat Ishraq", "Fajr_4 Rakat Chasht",
        "Dhuhr_4 Rakat Sunnah (Before)", "Dhuhr_2 Rakat Sunnah (After)",
        "Asr_4 Rakat Sunnah (Before)",
        "Maghrib_2 Rakat Sunnah (After)", "Maghrib_6 Rakat Awabeen",
        "Isha_2 Rakat Sunnah (After)", "Isha_4 Rakat Tahajjud"
    };
    // ডিফল্ট রাকাত সংখ্যা
    public static final int[] EXTRA_DEF_RAKAT = { 2, 4, 4, 4, 2, 4, 2, 6, 2, 4 };
'''
        # যদি আগে থেকে যোগ করা না থাকে, তবে যোগ করবে
        if 'EXTRA_PRAYERS_BN' not in c:
            c = c.replace('public static final String[][] SUNNAHS = {', new_constants + '\n    public static final String[][] SUNNAHS = {')
            
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ধাপ ১: AppConstants এ নতুন ডেটা এবং পুরনো ডেটাবেস ম্যাপ সফলভাবে যুক্ত হয়েছে!")
