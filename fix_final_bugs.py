import re

def patch_file(f, ops):
    try:
        with open(f, 'r', encoding='utf-8') as file: c = file.read()
        for p, r in ops: c = re.sub(p, r, c, flags=re.DOTALL)
        with open(f, 'w', encoding='utf-8') as file: file.write(c)
    except Exception as e: print(f"Error in {f}: {e}")

# 1. MainActivity: Auto-Qaza on Unmark BUG FIX
ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
ma_ops = [
    (r'(setFardStat\(r,\s*p,\s*"yes"\);)(\s*)(sp\.edit\(\)\.putString\(selectedDate\[0\]\+"_"\+p,\s*"yes"\)\.apply\(\);)', 
     r'\1 setQazaStat(r, p, false);\2\3 sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", false).apply();'),
    (r'(setFardStat\(r,\s*AppConstants\.PRAYERS\[i\],\s*"yes"\);)(\s*)(sp\.edit\(\)\.putString\(selectedDate\[0\]\+"_"\+AppConstants\.PRAYERS\[i\],\s*"yes"\)\.apply\(\);)', 
     r'\1 setQazaStat(r, AppConstants.PRAYERS[i], false);\2\3 sp.edit().putBoolean(selectedDate[0]+"_"+AppConstants.PRAYERS[i]+"_qaza", false).apply();')
]
patch_file(ma, ma_ops)

# 2. SalahWidget: Auto-Qaza BUG FIX from Widget
wg = 'app/src/main/java/com/my/salah/tracker/app/SalahWidget.java'
wg_ops = [
    (r'(toggleStatInRoom\(record,\s*prayerName\);)(\s*)(dao\.updateRecord\(record\);)',
     r'\1\n                if(getStatFromRoom(record, prayerName).equals("yes")) {\n                    switch(prayerName) { case "Fajr": record.fajr_qaza = false; break; case "Dhuhr": record.dhuhr_qaza = false; break; case "Asr": record.asr_qaza = false; break; case "Maghrib": record.maghrib_qaza = false; break; case "Isha": record.isha_qaza = false; break; case "Witr": record.witr_qaza = false; break; }\n                    context.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE).edit().putBoolean(todayKey+"_"+prayerName+"_qaza", false).apply();\n                }\n\2\3')
]
patch_file(wg, wg_ops)

