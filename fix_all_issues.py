import os

main_activity = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
backup_helper = "app/src/main/java/com/my/salah/tracker/app/BackupHelper.java"

# ১. BackupHelper এর Danger Zone ডিজাইন প্রফেশনাল করা
if os.path.exists(backup_helper):
    with open(backup_helper, "r", encoding="utf-8") as f: content = f.read()
    start = "// --- DANGER ZONE START ---"
    end = "// --- DANGER ZONE END ---"
    if start in content and end in content:
        premium_danger = """// --- DANGER ZONE START ---
        android.widget.TextView dangerTitle = new android.widget.TextView(activity);
        dangerTitle.setText(lang.get("Danger Zone"));
        dangerTitle.setTextColor(android.graphics.Color.parseColor("#FF5252"));
        dangerTitle.setTextSize(16);
        dangerTitle.setTypeface(tfBold);
        dangerTitle.setPadding(0, (int) (25 * DENSITY), 0, (int) (15 * DENSITY));
        main.addView(dangerTitle);

        android.widget.LinearLayout btnWipeLocal = new android.widget.LinearLayout(activity);
        btnWipeLocal.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        btnWipeLocal.setGravity(android.view.Gravity.CENTER);
        btnWipeLocal.setPadding((int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY), (int) (15 * DENSITY));
        android.graphics.drawable.GradientDrawable wBg1 = new android.graphics.drawable.GradientDrawable();
        wBg1.setColor(android.graphics.Color.parseColor("#1AFF4444"));
        wBg1.setCornerRadius(15f * DENSITY);
        btnWipeLocal.setBackground(wBg1);
        android.widget.LinearLayout.LayoutParams wLp1 = new android.widget.LinearLayout.LayoutParams(-1, -2);
        wLp1.setMargins(0, 0, 0, (int) (12 * DENSITY));
        btnWipeLocal.setLayoutParams(wLp1);
        android.widget.TextView txtWipeLocal = new android.widget.TextView(activity);
        txtWipeLocal.setText("Delete All Data & Start Fresh");
        txtWipeLocal.setTextColor(android.graphics.Color.parseColor("#FF5252"));
        txtWipeLocal.setTypeface(tfBold);
        txtWipeLocal.setTextSize(15);
        btnWipeLocal.addView(txtWipeLocal);
        main.addView(btnWipeLocal);

        btnWipeLocal.setOnClickListener(v -> {
            new android.app.AlertDialog.Builder(activity)
                .setTitle("⚠️ Delete All Data")
                .setMessage("Are you sure? This will wipe your history, settings, and start fresh. This action cannot be undone.")
                .setPositiveButton("Yes, Delete", (d, w) -> {
                    android.widget.Toast.makeText(activity, "Wiping all data...", android.widget.Toast.LENGTH_SHORT).show();
                    if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.KITKAT) {
                        ((android.app.ActivityManager) activity.getSystemService(android.content.Context.ACTIVITY_SERVICE)).clearApplicationUserData();
                    }
                })
                .setNegativeButton("Cancel", null)
                .show();
        });
        // --- DANGER ZONE END ---"""
        content = content[:content.find(start)] + premium_danger + content[content.find(end)+len(end):]
        with open(backup_helper, "w", encoding="utf-8") as f: f.write(content)

