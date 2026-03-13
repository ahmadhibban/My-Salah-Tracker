import os, re

def find_closing_brace(s, start):
    count = 0
    for i in range(start, len(s)):
        if s[i] == '{': count += 1
        elif s[i] == '}':
            count -= 1
            if count == 0: return i
    return -1

def main():
    m_path = None
    w_path = None
    for r, d, f in os.walk('.'):
        if 'build' in r or '.git' in r: continue
        if 'MainActivity.java' in f: m_path = os.path.join(r, 'MainActivity.java')
        if 'SalahWidget.java' in f: w_path = os.path.join(r, 'SalahWidget.java')

    if m_path:
        with open(m_path, 'r', encoding='utf-8') as f: c = f.read()

        # 1. আরবি তারিখের সাইজ ছোট করা (22 -> 16)
        c = c.replace('.setTextSize(22)', '.setTextSize(16)')

        # 2. থিম আইকন হাইড করা (থ্রিডি ইফেক্ট ক্র্যাশ ঠেকানোর জন্য)
        c = c.replace('iconsRow.addView(themeToggleBtn);', '/* iconsRow.addView(themeToggleBtn); */')
        c = c.replace('iconRow.addView(themeToggleBtn);', '/* iconRow.addView(themeToggleBtn); */')

        # 3. সেটিংসে "App Theme" এর নাম পরিবর্তন
        c = c.replace('lang.get("App Theme")', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"')

        # 4. ডুয়াল ডেট সেটিংস (ব্র্যাকেট গুনে নিখুঁতভাবে রিপ্লেস করা)
        idx = c.find('"hijri_offset"')
        if idx != -1:
            addimg_start = c.rfind('mr.addImg(', 0, idx)
            if addimg_start != -1:
                brace_start = c.find('{', addimg_start)
                if brace_start != -1:
                    brace_end = find_closing_brace(c, brace_start)
                    if brace_end != -1:
                        stmt_end = c.find(';', brace_end)
                        rep = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
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
                        c = c[:addimg_start] + rep + c[stmt_end+1:]

        with open(m_path, 'w', encoding='utf-8') as f: f.write(c)
        print("✅ MainActivity ১০০% নিখুঁতভাবে আপডেট করা হয়েছে!")

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f: cw = f.read()
        
        # 5. উইজেট থেকে ফালতু আগুন আইকন মুছে ফেলা
        cw = cw.replace('🔥', '').replace('🔥 ', '')
        cw = re.sub(r'"\s*স্ট্রিক:\s*"\s*\+\s*([a-zA-Z0-9_]+)', r'\1 + " দিনের স্ট্রিক"', cw)
        cw = re.sub(r'"\s*Streak:\s*"\s*\+\s*([a-zA-Z0-9_]+)', r'\1 + " DAYS STREAK"', cw)
        
        with open(w_path, 'w', encoding='utf-8') as f: f.write(cw)
        print("✅ SalahWidget আপডেট করা হয়েছে!")

if __name__ == '__main__': main()
