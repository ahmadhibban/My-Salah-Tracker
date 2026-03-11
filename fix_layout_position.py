import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "for(int i=0; i<6; i++) {"
end_marker = "cardsContainer.setAlpha(0f);"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker)

if start_idx != -1 and end_idx != -1:
    perfect_code = """for(int i=0; i<6; i++) {
            final String name = AppConstants.PRAYERS[i];
            final String key = selectedDate[0]+"_"+name; 
            final String stat = getFardStat(todayRec, name); 
            final boolean checked = stat.equals("yes") || stat.equals("excused");
            final boolean isQaza = getQazaStat(todayRec, name);
            
            // কার্ডের বেসিক লেআউট
            final LinearLayout card = new LinearLayout(this); 
            card.setPadding((int)(12*DENSITY), (int)(12*DENSITY), (int)(12*DENSITY), (int)(12*DENSITY)); 
            card.setGravity(android.view.Gravity.CENTER_VERTICAL);
            card.setOrientation(LinearLayout.HORIZONTAL);
            
            final android.graphics.drawable.GradientDrawable cb = new android.graphics.drawable.GradientDrawable(); 
            cb.setColor(stat.equals("excused") ? (isDarkTheme ? android.graphics.Color.parseColor("#1A1115") : android.graphics.Color.parseColor("#FCE4EC")) : themeColors[1]);
            cb.setCornerRadius(16f * DENSITY); 
            cb.setStroke((int)(1f*DENSITY), stat.equals("excused") ? android.graphics.Color.parseColor("#EC4899") : (checked ? colorAccent : android.graphics.Color.TRANSPARENT));
            card.setBackground(cb); 
            
            LinearLayout.LayoutParams cLp = new LinearLayout.LayoutParams(-1, -2); 
            cLp.setMargins(0, 0, 0, i==5 ? 0 : (int)(10*DENSITY)); 
            card.setLayoutParams(cLp);
            
            // ১. আইকন (বর্ডার এবং ব্যাকগ্রাউন্ড ছাড়া)
            android.view.View iconView = ui.getRoundImage(pImgs[i], pPaddings[i], android.graphics.Color.TRANSPARENT, colorAccent); 
            LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(40*DENSITY), (int)(40*DENSITY)); 
            icLp.setMargins(0, 0, (int)(14*DENSITY), 0); 
            iconView.setLayoutParams(icLp); 
            card.addView(iconView);
            
            // ২. নামাজের নাম (মাঝখানের পুরো ফাঁকা জায়গা নেবে)
            LinearLayout pName = new LinearLayout(this); 
            pName.setOrientation(LinearLayout.VERTICAL); 
            pName.setGravity(android.view.Gravity.CENTER_VERTICAL | android.view.Gravity.LEFT);
            LinearLayout.LayoutParams pNameLp = new LinearLayout.LayoutParams(0, -2, 1f); 
            pName.setLayoutParams(pNameLp);
            
            LinearLayout titleRow = new LinearLayout(this); 
            titleRow.setOrientation(LinearLayout.HORIZONTAL); 
            titleRow.setGravity(android.view.Gravity.CENTER_VERTICAL);
            
            TextView tv = new TextView(this); 
            tv.setSingleLine(true); tv.setEllipsize(android.text.TextUtils.TruncateAt.END); 
            tv.setText(lang.get(name)); 
            tv.setTextColor(stat.equals("excused") ? android.graphics.Color.parseColor("#EC4899") : themeColors[2]); 
            tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); 
            tv.setTextSize(16); 
            titleRow.addView(tv);
            
            if (isQaza && stat.equals("no")) {
                TextView qBadge = new TextView(this);
                qBadge.setSingleLine(true); qBadge.setEllipsize(android.text.TextUtils.TruncateAt.END);
                qBadge.setText(lang.get("QAZA")); qBadge.setTextColor(themeColors[2]); qBadge.setTextSize(10); qBadge.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); qBadge.setPadding((int)(6*DENSITY), (int)(2*DENSITY), (int)(6*DENSITY), (int)(2*DENSITY)); 
                android.graphics.drawable.GradientDrawable qBg = new android.graphics.drawable.GradientDrawable(); qBg.setColor(themeColors[5]); qBg.setCornerRadius(12f * DENSITY); qBadge.setBackground(qBg);
                LinearLayout.LayoutParams qLp = new LinearLayout.LayoutParams(-2, -2); qLp.setMargins((int)(8*DENSITY), 0, 0, 0); qBadge.setLayoutParams(qLp); titleRow.addView(qBadge);
            }
            pName.addView(titleRow);
            card.addView(pName);
            
            // ৩. সুন্নাহ বাটন (মাঝখান থেকে সরিয়ে একদম ডানে টিক চিহ্নের পাশে আনা হলো)
            final int finalI = i;
            if (AppConstants.SUNNAHS[i].length > 0 && !stat.equals("excused")) {
                TextView sunnahBtn = new TextView(this);
                sunnahBtn.setSingleLine(true); sunnahBtn.setEllipsize(android.text.TextUtils.TruncateAt.END);
                int doneSunnahs = 0; int totalS = AppConstants.SUNNAHS[i].length; 
                for(String sName : AppConstants.SUNNAHS[i]) { if (sp.getString(selectedDate[0]+"_"+name+"_Sunnah_"+sName, "no").equals("yes")) doneSunnahs++; }
                String cStr = sp.getString("custom_nafl_" + name, "");
                if(!cStr.isEmpty()) { for(String cN : cStr.split(",")) { if(cN.contains(":")) cN = cN.split(":")[0]; totalS++; if("yes".equals(sp.getString(selectedDate[0]+"_"+name+"_Custom_"+cN, "no"))) doneSunnahs++; } }
                String sText = totalS > 1 ? (lang.get("Extras") + " (" + lang.bnNum(doneSunnahs) + "/" + lang.bnNum(totalS) + ")") : (i == 5 ? lang.get("Tahajjud") : lang.get("Sunnah"));
                sunnahBtn.setText(sText); sunnahBtn.setTextSize(13); 
                
                android.graphics.drawable.GradientDrawable sBg = new android.graphics.drawable.GradientDrawable();
                sBg.setCornerRadius(12f * DENSITY);
                if(doneSunnahs > 0) { sBg.setColor(colorAccent); sunnahBtn.setTextColor(android.graphics.Color.WHITE); } 
                else { sBg.setColor(themeColors[5]); sunnahBtn.setTextColor(themeColors[2]); }
                sunnahBtn.setBackground(sBg);
                sunnahBtn.setPadding((int)(10*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(4*DENSITY));
                
                LinearLayout.LayoutParams sunnahLp = new LinearLayout.LayoutParams(-2, -2); 
                sunnahLp.setMargins(0, 0, (int)(12*DENSITY), 0); // টিক চিহ্নের থেকে একটু ফাঁকা
                sunnahBtn.setLayoutParams(sunnahLp);
                sunnahBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { showSunnahDialog(name, AppConstants.SUNNAHS[finalI]); } }); 
                
                // বাটনটিকে মূল কার্ড লেআউটে যোগ করা হলো (যাতে টিক চিহ্নের আগে থাকে)
                card.addView(sunnahBtn);
            }
            
            // ৪. টিক চিহ্নের চেকবক্স (সবশেষে)
            final FrameLayout checkLayout = new FrameLayout(this);
            checkLayout.addView(ui.getPremiumCheckbox(stat, colorAccent));
            card.addView(checkLayout);
            
            // ৫. জিরো-ফ্ল্যাশ (Zero-Flash) ক্লিক ইভেন্ট
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
                    
                    checkLayout.removeAllViews(); checkLayout.addView(ui.getPremiumCheckbox(newVal, colorAccent));
                    cb.setStroke((int)(1f*DENSITY), newVal.equals("yes") ? colorAccent : android.graphics.Color.TRANSPARENT);
                    
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
    
    final_content = content[:start_idx] + perfect_code + content[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(final_content)
    print("Icons border removed & Sunnah button moved next to Checkbox!")
else:
    print("Error finding markers.")
