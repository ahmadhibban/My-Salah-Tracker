import os, re

# 1. LanguageEngine: Public Suffix & New Words
l_path = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
c = open(l_path).read()
c = c.replace('private String getBnSuffix', 'public String getBnSuffix')
c = c.replace('bnMap.put("Skip", "এড়িয়ে যান");', 'bnMap.put("Skip", "এড়িয়ে যান");\n        bnMap.put("Limit Reached", "লিমিট শেষ");\n        bnMap.put("Cannot go back more than 100 years.", "১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়।");\n        bnMap.put("Already Added", "ইতিমধ্যেই যুক্ত আছে");\n        bnMap.put("Already in Qaza list.", "এই দিনটি আগে থেকেই কাজা লিস্টে যুক্ত আছে।");')
open(l_path,'w').write(c)

# 2. UIComponents: Progress Arc Drawable & Hijri Suffix
u_path = 'app/src/main/java/com/my/salah/tracker/app/UIComponents.java'
c = open(u_path).read()
pd = """public static class ProgressDrawable extends android.graphics.drawable.Drawable {
        private int d, t, c, bg; private float dens;
        public ProgressDrawable(int d, int t, int c, int bg, float dens) { this.d=d; this.t=t; this.c=c; this.bg=bg; this.dens=dens; }
        @Override public void draw(android.graphics.Canvas canvas) {
            android.graphics.Rect b = getBounds(); android.graphics.Paint p = new android.graphics.Paint(1);
            p.setStyle(android.graphics.Paint.Style.STROKE); p.setStrokeWidth(2.5f * dens); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);
            float r = Math.min(b.width(), b.height()) / 2f - (2.5f * dens);
            p.setColor(bg); canvas.drawCircle(b.exactCenterX(), b.exactCenterY(), r, p);
            if(d>0){ p.setColor(c); canvas.drawArc(new android.graphics.RectF(b.exactCenterX()-r, b.exactCenterY()-r, b.exactCenterX()+r, b.exactCenterY()+r), -90, 360f*(d/(float)t), false, p); }
        }
        @Override public void setAlpha(int a){} @Override public void setColorFilter(android.graphics.ColorFilter f){} @Override public int getOpacity(){return -3;}
    }\n\n    public View getPremiumIcon"""
if "ProgressDrawable" not in c: c = c.replace('public View getPremiumIcon', pd)
c = c.replace('String day = lang.bnNum(hijriCal.get(IslamicCalendar.DAY_OF_MONTH));', 'int hd = hijriCal.get(IslamicCalendar.DAY_OF_MONTH);\n                String day = lang.bnNum(hd) + lang.getBnSuffix(hd);')
open(u_path,'w').write(c)

# 3. MainActivity: Custom Border, Limits & Long Press Fix
m_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(m_path).read()
mh = """public int getStatusColor(String k) {
        if(k==null) return themeColors[4]; SalahRecord r = getRoomRecord(k); int d=0, e=0;
        for(String p : AppConstants.PRAYERS){ String s=getFardStat(r, p); if("yes".equals(s)) d++; else if("excused".equals(s)) e++; }
        if(d+e==0) return android.graphics.Color.TRANSPARENT; if(e==6) return android.graphics.Color.parseColor("#8B5CF6");
        return d==6 ? android.graphics.Color.parseColor("#22C55E") : android.graphics.Color.parseColor("#10B981");
    }
    public android.graphics.drawable.Drawable getProgressBorder(String k, boolean s) {
        int c = getStatusColor(k); int d=0; SalahRecord r = getRoomRecord(k);
        for(String p : AppConstants.PRAYERS){ String st=getFardStat(r, p); if("yes".equals(st)||"excused".equals(st)) d++; }
        if(s){ android.graphics.drawable.GradientDrawable gd=new android.graphics.drawable.GradientDrawable(); gd.setShape(android.graphics.drawable.GradientDrawable.OVAL); gd.setColor(colorAccent); return gd; }
        return new UIComponents.ProgressDrawable(d, 6, c==0?themeColors[4]:c, themeColors[4], DENSITY);
    }\n\n    private void loadTodayPage() {"""
if "getProgressBorder" not in c: c = c.replace('private void loadTodayPage() {', mh)

o_bg = """GradientDrawable dayBg = new GradientDrawable(); dayBg.setShape(GradientDrawable.OVAL); \n            if(isSel) { dayBg.setColor(colorAccent); t.setTextColor(Color.WHITE);\n            } else if (isAllDone && !isFuture) { dayBg.setColor(themeColors[5]); t.setTextColor(colorAccent); } else { dayBg.setColor(themeColors[1]); dayBg.setStroke((int)(1.5f*DENSITY), themeColors[4]); t.setTextColor(isFuture ? themeColors[4] : themeColors[3]);\n            } \n            t.setBackground(dayBg);"""
n_bg = """t.setTextColor(isSel ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : themeColors[2]));\n            t.setBackground(getProgressBorder(dKey, isSel));"""
c = c.replace(o_bg, n_bg)

o_prev = 'Calendar checkLimit = (Calendar) selectedCalArr[0].clone(); checkLimit.add(Calendar.DATE, -7); if(checkLimit.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { Calendar cL = (Calendar) selectedCalArr[0].clone(); cL.add(Calendar.DATE, -7); if(cL.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { selectedCalArr[0].add(Calendar.DATE, -7); } } else { ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } selectedDate[0] = sdf.format(selectedCalArr[0].getTime()); loadTodayPage();'
n_prev = 'Calendar chk = (Calendar) selectedCalArr[0].clone(); chk.add(Calendar.DATE, -7); if(chk.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { selectedCalArr[0].add(Calendar.DATE, -7); selectedDate[0] = sdf.format(selectedCalArr[0].getTime()); loadTodayPage(); } else { ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); }'
c = c.replace(o_prev, n_prev)

