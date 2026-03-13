import os, re

filepath_main = None
filepath_widget = None

for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        filepath_main = os.path.join(r, 'MainActivity.java')
    if 'SalahWidget.java' in f and 'build' not in r:
        filepath_widget = os.path.join(r, 'SalahWidget.java')

if filepath_main:
    with open(filepath_main, 'r', encoding='utf-8') as f:
        c = f.read()

    # আগের এলোমেলো ক্যালেন্ডার কোড খুঁজে বের করা
    start_idx = c.find('private int bnViewYear')
    if start_idx == -1:
        start_idx = c.find('private void showBengaliCalendar()')

    if start_idx != -1:
        end_idx = c.find('public static String getBnDateStr', start_idx)
        if end_idx == -1:
            end_idx = c.rfind('}')

        if end_idx != -1:
            perfect_calendar = """
    private int bnViewYear = 1430;
    private int bnViewMonth = 0;
    private android.app.AlertDialog tempBnDialog = null;

    private void showBengaliCalendar() {
        try {
            java.util.Calendar cal = java.util.Calendar.getInstance(); cal.setTime(new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse(selectedDate[0]));
            int y = cal.get(java.util.Calendar.YEAR), m = cal.get(java.util.Calendar.MONTH) + 1, d = cal.get(java.util.Calendar.DAY_OF_MONTH);
            int bY = y - 593; bnViewMonth = 0;
            if (m==4 && d>=14) {bnViewMonth=0;} else if(m==4) {bnViewMonth=11; bY--;}
            else if (m==5 && d<=14) {bnViewMonth=0;} else if(m==5) {bnViewMonth=1;} else if (m==6 && d<=14) {bnViewMonth=1;} else if(m==6) {bnViewMonth=2;} else if (m==7 && d<=15) {bnViewMonth=2;} else if(m==7) {bnViewMonth=3;} else if (m==8 && d<=15) {bnViewMonth=3;} else if(m==8) {bnViewMonth=4;} else if (m==9 && d<=15) {bnViewMonth=4;} else if(m==9) {bnViewMonth=5;} else if (m==10 && d<=15) {bnViewMonth=5;} else if(m==10) {bnViewMonth=6;} else if (m==11 && d<=14) {bnViewMonth=6;} else if(m==11) {bnViewMonth=7;} else if (m==12 && d<=14) {bnViewMonth=7;} else if(m==12) {bnViewMonth=8;} else if (m==1 && d<=13) {bnViewMonth=8; bY--;} else if(m==1) {bnViewMonth=9; bY--;} else if (m==2 && d<=12) {bnViewMonth=9; bY--;} else if(m==2) {bnViewMonth=10; bY--;} else if (m==3 && d<=14) {bnViewMonth=10; bY--;} else if(m==3) {bnViewMonth=11; bY--;}
            bnViewYear = bY;
        } catch(Exception e) {}
        
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); tempBnDialog = ad;
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER);
        
        renderBnGrid(main, ad);
        applyFont(main, appFonts[0], appFonts[1]); if(!isFinishing()) ad.show();
    }

    private void renderBnGrid(final android.widget.LinearLayout card, final android.app.AlertDialog dialog) {
        card.removeAllViews();
        final boolean isBn = sp.getString("app_lang", "en").equals("bn");

        android.widget.TextView yearChip = new android.widget.TextView(this); yearChip.setTextColor(colorAccent); yearChip.setTextSize(14); yearChip.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); yearChip.setPadding((int)(25*DENSITY), (int)(8*DENSITY), (int)(25*DENSITY), (int)(8*DENSITY));
        android.graphics.drawable.GradientDrawable yBg = new android.graphics.drawable.GradientDrawable(); yBg.setColor(colorAccent & 0x15FFFFFF); yBg.setCornerRadius(15f * DENSITY); yearChip.setBackground(yBg);
        android.widget.LinearLayout.LayoutParams yLp = new android.widget.LinearLayout.LayoutParams(-2, -2); yLp.gravity = android.view.Gravity.CENTER_HORIZONTAL; yLp.setMargins(0, 0, 0, (int)(15*DENSITY)); yearChip.setLayoutParams(yLp);
        String yrStr = String.valueOf(bnViewYear); if(isBn) yrStr = yrStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
        yearChip.setText(yrStr + (isBn ? " বঙ্গাব্দ ▼" : " BS ▼")); card.addView(yearChip);
        yearChip.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showBengaliYearPicker(card, dialog); }});

        android.widget.LinearLayout header = new android.widget.LinearLayout(this); header.setOrientation(android.widget.LinearLayout.HORIZONTAL); header.setGravity(android.view.Gravity.CENTER_VERTICAL);
        android.widget.TextView prev = new android.widget.TextView(this); prev.setText("❮"); prev.setTextSize(20); prev.setTextColor(themeColors[2]); prev.setPadding((int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY));
        android.widget.TextView title = new android.widget.TextView(this); String[] bMs = isBn ? new String[]{"বৈশাখ", "জ্যৈষ্ঠ", "আষাঢ়", "শ্রাবণ", "ভাদ্র", "আশ্বিন", "কার্তিক", "অগ্রহায়ণ", "পৌষ", "মাঘ", "ফাল্গুন", "চৈত্র"} : new String[]{"Boishakh", "Joistho", "Ashar", "Srabon", "Bhadro", "Ashwin", "Kartik", "Agrahayon", "Poush", "Magh", "Falgun", "Choitro"};
        title.setText(bMs[bnViewMonth]); title.setTextColor(themeColors[2]); title.setTextSize(18); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); title.setGravity(android.view.Gravity.CENTER);
        android.widget.TextView next = new android.widget.TextView(this); next.setText("❯"); next.setTextSize(20); next.setTextColor(themeColors[2]); next.setPadding((int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY), (int)(10*DENSITY));
        header.addView(prev); header.addView(title); header.addView(next); card.addView(header);

        prev.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { 
            card.animate().scaleX(0.95f).scaleY(0.95f).setDuration(50).withEndAction(new Runnable() { @Override public void run() { card.animate().scaleX(1f).scaleY(1f).setDuration(100).start(); bnViewMonth--; if(bnViewMonth < 0) { bnViewMonth = 11; bnViewYear--; } renderBnGrid(card, dialog); } }).start(); 
        }});
        next.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { 
            card.animate().scaleX(0.95f).scaleY(0.95f).setDuration(50).withEndAction(new Runnable() { @Override public void run() { card.animate().scaleX(1f).scaleY(1f).setDuration(100).start(); bnViewMonth++; if(bnViewMonth > 11) { bnViewMonth = 0; bnViewYear++; } renderBnGrid(card, dialog); } }).start(); 
        }});

        android.widget.LinearLayout weekdays = new android.widget.LinearLayout(this); weekdays.setOrientation(android.widget.LinearLayout.HORIZONTAL); weekdays.setPadding(0, (int)(15*DENSITY), 0, (int)(10*DENSITY));
        String[] wds = isBn ? new String[]{"র", "স", "ম", "ব", "ব", "শ", "শ"} : new String[]{"S", "M", "T", "W", "T", "F", "S"};
        for(String w : wds) { android.widget.TextView wt = new android.widget.TextView(this); wt.setText(w); wt.setTextColor(themeColors[3]); wt.setTextSize(12); wt.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); wt.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); wt.setGravity(android.view.Gravity.CENTER); weekdays.addView(wt); }
        card.addView(weekdays);

        int daysInMonth = 30; if(bnViewMonth >= 0 && bnViewMonth <= 5) daysInMonth = 31;
        else if(bnViewMonth == 10) { int gYear = bnViewYear + 594; daysInMonth = ((gYear % 4 == 0 && gYear % 100 != 0) || (gYear % 400 == 0)) ? 31 : 30; }

        int[] sMG = {java.util.Calendar.APRIL, java.util.Calendar.MAY, java.util.Calendar.JUNE, java.util.Calendar.JULY, java.util.Calendar.AUGUST, java.util.Calendar.SEPTEMBER, java.util.Calendar.OCTOBER, java.util.Calendar.NOVEMBER, java.util.Calendar.DECEMBER, java.util.Calendar.JANUARY, java.util.Calendar.FEBRUARY, java.util.Calendar.MARCH};
        int[] sDG = {14, 15, 15, 16, 16, 16, 16, 15, 15, 14, 13, 15};
        int gY = bnViewYear + 593 + (bnViewMonth >= 9 ? 1 : 0);
        java.util.Calendar cal = java.util.Calendar.getInstance(); cal.set(gY, sMG[bnViewMonth], sDG[bnViewMonth], 0, 0, 0);
        int sDOW = cal.get(java.util.Calendar.DAY_OF_WEEK);
        
        android.widget.LinearLayout grid = new android.widget.LinearLayout(this); grid.setOrientation(android.widget.LinearLayout.VERTICAL);
        int currentDay = 1; int cellCount = 1; java.text.SimpleDateFormat sdfG = new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
        
        for(int r=0; r<6; r++) {
            android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL);
            for(int c=0; c<7; c++) {
                android.widget.FrameLayout cell = new android.widget.FrameLayout(this); cell.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, (int)(45*DENSITY), 1f));
                if(cellCount >= sDOW && currentDay <= daysInMonth) {
                    final String cGreg = sdfG.format(cal.getTime()); boolean isSel = cGreg.equals(selectedDate[0]);
                    android.widget.TextView dt = new android.widget.TextView(this); String dStr = String.valueOf(currentDay);
                    if(isBn) dStr = dStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
                    dt.setText(dStr); dt.setGravity(android.view.Gravity.CENTER); dt.setTypeface(android.graphics.Typeface.DEFAULT); 
                    dt.setTextColor(isSel ? android.graphics.Color.WHITE : themeColors[2]);
                    android.widget.FrameLayout.LayoutParams dlp = new android.widget.FrameLayout.LayoutParams((int)(35*DENSITY), (int)(35*DENSITY)); dlp.gravity = android.view.Gravity.CENTER; dt.setLayoutParams(dlp);
                    if(isSel) { android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setShape(android.graphics.drawable.GradientDrawable.OVAL); bg.setColor(colorAccent); dt.setBackground(bg); }
                    cell.addView(dt);
                    cell.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { selectedDate[0] = cGreg; dialog.dismiss(); loadTodayPage(); refreshWidget(); } });
                    cal.add(java.util.Calendar.DATE, 1); currentDay++;
                }
                row.addView(cell); cellCount++;
            }
            grid.addView(row); if(currentDay > daysInMonth) break;
        }
        card.addView(grid);
        android.widget.TextView close = new android.widget.TextView(this); close.setText(isBn ? "বন্ধ করুন" : "CLOSE"); close.setTextColor(themeColors[3]); close.setTextSize(14); close.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); close.setGravity(android.view.Gravity.CENTER); close.setPadding(0, (int)(15*DENSITY), 0, 0); card.addView(close);
        close.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { dialog.dismiss(); } });
    }

    private void showBengaliYearPicker(final android.widget.LinearLayout parentCard, final android.app.AlertDialog calDialog) {
        final boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.FrameLayout yWrap = new android.widget.FrameLayout(this); yWrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout yMain = new android.widget.LinearLayout(this); yMain.setOrientation(android.widget.LinearLayout.VERTICAL); yMain.setPadding((int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY));
        android.graphics.drawable.GradientDrawable yGd = new android.graphics.drawable.GradientDrawable(); yGd.setColor(themeColors[1]); yGd.setCornerRadius(20f * DENSITY); yMain.setBackground(yGd);
        
        android.widget.TextView yTitle = new android.widget.TextView(this); yTitle.setText(isBn ? "সাল নির্বাচন করুন" : "Select Year"); yTitle.setTextColor(themeColors[2]); yTitle.setTextSize(20); yTitle.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); yTitle.setGravity(android.view.Gravity.CENTER); yTitle.setPadding(0, 0, 0, (int)(15*DENSITY)); yMain.addView(yTitle);
        android.widget.ScrollView sv = new android.widget.ScrollView(this); android.widget.LinearLayout list = new android.widget.LinearLayout(this); list.setOrientation(android.widget.LinearLayout.VERTICAL); list.setPadding((int)(20*DENSITY),0,(int)(20*DENSITY),0);
        
        final android.app.AlertDialog yAd = new android.app.AlertDialog.Builder(this).setView(yWrap).create();
        int currentRealBYear = java.util.Calendar.getInstance().get(java.util.Calendar.YEAR) - 593;
        
        for(int y = currentRealBYear + 1; y >= currentRealBYear - 100; y--) { 
            final int selectedY = y;
            android.widget.TextView yt = new android.widget.TextView(this); 
            String yStr = String.valueOf(y); if(isBn) yStr = yStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
            yt.setText(yStr + (isBn ? " বঙ্গাব্দ" : " BS")); yt.setTextSize(18); yt.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY)); yt.setGravity(android.view.Gravity.CENTER);
            yt.setTypeface(y == bnViewYear ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT);
            yt.setTextColor(y == bnViewYear ? colorAccent : themeColors[2]);
            yt.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View view) { bnViewYear = selectedY; yAd.dismiss(); renderBnGrid(parentCard, calDialog); }});
            android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams(-1, -2); lp.setMargins(0,0,0,(int)(5*DENSITY)); yt.setLayoutParams(lp); list.addView(yt);
        }
        sv.addView(list); yMain.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, (int)(300*DENSITY)));
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; yWrap.addView(yMain, flp);
        yAd.getWindow().setBackgroundDrawableResource(android.R.color.transparent); yAd.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(yWrap); yAd.show();
    }
"""
            c = c[:start_idx] + perfect_calendar + c[end_idx:]
            with open(filepath_main, 'w', encoding='utf-8') as f:
                f.write(c)
            print("✅ Step 3: MainActivity (100-Year Calendar) Updated!")

