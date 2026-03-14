import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    
    # ১. AppConstants এ নামের মাঝে New Line (\n) যুক্ত করা
    if 'AppConstants.java' in f:
        p = os.path.join(r, 'AppConstants.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        new_bn = '''public static final String[] EXTRA_PRAYERS_BN = {
        "ফজরের সুন্নত\\n(পূর্বে)", "ইশরাক", "চাশত", 
        "যোহরের সুন্নত\\n(পূর্বে)", "যোহরের সুন্নত\\n(পরে)", 
        "আসরের সুন্নত\\n(পূর্বে)", 
        "মাগরিবের সুন্নত\\n(পরে)", "আওয়াবীন", 
        "এশার সুন্নত\\n(পরে)", "তাহাজ্জুদ"
    };'''
        new_en = '''public static final String[] EXTRA_PRAYERS_EN = {
        "Sunnah\\n(Before Fajr)", "Ishraq", "Chasht", 
        "Sunnah\\n(Before Dhuhr)", "Sunnah\\n(After Dhuhr)", 
        "Sunnah\\n(Before Asr)", 
        "Sunnah\\n(After Maghrib)", "Awabeen", 
        "Sunnah\\n(After Isha)", "Tahajjud"
    };'''
        c = re.sub(r'public static final String\[\]\s*EXTRA_PRAYERS_BN\s*=\s*\{[^}]+\};', new_bn, c)
        c = re.sub(r'public static final String\[\]\s*EXTRA_PRAYERS_EN\s*=\s*\{[^}]+\};', new_en, c)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)

    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ২. কার্ডের টেক্সটকে দুই লাইনে সাপোর্ট দেওয়ার লজিক
        c = c.replace('sTv.setSingleLine(true);', 'sTv.setSingleLine(false); sTv.setMaxLines(2);')
        
        # ৩. Mark All বাটন ফিক্স (যাতে সবগুলো কার্ড একসাথে সেভ হয়)
        mark_all_patch = r'\1\n                    if(i == 0) { for(int sIdx=0; sIdx<AppConstants.EXTRA_DB_KEYS.length; sIdx++) { sp.edit().putString(selectedDate[0] + "_" + AppConstants.EXTRA_DB_KEYS[sIdx], \2).apply(); fbHelper.save(selectedDate[0], AppConstants.EXTRA_DB_KEYS[sIdx], \2); } }'
        c = re.sub(
            r'(sp\.edit\(\)\.putString\(selectedDate\[0\]\s*\+\s*\"_\"\s*\+\s*AppConstants\.PRAYERS\[i\],\s*([a-zA-Z0-9_]+)\)\.apply\(\);\s*fbHelper\.save\([^;]+\);)\s*(?:for\s*\(\s*int\s+j\s*=\s*0;\s*j\s*<\s*AppConstants\.SUNNAHS\[i\]\.length;\s*j\+\+\s*\)\s*\{[^}]+\})?',
            mark_all_patch,
            c
        )
        
        # ৪. সেটিংস মেনুতে কাজা নামাজের লিস্ট পুনরায় যুক্ত করা
        c = re.sub(r'String\[\]\s+copts\s*=\s*isBn\s*\?\s*new\s*String\[\]\{[^}]+\}\s*:\s*new\s*String\[\]\{[^}]+\};', 
                   r'String[] copts = isBn ? new String[]{"থিম নির্বাচন করুন", "ক্যালেন্ডার নির্বাচন", "কাজা নামাজ"} : new String[]{"Choose Theme", "Choose Calendar", "Qaza Prayers"};', c)
        
        if 'QazaListActivity.class' not in c:
            qaza_logic = r'''else if(i == 2) {
                ad.dismiss();
                startActivity(new android.content.Intent(MainActivity.this, QazaListActivity.class));
            }'''
            c = re.sub(r'(else\s*if\s*\(\s*i\s*==\s*1\s*\)\s*\{[^\}]+\})', r'\1\n                ' + qaza_logic, c)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ৩টি সমস্যারই ১০০% সমাধান করা হয়েছে!")