c = re.sub(r'v\.performHapticFeedback\(android\.view\.HapticFeedbackConstants\.LONG_PRESS\);\s*SalahRecord r = getRoomRecord\(selectedDate\[0\]\);\s*for\(String p : AppConstants\.PRAYERS\) \{\s*setQazaStat\(r, p, true\); setFardStat\(r, p, "no"\);\s*sp\.edit\(\)\.putBoolean\(selectedDate\[0\]\+"_"+p\+"_qaza", true\)\.putString\(selectedDate\[0\]\+"_"+p, "no"\)\.apply\(\);\s*fbHelper\.save\(selectedDate\[0\], p, "no"\);\s*\}\s*updateRoomRecord\(r\);\s*ui\.showSmartBanner\(root, lang\.get\("Qaza Saved"\), lang\.get\("Entire day marked as pending Qaza\."\), "img_warning", colorAccent, null\); loadTodayPage\(\); refreshWidget\(\);\s*return true;',
"""v.performHapticFeedback(android.view.HapticFeedbackConstants.LONG_PRESS); 
                SalahRecord r = getRoomRecord(selectedDate[0]);
                boolean allQ = true; for(String p:AppConstants.PRAYERS) if(!getQazaStat(r,p)) allQ=false;
                if(allQ){ ui.showSmartBanner(root, lang.get("Already Added"), lang.get("Already in Qaza list."), "img_tick", colorAccent, null); return true; }
                for(String p : AppConstants.PRAYERS) { setQazaStat(r, p, true); setFardStat(r, p, "no"); sp.edit().putBoolean(selectedDate[0]+"_"+p+"_qaza", true).putString(selectedDate[0]+"_"+p, "no").apply(); fbHelper.save(selectedDate[0], p, "no"); } 
                updateRoomRecord(r); ui.showSmartBanner(root, lang.get("Qaza Saved"), lang.get("Entire day marked as pending Qaza."), "img_warning", colorAccent, null); loadTodayPage(); refreshWidget(); return true;""", c)
open(m_path,'w').write(c)

# 4. CalendarHelper: Borders & Limits
c_path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
c = open(c_path).read()
o_c1 = """tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : (isDayCompleted ? colorAccent : themeColors[2])));\n                    GradientDrawable bgD = new GradientDrawable(); bgD.setShape(GradientDrawable.OVAL);\n                    if (dKey.equals(selectedDate[0])) { bgD.setColor(colorAccent); tv.setBackground(bgD); }\n                    else if (isDayCompleted && !isFuture) { bgD.setColor(themeColors[5]); tv.setBackground(bgD); }\n                    else { bgD.setColor(android.graphics.Color.TRANSPARENT); tv.setBackground(bgD); }"""
n_c1 = """tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : themeColors[2]));\n                    tv.setBackground(((MainActivity)activity).getProgressBorder(dKey, dKey.equals(selectedDate[0])));"""
c = c.replace(o_c1, n_c1)

o_c2 = """dTv.setTextColor(isSelected ? Color.WHITE : (isFutureDate ? themeColors[4] : (isAllDone ? colorAccent : themeColors[2])));\n                            \n                            GradientDrawable sBg = new GradientDrawable(); sBg.setShape(GradientDrawable.OVAL);\n                            if (isSelected) { sBg.setColor(colorAccent); dTv.setBackground(sBg); } \n                            else if (isAllDone && !isFutureDate) { sBg.setColor(themeColors[5]); dTv.setBackground(sBg); }"""
n_c2 = """dTv.setTextColor(isSelected ? android.graphics.Color.WHITE : (isFutureDate ? themeColors[4] : themeColors[2]));\n                            dTv.setBackground(((MainActivity)activity).getProgressBorder(cellDateKey, isSelected));"""
c = c.replace(o_c2, n_c2)

c_prev_g = """Calendar check = (Calendar) calendarViewPointer.clone(); check.add(Calendar.MONTH, -1);
                if(check.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { 
                    calendarViewPointer.add(Calendar.MONTH, -1); renderGregorian(card, dialog); 
                }"""
n_prev_g = """Calendar check = (Calendar) calendarViewPointer.clone(); check.add(Calendar.MONTH, -1);
                if(check.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { 
                    calendarViewPointer.add(Calendar.MONTH, -1); renderGregorian(card, dialog); 
                } else { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); }"""
c = c.replace(c_prev_g, n_prev_g)

o_prev_h = 'prev.setOnClickListener(new View.OnClickListener() { @Override public void onClick(View v) { hijriViewCal.add(Calendar.DATE, -29); renderHolder[0].run(); } });'
n_prev_h = 'prev.setOnClickListener(v -> { Calendar chk = (Calendar) hijriViewCal.clone(); chk.add(Calendar.DATE, -29); if(chk.get(Calendar.YEAR) >= Calendar.getInstance().get(Calendar.YEAR) - 100) { hijriViewCal.add(Calendar.DATE, -29); renderHolder[0].run(); } else { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } });'
c = c.replace(o_prev_h, n_prev_h)

c = c.replace('yMain.addView(sv, new LinearLayout.LayoutParams(-1, (int)(380*DENSITY)));', 'yMain.addView(sv, new LinearLayout.LayoutParams(-1, (int)(350*DENSITY)));')
c = c.replace('FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(280*DENSITY), -2);', 'FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(300*DENSITY), -2);')
open(c_path,'w').write(c)

print("✅ Phase 2: Magic Borders & Layout Sync Applied Successfully!")
