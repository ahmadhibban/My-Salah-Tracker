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

        # ১. আরবি তারিখের সাইজ একদম পারফেক্ট (13sp) করা
        c = re.sub(r'dHijri\.setTextSize\(\s*\d+\s*\);', 'dHijri.setTextSize(13);', c)

        # ২. স্ট্রিকের লেখা ছোট করা (যাতে চওড়া কমে যায়)
        c = c.replace('"১ বছরের স্ট্রিক"', '"১ বছর"').replace('"1 YEAR STREAK"', '"1 YEAR"')
        c = c.replace('" দিনের স্ট্রিক"', '" দিন"').replace('" DAYS STREAK"', '" DAYS"')

        # ৩. সেটিংসের পপ-আপগুলোকে কাস্টম রাউন্ডেড ডিজাইনে রিপ্লেস করা
        start_str = '// --- SETTINGS NEW START ---'
        end_str = '// --- SETTINGS NEW END ---'
        
        idx1 = c.find(start_str)
        idx2 = c.find(end_str)
        
        if idx1 != -1 and idx2 != -1:
            idx2 += len(end_str)
            custom_settings_ui = """// --- SETTINGS NEW START ---
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() {
            @Override public void run() { 
                final boolean isBn = sp.getString("app_lang", "en").equals("bn");
                android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL);
                main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
                
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "নির্বাচন করুন" : "Select Option");
                title.setTextColor(colorAccent); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                
                String[] copts = isBn ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                
                for(int i=0; i<copts.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this); row.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
                    android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(copts[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
                    row.addView(tv); main.addView(row);
                    row.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            if(w==0) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); }
                            else { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); }
                            ad.dismiss(); finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent);
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER;
                wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
                if(!isFinishing()) ad.show();
            }
        });

        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
            @Override public void run() {
                final boolean isBn = sp.getString("app_lang", "en").equals("bn");
                android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL);
                main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
                
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                title.setTextColor(colorAccent); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                
                for(int i=0; i<ops.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this); row.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
                    android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(ops[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
                    row.addView(tv); main.addView(row);
                    row.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            ad.dismiss();
                            final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset";
                            
                            android.widget.FrameLayout iWrap = new android.widget.FrameLayout(MainActivity.this);
                            android.widget.LinearLayout iMain = new android.widget.LinearLayout(MainActivity.this); iMain.setOrientation(android.widget.LinearLayout.VERTICAL);
                            iMain.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                            android.graphics.drawable.GradientDrawable igd = new android.graphics.drawable.GradientDrawable(); igd.setColor(themeColors[1]); igd.setCornerRadius(25f * DENSITY); iMain.setBackground(igd);
                            
                            android.widget.TextView iTitle = new android.widget.TextView(MainActivity.this); iTitle.setText(iH ? (isBn ? "আরবি তারিখ এডজাস্ট" : "Adjust Hijri") : (isBn ? "বাংলা তারিখ এডজাস্ট" : "Adjust Bengali"));
                            iTitle.setTextColor(colorAccent); iTitle.setTextSize(18); iTitle.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); iTitle.setPadding(0,0,0,(int)(15*DENSITY)); iMain.addView(iTitle);
                            
                            final android.widget.EditText inp = new android.widget.EditText(MainActivity.this); inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                            inp.setText(String.valueOf(sp.getInt(pK, 0))); inp.setTextColor(themeColors[2]);
                            android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setStroke((int)(1.5f*DENSITY), themeColors[3]); ibg.setCornerRadius(10f*DENSITY); inp.setBackground(ibg); inp.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
                            iMain.addView(inp);
                            
                            android.widget.TextView btn = new android.widget.TextView(MainActivity.this); btn.setText("OK"); btn.setTextColor(android.graphics.Color.WHITE); btn.setGravity(android.view.Gravity.CENTER); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                            btn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
                            android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(colorAccent); bg.setCornerRadius(20f*DENSITY); btn.setBackground(bg);
                            android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, -2); blp.setMargins(0, (int)(20*DENSITY), 0, 0); iMain.addView(btn, blp);
                            
                            final android.app.AlertDialog iAd = new android.app.AlertDialog.Builder(MainActivity.this).setView(iWrap).create();
                            btn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); iAd.dismiss(); } catch(Exception e){} } });
                            
                            android.widget.FrameLayout.LayoutParams iflp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); iflp.gravity = android.view.Gravity.CENTER;
                            iWrap.addView(iMain, iflp); iAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                            iAd.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(iMain, appFonts[0], appFonts[1]);
                            if(!isFinishing()) iAd.show();
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER;
                wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
                if(!isFinishing()) ad.show();
            }
        });
        // --- SETTINGS NEW END ---"""
            c = c[:idx1] + custom_settings_ui + c[idx2:]

        with open(m_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ MainActivity Patched Successfully (Custom UI Dialogs & Alignment)!")

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f:
            cw = f.read()

        # ৪. উইজেটে ৩টি তারিখ এবং স্ট্রিক যুক্ত করা
        if "MainActivity.getBnDateStr" not in cw:
            cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)([^,]*getHijri[^)]*)(\);)',
                        r'''try {
            String wg = new java.text.SimpleDateFormat("dd MMM, yyyy", java.util.Locale.US).format(new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse(dateStr));
            String wb = MainActivity.getBnDateStr(dateStr, sp);
            \1 \2 + " • " + wb + " • " + wg \3
        } catch(Exception e) { \1 \2 \3 }''', cw)
        
        if "cached_streak" not in cw:
            cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)([^,]*100\s*/\s*6\s*\+\s*"%".*?)(\);)',
                        r'''int wSt = sp.getInt("cached_streak", 0);
        boolean wIsBn = sp.getString("app_lang", "en").equals("bn");
        String wStStr = wSt >= 365 ? (wIsBn ? "১ বছর" : "1 YEAR") : (wIsBn ? String.valueOf(wSt).replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯") + " দিন" : wSt + " DAYS");
        \1 wStStr + "\\n" + \2 \3''', cw)

        with open(w_path, 'w', encoding='utf-8') as f:
            f.write(cw)
        print("✅ SalahWidget Patched Successfully (3 Dates & Streak over Percentage)!")

if __name__ == '__main__':
    main()
