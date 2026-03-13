import os, re

def main():
    for r, d, f in os.walk('.'):
        if 'build' in r or '.git' in r: continue
        
        # ১. মেইন অ্যাপ আপডেট
        if 'MainActivity.java' in f:
            p = os.path.join(r, f)
            with open(p, 'r', encoding='utf-8') as file: c = file.read()
            
            # আরবি তারিখের সাইজ ছোট করে পারফেক্ট করা
            c = c.replace('dHijri.setTextSize(22);', 'dHijri.setTextSize(16);')
            c = c.replace('dHijri.setTextSize(15);', 'dHijri.setTextSize(16);')
            
            # টপ বার থেকে থিম আইকন রিমুভ (থ্রিডি ইফেক্ট ক্র্যাশ ঠেকানোর জন্য)
            c = re.sub(r'(android\.view\.View|View)\s+themeToggleBtn.*?iconsRow\.addView\(themeToggleBtn\);', '', c, flags=re.DOTALL)
            
            # সেটিংসের নাম আপডেট
            c = c.replace('lang.get("App Theme")', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"')
            c = c.replace('"থিম পরিবর্তন (সাদা/কালো)"', '"কালার পরিবর্তন করুন"')
            c = c.replace('"Change Theme"', '"Change Color"')
            
            # সেটিংসে আরবি ও বাংলা তারিখ এডজাস্ট যুক্ত করা
            s_new = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() { @Override public void run() { boolean isBn = sp.getString("app_lang", "en").equals("bn"); final android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this); tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar"); String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"}; tb.setItems(ops, new android.content.DialogInterface.OnClickListener() { @Override public void onClick(android.content.DialogInterface dialog, int w) { final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset"; final android.widget.EditText inp = new android.widget.EditText(MainActivity.this); inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED); inp.setText(String.valueOf(sp.getInt(pK, 0))); String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)"); new android.app.AlertDialog.Builder(MainActivity.this).setTitle(dT).setView(inp).setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() { @Override public void onClick(android.content.DialogInterface d, int which) { try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); } catch(Exception e){} } }).show(); } }); tb.show(); } });"""
            
            c = re.sub(r'mr\.addImg\([^)]*?(Adjust Hijri Date|তারিখ এডজাস্ট).*?\.show\(\);\s*\}\s*\}\s*\);', s_new, c, flags=re.DOTALL)
            
            with open(p, 'w', encoding='utf-8') as file: file.write(c)
            print("✅ MainActivity ১০০% সাকসেসফুলি আপডেট করা হয়েছে!")

        # ২. উইজেট আপডেট
        if 'SalahWidget.java' in f:
            p = os.path.join(r, f)
            with open(p, 'r', encoding='utf-8') as file: cw = file.read()
            
            # উইজেট থেকে আগুন (🔥) আইকন মুছে মেইন অ্যাপের ডিজাইনের সাথে হুবহু মিল করা
            cw = cw.replace('🔥 ', '').replace('🔥', '')
            cw = cw.replace('"স্ট্রিক: " + st', 'st + " দিনের স্ট্রিক"')
            cw = cw.replace('"Streak: " + st', 'st + " DAYS STREAK"')
            
            with open(p, 'w', encoding='utf-8') as file: file.write(cw)
            print("✅ SalahWidget সাকসেসফুলি আপডেট করা হয়েছে!")

if __name__ == '__main__': main()
