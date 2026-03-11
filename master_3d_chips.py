import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "for(int i=0; i<6; i++) {"
end_marker = "cardsContainer.setAlpha(0f);"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    new_code = """for(int i=0; i<6; i++) {
            final String name = AppConstants.PRAYERS[i];
            final String key = selectedDate[0]+"_"+name; 
            final String stat = getFardStat(todayRec, name); 
            final boolean checked = stat.equals("yes") || stat.equals("excused");
            final boolean isQaza = getQazaStat(todayRec, name);
            
            // ১. বড় প্লেট (Outer Card)
            final LinearLayout card = new LinearLayout(this); 
            card.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY)); 
            card.setGravity(android.view.Gravity.CENTER_VERTICAL);
            card.setOrientation(LinearLayout.HORIZONTAL);
            
            int plateCol = themeColors[1];
            if (!isDarkTheme) plateCol = android.graphics.Color.parseColor("#F1F5F9");
            
            final android.graphics.drawable.GradientDrawable plateBg = new android.graphics.drawable.GradientDrawable(); 
            plateBg.setColor(stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : plateCol);
            plateBg.setCornerRadius(24f * DENSITY); 
            plateBg.setStroke((int)(1f*DENSITY), stat.equals("excused") ? android.graphics.Color.parseColor("#EC4899") : (checked ? colorAccent : android.graphics.Color.TRANSPARENT));
            card.setBackground(plateBg); 
            if(android.os.Build.VERSION.SDK_INT>=23) card.setForeground(card.getContext().getDrawable(android.R.attr.selectableItemBackground)); 
            
            LinearLayout.LayoutParams cLp = new LinearLayout.LayoutParams(-1, -2); 
            cLp.setMargins(0, 0, 0, i==5 ? 0 : (int)(12*DENSITY)); 
            card.setLayoutParams(cLp);
            
            // ইনার চিপের কালার
            int chipColor = isDarkTheme ? android.graphics.Color.parseColor("#2C2C2E") : android.graphics.Color.parseColor("#FFFFFF");
            if(stat.equals("excused")) chipColor = isDarkTheme ? android.graphics.Color.parseColor("#331520") : android.graphics.Color.parseColor("#FBCFE8");
            
            // ২. প্রথম বক্স (আইকন এবং নামাজের নাম)
            final LinearLayout infoChip = new LinearLayout(this);
            infoChip.setOrientation(LinearLayout.HORIZONTAL);
            infoChip.setGravity(android.view.Gravity.CENTER_VERTICAL);
            infoChip.setPadding((int)(10*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
            android.graphics.drawable.GradientDrawable infoBg = new android.graphics.drawable.GradientDrawable(); infoBg.setColor(chipColor); infoBg.setCornerRadius(18f * DENSITY);
            infoChip.setBackground(infoBg);
            if(android.os.Build.VERSION.SDK_INT >= 21) infoChip.setElevation(checked ? 0 : 4f * DENSITY); 
            
            LinearLayout.LayoutParams infoLp = new LinearLayout.LayoutParams(0, -2, 1f);
            infoLp.setMargins(0, 0, (int)(8*DENSITY), 0);
            infoChip.setLayoutParams(infoLp);
            
            android.view.View iconView = ui.getRoundImage(pImgs[i], pPaddings[i], android.graphics.Color.TRANSPARENT, colorAccent); 
            LinearLayout.LayoutParams icCardLp = new LinearLayout.LayoutParams((int)(38*DENSITY), (int)(38*DENSITY)); 
            icCardLp.setMargins(0,0,(int)(12*DENSITY),0); iconView.setLayoutParams(icCardLp); 
            infoChip.addView(iconView);
            
            LinearLayout textContainer = new LinearLayout(this); textContainer.setOrientation(LinearLayout.VERTICAL);
            LinearLayout titleRow = new LinearLayout(this); titleRow.setOrientation(LinearLayout.HORIZONTAL); titleRow.setGravity(android.view.Gravity.CENTER_VERTICAL);
            TextView tv = new TextView(this); tv.setSingleLine(true); tv.setEllipsize(android.text.TextUtils.TruncateAt.END); tv.setText(lang.get(name)); tv.setTextColor(stat.equals("excused") ? android.graphics.Color.parseColor("#EC4899") : themeColors[2]); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); tv.setTextSize(16); 
            titleRow.addView(tv);
            
            if (isQaza && stat.equals("no")) {
                TextView qBadge = new TextView(this);
                qBadge.setSingleLine(true); qBadge.setEllipsize(android.text.TextUtils.TruncateAt.END);
                qBadge.setText(lang.get("QAZA")); qBadge.setTextColor(themeColors[2]); qBadge.setTextSize(11); qBadge.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); qBadge.setPadding((int)(6*DENSITY), (int)(2*DENSITY), (int)(6*DENSITY), (int)(2*DENSITY)); 
                android.graphics.drawable.GradientDrawable qBg = new android.graphics.drawable.GradientDrawable(); qBg.setColor(themeColors[5]); qBg.setCornerRadius(12f * DENSITY); qBadge.setBackground(qBg);
                LinearLayout.LayoutParams qLp = new LinearLayout.LayoutParams(-2, -2); qLp.setMargins((int)(8*DENSITY), 0, 0, 0); qBadge.setLayoutParams(qLp); titleRow.addView(qBadge);
            }
            textContainer.addView(titleRow); infoChip.addView(textContainer);
            card.addView(infoChip);
            
            // ৩. দ্বিতীয় বক্স (সুন্নাহ এবং নফল)
            final int finalI = i;
            if (AppConstants.SUNNAHS[i].length > 0 && !stat.equals("excused")) {
                TextView sunnahBtn = new TextView(this);
                sunnahBtn.setSingleLine(true); sunnahBtn.setEllipsize(android.text.TextUtils.TruncateAt.END);
                int doneSunnahs = 0; int totalS = AppConstants.SUNNAHS[i].length; 
                for(String sName : AppConstants.SUNNAHS[i]) { if (sp.getString(selectedDate[0]+"_"+name+"_Sunnah_"+sName, "no").equals("yes")) doneSunnahs++; }
                String cStr = sp.getString("custom_nafl_" + name, "");
                if(!cStr.isEmpty()) { for(String cN : cStr.split(",")) { if(cN.contains(":")) cN = cN.split(":")[0]; totalS++; if("yes".equals(sp.getString(selectedDate[0]+"_"+name+"_Custom_"+cN, "no"))) doneSunnahs++; } }
                String sText = totalS > 1 ? (lang.get("Extras") + " (" + lang.bnNum(doneSunnahs) + "/" + lang.bnNum(totalS) + ")") : (i == 5 ? lang.get("Tahajjud") : lang.get("Sunnah"));
                sunnahBtn.setText(sText); sunnahBtn.setTextSize(14); 
                
                android.graphics.drawable.GradientDrawable customSunnahBg = new android.graphics.drawable.GradientDrawable(); customSunnahBg.setCornerRadius(18f * DENSITY);
                if(doneSunnahs > 0){customSunnahBg.setColor(colorAccent);sunnahBtn.setTextColor(android.graphics.Color.WHITE);}else{customSunnahBg.setColor(chipColor);sunnahBtn.setTextColor(themeColors[2]);} 
                sunnahBtn.setPadding((int)(12*DENSITY), (int)(16*DENSITY), (int)(12*DENSITY), (int)(16*DENSITY));
                sunnahBtn.setBackground(customSunnahBg); 
                if(android.os.Build.VERSION.SDK_INT >= 21) sunnahBtn.setElevation(doneSunnahs > 0 ? 0 : 4f * DENSITY);
                
                LinearLayout.LayoutParams customSunnahLp = new LinearLayout.LayoutParams(-2, -2); customSunnahLp.setMargins(0, 0, (int)(8*DENSITY), 0); sunnahBtn.setLayoutParams(customSunnahLp);
                sunnahBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showSunnahDialog(name, AppConstants.SUNNAHS[finalI]); } }); 
                card.addView(sunnahBtn);
            }
            
            // ৪. তৃতীয় বক্স (চেকবক্স)
            final FrameLayout chkContainer = new FrameLayout(this);
            android.graphics.drawable.GradientDrawable chkBg = new android.graphics.drawable.GradientDrawable(); chkBg.setColor(chipColor); chkBg.setCornerRadius(18f * DENSITY);
            chkContainer.setBackground(chkBg);
            chkContainer.setPadding((int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY), (int)(8*DENSITY));
            if(android.os.Build.VERSION.SDK_INT >= 21) chkContainer.setElevation(checked ? 0 : 4f * DENSITY);
            
            chkContainer.addView(ui.getPremiumCheckbox(stat, colorAccent));
            card.addView(chkContainer);
            
            // ৫. জিরো-ফ্ল্যাশ (Zero-Flash) ক্লিক ইভেন্ট (RemoveAllViews চিরতরে বন্ধ)
            card.setOnClickListener(new android.view.View.OnClickListener() { 
                @Override public void onClick(final android.view.View v) {
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); 
                    SalahRecord r = getRoomRecord(selectedDate[0]);
                    String currentStat = getFardStat(r, name);
                    if (currentStat.equals("excused")) { 
                        setFardStat(r, name, "no"); updateRoomRecord(r);
                        sp.edit().putString(key, "no").apply(); fbHelper.save(selectedDate[0], name, "no"); 
                        v.postDelayed(new Runnable() { @Override public void run() { loadTodayPage(); refreshWidget(); }}, 50);
                        return; 
                    }
                    
                    boolean wasChecked = currentStat.equals("yes"); 
                    String newVal = !wasChecked ? "yes" : "no"; 
                    
                    if(newVal.equals("yes") && getQazaStat(r, name)) { setQazaStat(r, name, false); sp.edit().putBoolean(key+"_qaza", false).apply(); }
                    setFardStat(r, name, newVal); updateRoomRecord(r);
                    sp.edit().putString(key, newVal).apply(); fbHelper.save(selectedDate[0], name, newVal); 
                    
                    v.animate().scaleX(0.97f).scaleY(0.97f).setDuration(100).withEndAction(new Runnable() { @Override public void run() { v.animate().scaleX(1f).scaleY(1f).setDuration(250).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); } }).start();
                    
                    // স্ক্রিন রিলোড না করে শুধুমাত্র ভেতরের ডিজাইনগুলো ডাইনামিক আপডেট করা হচ্ছে!
                    chkContainer.removeAllViews(); chkContainer.addView(ui.getPremiumCheckbox(newVal, colorAccent));
                    plateBg.setStroke((int)(1f*DENSITY), newVal.equals("yes") ? colorAccent : android.graphics.Color.TRANSPARENT);
                    
                    if(android.os.Build.VERSION.SDK_INT >= 21) {
                        infoChip.setElevation(newVal.equals("yes") ? 0 : 4f * DENSITY);
                        chkContainer.setElevation(newVal.equals("yes") ? 0 : 4f * DENSITY);
                    }
                    
                    if (!wasChecked) { 
                        int count = 0;
                        for(String p : AppConstants.PRAYERS) { String s = getFardStat(r, p); if(s.equals("yes") || s.equals("excused")) count++; } 
                        if (count == 6) { showSuccessSequence(); } 
                    }
                    refreshWidget();
                }
            });
            
            card.setOnLongClickListener(new android.view.View.OnLongClickListener() {
                @Override public boolean onLongClick(android.view.View v) {
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                    SalahRecord r = getRoomRecord(selectedDate[0]);
                    boolean wasQaza = getQazaStat(r, name);
                    if(!wasQaza) { 
                        setQazaStat(r, name, true); setFardStat(r, name, "no"); updateRoomRecord(r);
                        sp.edit().putBoolean(key+"_qaza", true).putString(key, "no").apply(); fbHelper.save(selectedDate[0], name, "no"); 
                        ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null); 
                    } 
                    else { 
                        setQazaStat(r, name, false); updateRoomRecord(r);
                        sp.edit().putBoolean(key+"_qaza", false).apply(); 
                        ui.showSmartBanner(root, lang.get("Qaza Removed"), lang.get("Name removed from Qaza list."), "img_tick", colorAccent, null);
                    }
                    loadTodayPage(); refreshWidget(); return true;
                }
            });
            if(isLandscape) { if(i<3) col1.addView(card); else col2.addView(card); } else cardsContainer.addView(card);
        }\n        """
    
    final_content = content[:start_idx] + new_code + content[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("Master 3D UI and Zero-Flash architecture injected successfully!")
else:
    print("Error: Could not find target markers.")
