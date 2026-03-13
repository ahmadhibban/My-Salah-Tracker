import os, re

def main():
    m_path = None
    for r, d, f in os.walk('.'):
        if 'Android/data' in r or '.git' in r or 'build' in r: continue
        if 'MainActivity.java' in f: m_path = os.path.join(r, 'MainActivity.java')

    if m_path:
        with open(m_path, 'r', encoding='utf-8') as f: c = f.read()

        # ১. আরবি তারিখের সাইজ ছোট করে পারফেক্ট করা (16 sp)
        c = re.sub(r'dHijri\.setTextSize\(\d+\);', 'dHijri.setTextSize(16);', c)
        
        # ২. মেইন পেজের টপ বার থেকে থিম আইকন রিমুভ করা (যাতে থ্রিডি ইফেক্ট ক্র্যাশ না করে)
        c = re.sub(r'(android\.view\.View|View)\s+themeToggleBtn.*?iconsRow\.addView\(themeToggleBtn\);', '', c, flags=re.DOTALL)
        
        # ৩. সেটিংসে "App Theme" এর নাম পরিবর্তন করে "কালার পরিবর্তন করুন" করা
        c = re.sub(r'lang\.get\("App Theme"\)', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"', c)
        
        # ৪. সেটিংস মেনুতে আগের ভুল ডেট এডজাস্টমেন্ট মুছে নতুন থিম ও ডুয়াল ডেট এডজাস্টমেন্ট বসানো
        c = re.sub(r'mr\.addImg\([^,]+,\s*"img_moon".*?\}\s*\);\s*\}\s*\);', '/* SETTINGS_PLACEHOLDER */', c, flags=re.DOTALL)
        c = re.sub(r'mr\.addImg\([^,]+,\s*(isDarkTheme\s*\?\s*"ic_sun"\s*:\s*"ic_moon"|"ic_moon").*?startActivity\(intent\);\s*\}\s*\}\s*\);', '', c, flags=re.DOTALL)

        new_settings = """
        // 1. Dark/Light Theme Toggle in Settings
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "থিম পরিবর্তন (সাদা/কালো)" : "Change Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() { @Override public void run() { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent); } });
        
        // 2. Dual Date Adjust in Settings
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() { @Override public void run() { boolean isBn = sp.getString("app_lang", "en").equals("bn"); final android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this); tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar"); String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"}; tb.setItems(ops, new android.content.DialogInterface.OnClickListener() { @Override public void onClick(android.content.DialogInterface dialog, int w) { final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset"; final android.widget.EditText inp = new android.widget.EditText(MainActivity.this); inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED); inp.setText(String.valueOf(sp.getInt(pK, 0))); String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)"); new android.app.AlertDialog.Builder(MainActivity.this).setTitle(dT).setView(inp).setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() { @Override public void onClick(android.content.DialogInterface d, int which) { try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); } catch(Exception e){} } }).show(); } }); tb.show(); } });
        """
        
        c = c.replace('/* SETTINGS_PLACEHOLDER */', new_settings)

        with open(m_path, 'w', encoding='utf-8') as f: f.write(c)
        print("✅ Success! Top Bar Design and Settings Menu are now fully optimized.")

if __name__ == '__main__': main()
