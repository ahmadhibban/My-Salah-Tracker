import os
def apply():
    mf = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
    uf = "app/src/main/java/com/my/salah/tracker/app/UIComponents.java"
    if not os.path.exists(mf):
        for r, d, f in os.walk("."):
            if "MainActivity.java" in f: mf = os.path.join(r, "MainActivity.java")
            if "UIComponents.java" in f: uf = os.path.join(r, "UIComponents.java")
    with open(uf, 'r', encoding='utf-8') as f: uc = f.read().replace('\r\n', '\n')
    o_ui = """public View getPremiumCheckbox(String status, int activeColorHex) { 
        TextView tv = new TextView(activity);
        tv.setGravity(Gravity.CENTER); tv.setTextSize(14); 
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); tv.setLayoutParams(lp); 
        GradientDrawable gd = new GradientDrawable(); gd.setShape(GradientDrawable.OVAL); 
        if(status.equals("yes")) { gd.setColor(activeColorHex); tv.setText("✓"); tv.setTextColor(Color.WHITE);
        } 
        else if (status.equals("excused")) { gd.setColor(activeColorHex); tv.setText("🌸"); tv.setTextColor(Color.WHITE);
        } 
        else { gd.setColor(Color.TRANSPARENT); gd.setStroke((int)(2*DENSITY), themeColors[4]); tv.setText("");
        } 
        tv.setBackground(gd); return tv;
    }"""
    n_ui = """public View getPremiumCheckbox(String status, int activeColorHex) { 
        TextView tv = new TextView(activity); tv.setGravity(Gravity.CENTER); tv.setTextSize(14);
        boolean chk = status.equals("yes") || status.equals("excused"); float dp = chk ? 0f : 3f;
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams((int)((26+dp)*DENSITY), (int)((26+dp)*DENSITY)); tv.setLayoutParams(lp); 
        android.content.SharedPreferences sp = activity.getSharedPreferences("salah_pro_final", 0);
        boolean dk = sp.getBoolean("is_dark_mode", false);
        int sCol = chk ? activeColorHex : (dk ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE);
        int shCol = dk ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0");
        android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(shCol); sh.setCornerRadius(8f*DENSITY);
        android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(sCol); su.setCornerRadius(8f*DENSITY);
        if (!chk) su.setStroke((int)(1.5f*DENSITY), dk ? android.graphics.Color.parseColor("#333333") : android.graphics.Color.parseColor("#E0E0E0"));
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
        int off = (int)(dp * DENSITY); ld.setLayerInset(0, 0, off, 0, 0); ld.setLayerInset(1, 0, 0, 0, off);
        tv.setBackground(ld); if (chk) { tv.setText(status.equals("yes")?"✓":"🌸"); tv.setTextColor(android.graphics.Color.WHITE); } else tv.setText("");
        tv.setPadding(0, 0, 0, off); return tv;
    }"""
    uc = uc.replace(o_ui, n_ui)
    with open(uf, 'w', encoding='utf-8') as f: f.write(uc)
    with open(mf, 'r', encoding='utf-8') as f: mc = f.read().replace('\r\n', '\n')
    eng = """private SimpleDateFormat sdf;
    public android.graphics.drawable.Drawable getSafe3D(int c1, int c2, float r, float dp) {
        float d = getResources().getDisplayMetrics().density;
        android.graphics.drawable.GradientDrawable sh = new android.graphics.drawable.GradientDrawable(); sh.setColor(c2); sh.setCornerRadius(r);
        android.graphics.drawable.GradientDrawable su = new android.graphics.drawable.GradientDrawable(); su.setColor(c1); su.setCornerRadius(r);
        android.graphics.drawable.LayerDrawable ld = new android.graphics.drawable.LayerDrawable(new android.graphics.drawable.Drawable[]{sh, su});
        int o = (int)(dp * d); ld.setLayerInset(0, 0, o, 0, 0); ld.setLayerInset(1, 0, 0, 0, o); return ld;
    }"""
    if "getSafe3D" not in mc: mc = mc.replace("private SimpleDateFormat sdf;", eng)
    r = {
        """GradientDrawable pcBg = new GradientDrawable(GradientDrawable.Orientation.BR_TL, pColors);
        pcBg.setCornerRadius(20f * DENSITY); pCard.setBackground(pcBg);""":
        """int pm = isDayTime ? android.graphics.Color.parseColor("#FF9500") : android.graphics.Color.parseColor("#1A2980");
        int ps = isDayTime ? android.graphics.Color.parseColor("#C77600") : android.graphics.Color.parseColor("#0F184A");
        pCard.setBackground(getSafe3D(pm, ps, 20f*DENSITY, 6f)); pCard.setPadding((int)(20*DENSITY), (int)(pCardPadV*DENSITY), (int)(20*DENSITY), (int)(pCardPadV*DENSITY) + (int)(6f*DENSITY));""",

        """GradientDrawable tBg = new GradientDrawable(GradientDrawable.Orientation.BR_TL, isDarkTheme ? new int[]{Color.parseColor("#1A2980"), Color.parseColor("#26D0CE")} : new int[]{Color.parseColor("#FF9500"), Color.parseColor("#FFCC00")}); tBg.setCornerRadius(100f); themeToggleBtn.setBackground(tBg);""":
        """themeToggleBtn.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 2f)); themeToggleBtn.setPadding(0, 0, 0, (int)(2f*DENSITY));""",

        """View offBtn = ui.getRoundImage("img_offline_warning", 6, themeColors[5], android.graphics.Color.parseColor("#FF5252")); LinearLayout.LayoutParams offLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY));""":
        """View offBtn = ui.getRoundImage("img_offline_warning", 6, android.graphics.Color.TRANSPARENT, android.graphics.Color.parseColor("#FF5252")); offBtn.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 2f)); offBtn.setPadding(0, 0, 0, (int)(2f*DENSITY)); LinearLayout.LayoutParams offLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY));""",
        """View periodBtn = ui.getRoundImage("img_period", 6, themeColors[5], colorAccent); LinearLayout.LayoutParams pLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY));""":
        """View periodBtn = ui.getRoundImage("img_period", 6, android.graphics.Color.TRANSPARENT, colorAccent); periodBtn.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 2f)); periodBtn.setPadding(0, 0, 0, (int)(2f*DENSITY)); LinearLayout.LayoutParams pLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY));""",

        """View settingsBtn = ui.getRoundImage("img_settings", 6, themeColors[5], colorAccent);
        LinearLayout.LayoutParams sLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY));""":
        """View settingsBtn = ui.getRoundImage("img_settings", 6, android.graphics.Color.TRANSPARENT, colorAccent); settingsBtn.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 2f)); settingsBtn.setPadding(0, 0, 0, (int)(2f*DENSITY));
        LinearLayout.LayoutParams sLp = new LinearLayout.LayoutParams((int)(34 * DENSITY), (int)(34 * DENSITY));""",

        """GradientDrawable badgeBg = new GradientDrawable(); badgeBg.setCornerRadius(15f * DENSITY); badgeBg.setColor(colorAccent); badgeBg.setStroke(0, android.graphics.Color.TRANSPARENT);
        streakBadge.setTextColor(android.graphics.Color.WHITE);
        streakBadge.setText(streakCount >= 365 ? lang.get("1 YEAR STREAK") : lang.bnNum(streakCount) + " " + lang.get("DAYS STREAK"));
        LinearLayout.LayoutParams badgeLp = new LinearLayout.LayoutParams(-2, -2); badgeLp.setMargins(0, 0, 0, (int)(10*DENSITY)); streakBadge.setLayoutParams(badgeLp); streakBadge.setBackground(badgeBg); leftHeader.addView(streakBadge);""":
        """streakBadge.setTextColor(colorAccent);
        streakBadge.setText(streakCount >= 365 ? lang.get("1 YEAR STREAK") : lang.bnNum(streakCount) + " " + lang.get("DAYS STREAK"));
        LinearLayout.LayoutParams badgeLp = new LinearLayout.LayoutParams(-2, -2); badgeLp.setMargins(0, 0, 0, (int)(10*DENSITY)); streakBadge.setLayoutParams(badgeLp); streakBadge.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.WHITE, isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 20f*DENSITY, 3f)); streakBadge.setPadding((int)(10*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(4*DENSITY) + (int)(3f*DENSITY)); leftHeader.addView(streakBadge);"""
    }
    for old_t, new_t in r.items(): mc = mc.replace(old_t, new_t)

    r2 = {
        """t.setBackground(getProgressBorder(dKey, isSel)); cell.addView(t);""":
        """t.setBackground(getSafe3D(isSel ? colorAccent : themeColors[1], isSel ? (isDarkTheme?android.graphics.Color.parseColor("#0A0A0C"):android.graphics.Color.parseColor("#cbd5e0")) : themeColors[4], 8f*DENSITY, isSel ? 0f : 3f)); t.setPadding(0, 0, 0, isSel ? 0 : (int)(3f*DENSITY)); cell.addView(t);""",

        """GradientDrawable bg1 = new GradientDrawable(); bg1.setColor(themeColors[1]); bg1.setCornerRadius(15f * DENSITY); markAllBtn.setBackground(bg1);
        if (Build.VERSION.SDK_INT >= 21) markAllBtn.setElevation(isDarkTheme ? 0f : 10f);""":
        """markAllBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 15f*DENSITY, 4f)); markAllBtn.setPadding(0, 0, 0, (int)(4f*DENSITY));""",

        """GradientDrawable bg2 = new GradientDrawable(); bg2.setColor(themeColors[1]); bg2.setCornerRadius(15f * DENSITY); todayBtn.setBackground(bg2);
        if (Build.VERSION.SDK_INT >= 21) todayBtn.setElevation(isDarkTheme ? 0f : 10f);""":
        """todayBtn.setBackground(getSafe3D(themeColors[1], isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"), 15f*DENSITY, 4f)); todayBtn.setPadding(0, 0, 0, (int)(4f*DENSITY));""",

        """GradientDrawable cb = new GradientDrawable(); cb.setColor(stat.equals("excused") ? (isDarkTheme ? Color.parseColor("#1A1115") : Color.parseColor("#FCE4EC")) : themeColors[1]);
        cb.setCornerRadius(16f * DENSITY); cb.setStroke((int)(1.5f*DENSITY), stat.equals("excused") ? Color.parseColor("#FF4081") : (checked ? colorAccent : themeColors[4]));
        card.setBackground(cb);""":
        """int cM = stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1];
        int cS = isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0");
        card.setBackground(getSafe3D(cM, cS, 16f*DENSITY, 5f));
        card.setPadding((int)(15*DENSITY), (int)(cardPadV*DENSITY), (int)(20*DENSITY), (int)(cardPadV*DENSITY) + (int)(5f*DENSITY));""",

        """GradientDrawable customSunnahBg = new GradientDrawable(); customSunnahBg.setCornerRadius(12f*DENSITY); if(doneSunnahs > 0){customSunnahBg.setColor(colorAccent);sunnahBtn.setTextColor(Color.WHITE);}else{customSunnahBg.setColor(themeColors[5]);sunnahBtn.setTextColor(themeColors[2]);} 
            sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY));
            sunnahBtn.setBackground(customSunnahBg);""":
        """sunnahBtn.setBackground(getSafe3D(doneSunnahs > 0 ? colorAccent : themeColors[1], themeColors[4], 12f*DENSITY, 3f));
            sunnahBtn.setTextColor(doneSunnahs > 0 ? android.graphics.Color.WHITE : themeColors[2]);
            sunnahBtn.setPadding((int)(10*DENSITY), (int)(5*DENSITY), (int)(10*DENSITY), (int)(5*DENSITY) + (int)(3f*DENSITY));""",

        """TextView iconTxt = new TextView(this); iconTxt.setText(prayerIcons[i]); iconTxt.setTextSize(22f); iconTxt.setGravity(Gravity.CENTER);""":
        """TextView iconTxt = new TextView(this); iconTxt.setText(prayerIcons[i]); iconTxt.setTextSize(22f); iconTxt.setGravity(Gravity.CENTER);
        iconTxt.setBackground(getSafe3D(isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#F5F7FA"), isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#cbd5e0"), 100f, 2f));
        iconTxt.setPadding((int)(10*DENSITY), (int)(6*DENSITY), (int)(10*DENSITY), (int)(6*DENSITY) + (int)(2f*DENSITY));"""
    }
    for o, n in r2.items(): mc = mc.replace(o, n)
    with open(mf, 'w', encoding='utf-8') as f: f.write(mc)
    print("✔ Magic Applied safely! Rebuild your app now.")

apply()