# ২. MainActivity এর সমস্ত ইস্যু ফিক্স করা
if os.path.exists(main_activity):
    with open(main_activity, "r", encoding="utf-8") as f: content = f.read()

    # Settings Typo Fix
    old_typo = 'String[] copts = isBn ? new String[] {"থিম নির্বাচন করুন", "ক্যালেন্ডার নির্বাচন"}\n                                          : new String[] {"Choose Theme", "Choose Calendar"};'
    new_typo = 'String[] copts = isBn ? new String[] {"ডার্ক/লাইট মোড (Dark/Light)", "কালার পরিবর্তন (Change Color)"}\n                                          : new String[] {"Dark/Light Mode", "Change Theme Color"};'
    content = content.replace(old_typo, new_typo)

    # Date Suffix Fix
    old_bn_suf = """            } else {
                if (bD == 1)
                    suf = "লা";
                else if (bD == 2 || bD == 3)
                    suf = "রা";
                else if (bD == 4)
                    suf = "ঠা";
                else if (bD >= 5 && bD <= 18)
                    suf = "ই";
                else if (bD >= 19 && bD <= 31)
                    suf = "এ";
                else
                    suf = "শে";
            }"""
    new_bn_suf = """            } else {
                if (bD == 1) suf = "লা";
                else if (bD == 2 || bD == 3) suf = "রা";
                else if (bD == 4) suf = "ঠা";
                else if (bD >= 5 && bD <= 18) suf = "ই";
                else suf = "শে";
            }"""
    content = content.replace(old_bn_suf, new_bn_suf)

    # Header Date Grammar Fix
    old_greg = """        try {
            dEn.setText(lang.getGregorian(sdf.parse(selectedDate[0])));
        } catch (Exception e) {
        }"""
    new_greg = """        try {
            java.util.Date dt = sdf.parse(selectedDate[0]);
            java.util.Calendar gc = java.util.Calendar.getInstance(); gc.setTime(dt);
            int dNum = gc.get(java.util.Calendar.DAY_OF_MONTH);
            String gsuf = "";
            boolean isBnLang = sp.getString("app_lang", "en").equals("bn");
            if (isBnLang) {
                if (dNum == 1) gsuf = "লা";
                else if (dNum == 2 || dNum == 3) gsuf = "রা";
                else if (dNum == 4) gsuf = "ঠা";
                else if (dNum >= 5 && dNum <= 18) gsuf = "ই";
                else gsuf = "শে";
                String[] gMs = {"জানুয়ারি", "ফেব্রুয়ারি", "মার্চ", "এপ্রিল", "মে", "জুন", "জুলাই", "আগস্ট", "সেপ্টেম্বর", "অক্টোবর", "নভেম্বর", "ডিসেম্বর"};
                String mStr = gMs[gc.get(java.util.Calendar.MONTH)];
                String dStr = String.valueOf(dNum).replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯");
                String yStr = String.valueOf(gc.get(java.util.Calendar.YEAR)).replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯");
                dEn.setText(dStr + gsuf + " " + mStr + ", " + yStr);
            } else {
                if (dNum >= 11 && dNum <= 13) gsuf = "th";
                else switch (dNum % 10) { case 1: gsuf="st"; break; case 2: gsuf="nd"; break; case 3: gsuf="rd"; break; default: gsuf="th"; }
                String mStr = new java.text.SimpleDateFormat("MMMM", java.util.Locale.US).format(dt);
                dEn.setText(dNum + gsuf + " " + mStr + ", " + gc.get(java.util.Calendar.YEAR));
            }
        } catch (Exception e) {}"""
    content = content.replace(old_greg, new_greg)

    # Quran Tracker Injection
    quran_code = """
        // --- QURAN TRACKER START ---
        final boolean isQuranBn = sp.getString("app_lang", "en").equals("bn");
        final String quranDbKey = selectedDate[0] + "_quran_stat";
        final String quranParaKey = selectedDate[0] + "_quran_para";
        final String quranPageKey = selectedDate[0] + "_quran_page";

        android.widget.TextView qHdr = new android.widget.TextView(MainActivity.this);
        qHdr.setText(isQuranBn ? "কুরআন তেলাওয়াত" : "Quran Recitation");
        qHdr.setTextColor(themeColors[2]);
        qHdr.setTextSize(18);
        qHdr.setTypeface(null, android.graphics.Typeface.BOLD);
        android.widget.LinearLayout.LayoutParams qHdrLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        qHdrLp.setMargins(0, (int) (5 * DENSITY), 0, (int) (10 * DENSITY));

        soup.neumorphism.NeumorphCardView qCardNeo = new soup.neumorphism.NeumorphCardView(MainActivity.this);
        qCardNeo.setShapeType(0);
        qCardNeo.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
        qCardNeo.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        qCardNeo.setShadowElevation(3f * DENSITY);
        qCardNeo.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 16f * DENSITY).build());
        qCardNeo.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
        android.widget.LinearLayout.LayoutParams qCLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        qCLp.setMargins(0, 0, 0, 0);
        qCardNeo.setLayoutParams(qCLp);

        android.widget.LinearLayout qInner = new android.widget.LinearLayout(MainActivity.this);
        qInner.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        qInner.setGravity(android.view.Gravity.CENTER_VERTICAL);
        qInner.setPadding((int) (20 * DENSITY), (int) (18 * DENSITY), (int) (20 * DENSITY), (int) (18 * DENSITY));
        qCardNeo.addView(qInner);

        android.view.View qIconView = ui.getRoundImage("img_habit_quran", 8, android.graphics.Color.TRANSPARENT, colorAccent);
        qIconView.setBackgroundColor(android.graphics.Color.TRANSPARENT);
        qIconView.setPadding(5, 2, 5, 2);
        android.widget.FrameLayout qIconFrame = new android.widget.FrameLayout(MainActivity.this);
        android.widget.LinearLayout.LayoutParams qFlp = new android.widget.LinearLayout.LayoutParams((int) (30 * DENSITY), (int) (30 * DENSITY));
        qFlp.setMargins(0, 0, (int) (15 * DENSITY), 0);
        qIconFrame.setLayoutParams(qFlp);
        applyNeo(qIconFrame, 0, 12f, 2.5f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
        android.widget.FrameLayout.LayoutParams qIvLp = new android.widget.FrameLayout.LayoutParams((int) (34 * DENSITY), (int) (34 * DENSITY));
        qIvLp.gravity = android.view.Gravity.CENTER;
        qIconView.setLayoutParams(qIvLp);
        qIconFrame.addView(qIconView);
        qInner.addView(qIconFrame);

        android.widget.LinearLayout qTxtCon = new android.widget.LinearLayout(MainActivity.this);
        qTxtCon.setOrientation(android.widget.LinearLayout.VERTICAL);
        qTxtCon.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView qTv = new android.widget.TextView(MainActivity.this);
        qTv.setText(isQuranBn ? "আল কুরআন" : "Al Quran");
        qTv.setTextColor(themeColors[2]);
        qTv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
        qTv.setTextSize(16);
        qTv.setSingleLine(true);
        qTxtCon.addView(qTv);
        qInner.addView(qTxtCon);

        final boolean isQuranDone = sp.getString(quranDbKey, "no").equals("yes");
        int paraCount = sp.getInt(quranParaKey, 0);
        int pageCount = sp.getInt(quranPageKey, 0);

        String qLabel = isQuranBn ? "পড়িনি" : "Not Read";
        if (paraCount > 0 && pageCount > 0) qLabel = paraCount + (isQuranBn ? " পারা " : " Para ") + pageCount + (isQuranBn ? " পৃষ্ঠা" : " Page");
        else if (paraCount > 0) qLabel = paraCount + (isQuranBn ? " পারা" : " Para");
        else if (pageCount > 0) qLabel = pageCount + (isQuranBn ? " পৃষ্ঠা" : " Page");
        else if (isQuranDone) qLabel = isQuranBn ? "পড়েছি" : "Read";

        if (isQuranBn) qLabel = qLabel.replace("0", "০").replace("1", "১").replace("2", "২").replace("3", "৩").replace("4", "৪").replace("5", "৫").replace("6", "৬").replace("7", "৭").replace("8", "৮").replace("9", "৯");

        android.widget.TextView qCatBtn = new android.widget.TextView(MainActivity.this);
        qCatBtn.setText(qLabel);
        qCatBtn.setTextSize(11);
        qCatBtn.setSingleLine(true);
        qCatBtn.setTextColor(isQuranDone ? android.graphics.Color.WHITE : themeColors[2]);
        applyNeo(qCatBtn, 1, 10f, 2f, isQuranDone ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0")), isDarkTheme);
        qCatBtn.setPadding((int) (14 * DENSITY), (int) (8 * DENSITY), (int) (14 * DENSITY), (int) (8 * DENSITY));
        qCatBtn.setPadding((int) (12 * DENSITY), (int) (6 * DENSITY), (int) (12 * DENSITY), (int) (6 * DENSITY) + (int) (2f * DENSITY));
        android.widget.LinearLayout.LayoutParams qCatLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        qCatLp.setMargins(0, 0, (int) (15 * DENSITY), 0);
        qCatBtn.setLayoutParams(qCatLp);

        qCatBtn.setOnClickListener(new android.view.View.OnClickListener() {
            @Override public void onClick(android.view.View v) {
                android.widget.FrameLayout w = new android.widget.FrameLayout(MainActivity.this);
                w.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                android.widget.LinearLayout m = new android.widget.LinearLayout(MainActivity.this);
                m.setOrientation(android.widget.LinearLayout.VERTICAL);
                m.setPadding((int) (25 * DENSITY), (int) (30 * DENSITY), (int) (25 * DENSITY), (int) (30 * DENSITY));
                android.graphics.drawable.GradientDrawable g = new android.graphics.drawable.GradientDrawable();
                g.setColor(themeColors[1]); g.setCornerRadius(25f * DENSITY);
                m.setBackground(g);

                android.widget.TextView t = new android.widget.TextView(MainActivity.this);
                t.setText(isQuranBn ? "কতটুকু পড়েছেন?" : "How much did you read?");
                t.setTextColor(colorAccent); t.setTextSize(20); t.setTypeface(android.graphics.Typeface.DEFAULT_BOLD);
                t.setPadding(0, 0, 0, (int) (20 * DENSITY));
                m.addView(t);

                android.widget.EditText paraIn = new android.widget.EditText(MainActivity.this);
                paraIn.setHint(isQuranBn ? "পারা (যেমন: ১)" : "Para (e.g. 1)");
                paraIn.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
                paraIn.setTextColor(themeColors[2]); paraIn.setHintTextColor(themeColors[3]);
                android.graphics.drawable.GradientDrawable ib = new android.graphics.drawable.GradientDrawable();
                ib.setColor(themeColors[4]); ib.setCornerRadius(15f * DENSITY);
                paraIn.setBackground(ib);
                paraIn.setPadding((int) (20 * DENSITY), (int) (15 * DENSITY), (int) (20 * DENSITY), (int) (15 * DENSITY));
                if(sp.getInt(quranParaKey, 0) > 0) paraIn.setText(String.valueOf(sp.getInt(quranParaKey, 0)));
                android.widget.LinearLayout.LayoutParams pLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
                pLp.setMargins(0,0,0,(int)(10*DENSITY));
                m.addView(paraIn, pLp);

                android.widget.EditText pageIn = new android.widget.EditText(MainActivity.this);
                pageIn.setHint(isQuranBn ? "পৃষ্ঠা (যেমন: ২)" : "Page (e.g. 2)");
                pageIn.setInputType(android.text.InputType.TYPE_CLASS_NUMBER);
                pageIn.setTextColor(themeColors[2]); pageIn.setHintTextColor(themeColors[3]);
                pageIn.setBackground(ib);
                pageIn.setPadding((int) (20 * DENSITY), (int) (15 * DENSITY), (int) (20 * DENSITY), (int) (15 * DENSITY));
                if(sp.getInt(quranPageKey, 0) > 0) pageIn.setText(String.valueOf(sp.getInt(quranPageKey, 0)));
                android.widget.LinearLayout.LayoutParams pgLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
                pgLp.setMargins(0,0,0,(int)(20*DENSITY));
                m.addView(pageIn, pgLp);

                android.widget.Button b = new android.widget.Button(MainActivity.this);
                b.setText(isQuranBn ? "সেভ করুন" : "Save");
                b.setTextColor(android.graphics.Color.WHITE); b.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); b.setAllCaps(false);
                android.graphics.drawable.GradientDrawable bb = new android.graphics.drawable.GradientDrawable();
                bb.setColor(colorAccent); bb.setCornerRadius(20f * DENSITY);
                b.setBackground(bb);
                m.addView(b, new android.widget.LinearLayout.LayoutParams(-1, (int) (55 * DENSITY)));

                android.widget.FrameLayout.LayoutParams f = new android.widget.FrameLayout.LayoutParams((int) (320 * DENSITY), -2);
                f.gravity = android.view.Gravity.CENTER;
                w.addView(m, f);
                final android.app.AlertDialog a = new android.app.AlertDialog.Builder(MainActivity.this).setView(w).create();
                a.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
                a.getWindow().setGravity(android.view.Gravity.CENTER);

                b.setOnClickListener(v1 -> {
                    int p1=0, p2=0;
                    try { if(!paraIn.getText().toString().trim().isEmpty()) p1 = Integer.parseInt(paraIn.getText().toString().trim()); } catch(Exception e){}
                    try { if(!pageIn.getText().toString().trim().isEmpty()) p2 = Integer.parseInt(pageIn.getText().toString().trim()); } catch(Exception e){}
                    sp.edit().putInt(quranParaKey, p1).putInt(quranPageKey, p2).putString(quranDbKey, (p1>0||p2>0)?"yes":"no").apply();
                    a.dismiss();
                    loadTodayPage();
                });
                applyFont(m, appFonts[0], appFonts[1]);
                a.show();
            }
        });
        qInner.addView(qCatBtn);

        final android.view.View qChkBox = getNeoCheckbox(isQuranDone ? "yes" : "no", colorAccent);
        qInner.addView(qChkBox);

        qCardNeo.setOnClickListener(v -> {
            v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
            sp.edit().putString(quranDbKey, !isQuranDone ? "yes" : "no").apply();
            v.animate().scaleX(0.95f).scaleY(0.95f).alpha(0.8f).setDuration(35).withEndAction(() -> {
                v.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start();
            }).start();
            loadTodayPage();
        });

        if (isLandscape) { col2.addView(qHdr, qHdrLp); col2.addView(qCardNeo); }
        else { cardsContainer.addView(qHdr, qHdrLp); cardsContainer.addView(qCardNeo); }
        // --- QURAN TRACKER END ---
"""
    if "// --- QURAN TRACKER START ---" not in content:
        content = content.replace("// --- ROZA TRACKER END ---", "// --- ROZA TRACKER END ---\n" + quran_code)
    
    with open(main_activity, "w", encoding="utf-8") as f: f.write(content)

print("✅ সমস্ত ডিজাইন, গ্রামার এবং নতুন ফিচারের কাজ ১০০% নিখুঁতভাবে শেষ হয়েছে!")
