import os, re
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # আগের সাধারণ সেটিংস রিমুভ করা
        c = re.sub(r'mr\.addImg\([^,]+,\s*(?:isDarkTheme\s*\?\s*"ic_sun"\s*:\s*"ic_moon"|"ic_sun"|"ic_moon").*?tb\.show\(\);\s*\}\s*\);', '', c, flags=re.DOTALL)
        c = re.sub(r'mr\.addImg\([^,]+,\s*"img_moon",.*?tb\.show\(\);\s*\}\s*\);', '', c, flags=re.DOTALL)
        
        # নতুন আলাদা ঘর (Box) যুক্ত সেটিংস বসানো
        settings_boxes = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() {
    @Override public void run() {
        final boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
        android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "নির্বাচন করুন" : "Select Option");
        title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        String[] copts = isBn ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
        for(int i=0; i<copts.length; i++) {
            final int w = i;
            android.widget.LinearLayout box = new android.widget.LinearLayout(MainActivity.this); box.setOrientation(android.widget.LinearLayout.HORIZONTAL); box.setGravity(android.view.Gravity.CENTER_VERTICAL);
            box.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
            android.graphics.drawable.GradientDrawable boxBg = new android.graphics.drawable.GradientDrawable(); boxBg.setColor(themeColors[4]); boxBg.setCornerRadius(15f * DENSITY); box.setBackground(boxBg);
            android.widget.LinearLayout.LayoutParams boxLp = new android.widget.LinearLayout.LayoutParams(-1, -2); boxLp.setMargins(0, 0, 0, (int)(10*DENSITY)); box.setLayoutParams(boxLp);
            android.view.View dot = new android.view.View(MainActivity.this); android.graphics.drawable.GradientDrawable dotBg = new android.graphics.drawable.GradientDrawable(); dotBg.setShape(android.graphics.drawable.GradientDrawable.OVAL); dotBg.setColor(colorAccent);
            android.widget.LinearLayout.LayoutParams dotLp = new android.widget.LinearLayout.LayoutParams((int)(10*DENSITY), (int)(10*DENSITY)); dotLp.setMargins(0, 0, (int)(15*DENSITY), 0); dot.setLayoutParams(dotLp); dot.setBackground(dotBg);
            android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(copts[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
            box.addView(dot); box.addView(tv); main.addView(box);
            box.setOnClickListener(new android.view.View.OnClickListener() {
                @Override public void onClick(android.view.View v) {
                    if(w==0) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); } else { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); }
                    ad.dismiss(); finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent);
                }
            });
        }
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
});

mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
    @Override public void run() {
        final boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
        android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
        title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
        String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
        for(int i=0; i<ops.length; i++) {
            final int w = i;
            android.widget.LinearLayout box = new android.widget.LinearLayout(MainActivity.this); box.setOrientation(android.widget.LinearLayout.HORIZONTAL); box.setGravity(android.view.Gravity.CENTER_VERTICAL);
            box.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
            android.graphics.drawable.GradientDrawable boxBg = new android.graphics.drawable.GradientDrawable(); boxBg.setColor(themeColors[4]); boxBg.setCornerRadius(15f * DENSITY); box.setBackground(boxBg);
            android.widget.LinearLayout.LayoutParams boxLp = new android.widget.LinearLayout.LayoutParams(-1, -2); boxLp.setMargins(0, 0, 0, (int)(10*DENSITY)); box.setLayoutParams(boxLp);
            android.view.View dot = new android.view.View(MainActivity.this); android.graphics.drawable.GradientDrawable dotBg = new android.graphics.drawable.GradientDrawable(); dotBg.setShape(android.graphics.drawable.GradientDrawable.OVAL); dotBg.setColor(colorAccent);
            android.widget.LinearLayout.LayoutParams dotLp = new android.widget.LinearLayout.LayoutParams((int)(10*DENSITY), (int)(10*DENSITY)); dotLp.setMargins(0, 0, (int)(15*DENSITY), 0); dot.setLayoutParams(dotLp); dot.setBackground(dotBg);
            android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(ops[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
            box.addView(dot); box.addView(tv); main.addView(box);
            box.setOnClickListener(new android.view.View.OnClickListener() {
                @Override public void onClick(android.view.View v) {
                    ad.dismiss();
                    final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset";
                    android.widget.FrameLayout iWrap = new android.widget.FrameLayout(MainActivity.this); iWrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                    android.widget.LinearLayout iMain = new android.widget.LinearLayout(MainActivity.this); iMain.setOrientation(android.widget.LinearLayout.VERTICAL); iMain.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                    android.graphics.drawable.GradientDrawable igd = new android.graphics.drawable.GradientDrawable(); igd.setColor(themeColors[1]); igd.setCornerRadius(20f * DENSITY); iMain.setBackground(igd);
                    android.widget.TextView iTitle = new android.widget.TextView(MainActivity.this); iTitle.setText(iH ? (isBn ? "আরবি তারিখ এডজাস্ট" : "Adjust Hijri") : (isBn ? "বাংলা তারিখ এডজাস্ট" : "Adjust Bengali")); iTitle.setTextColor(themeColors[2]); iTitle.setTextSize(18); iTitle.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); iTitle.setPadding(0,0,0,(int)(15*DENSITY)); iMain.addView(iTitle);
                    final android.widget.EditText inp = new android.widget.EditText(MainActivity.this); inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED); inp.setText(String.valueOf(sp.getInt(pK, 0))); inp.setTextColor(themeColors[2]);
                    android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setStroke((int)(1.5f*DENSITY), themeColors[3]); ibg.setCornerRadius(10f*DENSITY); inp.setBackground(ibg); inp.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY)); iMain.addView(inp);
                    android.widget.TextView btn = new android.widget.TextView(MainActivity.this); btn.setText("OK"); btn.setTextColor(android.graphics.Color.WHITE); btn.setGravity(android.view.Gravity.CENTER); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
                    android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(colorAccent); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                    android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, -2); blp.setMargins(0, (int)(20*DENSITY), 0, 0); iMain.addView(btn, blp);
                    final android.app.AlertDialog iAd = new android.app.AlertDialog.Builder(MainActivity.this).setView(iWrap).create();
                    btn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); iAd.dismiss(); } catch(Exception e){} } });
                    android.widget.FrameLayout.LayoutParams iflp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); iflp.gravity = android.view.Gravity.CENTER; iWrap.addView(iMain, iflp); iAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent); iAd.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(iMain, appFonts[0], appFonts[1]); if(!isFinishing()) iAd.show();
                }
            });
        }
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
});\n"""
        
        c = c.replace('mr.addImg("Advanced Statistics"', settings_boxes + '        mr.addImg("Advanced Statistics"')
        
        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ৩. সেটিংসের পপ-আপগুলোতে আলাদা ঘর (Box) যুক্ত করা হয়েছে!")
        break
