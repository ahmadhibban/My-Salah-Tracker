import os, re

def main():
    m_path = None
    w_path = None
    for r, d, f in os.walk('.'):
        if 'build' in r or '.git' in r: continue
        if 'MainActivity.java' in f: m_path = os.path.join(r, 'MainActivity.java')
        if 'SalahWidget.java' in f: w_path = os.path.join(r, 'SalahWidget.java')

    if m_path:
        with open(m_path, 'r', encoding='utf-8') as f:
            c = f.read()

        # 1. আরবি তারিখের সাইজ ছোট করা (যেকোনো ভেরিয়েবল নামই থাকুক না কেন)
        h_match = re.search(r'([a-zA-Z0-9_]+)\.setText\([^;]*?(?:getHijri|Hijri)', c)
        if h_match:
            v = h_match.group(1)
            c, n1 = re.subn(rf'{v}\.setTextSize\([^;]+\);', f'{v}.setTextSize(16);', c)
            print(f"✅ আরবি তারিখের সাইজ 16 করা হয়েছে ({n1} টি পরিবর্তন)")

        # 2. থিম আইকন রিমুভ (মেইন পেজের টপ বার থেকে)
        t_match = re.search(r'(?:View|android\.view\.View)\s+([a-zA-Z0-9_]+)\s*=\s*ui\.getRoundImage\([^;]+?(?:ic_moon|ic_sun)', c)
        if t_match:
            v = t_match.group(1)
            c, n2 = re.subn(rf'[a-zA-Z0-9_]+\.addView\(\s*{v}\s*\);', f'/* {v} removed to fix 3D effect */', c)
            print(f"✅ থিম আইকন মেইন পেজ থেকে রিমুভ করা হয়েছে ({n2} টি পরিবর্তন)")

        # 3. সেটিংসের নাম আপডেট ("থিম পরিবর্তন" -> "কালার পরিবর্তন করুন")
        c, n3_1 = re.subn(r'"থিম পরিবর্তন(?: করুন)?"', '"কালার পরিবর্তন করুন"', c)
        c, n3_2 = re.subn(r'lang\.get\(\s*"App Theme"\s*\)', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"', c)
        print(f"✅ সেটিংসের টেক্সট 'কালার পরিবর্তন' করা হয়েছে ({n3_1 + n3_2} টি পরিবর্তন)")

        # 4. ডুয়াল ডেট সেটিংস (আরবি ও বাংলা)
        s_match = re.search(r'([a-zA-Z0-9_]+)\.addImg\([^;]+?(?:Adjust Hijri Date|হিজরি তারিখ|hijri_offset).*?\}\s*\)\s*;\s*\}\s*\)\s*;', c, re.DOTALL)
        if s_match:
            caller = s_match.group(1)
            dual_setting = f"""{caller}.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {{
                @Override public void run() {{
                    boolean isBn = sp.getString("app_lang", "en").equals("bn");
                    final android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this);
                    tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                    String[] ops = isBn ? new String[]{{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"}} : new String[]{{"Hijri Date", "Bengali Date"}};
                    tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {{
                        @Override public void onClick(android.content.DialogInterface dialog, int w) {{
                            final boolean iH = (w == 0);
                            final String pK = iH ? "hijri_offset" : "bn_date_offset";
                            final android.widget.EditText inp = new android.widget.EditText(MainActivity.this);
                            inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                            inp.setText(String.valueOf(sp.getInt(pK, 0)));
                            String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)");
                            new android.app.AlertDialog.Builder(MainActivity.this).setTitle(dT).setView(inp).setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() {{
                                @Override public void onClick(android.content.DialogInterface d, int which) {{
                                    try {{ sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); }} catch(Exception e){{}}
                                }}
                            }}).show();
                        }}
                    }}); tb.show();
                }}
            }});"""
            c = c.replace(s_match.group(0), dual_setting)
            print("✅ সেটিংসে বাংলা এবং আরবি ডেট এডজাস্টমেন্ট সফলভাবে যুক্ত করা হয়েছে।")

        with open(m_path, 'w', encoding='utf-8') as f:
            f.write(c)

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f:
            cw = f.read()

        # 5. উইজেট আপডেট (যেকোনো ফরমেটই থাকুক না কেন ঠিক করবে)
        cw = cw.replace('🔥', '')
        cw, w1 = re.subn(r'"\s*স্ট্রিক:\s*"\s*\+\s*([^;\n\)]+)', r'\1 + " দিনের স্ট্রিক"', cw)
        cw, w2 = re.subn(r'"\s*Streak:\s*"\s*\+\s*([^;\n\)]+)', r'\1 + " DAYS STREAK"', cw)
        
        with open(w_path, 'w', encoding='utf-8') as f:
            f.write(cw)
        print(f"✅ উইজেট থেকে আইকন মুছে স্ট্রিক টেক্সট ঠিক করা হয়েছে ({w1 + w2} টি পরিবর্তন)।")

if __name__ == '__main__':
    main()
