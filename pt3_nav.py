ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()

methods = """
    private void setupBottomNav() {
        bottomNav.removeAllViews();
        String[] titles = {lang.get("Salah"), lang.get("Stats"), lang.get("Habits")};
        String[] icons = {"img_tab_salah", "img_tab_stats", "img_tab_habits"};
        for(int i=0; i<3; i++) {
            final int idx = i; boolean isActive = (currentTab == i);
            android.widget.LinearLayout tab = new android.widget.LinearLayout(this); tab.setOrientation(android.widget.LinearLayout.VERTICAL); tab.setGravity(android.view.Gravity.CENTER);
            tab.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); tab.setPadding(0, (int)(12*DENSITY), 0, (int)(12*DENSITY));
            android.view.View icon = ui.getRoundImage(icons[i], 0, android.graphics.Color.TRANSPARENT, isActive ? colorAccent : themeColors[3]);
            android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(26*DENSITY), (int)(26*DENSITY)); icLp.setMargins(0,0,0,(int)(4*DENSITY)); icon.setLayoutParams(icLp);
            android.widget.TextView tv = new android.widget.TextView(this); tv.setText(titles[i]); tv.setTextSize(12); tv.setTypeface(isActive ? appFonts[1] : appFonts[0]); tv.setTextColor(isActive ? colorAccent : themeColors[3]);
            tab.addView(icon); tab.addView(tv);
            tab.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); switchTab(idx); });
            bottomNav.addView(tab);
        }
    }

    private void switchTab(int index) {
        currentTab = index; setupBottomNav(); fragmentContainer.removeAllViews();
        android.widget.ScrollView sv = new android.widget.ScrollView(this); sv.setFillViewport(true); sv.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
        contentArea = new android.widget.LinearLayout(this); contentArea.setOrientation(android.widget.LinearLayout.VERTICAL); sv.addView(contentArea, new android.widget.FrameLayout.LayoutParams(-1, -1));
        fragmentContainer.addView(sv);
        if(index == 0) loadTodayPageCore();
        else if(index == 1) loadStatsTab();
        else if(index == 2) loadHabitsTab();
    }

    private void loadStatsTab() {
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Stats")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        
        try {
            java.lang.reflect.Method m = StatsHelper.class.getDeclaredMethod("renderStats", android.widget.LinearLayout.class, android.app.AlertDialog.class, boolean.class);
            m.setAccessible(true);
            
            android.widget.TextView wT = new android.widget.TextView(this); wT.setText(lang.get("Weekly Statistics")); wT.setTextColor(themeColors[3]); wT.setTypeface(appFonts[1]); contentArea.addView(wT);
            android.widget.LinearLayout wC = new android.widget.LinearLayout(this); wC.setOrientation(android.widget.LinearLayout.VERTICAL); wC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY));
            android.graphics.drawable.GradientDrawable wBg = new android.graphics.drawable.GradientDrawable(); wBg.setColor(themeColors[1]); wBg.setCornerRadius(25f*DENSITY); wC.setBackground(wBg);
            android.widget.LinearLayout.LayoutParams wLp = new android.widget.LinearLayout.LayoutParams(-1, -2); wLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); wC.setLayoutParams(wLp);
            m.invoke(statsHelper, wC, null, true); wC.removeViewAt(wC.getChildCount()-1); contentArea.addView(wC);

            android.widget.TextView mT = new android.widget.TextView(this); mT.setText(lang.get("Monthly Statistics")); mT.setTextColor(themeColors[3]); mT.setTypeface(appFonts[1]); contentArea.addView(mT);
            android.widget.LinearLayout mC = new android.widget.LinearLayout(this); mC.setOrientation(android.widget.LinearLayout.VERTICAL); mC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY));
            android.graphics.drawable.GradientDrawable mBg = new android.graphics.drawable.GradientDrawable(); mBg.setColor(themeColors[1]); mBg.setCornerRadius(25f*DENSITY); mC.setBackground(mBg);
            android.widget.LinearLayout.LayoutParams mLp = new android.widget.LinearLayout.LayoutParams(-1, -2); mLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); mC.setLayoutParams(mLp);
            m.invoke(statsHelper, mC, null, false); mC.removeViewAt(mC.getChildCount()-1); contentArea.addView(mC);
        } catch(Exception e){}
    }

    private void loadHabitsTab() {
        contentArea.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
        android.widget.TextView h = new android.widget.TextView(this); h.setText(lang.get("Daily Habits")); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        
        // Ayat of the Day
        android.widget.LinearLayout ayatCard = new android.widget.LinearLayout(this); ayatCard.setOrientation(android.widget.LinearLayout.VERTICAL); ayatCard.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable aBg = new android.graphics.drawable.GradientDrawable(android.graphics.drawable.GradientDrawable.Orientation.TL_BR, new int[]{colorAccent, android.graphics.Color.parseColor("#1A2980")}); aBg.setCornerRadius(25f*DENSITY); ayatCard.setBackground(aBg);
        android.widget.LinearLayout.LayoutParams aLp = new android.widget.LinearLayout.LayoutParams(-1, -2); aLp.setMargins(0,0,0,(int)(20*DENSITY)); ayatCard.setLayoutParams(aLp);
        android.widget.TextView aTitle = new android.widget.TextView(this); aTitle.setText("✨ " + lang.get("Ayat of the Day")); aTitle.setTextColor(android.graphics.Color.WHITE); aTitle.setTextSize(14); aTitle.setTypeface(appFonts[1]); aTitle.setAlpha(0.8f); aTitle.setPadding(0,0,0,(int)(15*DENSITY)); ayatCard.addView(aTitle);
        String[] ar = {"فَإِنَّ مَعَ الْعُسْرِ يُسْرًا", "وَهُوَ مَعَكُمْ أَيْنَ مَا كُنتُمْ", "فَاذْكُرُونِي أَذْكُرْكُمْ"}; String[] bn = {"নিশ্চয়ই কষ্টের সাথেই রয়েছে স্বস্তি। (৯৪:৫)", "তোমরা যেখানেই থাকো না কেন, তিনি তোমাদের সাথেই আছেন। (৫৭:৪)", "তোমরা আমাকে স্মরণ করো, আমিও তোমাদের স্মরণ করব। (২:১৫২)"};
        int rIdx = java.util.Calendar.getInstance().get(java.util.Calendar.DAY_OF_YEAR) % ar.length;
        android.widget.TextView aAr = new android.widget.TextView(this); aAr.setText(ar[rIdx]); aAr.setTextColor(android.graphics.Color.WHITE); aAr.setTextSize(26); aAr.setTypeface(appFonts[1]); aAr.setGravity(android.view.Gravity.CENTER); aAr.setPadding(0,0,0,(int)(10*DENSITY)); ayatCard.addView(aAr);
        android.widget.TextView aBn = new android.widget.TextView(this); aBn.setText(bn[rIdx]); aBn.setTextColor(android.graphics.Color.WHITE); aBn.setTextSize(14); aBn.setTypeface(appFonts[0]); aBn.setGravity(android.view.Gravity.CENTER); ayatCard.addView(aBn);
        contentArea.addView(ayatCard);

        // Habit Cards Builder
        class HB {
            void add(String id, String title, String icon, String defVal) {
                android.widget.LinearLayout card = new android.widget.LinearLayout(MainActivity.this); card.setOrientation(android.widget.LinearLayout.HORIZONTAL); card.setGravity(android.view.Gravity.CENTER_VERTICAL); card.setPadding((int)(15*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));
                android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(themeColors[1]); cBg.setCornerRadius(20f*DENSITY); card.setBackground(cBg);
                android.widget.LinearLayout.LayoutParams cLp = new android.widget.LinearLayout.LayoutParams(-1, -2); cLp.setMargins(0,0,0,(int)(10*DENSITY)); card.setLayoutParams(cLp);
                android.view.View ic = ui.getRoundImage(icon, 8, themeColors[5], colorAccent); android.widget.LinearLayout.LayoutParams icLp = new android.widget.LinearLayout.LayoutParams((int)(45*DENSITY), (int)(45*DENSITY)); icLp.setMargins(0,0,(int)(15*DENSITY),0); ic.setLayoutParams(icLp); card.addView(ic);
                android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(title); tv.setTextColor(themeColors[2]); tv.setTypeface(appFonts[1]); tv.setTextSize(16); tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); card.addView(tv);
                android.widget.TextView valTv = new android.widget.TextView(MainActivity.this); valTv.setText(sp.getString(selectedDate[0]+"_"+id, defVal)); valTv.setTextColor(colorAccent); valTv.setTypeface(appFonts[1]); valTv.setTextSize(14); valTv.setPadding((int)(15*DENSITY),(int)(8*DENSITY),(int)(15*DENSITY),(int)(8*DENSITY));
                android.graphics.drawable.GradientDrawable vBg = new android.graphics.drawable.GradientDrawable(); vBg.setColor(themeColors[5]); vBg.setCornerRadius(12f*DENSITY); valTv.setBackground(vBg); card.addView(valTv);
                card.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); showHabitInput(id, title, valTv); });
                contentArea.addView(card);
            }
            void addZikr() {
                android.widget.LinearLayout card = new android.widget.LinearLayout(MainActivity.this); card.setOrientation(android.widget.LinearLayout.VERTICAL); card.setGravity(android.view.Gravity.CENTER); card.setPadding((int)(20*DENSITY), (int)(30*DENSITY), (int)(20*DENSITY), (int)(30*DENSITY));
                android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(themeColors[1]); cBg.setCornerRadius(25f*DENSITY); card.setBackground(cBg); card.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, -2));
                android.widget.TextView tv = new android.widget.TextView(MainActivity.this); tv.setText(lang.get("Daily Zikr")); tv.setTextColor(themeColors[3]); tv.setTypeface(appFonts[1]); tv.setTextSize(14); card.addView(tv);
                final android.widget.TextView countTv = new android.widget.TextView(MainActivity.this); countTv.setText(lang.bnNum(sp.getInt(selectedDate[0]+"_zikr", 0))); countTv.setTextColor(colorAccent); countTv.setTypeface(appFonts[1]); countTv.setTextSize(60); countTv.setPadding(0,(int)(10*DENSITY),0,(int)(10*DENSITY)); card.addView(countTv);
                card.setOnClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); int c = sp.getInt(selectedDate[0]+"_zikr", 0) + 1; sp.edit().putInt(selectedDate[0]+"_zikr", c).apply(); countTv.setText(lang.bnNum(c)); countTv.animate().scaleX(1.2f).scaleY(1.2f).setDuration(50).withEndAction(()->countTv.animate().scaleX(1f).scaleY(1f).setDuration(150).start()).start(); });
                card.setOnLongClickListener(v -> { v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); sp.edit().putInt(selectedDate[0]+"_zikr", 0).apply(); countTv.setText(lang.bnNum(0)); return true; });
                contentArea.addView(card);
            }
        }
        HB hb = new HB();
        hb.add("roza", lang.get("Fasting (Roza)"), "img_habit_roza", lang.get("Not Fasting"));
        hb.add("quran", lang.get("Quran Recitation"), "img_habit_quran", "0 " + lang.get("Pages/Surah"));
        hb.addZikr();
    }

    private void showHabitInput(String id, String title, android.widget.TextView valTv) {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY));
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        android.widget.TextView t = new android.widget.TextView(this); t.setText(title); t.setTextColor(themeColors[2]); t.setTextSize(20); t.setTypeface(appFonts[1]); t.setGravity(android.view.Gravity.CENTER); t.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(t);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER);
        
        if(id.equals("roza")) {
            String[] opts = {lang.get("Fard"), lang.get("Nafl"), lang.get("Qaza"), lang.get("Not Fasting")};
            for(String opt : opts) {
                android.widget.TextView b = new android.widget.TextView(this); b.setText(opt); b.setTextColor(themeColors[2]); b.setTextSize(16); b.setGravity(android.view.Gravity.CENTER); b.setPadding(0,(int)(15*DENSITY),0,(int)(15*DENSITY));
                android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setColor(themeColors[4]); bg.setCornerRadius(15f*DENSITY); b.setBackground(bg);
                android.widget.LinearLayout.LayoutParams lp = new android.widget.LinearLayout.LayoutParams(-1, -2); lp.setMargins(0,0,0,(int)(10*DENSITY)); b.setLayoutParams(lp);
                b.setOnClickListener(v -> { sp.edit().putString(selectedDate[0]+"_"+id, opt).apply(); valTv.setText(opt); ad.dismiss(); }); main.addView(b);
            }
        } else {
            final android.widget.EditText et = new android.widget.EditText(this); et.setHint(lang.get("Pages/Surah")); et.setTextColor(themeColors[2]); et.setHintTextColor(themeColors[3]);
            android.graphics.drawable.GradientDrawable ibg = new android.graphics.drawable.GradientDrawable(); ibg.setColor(themeColors[4]); ibg.setCornerRadius(15f*DENSITY); et.setBackground(ibg); et.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY));
            main.addView(et, new android.widget.LinearLayout.LayoutParams(-1, -2));
            android.widget.Button btn = new android.widget.Button(this); btn.setText(lang.get("OK")); btn.setTextColor(android.graphics.Color.WHITE); android.graphics.drawable.GradientDrawable bbg = new android.graphics.drawable.GradientDrawable(); bbg.setColor(colorAccent); bbg.setCornerRadius(15f*DENSITY); btn.setBackground(bbg);
            android.widget.LinearLayout.LayoutParams blp = new android.widget.LinearLayout.LayoutParams(-1, (int)(50*DENSITY)); blp.setMargins(0,(int)(20*DENSITY),0,0); main.addView(btn, blp);
            btn.setOnClickListener(v -> { String txt = et.getText().toString().trim(); if(!txt.isEmpty()) { sp.edit().putString(selectedDate[0]+"_"+id, txt).apply(); valTv.setText(txt); } ad.dismiss(); });
        }
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(300*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp); applyFont(main, appFonts[0], appFonts[1]); ad.show();
    }
"""

c = c.replace('private void loadTodayPage() {', 'private void loadTodayPageCore() {')
c = c.rstrip()
if c.endswith('}'): c = c[:-1].rstrip()
c += "\n" + methods + "\n}\n"

open(ma, 'w').write(c)
print("✅ Part 3 Done! Everything is set up perfectly.")
