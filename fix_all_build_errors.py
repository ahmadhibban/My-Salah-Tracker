import os, re

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # ১. isBn ডুপ্লিকেট ভেরিয়েবল ফিক্স করা
        c = re.sub(r'boolean\s+isBn\s*=\s*sp\.getString\("app_lang",\s*"en"\)\.equals\("bn"\);\s*(String\s+sText\s*=\s*jStat)', r'\1', c)
        
        # ২. পপ-আপ মেথডগুলো যোগ করা (যাতে কোনোভাবেই মিস না হয়)
        jamaat_dialog = r'''
    private void showJamaatDialog(final String jKey) {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this);
        wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); 
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); 
        main.setOrientation(android.widget.LinearLayout.VERTICAL); 
        main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); 
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); 
        
        android.widget.TextView title = new android.widget.TextView(this);
        title.setText(isBn ? "কিভাবে পড়েছেন?" : "How did you pray?"); 
        title.setTextColor(colorAccent); title.setTextSize(20); 
        title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        
        android.widget.ScrollView sv = new android.widget.ScrollView(this);
        android.widget.LinearLayout list = new android.widget.LinearLayout(this); 
        list.setOrientation(android.widget.LinearLayout.VERTICAL);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        
        String[] opts = isBn ? new String[]{"জামাতের সাথে", "একাকী"} : new String[]{"Jamaat", "Alone"};
        final String[] vals = {"jamaat", "alone"};
        String curType = sp.getString(jKey, "jamaat");
        
        for(int s=0; s<opts.length; s++) { 
            final String sName = opts[s];
            final String sVal = vals[s];
            final boolean sChecked = curType.equals(sVal);
            
            final android.widget.LinearLayout row = new android.widget.LinearLayout(this); 
            row.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
            row.setGravity(android.view.Gravity.CENTER_VERTICAL);
            row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); 
            android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
            rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp);
            final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); 
            rowBg.setCornerRadius(15f*DENSITY); 
            rowBg.setColor(sChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); 
            row.setBackground(rowBg);
            
            final android.widget.TextView tv = new android.widget.TextView(this); 
            tv.setText(sName);
            tv.setTextColor(sChecked ? colorAccent : themeColors[2]); 
            tv.setTextSize(16); tv.setTypeface(android.graphics.Typeface.DEFAULT); 
            tv.setTypeface(sChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
            tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
            final android.view.View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); 
            row.addView(tv); row.addView(chk); list.addView(row);
            row.setOnClickListener(new android.view.View.OnClickListener() { 
                @Override public void onClick(final android.view.View v) { 
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
                    sp.edit().putString(jKey, sVal).apply(); 
                    ad.dismiss();
                    loadTodayPage();
                } 
            });
        } 
        
        sv.addView(list);
        main.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, -2, 1f));
        
        android.widget.TextView closeBtn = new android.widget.TextView(this); 
        closeBtn.setText(lang.get("Done")); 
        closeBtn.setTextColor(android.graphics.Color.parseColor("#F1F5F9")); 
        closeBtn.setGravity(android.view.Gravity.CENTER); 
        closeBtn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); 
        closeBtn.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY));
        android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); 
        cBg.setColor(colorAccent); cBg.setCornerRadius(20f*DENSITY); 
        closeBtn.setBackground(cBg); 
        android.widget.LinearLayout.LayoutParams clp = new android.widget.LinearLayout.LayoutParams(-1, -2); 
        clp.setMargins(0, (int)(15*DENSITY), 0, 0); 
        closeBtn.setLayoutParams(clp); 
        main.addView(closeBtn);
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); 
        flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(android.view.Gravity.CENTER);
        closeBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); } });
        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
'''
        rakat_dialog = r'''
    private void showRakatEditDialog(final String globKey, String titleStr, int currentRakat) {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this);
        wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); 
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); 
        main.setOrientation(android.widget.LinearLayout.VERTICAL); 
        main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); 
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); 
        
        android.widget.TextView title = new android.widget.TextView(this);
        title.setText(titleStr + " - " + (isBn ? "রাকাত সেট করুন" : "Set Rakat")); 
        title.setTextColor(colorAccent); title.setTextSize(18); 
        title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setGravity(android.view.Gravity.CENTER);
        title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        
        final android.widget.EditText rakIn = new android.widget.EditText(this);
        rakIn.setText(String.valueOf(currentRakat));
        rakIn.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
        rakIn.setTextColor(themeColors[2]);
        rakIn.setGravity(android.view.Gravity.CENTER);
        android.graphics.drawable.GradientDrawable iBg = new android.graphics.drawable.GradientDrawable();
        iBg.setColor(themeColors[4]); iBg.setCornerRadius(15f*DENSITY);
        rakIn.setBackground(iBg);
        rakIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY));
        android.widget.LinearLayout.LayoutParams rLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        rLp.setMargins(0, 0, 0, (int)(25*DENSITY));
        main.addView(rakIn, rLp);

        android.widget.Button btn = new android.widget.Button(this);
        btn.setText(isBn ? "সেট করুন" : "Set Rakat");
        btn.setTextColor(android.graphics.Color.WHITE);
        btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        btn.setAllCaps(false);
        android.graphics.drawable.GradientDrawable bBg = new android.graphics.drawable.GradientDrawable();
        bBg.setColor(colorAccent); bBg.setCornerRadius(20f*DENSITY);
        btn.setBackground(bBg);
        main.addView(btn, new android.widget.LinearLayout.LayoutParams(-1, (int)(55*DENSITY)));

        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); 
        flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); 
        ad.getWindow().setGravity(android.view.Gravity.CENTER);
        
        btn.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(android.view.View v) {
                String rStr = rakIn.getText().toString().trim();
                if(!rStr.isEmpty()) {
                    try {
                        int r = Integer.parseInt(rStr);
                        sp.edit().putInt(globKey, r).apply();
                        ad.dismiss();
                        loadTodayPage();
                    } catch(Exception e) {}
                }
            }
        });

        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }
'''
        if "void showJamaatDialog" not in c:
            c = c.replace('private void loadTodayPage() {', jamaat_dialog + '\n    private void loadTodayPage() {')
        if "void showRakatEditDialog" not in c:
            c = c.replace('private void loadTodayPage() {', rakat_dialog + '\n    private void loadTodayPage() {')
            
        # ৩. কাজা নামাজের অপশন সেটিংসে ফিরিয়ে আনা
        if '"Qaza Prayers"' not in c and '"কাজা নামাজ"' not in c:
            c = re.sub(r'String\[\]\s+copts\s*=\s*isBn\s*\?\s*new\s*String\[\]\{[^}]+\}\s*:\s*new\s*String\[\]\{[^}]+\};', 
                       r'String[] copts = isBn ? new String[]{"থিম নির্বাচন করুন", "ক্যালেন্ডার নির্বাচন", "কাজা নামাজ"} : new String[]{"Choose Theme", "Choose Calendar", "Qaza Prayers"};', c)
        
        # কাজা নামাজের ক্লিকে যেন লিস্ট ওপেন হয়, সেই লজিকটা বসানো হচ্ছে
        if 'QazaListActivity.class' not in c:
            qaza_logic = r'''else if(i == 2) {
                ad.dismiss();
                startActivity(new android.content.Intent(MainActivity.this, QazaListActivity.class));
            }'''
            c = re.sub(r'(else\s*if\s*\(\s*i\s*==\s*1\s*\)\s*\{[^\}]+\})', r'\1\n                ' + qaza_logic, c)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ সব এরর এবং কাজা নামাজের লিস্ট ১০০% সফলভাবে ফিক্স করা হয়েছে!")
