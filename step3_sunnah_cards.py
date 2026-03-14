import os

for r, d, f in os.walk('.'):
    if 'build' in r: continue
    if 'MainActivity.java' in f:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        
        # সুন্নত ও নফল কার্ডগুলোর লজিক এবং ইউআই
        sunnah_block = r'''
        // --- SUNNAH & NAFIL TRACKER START ---
        android.widget.TextView sHdr = new android.widget.TextView(MainActivity.this);
        boolean sIsBn = sp.getString("app_lang", "en").equals("bn");
        sHdr.setText(sIsBn ? "সুন্নত ও নফল" : "Sunnah & Nafil");
        sHdr.setTextColor(themeColors[2]);
        sHdr.setTextSize(18);
        sHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams sHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        sHdrLp.setMargins(0, (int)(15*DENSITY), 0, (int)(10*DENSITY));
        if(isLandscape) col2.addView(sHdr, sHdrLp); else cardsContainer.addView(sHdr, sHdrLp);

        for(int sIdx = 0; sIdx < AppConstants.EXTRA_DB_KEYS.length; sIdx++) {
            final String sDbKey = selectedDate[0] + "_" + AppConstants.EXTRA_DB_KEYS[sIdx];
            final String sTitleBn = AppConstants.EXTRA_PRAYERS_BN[sIdx];
            final String sTitleEn = AppConstants.EXTRA_PRAYERS_EN[sIdx];
            final int sDefRak = AppConstants.EXTRA_DEF_RAKAT[sIdx];
            final String globRakatKey = "glob_rakat_" + AppConstants.EXTRA_DB_KEYS[sIdx];
            
            final String cardTitle = sIsBn ? sTitleBn : sTitleEn;
            final String stat2 = sp.getString(sDbKey, "no");
            final boolean checked2 = stat2.equals("yes");
            
            soup.neumorphism.NeumorphCardView sCard = new soup.neumorphism.NeumorphCardView(MainActivity.this);
            sCard.setShapeType(0);
            sCard.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
            sCard.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
            sCard.setShadowElevation(3f * DENSITY);
            sCard.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 16f*DENSITY).build());
            sCard.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
            android.widget.LinearLayout.LayoutParams scLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
            scLp.setMargins(0, 0, 0, sIdx == AppConstants.EXTRA_DB_KEYS.length - 1 ? (int)(15*DENSITY) : 0);
            sCard.setLayoutParams(scLp);

            android.widget.LinearLayout sInner = new android.widget.LinearLayout(MainActivity.this);
            sInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
            sInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
            sInner.setPadding((int)(20*DENSITY), (int)(18*DENSITY), (int)(20*DENSITY), (int)(18*DENSITY));
            sCard.addView(sInner);

            android.view.View sIconView = ui.getRoundImage("img_custom_nafl", 8, android.graphics.Color.TRANSPARENT, colorAccent);
            sIconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
            sIconView.setPadding(5, 2, 5, 2);
            android.widget.FrameLayout sIconFrame = new android.widget.FrameLayout(MainActivity.this);
            android.widget.LinearLayout.LayoutParams sFlp = new android.widget.LinearLayout.LayoutParams((int)(30*DENSITY), (int)(30*DENSITY));
            sFlp.setMargins(0, 0, (int)(15*DENSITY), 0);
            sIconFrame.setLayoutParams(sFlp);
            applyNeo(sIconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
            android.widget.FrameLayout.LayoutParams sIvLp = new android.widget.FrameLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY));
            sIvLp.gravity = android.view.Gravity.CENTER;
            sIconView.setLayoutParams(sIvLp);
            sIconFrame.addView(sIconView);
            sInner.addView(sIconFrame);

            android.widget.LinearLayout sTxtCon = new android.widget.LinearLayout(MainActivity.this);
            sTxtCon.setOrientation(android.widget.LinearLayout.VERTICAL);
            sTxtCon.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
            android.widget.TextView sTv = new android.widget.TextView(MainActivity.this);
            sTv.setText(cardTitle);
            sTv.setTextColor(themeColors[2]);
            sTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
            sTv.setTextSize(16);
            sTv.setSingleLine(true);
            sTxtCon.addView(sTv);
            sInner.addView(sTxtCon);

            android.widget.TextView rakatBtn = new android.widget.TextView(MainActivity.this);
            final int curRakat = sp.getInt(globRakatKey, sDefRak);
            String rakStr = String.valueOf(curRakat);
            if (sIsBn) rakStr = rakStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
            rakatBtn.setText(rakStr + (sIsBn ? " রাকাত" : " Rakat"));
            rakatBtn.setTextSize(11);
            rakatBtn.setSingleLine(true);
            rakatBtn.setTextColor(checked2 ? android.graphics.Color.WHITE : themeColors[2]);
            
            applyNeo(rakatBtn, 1, 10f, 2f, checked2 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme);
            
            rakatBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY));
            rakatBtn.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY));
            android.widget.LinearLayout.LayoutParams rakLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
            rakLp.setMargins(0, 0, (int)(15*DENSITY), 0);
            rakatBtn.setLayoutParams(rakLp);
            
            final int finalSIdx = sIdx;
            rakatBtn.setOnClickListener(new android.view.View.OnClickListener() {
                @Override public void onClick(android.view.View v) {
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                    showRakatEditDialog(globRakatKey, cardTitle, curRakat);
                }
            });
            sInner.addView(rakatBtn);

            final android.view.View sChk = getNeoCheckbox(stat2, colorAccent);
            sInner.addView(sChk);

            sCard.setOnClickListener(new android.view.View.OnClickListener() {
                @Override public void onClick(final android.view.View v) {
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                    String newVal = checked2 ? "no" : "yes";
                    sp.edit().putString(sDbKey, newVal).apply();
                    fbHelper.save(selectedDate[0], AppConstants.EXTRA_DB_KEYS[finalSIdx], newVal);
                    
                    v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(35).withEndAction(new Runnable() { 
                        @Override public void run() { 
                            v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); 
                        } 
                    }).start();
                    loadTodayPage();
                }
            });

            if(isLandscape) col2.addView(sCard); else cardsContainer.addView(sCard);
        }
        // --- SUNNAH & NAFIL TRACKER END ---
        
        // --- ROZA TRACKER START ---
        '''

        # রাকাত পরিবর্তনের ডায়ালগ
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
        # রোজার সেকশনের ঠিক আগে সুন্নতের কার্ডগুলো যুক্ত করা হচ্ছে
        if "SUNNAH & NAFIL TRACKER START" not in c:
            c = c.replace('// --- ROZA TRACKER START ---', sunnah_block)
            
        # রাকাত সেভ করার ডায়ালগ মেথড যুক্ত করা হচ্ছে
        if "showRakatEditDialog" not in c:
            c = c.replace('public class MainActivity extends Activity {', 'public class MainActivity extends Activity {\n' + rakat_dialog)

        with open(p, 'w', encoding='utf-8') as file: file.write(c)

print("✅ ধাপ ৩: ১০টি সুন্নত ও নফল নামাজের কার্ড এবং রাকাত অপশন যুক্ত করা হয়েছে!")
