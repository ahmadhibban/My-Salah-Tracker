import os, re

filepath = None
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        filepath = os.path.join(r, 'MainActivity.java')
        break

if filepath:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # পুরানো, ফালতু এবং ডুপ্লিকেট সেটিংস মুছে ফেলা
    c = re.sub(r'mr\.addImg\([^,]+,\s*"img_moon".*?\}\s*\);\s*\}\s*\);', '', c, flags=re.DOTALL)
    c = re.sub(r'mr\.addImg\([^,]+,\s*(?:isDarkTheme\s*\?\s*"ic_sun"\s*:\s*"ic_moon"|"ic_sun"|"ic_moon").*?\}\s*\);\s*\}\s*\);', '', c, flags=re.DOTALL)
    c = re.sub(r'mr\.addImg\("Choose Theme".*?\}\);', '', c, flags=re.DOTALL)
    c = re.sub(r'mr\.addImg\(lang\.get\("App Theme"\).*?\}\);', '', c, flags=re.DOTALL)
    c = re.sub(r'// --- SETTINGS NEW START ---.*?// --- SETTINGS NEW END ---', '', c, flags=re.DOTALL)

    # অরিজিনাল সিস্টেম পপ-আপ যুক্ত করা (হুবহু মিলানোর জন্য)
    native_settings = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() {
        @Override public void run() {
            final boolean isBn = sp.getString("app_lang", "en").equals("bn");
            android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this);
            tb.setTitle(isBn ? "নির্বাচন করুন" : "Select Option");
            String[] ops = isBn ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
            tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {
                @Override public void onClick(android.content.DialogInterface dialog, int w) {
                    if(w==0) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); }
                    else { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); }
                    finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent);
                }
            });
            tb.show();
        }
    });

    mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
        @Override public void run() {
            final boolean isBn = sp.getString("app_lang", "en").equals("bn");
            android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this);
            tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
            String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
            tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {
                @Override public void onClick(android.content.DialogInterface dialog, int w) {
                    final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset";
                    android.app.AlertDialog.Builder ib = new android.app.AlertDialog.Builder(MainActivity.this);
                    ib.setTitle(iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)"));
                    final android.widget.EditText inp = new android.widget.EditText(MainActivity.this);
                    inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                    inp.setText(String.valueOf(sp.getInt(pK, 0)));
                    android.widget.FrameLayout fl = new android.widget.FrameLayout(MainActivity.this);
                    fl.setPadding((int)(20*DENSITY), (int)(10*DENSITY), (int)(20*DENSITY), (int)(10*DENSITY));
                    fl.addView(inp); ib.setView(fl);
                    ib.setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() {
                        @Override public void onClick(android.content.DialogInterface d, int which) {
                            try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); } catch(Exception e){}
                        }
                    });
                    ib.show();
                }
            });
            tb.show();
        }
    });
    """
    if "Change Color & Theme" not in c:
        c = c.replace('mr.addImg("Advanced Statistics"', native_settings + '\n        mr.addImg("Advanced Statistics"')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Step 2 Done!")
else:
    print("❌ MainActivity.java Not Found!")
