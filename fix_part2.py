import re

ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()

def remove_method(text, sig):
    while True:
        idx = text.find(sig)
        if idx == -1: break
        start = text.find('{', idx)
        if start == -1: break
        count = 1; i = start + 1
        while i < len(text) and count > 0:
            if text[i] == '{': count += 1
            elif text[i] == '}': count -= 1
            i += 1
        if count == 0: text = text[:idx] + text[i:]
        else: break
    return text

c = remove_method(c, "private void showSunnahDialog")
c = remove_method(c, "private void showAddCustomPrayerDialog")
c = remove_method(c, "private void showDeleteCustomPrayerDialog")

new_methods = """
    private void showSunnahDialog(final String prayer, final String[] sunnahList) { 
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd); 
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get(prayer) + " " + lang.get("Extras")); title.setTextColor(colorAccent); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setPadding(0, 0, 0, (int)(20*DENSITY)); main.addView(title); 
        android.widget.ScrollView sv = new android.widget.ScrollView(this); android.widget.LinearLayout list = new android.widget.LinearLayout(this); list.setOrientation(android.widget.LinearLayout.VERTICAL);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); 
        for(int s=0; s<sunnahList.length; s++) { 
            final String sName = sunnahList[s]; final String sKey = selectedDate[0] + "_" + prayer + "_Sunnah_" + sName; final boolean sChecked = sp.getString(sKey, "no").equals("yes");
            final android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL); row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); rowBg.setCornerRadius(15f*DENSITY); rowBg.setColor(sChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); row.setBackground(rowBg);
            final android.widget.TextView tv = new android.widget.TextView(this); tv.setText(lang.get(sName)); tv.setTextColor(sChecked ? colorAccent : themeColors[2]); tv.setTextSize(16); tv.setTypeface(sChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT); tv.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f)); final android.view.View chk = ui.getPremiumCheckbox(sChecked ? "yes" : "no", colorAccent); row.addView(tv); row.addView(chk); list.addView(row);
            row.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); boolean cur = sp.getString(sKey, "no").equals("yes"); boolean newVal = !cur; sp.edit().putString(sKey, newVal ? "yes" : "no").apply(); fbHelper.save(selectedDate[0], prayer + "_Sunnah_" + sName, newVal ? "yes" : "no"); android.widget.TextView t = (android.widget.TextView) chk; android.graphics.drawable.GradientDrawable bg = (android.graphics.drawable.GradientDrawable) t.getBackground(); if(newVal) { bg.setColor(colorAccent); bg.setStroke(0, android.graphics.Color.TRANSPARENT); t.setText("✓"); t.setTextColor(android.graphics.Color.WHITE); rowBg.setColor(themeColors[4]); tv.setTextColor(colorAccent); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); } else { bg.setColor(android.graphics.Color.TRANSPARENT); bg.setStroke((int)(2*DENSITY), themeColors[4]); t.setText(""); rowBg.setColor(android.graphics.Color.TRANSPARENT); tv.setTextColor(themeColors[2]); tv.setTypeface(android.graphics.Typeface.DEFAULT); } } });
        } 
        String cStr = sp.getString("custom_nafl_" + prayer, "");
        if(!cStr.isEmpty()) {
            for(final String cItem : cStr.split(",")) {
                if(cItem.trim().isEmpty()) continue; String[] pts = cItem.split(":"); final String cName = pts[0]; final String cRak = pts.length>1?pts[1]:"2";
                final String cKey = selectedDate[0] + "_" + prayer + "_Custom_" + cName; final boolean cChecked = sp.getString(cKey, "no").equals("yes");
                final android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL); row.setGravity(android.view.Gravity.CENTER_VERTICAL); row.setPadding((int)(10*DENSITY), (int)(12*DENSITY), (int)(10*DENSITY), (int)(12*DENSITY)); android.widget.LinearLayout.LayoutParams rowLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rowLp.setMargins(0, 0, 0, (int)(10*DENSITY)); row.setLayoutParams(rowLp); final android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); rowBg.setCornerRadius(15f*DENSITY); rowBg.setColor(cChecked ? themeColors[4] : android.graphics.Color.TRANSPARENT); row.setBackground(rowBg);
                android.widget.LinearLayout tCon = new android.widget.LinearLayout(this); tCon.setOrientation(android.widget.LinearLayout.VERTICAL); tCon.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
                final android.widget.TextView tv = new android.widget.TextView(this); tv.setText("⭐ " + cName); tv.setTextColor(cChecked ? colorAccent : themeColors[2]); tv.setTextSize(16); tv.setTypeface(cChecked ? android.graphics.Typeface.DEFAULT_BOLD : android.graphics.Typeface.DEFAULT); tCon.addView(tv);
                android.widget.TextView tvR = new android.widget.TextView(this); tvR.setText(lang.bnNum(cRak) + " " + lang.get("Rakats")); tvR.setTextColor(themeColors[3]); tvR.setTextSize(12); tvR.setPadding(0,0,0,0); tCon.addView(tvR); row.addView(tCon);
                final android.view.View chk = ui.getPremiumCheckbox(cChecked ? "yes" : "no", colorAccent); row.addView(chk); list.addView(row);
                row.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(final android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); boolean cur = sp.getString(cKey, "no").equals("yes"); boolean newVal = !cur; sp.edit().putString(cKey, newVal ? "yes" : "no").apply(); fbHelper.save(selectedDate[0], prayer + "_Custom_" + cName, newVal ? "yes" : "no"); android.widget.TextView t = (android.widget.TextView) chk; android.graphics.drawable.GradientDrawable bg = (android.graphics.drawable.GradientDrawable) t.getBackground(); if(newVal) { bg.setColor(colorAccent); bg.setStroke(0, android.graphics.Color.TRANSPARENT); t.setText("✓"); t.setTextColor(android.graphics.Color.WHITE); rowBg.setColor(themeColors[4]); tv.setTextColor(colorAccent); tv.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); } else { bg.setColor(android.graphics.Color.TRANSPARENT); bg.setStroke((int)(2*DENSITY), themeColors[4]); t.setText(""); rowBg.setColor(android.graphics.Color.TRANSPARENT); tv.setTextColor(themeColors[2]); tv.setTypeface(android.graphics.Typeface.DEFAULT); } } });
                row.setOnLongClickListener(new android.view.View.OnLongClickListener() { @Override public boolean onLongClick(android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); showDeleteCustomPrayerDialog(prayer, cName, ad); return true; } });
            }
        }
        android.widget.LinearLayout addBtn = new android.widget.LinearLayout(this); addBtn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY)); addBtn.setGravity(android.view.Gravity.CENTER); android.graphics.drawable.GradientDrawable aBg = new android.graphics.drawable.GradientDrawable(); aBg.setColor(themeColors[4]); aBg.setCornerRadius(15f*DENSITY); addBtn.setBackground(aBg); android.widget.LinearLayout.LayoutParams aLp = new android.widget.LinearLayout.LayoutParams(-1, -2); aLp.setMargins(0, (int)(10*DENSITY), 0, (int)(10*DENSITY)); addBtn.setLayoutParams(aLp);
        android.widget.TextView aTxt = new android.widget.TextView(this); aTxt.setText("➕ " + lang.get("Add Extra Prayer")); aTxt.setTextColor(themeColors[2]); aTxt.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); addBtn.addView(aTxt);
        addBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY); showAddCustomPrayerDialog(prayer, ad); } }); list.addView(addBtn);
        sv.addView(list); main.addView(sv, new android.widget.LinearLayout.LayoutParams(-1, -2, 1f));
        android.widget.TextView closeBtn = new android.widget.TextView(this); closeBtn.setText(lang.get("Done")); closeBtn.setTextColor(android.graphics.Color.WHITE); closeBtn.setGravity(android.view.Gravity.CENTER); closeBtn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); closeBtn.setPadding(0, (int)(15*DENSITY), 0, (int)(15*DENSITY)); android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(colorAccent); cBg.setCornerRadius(20f*DENSITY); closeBtn.setBackground(cBg); android.widget.LinearLayout.LayoutParams clp = new android.widget.LinearLayout.LayoutParams(-1, -2); clp.setMargins(0, (int)(15*DENSITY), 0, 0); closeBtn.setLayoutParams(clp); main.addView(closeBtn); 
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); 
        closeBtn.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { ad.dismiss(); loadTodayPage(); refreshWidget(); } });
        applyFont(main, appFonts[0], appFonts[1]); ad.show(); 
    }

    private void showAddCustomPrayerDialog(final String prayer, final android.app.AlertDialog parentDialog) {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(30f * DENSITY); main.setBackground(gd);
        android.widget.TextView iconView = new android.widget.TextView(this); iconView.setText("⭐"); iconView.setTextSize(40); iconView.setGravity(android.view.Gravity.CENTER); main.addView(iconView);
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get("Add Extra Prayer")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); title.setPadding(0, (int)(10*DENSITY), 0, (int)(25*DENSITY)); main.addView(title);
        final android.widget.EditText nameIn = new android.widget.EditText(this); nameIn.setHint(lang.get("Prayer Name (e.g. Ishraq)")); nameIn.setTextColor(themeColors[2]); nameIn.setHintTextColor(themeColors[3]); android.graphics.drawable.GradientDrawable iBg = new android.graphics.drawable.GradientDrawable(); iBg.setColor(themeColors[4]); iBg.setCornerRadius(15f*DENSITY); nameIn.setBackground(iBg); nameIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY)); main.addView(nameIn, new android.widget.LinearLayout.LayoutParams(-1, -2));
        final android.widget.EditText rakIn = new android.widget.EditText(this); rakIn.setHint(lang.get("Rakats (e.g. 2)")); rakIn.setInputType(android.text.InputType.TYPE_CLASS_NUMBER); rakIn.setTextColor(themeColors[2]); rakIn.setHintTextColor(themeColors[3]); rakIn.setBackground(iBg); rakIn.setPadding((int)(20*DENSITY),(int)(15*DENSITY),(int)(20*DENSITY),(int)(15*DENSITY)); android.widget.LinearLayout.LayoutParams rLp = new android.widget.LinearLayout.LayoutParams(-1, -2); rLp.setMargins(0,(int)(10*DENSITY),0,(int)(25*DENSITY)); main.addView(rakIn, rLp);
        android.widget.Button btn = new android.widget.Button(this); btn.setText(lang.get("Add Prayer")); btn.setTextColor(android.graphics.Color.WHITE); btn.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btn.setAllCaps(false); android.graphics.drawable.GradientDrawable bBg = new android.graphics.drawable.GradientDrawable(); bBg.setColor(android.graphics.Color.parseColor("#F59E0B")); bBg.setCornerRadius(20f*DENSITY); btn.setBackground(bBg); main.addView(btn, new android.widget.LinearLayout.LayoutParams(-1, (int)(55*DENSITY)));
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
        btn.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){
            String n = nameIn.getText().toString().trim().replace(":", "").replace(",", ""); String r = rakIn.getText().toString().trim();
            if(!n.isEmpty()) { String cList = sp.getString("custom_nafl_" + prayer, ""); sp.edit().putString("custom_nafl_" + prayer, cList + (cList.isEmpty()?"":",") + n + ":" + (r.isEmpty()?"2":r)).apply(); ad.dismiss(); if(parentDialog!=null) parentDialog.dismiss(); loadTodayPage(); refreshWidget(); int idx = java.util.Arrays.asList(AppConstants.PRAYERS).indexOf(prayer); if(idx != -1) showSunnahDialog(prayer, AppConstants.SUNNAHS[idx]); }
        }}); ad.show();
    }
    
    private void showDeleteCustomPrayerDialog(final String prayer, final String cName, final android.app.AlertDialog parentDialog) {
        android.widget.FrameLayout wrap = new android.widget.FrameLayout(this); wrap.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); android.widget.LinearLayout main = new android.widget.LinearLayout(this); main.setOrientation(android.widget.LinearLayout.VERTICAL); main.setPadding((int)(25*DENSITY), (int)(30*DENSITY), (int)(25*DENSITY), (int)(30*DENSITY)); android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); main.setBackground(gd);
        android.widget.TextView title = new android.widget.TextView(this); title.setText(lang.get("Delete Extra Prayer?")); title.setTextColor(android.graphics.Color.parseColor("#FF5252")); title.setTextSize(20); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); main.addView(title);
        android.widget.TextView sub = new android.widget.TextView(this); sub.setText(lang.get("This will remove it from your list.")); sub.setTextColor(themeColors[3]); sub.setGravity(android.view.Gravity.CENTER); sub.setPadding(0,(int)(10*DENSITY),0,(int)(25*DENSITY)); main.addView(sub);
        android.widget.LinearLayout row = new android.widget.LinearLayout(this); row.setOrientation(android.widget.LinearLayout.HORIZONTAL);
        android.widget.Button btnC = new android.widget.Button(this); btnC.setText(lang.get("CANCEL")); btnC.setTextColor(themeColors[2]); btnC.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btnC.setAllCaps(false); android.graphics.drawable.GradientDrawable cBg = new android.graphics.drawable.GradientDrawable(); cBg.setColor(themeColors[4]); cBg.setCornerRadius(15f*DENSITY); btnC.setBackground(cBg); android.widget.LinearLayout.LayoutParams lpC = new android.widget.LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f); lpC.setMargins(0,0,(int)(10*DENSITY),0); row.addView(btnC, lpC);
        android.widget.Button btnD = new android.widget.Button(this); btnD.setText(lang.get("Delete")); btnD.setTextColor(android.graphics.Color.WHITE); btnD.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); btnD.setAllCaps(false); android.graphics.drawable.GradientDrawable dBg = new android.graphics.drawable.GradientDrawable(); dBg.setColor(android.graphics.Color.parseColor("#FF5252")); dBg.setCornerRadius(15f*DENSITY); btnD.setBackground(dBg); row.addView(btnD, new android.widget.LinearLayout.LayoutParams(0, (int)(50*DENSITY), 1f)); main.addView(row);
        android.widget.FrameLayout.LayoutParams flp = new android.widget.FrameLayout.LayoutParams((int)(320*DENSITY), -2); flp.gravity = android.view.Gravity.CENTER; wrap.addView(main, flp);
        final android.app.AlertDialog ad = new android.app.AlertDialog.Builder(this).setView(wrap).create(); ad.getWindow().setBackgroundDrawableResource(android.R.color.transparent); ad.getWindow().setGravity(android.view.Gravity.CENTER); applyFont(main, appFonts[0], appFonts[1]);
        btnC.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){ad.dismiss();}});
        btnD.setOnClickListener(new android.view.View.OnClickListener(){@Override public void onClick(android.view.View v){ String cList = sp.getString("custom_nafl_" + prayer, ""); String[] pts = cList.split(","); StringBuilder sb = new StringBuilder(); for(String p : pts) { if(!p.startsWith(cName+":") && !p.equals(cName)) { sb.append(p).append(","); } } String res = sb.toString(); if(res.endsWith(",")) res = res.substring(0, res.length()-1); sp.edit().putString("custom_nafl_" + prayer, res).apply(); ad.dismiss(); if(parentDialog!=null) parentDialog.dismiss(); loadTodayPage(); refreshWidget(); int idx = java.util.Arrays.asList(AppConstants.PRAYERS).indexOf(prayer); if(idx != -1) showSunnahDialog(prayer, AppConstants.SUNNAHS[idx]); }}); ad.show();
    }
"""

c = c.rstrip()
if c.endswith('}'): c = c[:-1].rstrip()
c += "\n" + new_methods + "\n}\n"
open(ma, 'w').write(c)

print("✅ Part 2 Done! NOW YOU CAN BUILD.")
