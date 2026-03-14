import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ১. থিম পপ-আপ থেকে কাজা নামাজের ভুল অপশন সরানো
        c = re.sub(r'String\[\]\s+copts\s*=\s*isBn\s*\?\s*new\s*String\[\]\{"থিম নির্বাচন করুন",\s*"ক্যালেন্ডার নির্বাচন",\s*"কাজা নামাজ"\}\s*:\s*new\s*String\[\]\{"Choose Theme",\s*"Choose Calendar",\s*"Qaza Prayers"\};',
                   r'String[] copts = isBn ? new String[]{"থিম নির্বাচন করুন", "ক্যালেন্ডার নির্বাচন"} : new String[]{"Choose Theme", "Choose Calendar"};', c)
        
        # ২. ভুল জায়গায় থাকা ক্লিক লজিক সরানো
        c = re.sub(r'else\s*if\s*\(\s*(fi|i)\s*==\s*2\s*\)\s*\{\s*ad\.dismiss\(\);\s*startActivity\(new\s*android\.content\.Intent\(MainActivity\.this,\s*QazaListActivity\.class\)\);\s*\}', '', c)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ থিম পপ-আপ থেকে কাজা নামাজের ভুল অপশনটি সফলভাবে সরানো হয়েছে!")
