import os
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        parts = c.split('mr.addImg(')
        new_c = parts[0]
        for pt in parts[1:]:
            if 'ic_sun' in pt or '"img_moon"' in pt or 'Choose Theme' in pt or 'App Theme' in pt or 'হিজরি তারিখ সেটিং' in pt or 'Adjust Date' in pt or 'কালার ও থিম' in pt: continue
            new_c += 'mr.addImg(' + pt

        settings = """mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() {
            @Override public void run() {
                final boolean isBn = sp.getString("app_lang", "en").equals("bn");
                android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "নির্বাচন করুন" : "Select Option"); title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                String[] copts = isBn ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                for(int i=0; i<copts.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout box = new android.widget.LinearLayout(MainActivity.this); box.setOrientation(android.widget.LinearLayout.HORIZONTAL); box.setGravity(android.view.Gravity.CENTER_VERTICAL); box.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                    android.graphics.drawable.GradientDrawable boxBg = new android.graphics.drawable.GradientDrawable(); boxBg.setColor(themeColors[4]); boxBg.setCornerRadius(15f * DENSITY); box.setBackground(boxBg);
                    android.widget.LinearLayout.LayoutParams boxLp = new android.widget.LinearLayout.LayoutParams(-1, -2); boxLp.setMargins(0, 0, 0, (int)(10*DENSITY)); box.setLayoutParams(boxLp);
                    android.view.View dot = new android.view.View(MainActivity.this); android.graphics.drawable.GradientDrawable dotBg = new android.graphics.drawable.GradientDrawable(); dotBg.setShape(android.graphics.drawable.GradientDrawable.OVAL); dotBg.setColor(colorAccent);
                    android.widget.LinearLayout.LayoutParams dotLp = new android.widget.LinearLayout.LayoutParams((int)(8*DENSITY), (int)(8*DENSITY)); dotLp.setMargins(0, 0, (int)(15*DENSITY), 0); dot.setLayoutParams(dotLp); dot.setBackground(dotBg);
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
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar"); title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                for(int i=0; i<ops.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout box = new android.widget.LinearLayout(MainActivity.this); box.setOrientation(android.widget.LinearLayout.HORIZONTAL); box.setGravity(android.view.Gravity.CENTER_VERTICAL); box.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                    android.graphics.drawable.GradientDrawable boxBg = new android.graphics.drawable.GradientDrawable(); boxBg.setColor(themeColors[4]); boxBg.setCornerRadius(15f * DENSITY); box.setBackground(boxBg);
                    android.widget.LinearLayout.LayoutParams boxLp = new android.widget.LinearLayout.LayoutParams(-1, -2); boxLp.setMargins(0, 0, 0, (int)(10*DENSITY)); box.setLayoutParams(boxLp);
                    android.view.View dot = new android.view.View(MainActivity.this); android.graphics.drawable.GradientDrawable dotBg = new android.graphics.drawable.GradientDrawable(); dotBg.setShape(android.graphics.drawable.GradientDrawable.OVAL); dotBg.setColor(colorAccent);
                    android.widget.LinearLayout.LayoutParams dotLp = new android.widget.LinearLayout.LayoutParams((int)(8*DENSITY), (int)(8*DENSITY)); dotLp.setMargins(0, 0, (int)(15*DENSITY), 0); dot.setLayoutParams(dotLp); dot.setBackground(dotBg);
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
                            
                            String[] subOpts = isBn ? new String[]{"-১ দিন (গতকাল)", "ডিফল্ট (০)", "+১ দিন (আগামীকাল)"} : new String[]{"-1 Day (Yesterday)", "Default (0)", "+1 Day (Tomorrow)"};
                            final int[] vals = {-1, 0, 1}; int currentVal = sp.getInt(pK, 0);
                            final android.app.AlertDialog iAd = new android.app.AlertDialog.Builder(MainActivity.this).setView(iWrap).create();
                            for(int j=0; j<3; j++) {
                                final int sj = j;
                                android.widget.LinearLayout sBox = new android.widget.LinearLayout(MainActivity.this); sBox.setOrientation(android.widget.LinearLayout.HORIZONTAL); sBox.setGravity(android.view.Gravity.CENTER_VERTICAL); sBox.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY));
                                android.graphics.drawable.GradientDrawable sBoxBg = new android.graphics.drawable.GradientDrawable(); sBoxBg.setColor(vals[sj] == currentVal ? colorAccent : themeColors[4]); sBoxBg.setCornerRadius(15f * DENSITY); sBox.setBackground(sBoxBg);
                                android.widget.LinearLayout.LayoutParams sBoxLp = new android.widget.LinearLayout.LayoutParams(-1, -2); sBoxLp.setMargins(0, 0, 0, (int)(10*DENSITY)); sBox.setLayoutParams(sBoxLp);
                                android.view.View sDot = new android.view.View(MainActivity.this); android.graphics.drawable.GradientDrawable sDotBg = new android.graphics.drawable.GradientDrawable(); sDotBg.setShape(android.graphics.drawable.GradientDrawable.OVAL); sDotBg.setColor(vals[sj] == currentVal ? android.graphics.Color.WHITE : colorAccent);
                                android.widget.LinearLayout.LayoutParams sDotLp = new android.widget.LinearLayout.LayoutParams((int)(8*DENSITY), (int)(8*DENSITY)); sDotLp.setMargins(0, 0, (int)(15*DENSITY), 0); sDot.setLayoutParams(sDotLp); sDot.setBackground(sDotBg);
                                android.widget.TextView sTv = new android.widget.TextView(MainActivity.this); sTv.setText(subOpts[sj]); sTv.setTextColor(vals[sj] == currentVal ? android.graphics.Color.WHITE : themeColors[2]); sTv.setTextSize(16); sTv.setTypeface(vals[sj] == currentVal ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
                                sBox.addView(sDot); sBox.addView(sTv); iMain.addView(sBox);
                                sBox.setOnClickListener(new android.view.View.OnClickListener() {
                                    @Override public void onClick(android.view.View v) {
                                        try { sp.edit().putInt(pK, vals[sj]).apply(); loadTodayPage(); refreshWidget(); iAd.dismiss(); } catch(Exception e){}
                                    }
                                });
                            }
                            android.widget.FrameLayout.LayoutParams iflp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); iflp.gravity = android.view.Gravity.CENTER; iWrap.addView(iMain, iflp); iAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent); iAd.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(iMain, appFonts[0], appFonts[1]); if(!isFinishing()) iAd.show();
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
            }
        });\n"""
        new_c = new_c.replace('mr.addImg("Advanced Statistics"', settings + '        mr.addImg("Advanced Statistics"')
        with open(p, 'w', encoding='utf-8') as file: file.write(new_c)
        print("✅ ১. সেটিংস ডুপ্লিকেট ফিক্স এবং ৩-অপশন (-১, ০, +১) পপ-আপ বসানো হয়েছে!")
        break