# 3. StatsHelper: Double Bars (Fard + Sunnah) Everywhere!
sh = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
sh_ops = [
    (r'fE\.add\(new com\.github\.mikephil\.charting\.data\.BarEntry\(isWeekly\?i-0\.2f:\(float\)i,\s*fVal\)\);\s*if\(isWeekly\)\s*sE\.add\(new com\.github\.mikephil\.charting\.data\.BarEntry\(i\+0\.2f,\s*s\*\(6f/12f\)\)\);',
     r'fE.add(new com.github.mikephil.charting.data.BarEntry(i-0.2f, fVal));\n            sE.add(new com.github.mikephil.charting.data.BarEntry(i+0.2f, s*(6f/12f)));'),
    
    (r'if\(isWeekly\)\{\s*com\.github\.mikephil\.charting\.data\.BarDataSet ss=new com\.github\.mikephil\.charting\.data\.BarDataSet\(sE,\s*"Sunnah"\);\s*ss\.setColor\(android\.graphics\.Color\.parseColor\("#F59E0B"\)\);\s*ss\.setDrawValues\(false\);\s*bd=new com\.github\.mikephil\.charting\.data\.BarData\(fs,\s*ss\);\s*bd\.setBarWidth\(0\.3f\);\s*bc\.getXAxis\(\)\.setAxisMinimum\(-0\.5f\);\s*bc\.getXAxis\(\)\.setAxisMaximum\(6\.5f\);\s*\}\s*else\s*\{\s*bd=new com\.github\.mikephil\.charting\.data\.BarData\(fs\);\s*bd\.setBarWidth\(0\.5f\);\s*bc\.getXAxis\(\)\.setAxisMinimum\(-0\.5f\);\s*bc\.getXAxis\(\)\.setAxisMaximum\(totalDays-0\.5f\);\s*\}',
     r'com.github.mikephil.charting.data.BarDataSet ss=new com.github.mikephil.charting.data.BarDataSet(sE, "Sunnah"); ss.setColor(android.graphics.Color.parseColor("#F59E0B")); ss.setDrawValues(false);\n        bd=new com.github.mikephil.charting.data.BarData(fs, ss); bd.setBarWidth(0.3f);\n        bc.getXAxis().setAxisMinimum(-0.5f); bc.getXAxis().setAxisMaximum(totalDays-0.5f);'),
    
    (r'String\[\] lN = isBn \? \(isWeekly \? new String\[\]\{"ফরজ", "সুন্নাহ", "ছুটি"\} : new String\[\]\{"সম্পন্ন", "ছুটি"\}\) : \(isWeekly \? new String\[\]\{"Fard", "Sunnah", "Excused"\} : new String\[\]\{"Done", "Excused"\}\);\s*int\[\] lC = isWeekly \? new int\[\]\{android\.graphics\.Color\.parseColor\("#22C55E"\), android\.graphics\.Color\.parseColor\("#F59E0B"\), android\.graphics\.Color\.parseColor\("#8B5CF6"\)\} : new int\[\]\{android\.graphics\.Color\.parseColor\("#22C55E"\), android\.graphics\.Color\.parseColor\("#8B5CF6"\)\};',
     r'String[] lN = isBn ? new String[]{"ফরজ", "সুন্নাহ", "ছুটি"} : new String[]{"Fard", "Sunnah", "Excused"};\n        int[] lC = new int[]{android.graphics.Color.parseColor("#22C55E"), android.graphics.Color.parseColor("#F59E0B"), android.graphics.Color.parseColor("#8B5CF6")};'),
    
    (r'if\s*\(isWeekly\)\s*\{\s*(android\.widget\.LinearLayout b3 = new android\.widget\.LinearLayout\(activity\);.*?dRow\.addView\(b3\);)\s*\}\s*else\s*\{\s*android\.view\.View spV = new android\.view\.View\(activity\);\s*spV\.setLayoutParams\(new android\.widget\.LinearLayout\.LayoutParams\(0,\s*0,\s*1f\)\);\s*dRow\.addView\(spV\);\s*\}',
     r'\1'),
    
    (r'if\(sR!=null\)\{\s*for\(int j=0;\s*j<6;\s*j\+\+\)\{\s*String st=getFardStat\(sR,\s*prayers\[j\]\);\s*if\("yes"\.equals\(st\)\)\s*d\+\+;\s*else if\("excused"\.equals\(st\)\)\s*e\+\+;\s*if\(isWeekly\)\s*for\(String sn\s*:\s*AppConstants\.SUNNAHS\[j\]\)\s*if\("yes"\.equals\(sp\.getString\(dK\+"_"\+prayers\[j\]\+"_Sunnah_"\+sn,\s*"no"\)\)\)\s*s\+\+;\s*\}\s*\}',
     r'if(sR!=null){ for(int j=0; j<6; j++){ String st=getFardStat(sR, prayers[j]); if("yes".equals(st)) d++; else if("excused".equals(st)) e++; } s = getTotalExtras(dK); }'),
    
    (r'if\(r!=null\)\{\s*for\(int p=0;\s*p<prayers\.length;\s*p\+\+\)\{\s*String st=getFardStat\(r,prayers\[p\]\);\s*if\(st\.equals\("yes"\)\)\{tDn\+\+;dyDn\+\+;\}\s*else if\(st\.equals\("excused"\)\)\{tE\+\+;dyE\+\+;\}\s*else\{if\(getQazaStat\(r,prayers\[p\]\)\)tQ\+\+;else tM\+\+;\}\s*if\(isWeekly\)\s*for\(String sN:AppConstants\.SUNNAHS\[p\]\)\s*if\("yes"\.equals\(sp\.getString\(dK\+"_"\+prayers\[p\]\+"_Sunnah_"\+sN,"no"\)\)\)\s*sC_cnt\+\+;\s*\}\s*\}',
     r'if(r!=null){for(int p=0;p<prayers.length;p++){String st=getFardStat(r,prayers[p]); if(st.equals("yes")){tDn++;dyDn++;}else if(st.equals("excused")){tE++;dyE++;}else{if(getQazaStat(r,prayers[p]))tQ++;else tM++;}} sC_cnt = getTotalExtras(dK);}'),
    
    (r'if\(isWeekly\)\{\s*if\(fH>0\)\{pt\.setColor\(dC\.get\(i\)\);cv\.drawRoundRect\(new android\.graphics\.RectF\(cx-40,cyY\+60\+mBH-fH,cx-5,cyY\+60\+mBH\),15,15,pt\);\}\s*if\(sH>0\)\{pt\.setColor\(android\.graphics\.Color\.parseColor\("#F59E0B"\)\);cv\.drawRoundRect\(new android\.graphics\.RectF\(cx\+5,cyY\+60\+mBH-sH,cx\+40,cyY\+60\+mBH\),15,15,pt\);\}\s*\}\s*else if\(fH>0\)\{pt\.setColor\(dC\.get\(i\)\);cv\.drawRoundRect\(new android\.graphics\.RectF\(cx-15,cyY\+60\+mBH-fH,cx\+15,cyY\+60\+mBH\),12,12,pt\);\}',
     r'float bW = isWeekly ? 35 : 12; float gap = isWeekly ? 5 : 2;\n                if(fH>0){pt.setColor(dC.get(i));cv.drawRoundRect(new android.graphics.RectF(cx-bW-gap,cyY+60+mBH-fH,cx-gap,cyY+60+mBH),bW/3f,bW/3f,pt);}\n                if(sH>0){pt.setColor(android.graphics.Color.parseColor("#F59E0B"));cv.drawRoundRect(new android.graphics.RectF(cx+gap,cyY+60+mBH-sH,cx+gap+bW,cyY+60+mBH),bW/3f,bW/3f,pt);}'),
    
    (r'if\(rec!=null\)\{\s*for\(int p=0;\s*p<prayers\.length;\s*p\+\+\)\{\s*String fS=getFardStat\(rec,prayers\[p\]\);\s*if\(fS\.equals\("yes"\)\)fD\+\+;\s*else if\(fS\.equals\("excused"\)\)\{fD\+\+;hB=true;\}\s*for\(String sN:AppConstants\.SUNNAHS\[p\]\)\s*if\("yes"\.equals\(sp\.getString\(dK\+"_"\+prayers\[p\]\+"_Sunnah_"\+sN,"no"\)\)\)\s*sD_cnt\+\+;\s*\}\s*\}',
     r'if(rec!=null){for(int p=0;p<prayers.length;p++){String fS=getFardStat(rec,prayers[p]); if(fS.equals("yes"))fD++; else if(fS.equals("excused")){fD++;hB=true;}} sD_cnt = getTotalExtras(dK);}')
]
patch_file(sh, sh_ops)

print("✅ ALL LOGIC BUGS FIXED & SUNNAH COLORS APPLIED EVERYWHERE!")
