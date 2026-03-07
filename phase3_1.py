import re

def update_file(path, old_code, new_code):
    import os
    if os.path.exists(path):
        content = open(path, 'r', encoding='utf-8').read()
        if old_code in content:
            with open(path, 'w', encoding='utf-8') as f: f.write(content.replace(old_code, new_code))
            return True
    return False

f_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'

# 1. Y-Axis Label Fix
update_file(f_path, 'setLabelCount(6, true)', 'setLabelCount(7, true)')

# 2. Replace renderStats to support Double-Bar and Click-to-Jump
c = open(f_path).read()
pattern = r'private\s+void\s+renderStats\s*\([^)]*\)\s*\{'
m = re.search(pattern, c)
if m:
    s=m.start(); b=0; e=-1; im=False
    for i in range(s, len(c)):
        if c[i]=='{': b+=1; im=True
        elif c[i]=='}':
            b-=1
            if im and b==0: e=i+1; break
    if e!=-1:
        new_render = """private void renderStats(final android.widget.LinearLayout card, final android.app.AlertDialog dialog, final boolean isWeekly) {
        card.removeAllViews(); boolean isBn = sp.getString("app_lang", "en").equals("bn");
        android.widget.LinearLayout nav = new android.widget.LinearLayout(activity); nav.setGravity(android.view.Gravity.CENTER_VERTICAL); nav.setPadding(0, 0, 0, (int)(25*DENSITY));
        android.widget.TextView prev = new android.widget.TextView(activity); prev.setText("❮"); prev.setTextSize(22); prev.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY)); prev.setTextColor(colorAccent);
        ui.addClickFeedback(prev); prev.setOnClickListener(v -> { java.util.Calendar check = (java.util.Calendar) statsCalPointer.clone(); if(isWeekly) check.add(java.util.Calendar.DATE, -7); else check.add(java.util.Calendar.MONTH, -1); if(check.get(java.util.Calendar.YEAR) >= java.util.Calendar.getInstance().get(java.util.Calendar.YEAR) - 100) { if(isWeekly) statsCalPointer.add(java.util.Calendar.DATE, -7); else statsCalPointer.add(java.util.Calendar.MONTH, -1); renderStats(card, dialog, isWeekly); } else { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } });
        final java.util.Calendar temp = (java.util.Calendar) statsCalPointer.clone(); final int totalDays = isWeekly ? 7 : temp.getActualMaximum(java.util.Calendar.DAY_OF_MONTH);
        if(isWeekly) while (temp.get(java.util.Calendar.DAY_OF_WEEK) != java.util.Calendar.SATURDAY) temp.add(java.util.Calendar.DATE, -1); else temp.set(java.util.Calendar.DAY_OF_MONTH, 1);
        final java.util.Calendar startCal = (java.util.Calendar) temp.clone(); java.util.Calendar endCal = (java.util.Calendar) startCal.clone(); endCal.add(java.util.Calendar.DATE, totalDays - 1);
        
        android.widget.TextView title = new android.widget.TextView(activity); java.text.SimpleDateFormat mF = new java.text.SimpleDateFormat("MMMM", java.util.Locale.US);
        title.setText(isWeekly ? "📊 " + lang.getShortGreg(startCal.getTime()) + " - " + lang.getShortGreg(endCal.getTime()) : "📊 " + lang.get(mF.format(statsCalPointer.getTime())) + " " + lang.bnNum(statsCalPointer.get(java.util.Calendar.YEAR)));
        title.setTextColor(themeColors[2]); title.setTextSize(16); title.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); title.setGravity(android.view.Gravity.CENTER); title.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        
        android.widget.TextView next = new android.widget.TextView(activity); next.setText("❯"); next.setTextSize(22); next.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));
        final java.util.Calendar now = java.util.Calendar.getInstance(); final boolean isFuture = isWeekly ? (startCal.clone().after(now)) : ((statsCalPointer.get(java.util.Calendar.YEAR) > now.get(java.util.Calendar.YEAR)) || (statsCalPointer.get(java.util.Calendar.YEAR) == now.get(java.util.Calendar.YEAR) && statsCalPointer.get(java.util.Calendar.MONTH) >= now.get(java.util.Calendar.MONTH)));
        next.setTextColor(isFuture ? themeColors[4] : colorAccent);
        ui.addClickFeedback(next); next.setOnClickListener(v -> { if(!isFuture){ if(isWeekly) statsCalPointer.add(java.util.Calendar.DATE, 7); else statsCalPointer.add(java.util.Calendar.MONTH, 1); renderStats(card, dialog, isWeekly); } else { ui.showPremiumLocked(colorAccent); } });
        nav.addView(prev); nav.addView(title); nav.addView(next); card.addView(nav);

        java.util.ArrayList<com.github.mikephil.charting.data.BarEntry> fE = new java.util.ArrayList<>(), sE = new java.util.ArrayList<>();
        java.util.ArrayList<Integer> fC = new java.util.ArrayList<>(); String[] lbls = new String[totalDays];
        java.text.SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US); int tDone=0, tExc=0, tSun=0, daysPassed=0;
        
        for(int i=0; i<totalDays; i++) {
            String dK = sdf.format(startCal.getTime()); int d=0, e=0, s=0; SalahRecord sR = getRoomRecord(dK);
            if(startCal.before(now) || dK.equals(sdf.format(now.getTime()))) {
                daysPassed++;
                if(sR!=null){ for(int j=0; j<6; j++){ String st=getFardStat(sR, prayers[j]); if("yes".equals(st)) d++; else if("excused".equals(st)) e++;
                if(isWeekly) for(String sn : AppConstants.SUNNAHS[j]) if("yes".equals(sp.getString(dK+"_"+prayers[j]+"_Sunnah_"+sn, "no"))) s++; } }
                tDone+=d; tExc+=e; tSun+=s;
            }
            float fVal = d+e;
            fE.add(new com.github.mikephil.charting.data.BarEntry(isWeekly?i-0.2f:(float)i, fVal));
            if(isWeekly) sE.add(new com.github.mikephil.charting.data.BarEntry(i+0.2f, s*(6f/12f)));
            fC.add(fVal==0?android.graphics.Color.TRANSPARENT:((MainActivity)activity).getStatusColor(dK));
            lbls[i] = isWeekly ? new java.text.SimpleDateFormat("E", java.util.Locale.US).format(startCal.getTime()).substring(0,1) : (isBn?lang.bnNum(i+1):""+(i+1));
            if(isBn && isWeekly) lbls[i] = new String[]{"র","সো","ম","বু","বৃ","শু","শ"}[startCal.get(java.util.Calendar.DAY_OF_WEEK)-1];
            startCal.add(java.util.Calendar.DATE, 1);
        }
        
        com.github.mikephil.charting.charts.BarChart bc = new com.github.mikephil.charting.charts.BarChart(activity); bc.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, (int)(180*DENSITY)));
        com.github.mikephil.charting.data.BarDataSet fs=new com.github.mikephil.charting.data.BarDataSet(fE, "Fard"); fs.setColors(fC); fs.setDrawValues(false);
        com.github.mikephil.charting.data.BarData bd;
        if(isWeekly){ com.github.mikephil.charting.data.BarDataSet ss=new com.github.mikephil.charting.data.BarDataSet(sE, "Sunnah"); ss.setColor(android.graphics.Color.parseColor("#F59E0B")); ss.setDrawValues(false); bd=new com.github.mikephil.charting.data.BarData(fs, ss); bd.setBarWidth(0.3f); bc.getXAxis().setAxisMinimum(-0.5f); bc.getXAxis().setAxisMaximum(6.5f); }
        else { bd=new com.github.mikephil.charting.data.BarData(fs); bd.setBarWidth(0.5f); bc.getXAxis().setAxisMinimum(-0.5f); bc.getXAxis().setAxisMaximum(totalDays-0.5f); }
        bc.setData(bd); bc.getAxisLeft().setAxisMinimum(0); bc.getAxisLeft().setAxisMaximum(6); bc.getAxisLeft().setLabelCount(7, true);
        bc.getXAxis().setPosition(com.github.mikephil.charting.components.XAxis.XAxisPosition.BOTTOM); bc.getXAxis().setDrawGridLines(false); bc.getXAxis().setTextColor(themeColors[3]);
        bc.getXAxis().setValueFormatter(new com.github.mikephil.charting.formatter.ValueFormatter(){@Override public String getFormattedValue(float v){int idx=Math.round(v); return (idx>=0&&idx<lbls.length)?lbls[idx]:"";}});
        bc.getLegend().setEnabled(false); bc.getDescription().setEnabled(false); bc.getAxisRight().setEnabled(false);
        
        final java.util.Calendar sCalClick = (java.util.Calendar) temp.clone(); if(isWeekly) while (sCalClick.get(java.util.Calendar.DAY_OF_WEEK) != java.util.Calendar.SATURDAY) sCalClick.add(java.util.Calendar.DATE, -1); else sCalClick.set(java.util.Calendar.DAY_OF_MONTH, 1);
        bc.setOnChartValueSelectedListener(new com.github.mikephil.charting.listener.OnChartValueSelectedListener() {
            @Override public void onValueSelected(com.github.mikephil.charting.data.Entry e, com.github.mikephil.charting.highlight.Highlight h) {
                int idx = Math.round(e.getX()); final java.util.Calendar tCal = (java.util.Calendar) sCalClick.clone(); tCal.add(java.util.Calendar.DATE, idx); java.util.Calendar n = java.util.Calendar.getInstance();
                if(tCal.after(n) && !sdf.format(tCal.getTime()).equals(sdf.format(n.getTime()))) { ui.showPremiumLocked(colorAccent); }
                else if(tCal.get(java.util.Calendar.YEAR) < n.get(java.util.Calendar.YEAR) - 100) { android.widget.FrameLayout r = activity.findViewById(android.R.id.content); if(r != null) ui.showSmartBanner(r, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); }
                else { new android.os.Handler(android.os.Looper.getMainLooper()).postDelayed(() -> { dialog.dismiss(); if(activity instanceof MainActivity) { try{ java.lang.reflect.Field f = MainActivity.class.getDeclaredField("selectedDate"); f.setAccessible(true); String[] arr = (String[]) f.get(activity); arr[0] = sdf.format(tCal.getTime()); java.lang.reflect.Method m = MainActivity.class.getDeclaredMethod("loadTodayPage"); m.setAccessible(true); m.invoke(activity); }catch(Exception ex){} } }, 150); }
            }
            @Override public void onNothingSelected() {}
        });
        card.addView(bc);
        
        android.widget.LinearLayout legBox = new android.widget.LinearLayout(activity); legBox.setGravity(android.view.Gravity.CENTER); legBox.setPadding(0, (int)(15*DENSITY), 0, (int)(5*DENSITY));
        String[] lN = isBn ? (isWeekly ? new String[]{"ফরজ", "সুন্নাহ", "ছুটি"} : new String[]{"সম্পন্ন", "ছুটি"}) : (isWeekly ? new String[]{"Fard", "Sunnah", "Excused"} : new String[]{"Done", "Excused"});
        int[] lC = isWeekly ? new int[]{android.graphics.Color.parseColor("#22C55E"), android.graphics.Color.parseColor("#F59E0B"), android.graphics.Color.parseColor("#8B5CF6")} : new int[]{android.graphics.Color.parseColor("#22C55E"), android.graphics.Color.parseColor("#8B5CF6")};
        for(int i=0; i<lN.length; i++) {
            android.widget.LinearLayout item = new android.widget.LinearLayout(activity); item.setGravity(android.view.Gravity.CENTER); item.setPadding((int)(10*DENSITY),0,(int)(10*DENSITY),0);
            android.view.View dot = new android.view.View(activity); dot.setLayoutParams(new android.widget.LinearLayout.LayoutParams((int)(12*DENSITY), (int)(12*DENSITY)));
            android.graphics.drawable.GradientDrawable dGd = new android.graphics.drawable.GradientDrawable(); dGd.setColor(lC[i]); dGd.setCornerRadius(6*DENSITY); dot.setBackground(dGd);
            android.widget.TextView txt = new android.widget.TextView(activity); txt.setText(lN[i]); txt.setTextColor(themeColors[3]); txt.setTextSize(12); txt.setPadding((int)(5*DENSITY),0,0,0);
            item.addView(dot); item.addView(txt); legBox.addView(item);
        }
        card.addView(legBox);

        int tMiss = (daysPassed*6) - tDone - tExc; if(tMiss<0) tMiss=0;
        android.widget.LinearLayout dRow = new android.widget.LinearLayout(activity); dRow.setPadding(0, (int)(25*DENSITY), 0, (int)(10*DENSITY)); 
        android.widget.LinearLayout b1 = new android.widget.LinearLayout(activity); b1.setOrientation(1); b1.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView t1 = new android.widget.TextView(activity); t1.setText(lang.bnNum(tDone)); t1.setTextSize(24); t1.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); t1.setTextColor(android.graphics.Color.parseColor("#22C55E")); android.widget.TextView l1 = new android.widget.TextView(activity); l1.setText(isBn ? "ফরজ" : "Fard"); l1.setTextSize(11); l1.setTextColor(themeColors[3]); b1.addView(t1); b1.addView(l1); dRow.addView(b1);
        if (isWeekly) {
            android.widget.LinearLayout b3 = new android.widget.LinearLayout(activity); b3.setOrientation(1); b3.setGravity(17); b3.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
            android.widget.TextView t3 = new android.widget.TextView(activity); t3.setText(lang.bnNum(tSun)); t3.setTextSize(24); t3.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); t3.setTextColor(android.graphics.Color.parseColor("#F59E0B")); t3.setGravity(17); android.widget.TextView l3 = new android.widget.TextView(activity); l3.setText(isBn ? "সুন্নাহ" : "Sunnah"); l3.setTextSize(11); l3.setTextColor(themeColors[3]); l3.setGravity(17); b3.addView(t3); b3.addView(l3); dRow.addView(b3);
        } else { android.view.View spV = new android.view.View(activity); spV.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, 0, 1f)); dRow.addView(spV); }
        android.widget.LinearLayout b2 = new android.widget.LinearLayout(activity); b2.setOrientation(1); b2.setGravity(5); b2.setLayoutParams(new android.widget.LinearLayout.LayoutParams(0, -2, 1f));
        android.widget.TextView t2 = new android.widget.TextView(activity); t2.setText(lang.bnNum(tMiss)); t2.setTextSize(24); t2.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); t2.setTextColor(android.graphics.Color.parseColor("#FF5252")); t2.setGravity(5); android.widget.TextView l2 = new android.widget.TextView(activity); l2.setText(lang.get("Missed")); l2.setTextSize(11); l2.setTextColor(themeColors[3]); l2.setGravity(5); b2.addView(t2); b2.addView(l2); dRow.addView(b2); card.addView(dRow);
        
        android.widget.TextView close = new android.widget.TextView(activity); close.setText(lang.get("CLOSE")); close.setTextColor(themeColors[3]); close.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY)); close.setTypeface(android.graphics.Typeface.DEFAULT_BOLD); close.setGravity(17); ui.addClickFeedback(close); close.setOnClickListener(v -> { if(dialog!=null) dialog.dismiss(); }); card.addView(close); applyFont(card, appFonts[0], appFonts[1]);
    }"""
        c = c[:s] + new_render + c[e:]
        open(f_path,'w').write(c)
        print("✅ Phase 3.1: App Chart (0-6 Axis, Double Bar & Click to Jump) Added!")
    else: print("Error parsing RenderStats")
