import os

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

        # 1. Inject getBnDateStr for proper Bengali suffixes
        bn_method = """
    public static String getBnDateStr(String dateStr, android.content.SharedPreferences sp) {
        try {
            String[] p = dateStr.split("-"); int y = Integer.parseInt(p[0]), m = Integer.parseInt(p[1]), d = Integer.parseInt(p[2]);
            int bY = y - 593, bM = 0, bD = 0; boolean isLeap = (y%4==0 && y%100!=0)||(y%400==0);
            if (m==4 && d>=14) {bM=0; bD=d-13;} else if(m==4) {bM=11; bD=d+17; bY--;}
            else if (m==5 && d<=14) {bM=0; bD=d+17;} else if(m==5) {bM=1; bD=d-14;}
            else if (m==6 && d<=14) {bM=1; bD=d+17;} else if(m==6) {bM=2; bD=d-14;}
            else if (m==7 && d<=15) {bM=2; bD=d+16;} else if(m==7) {bM=3; bD=d-15;}
            else if (m==8 && d<=15) {bM=3; bD=d+16;} else if(m==8) {bM=4; bD=d-15;}
            else if (m==9 && d<=15) {bM=4; bD=d+16;} else if(m==9) {bM=5; bD=d-15;}
            else if (m==10 && d<=15) {bM=5; bD=d+15;} else if(m==10) {bM=6; bD=d-15;}
            else if (m==11 && d<=14) {bM=6; bD=d+16;} else if(m==11) {bM=7; bD=d-14;}
            else if (m==12 && d<=14) {bM=7; bD=d+16;} else if(m==12) {bM=8; bD=d-14;}
            else if (m==1 && d<=13) {bM=8; bD=d+17; bY--;} else if(m==1) {bM=9; bD=d-13; bY--;}
            else if (m==2 && d<=12) {bM=9; bD=d+18; bY--;} else if(m==2) {bM=10; bD=d-12; bY--;}
            else if (m==3 && d<=14) {bM=10; bD=d+(isLeap?17:16); bY--;} else if(m==3) {bM=11; bD=d-14; bY--;}
            bD += sp.getInt("bn_date_offset", 0);
            boolean isBn = sp.getString("app_lang", "en").equals("bn");
            String[] bMs = isBn ? new String[]{"বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"} : new String[]{"Boishakh", "Joistho", "Ashar", "Srabon", "Bhadro", "Ashwin", "Kartik", "Agrahayon", "Poush", "Magh", "Falgun", "Choitro"};
            
            String suf = "";
            if (!isBn) {
                if (bD >= 11 && bD <= 13) suf = "th";
                else switch (bD % 10) { case 1: suf="st"; break; case 2: suf="nd"; break; case 3: suf="rd"; break; default: suf="th"; }
            } else {
                if(bD == 1) suf = "লা"; else if(bD == 2 || bD == 3) suf = "রা"; else if(bD == 4) suf = "ঠা"; else if(bD >= 5 && bD <= 18) suf = "ই"; else if(bD >= 19 && bD <= 31) suf = "এ"; else suf = "শে";
            }

            String dayStr = String.valueOf(bD), yearStr = String.valueOf(bY);
            if(isBn) {
                dayStr = dayStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
                yearStr = yearStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
            }
            return dayStr + suf + " " + bMs[bM] + ", " + yearStr;
        } catch(Exception e) { return ""; }
    }
"""
        if "public static String getBnDateStr" not in c:
            c = c.replace("private String tBn(String s) {", bn_method + "\n    private String tBn(String s) {")

        # 2. Perfect Header Replacement (Removes Theme icon, aligns Streak)
        start_str = "LinearLayout header = new LinearLayout(this);"
        end_str = "contentArea.addView(header);"
        
        idx1 = c.find(start_str)
        idx2 = c.find(end_str)
        if idx1 != -1 and idx2 != -1:
            idx2 += len(end_str)
            new_header = """// === NEW HEADER LAYOUT START ===
        android.widget.LinearLayout header = new android.widget.LinearLayout(this); 
        header.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
        header.setGravity(android.view.Gravity.CENTER_VERTICAL); 
        header.setPadding((int)(20*DENSITY), (int)(headPadT*DENSITY), (int)(20*DENSITY), (int)(10*DENSITY));
        
        android.widget.LinearLayout leftHeader = new android.widget.LinearLayout(this); 
        leftHeader.setOrientation(android.widget.LinearLayout.VERTICAL);
        leftHeader.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); 
        leftHeader.setGravity(android.view.Gravity.CENTER_VERTICAL);
        
        android.widget.LinearLayout hRow = new android.widget.LinearLayout(this);
        hRow.setOrientation(android.widget.LinearLayout.HORIZONTAL); hRow.setGravity(android.view.Gravity.CENTER_VERTICAL);
        android.view.View moon = ui.getRoundImage("img_moon", 0, android.graphics.Color.TRANSPARENT, themeColors[3]);
        android.widget.LinearLayout.LayoutParams mLp = new android.widget.LinearLayout.LayoutParams((int)(14*DENSITY), (int)(14*DENSITY)); mLp.setMargins(0,0,(int)(6*DENSITY),0);
        moon.setLayoutParams(mLp); hRow.addView(moon);
        android.widget.TextView dHijri = new android.widget.TextView(this); 
        try { dHijri.setText(ui.getHijriDate(sdf.parse(selectedDate[0]), sp.getInt("hijri_offset", 0))); } catch(Exception e) {}
        dHijri.setTextColor(themeColors[2]); dHijri.setTextSize(16); dHijri.setTypeface(appFonts[1], android.graphics.Typeface.BOLD); 
        hRow.addView(dHijri); leftHeader.addView(hRow);
        hRow.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showHijri(); } });

        android.widget.TextView dBn = new android.widget.TextView(this);
        try { dBn.setText(getBnDateStr(selectedDate[0], sp)); } catch(Exception e) {}
        dBn.setTextColor(colorAccent); dBn.setTextSize(15); dBn.setTypeface(appFonts[0], android.graphics.Typeface.BOLD);
        dBn.setPadding(0, (int)(4*DENSITY), 0, (int)(2*DENSITY));
        leftHeader.addView(dBn);
        dBn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showGregorian(); }}); 

        android.widget.TextView dEn = new android.widget.TextView(this);
        try { dEn.setText(lang.getGregorian(sdf.parse(selectedDate[0]))); } catch(Exception e) {} 
        dEn.setTextColor(themeColors[3]); dEn.setTextSize(12); dEn.setTypeface(appFonts[0], android.graphics.Typeface.NORMAL); 
        leftHeader.addView(dEn);
        dEn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showGregorian(); }}); 
        
        android.widget.LinearLayout rightHeader = new android.widget.LinearLayout(this); 
        rightHeader.setOrientation(android.widget.LinearLayout.HORIZONTAL); 
        rightHeader.setGravity(android.view.Gravity.END | android.view.Gravity.CENTER_VERTICAL);
        
        int streakCount = ui.calculateStreak(sp, AppConstants.PRAYERS);
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        
        android.widget.TextView stBadge = new android.widget.TextView(this); 
        stBadge.setTextSize(12); stBadge.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        stBadge.setTextColor(colorAccent);
        stBadge.setText(streakCount >= 365 ? (isBn ? "১ বছরের স্ট্রিক" : "1 YEAR STREAK") : (isBn ? lang.bnNum(streakCount) + " দিনের স্ট্রিক" : streakCount + " DAYS STREAK"));
        applyNeo(stBadge, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); 
        stBadge.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY)); 
        android.widget.LinearLayout.LayoutParams badgeLp = new android.widget.LinearLayout.LayoutParams(-2, -2); 
        badgeLp.setMargins(0, 0, (int)(10*DENSITY), 0); 
        rightHeader.addView(stBadge, badgeLp);

        android.view.View periodBtn = ui.getRoundImage("img_period", 6, android.graphics.Color.TRANSPARENT, colorAccent); applyNeo(periodBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); android.widget.LinearLayout.LayoutParams pLp = new android.widget.LinearLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY)); pLp.setMargins(0,0,(int)(8*DENSITY),0); periodBtn.setLayoutParams(pLp); periodBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showExcuseDialog(); } }); rightHeader.addView(periodBtn); 
        android.view.View settingsBtn = ui.getRoundImage("img_settings", 6, android.graphics.Color.TRANSPARENT, colorAccent); applyNeo(settingsBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme); android.widget.LinearLayout.LayoutParams sLp = new android.widget.LinearLayout.LayoutParams((int)(34*DENSITY), (int)(34*DENSITY)); settingsBtn.setLayoutParams(sLp); settingsBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showSettingsMenu(); } }); rightHeader.addView(settingsBtn);
        
        header.addView(leftHeader); header.addView(rightHeader); contentArea.addView(header);
        // === NEW HEADER LAYOUT END ==="""
            c = c[:idx1] + new_header + c[idx2:]

        # 3. Settings Menu (Dual Date + Theme Option moved here)
        s_str1 = 'mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "হিজরি তারিখ সেটিং" : "Adjust Hijri Date"'
        s_str2 = 'mr.addImg("Advanced Statistics", "img_stats"'
        s_idx1 = c.find(s_str1)
        s_idx2 = c.find(s_str2)
        if s_idx1 != -1 and s_idx2 != -1:
            new_settings = """// --- SETTINGS NEW START ---
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() { @Override public void run() { 
            final android.app.AlertDialog.Builder cb = new android.app.AlertDialog.Builder(MainActivity.this);
            cb.setTitle(sp.getString("app_lang", "en").equals("bn") ? "নির্বাচন করুন" : "Select Option");
            String[] copts = sp.getString("app_lang", "en").equals("bn") ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
            cb.setItems(copts, new android.content.DialogInterface.OnClickListener() { @Override public void onClick(android.content.DialogInterface d, int w) {
                if(w==0) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); }
                else { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); }
                finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent);
            }}); cb.show();
        }});

        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "তারিখ এডজাস্ট (আরবি/বাংলা)" : "Adjust Date (+/-)", "img_moon", new Runnable() {
            @Override public void run() {
                boolean isBn = sp.getString("app_lang", "en").equals("bn");
                final android.app.AlertDialog.Builder tb = new android.app.AlertDialog.Builder(MainActivity.this);
                tb.setTitle(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                tb.setItems(ops, new android.content.DialogInterface.OnClickListener() {
                    @Override public void onClick(android.content.DialogInterface dialog, int w) {
                        final boolean iH = (w == 0);
                        final String pK = iH ? "hijri_offset" : "bn_date_offset";
                        final android.widget.EditText inp = new android.widget.EditText(MainActivity.this);
                        inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                        inp.setText(String.valueOf(sp.getInt(pK, 0)));
                        String dT = iH ? (isBn ? "আরবি তারিখ এডজাস্ট (+/-)" : "Adjust Hijri (+/-)") : (isBn ? "বাংলা তারিখ এডজাস্ট (+/-)" : "Adjust Bengali (+/-)");
                        new android.app.AlertDialog.Builder(MainActivity.this).setTitle(dT).setView(inp).setPositiveButton("OK", new android.content.DialogInterface.OnClickListener() {
                            @Override public void onClick(android.content.DialogInterface d, int which) {
                                try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); } catch(Exception e){}
                            }
                        }).show();
                    }
                }); tb.show();
            }
        });
        // --- SETTINGS NEW END ---
        """
            c = c[:s_idx1] + new_settings + c[s_idx2:]

        # Clean old duplicate theme options
        c = c.replace('mr.addImg("Choose Theme"', '// mr.addImg("Choose Theme"')

        with open(m_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ MainActivity Patched Successfully!")

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f:
            cw = f.read()

        cw = cw.replace('🔥 ', '').replace('🔥', '')
        import re
        cw = re.sub(r'"[^"]*স্ট্রিক:\s*"\s*\+\s*([a-zA-Z0-9_]+)', r'\1 + " দিনের স্ট্রিক"', cw)
        cw = re.sub(r'"[^"]*Streak:\s*"\s*\+\s*([a-zA-Z0-9_]+)', r'\1 + " DAYS STREAK"', cw)

        with open(w_path, 'w', encoding='utf-8') as f:
            f.write(cw)
        print("✅ SalahWidget Patched Successfully!")

if __name__ == '__main__': main()
