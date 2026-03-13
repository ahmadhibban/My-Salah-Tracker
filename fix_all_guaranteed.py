import os, re

def main():
    found_main = False
    found_widget = False
    
    for r, d, files in os.walk('.'):
        if 'build' in r or '.git' in r: continue
        
        if 'MainActivity.java' in files:
            path = os.path.join(r, 'MainActivity.java')
            found_main = True
            with open(path, 'r', encoding='utf-8') as f: c = f.read()
            
            # 1. আরবি তারিখের সাইজ ছোট করা
            c = c.replace('dHijri.setTextSize(22);', 'dHijri.setTextSize(16);')
            c = c.replace('dHijri.setTextSize(15);', 'dHijri.setTextSize(16);')
            
            # 2. থিম আইকন রিমুভ করা (3D Effect ঠিক করার জন্য)
            c = re.sub(r'(?:android\.view\.)?View\s+themeToggleBtn\s*=[^;]+;.*?iconsRow\.addView\(themeToggleBtn\);', '', c, flags=re.DOTALL)
            c = re.sub(r'(?:android\.view\.)?View\s+themeToggleBtn\s*=[^;]+;.*?iconRow\.addView\(themeToggleBtn\);', '', c, flags=re.DOTALL)
            
            # 3. সেটিংসের নাম পরিবর্তন
            c = c.replace('"Choose Theme"', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"')
            c = c.replace('lang.get("App Theme")', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"')
            
            # 4. ডুয়াল ডেট এডজাস্টমেন্ট
            idx = c.find('"img_moon", new Runnable()')
            if idx != -1:
                start = c.rfind('mr.addImg', 0, idx)
                end = c.find('});', idx)
                if start != -1 and end != -1:
                    new_setting = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
    @Override public void run() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        final android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this);
        tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
        String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
        tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {
            @Override public void onClick(android.content.DialogInterface dialog, int w) {
                final boolean iH = (w == 0);
                final String pK = iH ? "hijri_offset" : "bn_date_offset";
                final android.widget.EditText inp = new android.widget.EditText(MainActivity.this);
                inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                inp.setText(String.valueOf(sp.getInt(pK, 0)));
                String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)");
                new android.app.AlertDialog.Builder(MainActivity.this).setTitle(dT).setView(inp).setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() {
                    @Override public void onClick(android.content.DialogInterface d, int which) {
                        try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); } catch(Exception e){}
                    }
                }).show();
            }
        }); tb.show();
    }
});"""
                    c = c[:start] + new_setting + c[end+3:]

            with open(path, 'w', encoding='utf-8') as f: f.write(c)
            print(f"✅ Modified File: {path}")

        if 'SalahWidget.java' in files:
            path = os.path.join(r, 'SalahWidget.java')
            found_widget = True
            with open(path, 'r', encoding='utf-8') as f: cw = f.read()
            
            # 5. উইজেটের স্ট্রিক ফিক্স করা
            cw = cw.replace('🔥 ', '').replace('🔥', '')
            cw = cw.replace('"স্ট্রিক: " + st + "\\n"', 'st + " দিনের স্ট্রিক\\n"')
            cw = cw.replace('"Streak: " + st + "\\n"', 'st + " DAYS STREAK\\n"')
            
            with open(path, 'w', encoding='utf-8') as f: f.write(cw)
            print(f"✅ Modified File: {path}")
            
    if not found_main: print("❌ MainActivity.java Not Found!")
    if not found_widget: print("❌ SalahWidget.java Not Found!")

if __name__ == '__main__':
    main()
