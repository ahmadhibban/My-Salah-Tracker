import os, re

def main():
    m_path = None
    w_path = None
    for r, d, f in os.walk('.'):
        if 'build' in r or '.git' in r: continue
        if 'MainActivity.java' in f: m_path = os.path.join(r, 'MainActivity.java')
        if 'SalahWidget.java' in f: w_path = os.path.join(r, 'SalahWidget.java')

    if m_path:
        with open(m_path, 'r', encoding='utf-8') as f: c = f.read()

        # 1. আরবি তারিখ ছোট করা
        c = re.sub(r'dHijri\.setTextSize\(\s*\d+\s*\);', 'dHijri.setTextSize(13);', c)

        # 2. বাংলা তারিখে ক্লিক করলে বাংলা ক্যালেন্ডার ওপেন করা
        c = re.sub(r'dBn\.setOnClickListener\(.*?calHelper\.showGregorian\(\).*?\}\s*\);', 'dBn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showBengaliCalendar(); }});', c, flags=re.DOTALL)

        # 3. 100 Year Bengali Calendar Grid (Appended to MainActivity)
        bengali_grid_code = """
    // ==========================================
    // 100-YEAR BENGALI CALENDAR GRID
    // ==========================================
    private int bnViewYear = 1430;
    private int bnViewMonth = 0;
    private android.app.AlertDialog tempDialog = null;

    private void showBengaliCalendar() {
        try {
            java.util.Calendar cal = java.util.Calendar.getInstance();
            cal.setTime(new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse(selectedDate[0]));
            int y = cal.get(java.util.Calendar.YEAR), m = cal.get(java.util.Calendar.MONTH) + 1, d = cal.get(java.util.Calendar.DAY_OF_MONTH);
            int bY = y - 593; bnViewMonth = 0;
            if (m==4 && d>=14) {bnViewMonth=0;} else if(m==4) {bnViewMonth=11; bY--;}
            else if (m==5 && d<=14) {bnViewMonth=0;} else if(m==5) {bnViewMonth=1;}
            else if (m==6 && d<=14) {bnViewMonth=1;} else if(m==6) {bnViewMonth=2;}
            else if (m==7 && d<=15) {bnViewMonth=2;} else if(m==7) {bnViewMonth=3;}
            else if (m==8 && d<=15) {bnViewMonth=3;} else if(m==8) {bnViewMonth=4;}
            else if (m==9 && d<=15) {bnViewMonth=4;} else if(m==9) {bnViewMonth=5;}
            else if (m==10 && d<=15) {bnViewMonth=5;} else if(m==10) {bnViewMonth=6;}
            else if (m==11 && d<=14) {bnViewMonth=6;} else if(m==11) {bnViewMonth=7;}
            else if (m==12 && d<=14) {bnViewMonth=7;} else if(m==12) {bnViewMonth=8;}
            else if (m==1 && d<=13) {bnViewMonth=8; bY--;} else if(m==1) {bnViewMonth=9; bY--;}
            else if (m==2 && d<=12) {bnViewMonth=9; bY--;} else if(m==2) {bnViewMonth=10; bY--;}
            else if (m==3 && d<=14) {bnViewMonth=10; bY--;} else if(m==3) {bnViewMonth=11; bY--;}
            bnViewYear = bY;
        } catch(Exception e) {}
        renderBengaliCalendarGrid();
    }

    private void renderBengaliCalendarGrid() {
        final boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); 
        wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        
        android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); 
        main.setOrientation(android.widget.LinearLayout.VERTICAL);
        main.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); 
        gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);

        android.widget.LinearLayout header = new android.widget.LinearLayout(MainActivity.this);
        header.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        header.setGravity(android.view.Gravity.CENTER_VERTICAL);
        
        android.widget.TextView prev = new android.widget.TextView(MainActivity.this);
        prev.setText("❮"); prev.setTextSize(20); prev.setTextColor(themeColors[2]); prev.setPadding((int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY));
        
        android.widget.TextView title = new android.widget.TextView(MainActivity.this);
        String[] bMs = isBn ? new String[]{"বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"} : new String[]{"Boishakh", "Joistho", "Ashar", "Srabon", "Bhadro", "Ashwin", "Kartik", "Agrahayon", "Poush", "Magh", "Falgun", "Choitro"};
        String yrStr = String.valueOf(bnViewYear);
        if(isBn) yrStr = yrStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
        title.setText(bMs[bnViewMonth] + " " + yrStr);
        title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        title.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); title.setGravity(android.view.Gravity.CENTER);
        
        android.widget.TextView next = new android.widget.TextView(MainActivity.this);
        next.setText("❯"); next.setTextSize(20); next.setTextColor(themeColors[2]); next.setPadding((int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY));
        
        header.addView(prev); header.addView(title); header.addView(next);
        main.addView(header);

        android.widget.LinearLayout weekdays = new android.widget.LinearLayout(MainActivity.this);
        weekdays.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        weekdays.setPadding(0, (int)(15*DENSITY), 0, (int)(10*DENSITY));
        String[] wds = isBn ? new String[]{"রবি", "সোম", "মঙ্গল", "বুধ", "বৃহঃ", "শুক্র", "শনি"} : new String[]{"Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"};
        for(String w : wds) {
            android.widget.TextView wt = new android.widget.TextView(MainActivity.this); wt.setText(w); wt.setTextColor(themeColors[3]); wt.setTextSize(12); wt.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); wt.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); wt.setGravity(android.view.Gravity.CENTER);
            weekdays.addView(wt);
        }
        main.addView(weekdays);

        int daysInMonth = 30;
        if(bnViewMonth >= 0 && bnViewMonth <= 5) daysInMonth = 31;
        else if(bnViewMonth == 10) {
            int gYear = bnViewYear + 594;
            boolean isLeap = (gYear % 4 == 0 && gYear % 100 != 0) || (gYear % 400 == 0);
            daysInMonth = isLeap ? 31 : 30;
        }

        int[] startMonthG = {java.util.Calendar.APRIL, java.util.Calendar.MAY, java.util.Calendar.JUNE, java.util.Calendar.JULY, java.util.Calendar.AUGUST, java.util.Calendar.SEPTEMBER, java.util.Calendar.OCTOBER, java.util.Calendar.NOVEMBER, java.util.Calendar.DECEMBER, java.util.Calendar.JANUARY, java.util.Calendar.FEBRUARY, java.util.Calendar.MARCH};
        int[] startDayG = {14, 15, 15, 16, 16, 16, 16, 15, 15, 14, 13, 15};
        int gYear = bnViewYear + 593 + (bnViewMonth >= 9 ? 1 : 0);
        
        java.util.Calendar cal = java.util.Calendar.getInstance();
        cal.set(gYear, startMonthG[bnViewMonth], startDayG[bnViewMonth], 0, 0, 0);
        int startDayOfWeek = cal.get(java.util.Calendar.DAY_OF_WEEK); 
        
        android.widget.LinearLayout grid = new android.widget.LinearLayout(MainActivity.this);
        grid.setOrientation(android.widget.LinearLayout.VERTICAL);
        
        int currentDay = 1; int cellCount = 1;
        java.text.SimpleDateFormat sdfG = new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
        
        for(int r=0; r<6; r++) {
            android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this);
            row.setOrientation(android.widget.LinearLayout.HORIZONTAL);
            for(int c=0; c<7; c++) {
                android.widget.FrameLayout cell = new android.widget.FrameLayout(MainActivity.this);
                cell.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, (int)(45*DENSITY), 1f));
                if(cellCount >= startDayOfWeek && currentDay <= daysInMonth) {
                    final String cellGregDate = sdfG.format(cal.getTime());
                    boolean isSelected = cellGregDate.equals(selectedDate[0]);
                    
                    android.widget.TextView dt = new android.widget.TextView(MainActivity.this);
                    String dStr = String.valueOf(currentDay);
                    if(isBn) dStr = dStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
                    dt.setText(dStr); dt.setGravity(android.view.Gravity.CENTER); dt.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                    dt.setTextColor(isSelected ? android.graphics.Color.WHITE : themeColors[2]);
                    android.widget.FrameLayout.LayoutParams dlp = new android.widget.FrameLayout.LayoutParams((int)(35*DENSITY), (int)(35*DENSITY));
                    dlp.gravity = android.view.Gravity.CENTER; dt.setLayoutParams(dlp);
                    
                    if(isSelected) {
                        android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable();
                        bg.setShape(android.graphics.drawable.GradientDrawable.OVAL); bg.setColor(colorAccent); dt.setBackground(bg);
                    }
                    cell.addView(dt);
                    cell.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            selectedDate[0] = cellGregDate;
                            if (tempDialog != null) tempDialog.dismiss();
                            loadTodayPage(); refreshWidget();
                        }
                    });
                    cal.add(java.util.Calendar.DATE, 1);
                    currentDay++;
                }
                row.addView(cell); cellCount++;
            }
            grid.addView(row);
            if(currentDay > daysInMonth) break;
        }
        main.addView(grid);

        android.widget.TextView close = new android.widget.TextView(MainActivity.this);
        close.setText(isBn ? "বন্ধ করুন" : "CLOSE"); close.setTextColor(themeColors[3]); close.setTextSize(14); close.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        close.setGravity(android.view.Gravity.CENTER); close.setPadding(0, (int)(15*DENSITY), 0, 0);
        main.addView(close);

        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); 
        flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp); 
        
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
        tempDialog = ad;
        
        close.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); } });
        prev.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { 
            bnViewMonth--; if(bnViewMonth < 0) { bnViewMonth = 11; bnViewYear--; } ad.dismiss(); renderBengaliCalendarGrid(); 
        } });
        next.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { 
            bnViewMonth++; if(bnViewMonth > 11) { bnViewMonth = 0; bnViewYear++; } ad.dismiss(); renderBengaliCalendarGrid(); 
        } });

        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        ad.getWindow().setGravity(android.view.Gravity.CENTER); 
        applyFont(main, appFonts[0], appFonts[1]); 
        if(!isFinishing()) ad.show();
    }
"""
        if "void showBengaliCalendar()" not in c:
            last_brace = c.rfind('}')
            c = c[:last_brace] + bengali_grid_code + '\n' + c[last_brace:]

        # 4. Settings Design matching user's app
        s_regex = r'// --- SETTINGS NEW START ---.*?// --- SETTINGS NEW END ---'
        new_s = """// --- SETTINGS NEW START ---
        mr.addImg(sp.getString("app_lang", "en").equals("bn") ? "কালার ও থিম পরিবর্তন" : "Change Color & Theme", isDarkTheme ? "ic_sun" : "ic_moon", new Runnable() {
            @Override public void run() { 
                final boolean isBn = sp.getString("app_lang", "en").equals("bn");
                android.widget.FrameLayout wrap = new android.widget.FrameLayout(MainActivity.this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout main = new android.widget.LinearLayout(MainActivity.this); main.setOrientation(android.widget.LinearLayout.VERTICAL);
                main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
                
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "নির্বাচন করুন" : "Select Option");
                title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                
                String[] copts = isBn ? new String[]{"থিম পরিবর্তন (সাদা/কালো)", "কালার পরিবর্তন করুন"} : new String[]{"Change Theme (Dark/Light)", "Change Color"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                
                for(int i=0; i<copts.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL);
                    row.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
                    android.widget.TextView dot = new android.widget.TextView(MainActivity.this); dot.setText("• "); dot.setTextColor(colorAccent); dot.setTextSize(20);
                    android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(copts[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
                    row.addView(dot); row.addView(tv); main.addView(row);
                    row.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            if(w==0) { sp.edit().putBoolean("is_dark_mode", !isDarkTheme).apply(); }
                            else { sp.edit().putInt("app_theme", (activeTheme + 1) % 6).apply(); }
                            ad.dismiss(); finish(); overridePendingTransition(0, 0); android.content.Intent intent = new android.content.Intent(MainActivity.this, MainActivity.class); try{intent.putExtra("RESTORE_DATE", sdf.parse(selectedDate[0]).getTime());}catch(Exception e){} startActivity(intent);
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER;
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
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
                
                android.widget.TextView title = new android.widget.TextView(MainActivity.this); title.setText(isBn ? "ক্যালেন্ডার নির্বাচন" : "Select Calendar");
                title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title);
                
                String[] ops = isBn ? new String[]{"আরবি তারিখ (Hijri)", "বাংলা তারিখ (Bengali)"} : new String[]{"Hijri Date", "Bengali Date"};
                final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(MainActivity.this).setView(wrap).create();
                
                for(int i=0; i<ops.length; i++) {
                    final int w = i;
                    android.widget.LinearLayout row = new android.widget.LinearLayout(MainActivity.this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL);
                    row.setPadding(0, (int)(10*DENSITY), 0, (int)(10*DENSITY));
                    android.widget.TextView dot = new android.widget.TextView(MainActivity.this); dot.setText("• "); dot.setTextColor(colorAccent); dot.setTextSize(20);
                    android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(ops[i]); tv.setTextColor(themeColors[2]); tv.setTextSize(16);
                    row.addView(dot); row.addView(tv); main.addView(row);
                    row.setOnClickListener(new android.view.View.OnClickListener() {
                        @Override public void onClick(android.view.View v) {
                            ad.dismiss();
                            final boolean iH = (w == 0); final String pK = iH ? "hijri_offset" : "bn_date_offset";
                            android.widget.FrameLayout iWrap = new android.widget.FrameLayout(MainActivity.this); iWrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                            android.widget.LinearLayout iMain = new android.widget.LinearLayout(MainActivity.this); iMain.setOrientation(android.widget.LinearLayout.VERTICAL);
                            iMain.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
                            android.graphics.drawable.GradientDrawable igd = new android.graphics.drawable.GradientDrawable(); igd.setColor(themeColors[1]); igd.setCornerRadius(20f * DENSITY); iMain.setBackground(igd);
                            
                            android.widget.TextView iTitle = new android.widget.TextView(MainActivity.this); iTitle.setText(iH ? (isBn ? "আরবি তারিখ এডজাস্ট" : "Adjust Hijri") : (isBn ? "বাংলা তারিখ এডজাস্ট" : "Adjust Bengali"));
                            iTitle.setTextColor(themeColors[2]); iTitle.setTextSize(18); iTitle.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); iTitle.setPadding(0,0,0,(int)(15*DENSITY)); iMain.addView(iTitle);
                            
                            final android.widget.EditText inp = new android.widget.EditText(MainActivity.this); inp.setInputType(android.text.InputType.TYPE_CLASS_NUMBER | android.text.InputType.TYPE_NUMBER_FLAG_SIGNED);
                            inp.setText(String.valueOf(sp.getInt(pK, 0))); inp.setTextColor(themeColors[2]);
                            android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setStroke((int)(1.5f*DENSITY), themeColors[3]); ibg.setCornerRadius(10f*DENSITY); inp.setBackground(ibg); inp.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
                            iMain.addView(inp);
                            
                            android.widget.TextView btn = new android.widget.TextView(MainActivity.this); btn.setText("OK"); btn.setTextColor(android.graphics.Color.WHITE); btn.setGravity(android.view.Gravity.CENTER); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                            btn.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
                            android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(colorAccent); bg.setCornerRadius(15f*DENSITY); btn.setBackground(bg);
                            android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, -2); blp.setMargins(0, (int)(20*DENSITY), 0, 0); iMain.addView(btn, blp);
                            
                            final android.app.AlertDialog iAd = new android.app.AlertDialog.Builder(MainActivity.this).setView(iWrap).create();
                            btn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { try { sp.edit().putInt(pK, Integer.parseInt(inp.getText().toString())).apply(); loadTodayPage(); refreshWidget(); iAd.dismiss(); } catch(Exception e){} } });
                            
                            android.widget.FrameLayout.LayoutParams iflp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); iflp.gravity = android.view.Gravity.CENTER;
                            iWrap.addView(iMain, iflp); iAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                            iAd.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(iMain, appFonts[0], appFonts[1]);
                            if(!isFinishing()) iAd.show();
                        }
                    });
                }
                android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER;
                wrap.addView(main, flp); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
                if(!isFinishing()) ad.show();
            }
        });
        // --- SETTINGS NEW END ---"""
            if '// --- SETTINGS NEW START ---' in c:
                c = re.sub(s_regex, new_s, c, flags=re.DOTALL)
            else:
                c = c.replace('mr.addImg("Choose Theme"', new_s + '\n        mr.addImg("Choose Theme"')

            with open(m_path, 'w', encoding='utf-8') as f: f.write(c)
            print("✅ MainActivity Patched (100-Year Calendar + Custom Settings UI)")

    if w_path:
        with open(w_path, 'r', encoding='utf-8') as f: cw = f.read()
        cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)([^,]*getHijri[^)]*)(\s*\);)',
                    r'''try {
            String wg = MainActivity.lang.getGregorian(new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse(dateStr));
            String wb = MainActivity.getBnDateStr(dateStr, sp);
            \1 MainActivity.lang.getHijri(dateStr) + " • " + wb + " • " + wg \3
        } catch(Exception e) { \1 \2 \3 }''', cw)
        
        cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)(.*?100\s*/\s*6\s*\+\s*"%".*?)(\s*\);)',
                    r'''int wSt = sp.getInt("cached_streak", 0);
        boolean wIsBn = sp.getString("app_lang", "en").equals("bn");
        String wStStr = wSt >= 365 ? (wIsBn ? "১ বছর" : "1 YEAR") : (wIsBn ? String.valueOf(wSt).replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯") + " দিন" : wSt + " DAYS");
        \1 wStStr + "\\n" + \2 \3''', cw)

        with open(w_path, 'w', encoding='utf-8') as f: f.write(cw)
        print("✅ Widget Patched (3 Dates + Streak)")

if __name__ == '__main__': main()
