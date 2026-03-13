import os

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

        # ১. আরবি তারিখের সাইজ ছোট করা
        c = c.replace('dHijri.setTextSize(22);', 'dHijri.setTextSize(16);')

        # ২. মেইন পেজ থেকে থিম আইকন রিমুভ করা
        theme_btn_start = 'View themeToggleBtn = ui.getRoundImage(isDarkTheme ? "ic_moon" : "ic_sun", 6, Color.TRANSPARENT, colorAccent);'
        theme_btn_end = 'iconsRow.addView(themeToggleBtn);'
        
        if theme_btn_start in c and theme_btn_end in c:
            start_idx = c.find(theme_btn_start)
            end_idx = c.find(theme_btn_end) + len(theme_btn_end)
            # মাঝখানের অংশটুকু সাবধানে কেটে ফেলা
            c = c[:start_idx] + c[end_idx:]

        # ৩. সেটিংসে "App Theme" পরিবর্তন করে "কালার পরিবর্তন করুন"
        c = c.replace('lang.get("App Theme")', 'sp.getString("app_lang", "en").equals("bn") ? "কালার পরিবর্তন করুন" : "Change Color"')

        # ৪. সেটিংসে ডুয়াল ডেট এডজাস্টমেন্ট (হিজরি সেটিং মুছে এটা বসানো)
        hijri_start = 'mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "হিজরি তারিখ সেটিং" : "Adjust Hijri Date"'
        
        if hijri_start in c:
            h_idx = c.find(hijri_start)
            h_end_idx = c.find('});', c.find('.show();', h_idx)) + 3
            
            dual_date_setting = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
            @Override
            public void run() {
                boolean isBn = sp.getString("app_lang", "en").equals("bn");
                final AlertDialog.Builder tb = new AlertDialog.Builder(MainActivity.this);
                tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(android.content.DialogInterface dialog, int w) {
                        final boolean iH = (w == 0);
                        final String pK = iH ? "hijri_offset" : "bn_date_offset";
                        final EditText inp = new EditText(MainActivity.this);
                        inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                        inp.setText(String.valueOf(sp.getInt(pK, 0)));
                        String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)");
                        new AlertDialog.Builder(MainActivity.this)
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
            # কোড রিপ্লেস
            c = c[:h_idx] + dual_date_setting + c[h_end_idx:]

        with open(m_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ MainActivity Update Successful!")

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f:
            cw = f.read()

        # ৫. উইজেট থেকে আগুন আইকন মুছে মেইন অ্যাপের মতো ডিজাইন করা
        cw = cw.replace('"🔥 স্ট্রিক: " + st + "\\n"', 'st + " দিনের স্ট্রিক\\n"')
        cw = cw.replace('"🔥 Streak: " + st + "\\n"', 'st + " DAYS STREAK\\n"')

        with open(w_path, 'w', encoding='utf-8') as f:
            f.write(cw)
        print("✅ SalahWidget Update Successful!")

if __name__ == '__main__':
    main()
