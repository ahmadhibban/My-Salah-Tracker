import os, re
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        p = os.path.join(r, 'MainActivity.java')
        with open(p, 'r', encoding='utf-8') as file: c = file.read()
        cell_logic = """final String cGreg = sdfG.format(cal.getTime()); boolean isSel = cGreg.equals(selectedDate[0]);
                    final boolean isFutureDate = cal.getTime().after(tCal.getTime()) && !cGreg.equals(sdfG.format(tCal.getTime()));
                    boolean isAllDone = true; if(!isFutureDate) { for(String pr : AppConstants.PRAYERS) { String stat = sp.getString(cGreg+"_"+pr, "no"); if(!stat.equals("yes") && !stat.equals("excused")) { isAllDone = false; break; } } } else { isAllDone = false; }
                    android.widget.TextView dt = new android.widget.TextView(MainActivity.this); String dStr = String.valueOf(currentDay);
                    if(isBn) dStr = dStr.replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯");
                    dt.setText(dStr); dt.setGravity(android.view.Gravity.CENTER); dt.setTypeface(android.graphics.Typeface.DEFAULT);
                    dt.setTextColor(isSel ? android.graphics.Color.WHITE : themeColors[2]);
                    if(isFutureDate) dt.setAlpha(0.3f);
                    android.widget.FrameLayout.LayoutParams dlp = new android.widget.FrameLayout.LayoutParams((int)(35*DENSITY), (int)(35*DENSITY)); dlp.gravity = android.view.Gravity.CENTER; dt.setLayoutParams(dlp);
                    if(isSel) { android.graphics.drawable.GradientDrawable bg = new android.graphics.drawable.GradientDrawable(); bg.setShape(android.graphics.drawable.GradientDrawable.OVAL); bg.setColor(colorAccent); dt.setBackground(bg); }
                    else if(isAllDone) { dt.setBackground(MainActivity.this.getProgressBorder(cGreg, false)); }
                    cell.addView(dt);
                    cell.setOnClickListener(new android.view.View.OnClickListener() { @Override public void onClick(android.view.View v) { if(isFutureDate) { ui.showPremiumLocked(colorAccent); } else { selectedDate[0] = cGreg; dialog.dismiss(); loadTodayPage(); refreshWidget(); } } });"""
        c = re.sub(r'final String cGreg = sdfG\.format\(cal\.getTime\(\)\);.*?loadTodayPage\(\);\s*refreshWidget\(\);\s*\}\s*\}\s*\);', cell_logic, c, flags=re.DOTALL)
        with open(p, 'w', encoding='utf-8') as file: file.write(c)
        print("✅ ৪. ক্যালেন্ডারের তারিখ (ইনভিজিবল এবং প্রোগ্রেস বর্ডার) ফিক্স করা হয়েছে!")
        break