if filepath_widget:
    with open(filepath_widget, 'r', encoding='utf-8') as f:
        cw = f.read()

    # উইজেটে ৩টি তারিখ এবং স্ট্রিক বসানো
    if "getBnDateStr" not in cw:
        cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)([^,]*getHijri[^)]*)(\s*\);)',
                    r'''try {
        String wg = MainActivity.lang.getGregorian(new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse(dateStr));
        String wb = MainActivity.getBnDateStr(dateStr, sp);
        \1 MainActivity.lang.getHijri(dateStr) + " • " + wb + " • " + wg \3
    } catch(Exception e) { \1 \2 \3 }''', cw)
    
    if "wStStr" not in cw:
        cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)(.*?100\s*/\s*6\s*\+\s*"%".*?)(\s*\);)',
                    r'''int wSt = sp.getInt("cached_streak", 0);
    boolean wIsBn = sp.getString("app_lang", "en").equals("bn");
    String wStStr = wSt >= 365 ? (wIsBn ? "১ বছর" : "1 YEAR") : (wIsBn ? String.valueOf(wSt).replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯") + " দিন" : wSt + " DAYS");
    \1 wStStr + "\\n" + \2 \3''', cw)

    cw = cw.replace('🔥 ', '').replace('🔥', '')

    with open(filepath_widget, 'w', encoding='utf-8') as f:
        f.write(cw)
    print("✅ Step 3: SalahWidget Updated!")
