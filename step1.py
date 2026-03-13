import os, re

filepath = None
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        filepath = os.path.join(r, 'MainActivity.java')
        break

if filepath:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # স্ট্রিক ছোট করা
    c = c.replace('"1 YEAR STREAK"', '(sp.getString("app_lang", "en").equals("bn") ? "১ বছর" : "1 YEAR")')
    c = c.replace('"DAYS STREAK"', '(sp.getString("app_lang", "en").equals("bn") ? "দিন" : "DAYS")')
    c = c.replace('"১ বছরের স্ট্রিক"', '(sp.getString("app_lang", "en").equals("bn") ? "১ বছর" : "1 YEAR")')
    c = c.replace('" দিনের স্ট্রিক"', '(sp.getString("app_lang", "en").equals("bn") ? "দিন" : "DAYS")')

    # তারিখের সিরিয়াল এবং সাইজ হুবহু মিলানো
    start = c.find('LinearLayout leftHeader =')
    if start == -1: start = c.find('android.widget.LinearLayout leftHeader =')
    end = c.find('LinearLayout rightHeader =', start)
    if end == -1: end = c.find('android.widget.LinearLayout rightHeader =', start)

    if start != -1 and end != -1:
        new_header = """android.widget.LinearLayout leftHeader = new android.widget.LinearLayout(this);
        leftHeader.setOrientation(android.widget.LinearLayout.VERTICAL);
        leftHeader.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        leftHeader.setGravity(android.view.Gravity.CENTER_VERTICAL);

        android.widget.TextView dEn = new android.widget.TextView(this);
        try { dEn.setText(lang.getGregorian(sdf.parse(selectedDate[0]))); } catch(Exception e) {}
        dEn.setTextColor(themeColors[3]); dEn.setTextSize(12); dEn.setTypeface(appFonts[0], android.graphics.Typeface.NORMAL);
        dEn.setPadding(0, 0, 0, (int)(2*DENSITY));
        leftHeader.addView(dEn);
        dEn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showGregorian(); }});

        android.widget.TextView dBn = new android.widget.TextView(this);
        try { dBn.setText(getBnDateStr(selectedDate[0], sp)); } catch(Exception e) {}
        dBn.setTextColor(themeColors[2]); dBn.setTextSize(14); dBn.setTypeface(appFonts[0], android.graphics.Typeface.BOLD);
        dBn.setPadding(0, 0, 0, (int)(4*DENSITY));
        leftHeader.addView(dBn);
        dBn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showBengaliCalendar(); }});

        android.widget.LinearLayout hRow = new android.widget.LinearLayout(this);
        hRow.setOrientation(android.widget.LinearLayout.HORIZONTAL); hRow.setGravity(android.view.Gravity.CENTER_VERTICAL);
        android.view.View moon = ui.getRoundImage("img_moon", 0, android.graphics.Color.TRANSPARENT, colorAccent);
        android.widget.LinearLayout.LayoutParams mLp = new android.widget.LinearLayout.LayoutParams((int)(16*DENSITY), (int)(16*DENSITY)); mLp.setMargins(0,0,(int)(8*DENSITY),0);
        moon.setLayoutParams(mLp); hRow.addView(moon);
        android.widget.TextView dHijri = new android.widget.TextView(this);
        try { dHijri.setText(ui.getHijriDate(sdf.parse(selectedDate[0]), sp.getInt("hijri_offset", 0))); } catch(Exception e) {}
        dHijri.setTextColor(colorAccent); dHijri.setTextSize(20); dHijri.setTypeface(appFonts[1], android.graphics.Typeface.BOLD);
        hRow.addView(dHijri); leftHeader.addView(hRow);
        hRow.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { calHelper.showHijri(); } });

        """
        c = c[:start] + new_header + c[end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Step 1 Done!")
else:
    print("❌ MainActivity.java Not Found!")
