import os, re

def main():
    m_path = None
    w_path = None
    
    # ফাইলগুলো খুঁজে বের করা
    for r, d, f in os.walk('.'):
        if 'build' in r or '.git' in r: continue
        if 'MainActivity.java' in f: m_path = os.path.join(r, 'MainActivity.java')
        if 'SalahWidget.java' in f: w_path = os.path.join(r, 'SalahWidget.java')

    if m_path:
        with open(m_path, 'r', encoding='utf-8') as f:
            c = f.read()

        # ১. আরবি তারিখের সাইজ ছোট করা (যেকোনো সাইজ থাকলে 16 করবে)
        c, n1 = re.subn(r'dHijri\.setTextSize\(\s*\d+\s*\);', 'dHijri.setTextSize(16);', c)
        print(f"✅ আরবি তারিখের সাইজ আপডেট হয়েছে: {n1} জায়গায়")

        # ২. মেইন পেজ থেকে থিম আইকন রিমুভ করা
        c, n2 = re.subn(r'(?:android\.view\.)?View\s+themeToggleBtn.*?iconsRow\.addView\(themeToggleBtn\);', '', c, flags=re.DOTALL)
        print(f"✅ মেইন পেজ থেকে থিম আইকন রিমুভ হয়েছে: {n2} জায়গায়")

        # ৩. সেটিংসে "App Theme" পরিবর্তন করে "কালার পরিবর্তন করুন"
        c, n3 = re.subn(r'lang\.get\(\s*"App Theme"\s*\)', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"', c)
        if n3 == 0:
            c, n3 = re.subn(r'"App Theme"', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"', c)
        print(f"✅ সেটিংসের টেক্সট আপডেট হয়েছে: {n3} জায়গায়")

        # ৪. সেটিংসে ডুয়াল ডেট এডজাস্টমেন্ট
        hijri_regex = r'mr\.addImg\(\s*sp\.getString\("app_lang",\s*"en"\)\.equals\("bn"\)\s*\?\s*"হিজরি তারিখ সেটিং"\s*:\s*"Adjust Hijri Date".*?\}\s*\)\s*;\s*\}\s*\)\s*;'
        
        dual_date_setting = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
            @Override
            public void run() {
                boolean isBn = sp.getString("app_lang", "en").equals("bn");
                final android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this);
                tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface dialog, int w) {
                        final boolean iH = (w == 0);
                        final String pK = iH ? "hijri_offset" : "bn_date_offset";
                        final android.widget.EditText inp = new android.widget.EditText(MainActivity.this);
                        inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                        inp.setText(String.valueOf(sp.getInt(pK, 0)));
                        String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)");
                        new android.app.AlertDialog.Builder(MainActivity.this)
                            .setTitle(dT)
                            .setView(inp)
                            .setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() {
                                @Override
                                public void onClick(android.content.DialogInterface d, int which) {
                                    try {
                                        sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply();
                                        loadTodayPage();
                                    } catch (Exception e) {}
                                }
                            }).show();
                    }
                });
                tb.show();
            }
        });"""
        
        c, n4 = re.subn(hijri_regex, dual_date_setting, c, flags=re.DOTALL)
        print(f"✅ ডুয়াল ডেট সেটিংস যুক্ত হয়েছে: {n4} জায়গায়")

        with open(m_path, 'w', encoding='utf-8') as f:
            f.write(c)

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f:
            cw = f.read()

        # ৫. উইজেট থেকে ফালতু আগুন আইকন মুছে ফেলা
        cw, w1 = re.subn(r'"🔥\s*স্ট্রিক:\s*"\s*\+\s*st\s*\+\s*"\\n"', 'st + " দিনের স্ট্রিক\\n"', cw)
        cw, w2 = re.subn(r'"🔥\s*Streak:\s*"\s*\+\s*st\s*\+\s*"\\n"', 'st + " DAYS STREAK\\n"', cw)
        
        # ব্যাকআপ হিসেবে যদি অন্যভাবে লেখা থাকে
        cw = cw.replace('🔥 ', '').replace('🔥', '')
        
        with open(w_path, 'w', encoding='utf-8') as f:
            f.write(cw)
        print(f"✅ উইজেটের স্ট্রিক আপডেট হয়েছে! (Match: {w1}, {w2})")

if __name__ == '__main__':
    main()
