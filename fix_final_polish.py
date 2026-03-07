import re

# 1. StatsHelper: Remove Table & Fix PDF Header Align
sp = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
sc = open(sp).read()
sc = re.sub(r'int p2H = \(tD\*35\)\+150;.*?doc\.finishPage\(pg2\);', '', sc, flags=re.DOTALL)
sc = sc.replace('pt.setColor(android.graphics.Color.parseColor("#555555")); pt.setTextSize(14); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); cv.drawText(wT,pd+20,wY+30,pt);',
                'pt.setColor(android.graphics.Color.parseColor("#555555")); pt.setTextSize(14); pt.setTypeface(android.graphics.Typeface.create(appFonts[1],1)); pt.setTextAlign(android.graphics.Paint.Align.LEFT); cv.drawText(wT,pd+20,wY+30,pt);')
open(sp, 'w').write(sc)

# 2. MainActivity: Custom Qaza Image Instead of Emoji
mp = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
mc = open(mp).read()
mc = re.sub(r'TextView mosqueIcon = new TextView\(this\);\s*mosqueIcon\.setText\("🕌"\); mosqueIcon\.setTextSize\(60\); mosqueIcon\.setGravity\(Gravity\.CENTER\); mosqueIcon\.setPadding\(0, \(int\)\(20\*DENSITY\), 0, \(int\)\(10\*DENSITY\)\); list\.addView\(mosqueIcon\);',
            'View customEmptyIcon = ui.getRoundImage("img_empty_qaza", 0, android.graphics.Color.TRANSPARENT, 0); LinearLayout.LayoutParams icLp = new LinearLayout.LayoutParams((int)(80*DENSITY), (int)(80*DENSITY)); icLp.gravity = Gravity.CENTER; icLp.setMargins(0, (int)(20*DENSITY), 0, (int)(10*DENSITY)); customEmptyIcon.setLayoutParams(icLp); list.addView(customEmptyIcon);', mc)
open(mp, 'w').write(mc)

# 3. CalendarHelper: Sync Hijri & Gregorian UI 100%
cp = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
cc = open(cp).read()

cc = cc.replace('final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(15*DENSITY), (int)(20*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));\n        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(20f * DENSITY); main.setBackground(gd);',
                'final LinearLayout main = new LinearLayout(activity); main.setOrientation(LinearLayout.VERTICAL); main.setPadding((int)(20*DENSITY), (int)(25*DENSITY), (int)(20*DENSITY), (int)(25*DENSITY));\n        GradientDrawable gd = new GradientDrawable(); gd.setColor(themeColors[1]); gd.setCornerRadius(25f * DENSITY); gd.setStroke((int)(1.5f*DENSITY), themeColors[4]); main.setBackground(gd);')

cc = cc.replace('FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams((int)(340*DENSITY), -2); flp.gravity = Gravity.CENTER; wrap.addView(main, flp);',
                'FrameLayout.LayoutParams flp = new FrameLayout.LayoutParams(-1, -2); flp.gravity = Gravity.CENTER; flp.setMargins((int)(20*DENSITY), 0, (int)(20*DENSITY), 0); wrap.addView(main, flp);')

cc = cc.replace('yearChip.setPadding((int)(16*DENSITY), (int)(6*DENSITY), (int)(16*DENSITY), (int)(6*DENSITY));\n        GradientDrawable yBg = new GradientDrawable(); yBg.setColor(themeColors[4]); yBg.setCornerRadius(15f * DENSITY); yearChip.setBackground(yBg);',
                'yearChip.setPadding((int)(25*DENSITY), (int)(8*DENSITY), (int)(25*DENSITY), (int)(8*DENSITY));\n        GradientDrawable yBg = new GradientDrawable(); yBg.setColor(colorAccent & 0x15FFFFFF); yBg.setCornerRadius(15f * DENSITY); yearChip.setBackground(yBg);')

cc = cc.replace('TextView cancelBtn = new TextView(activity); cancelBtn.setText(lang.get("CANCEL")); cancelBtn.setTextColor(colorAccent); cancelBtn.setTextSize(14); cancelBtn.setTypeface(Typeface.DEFAULT_BOLD); cancelBtn.setPadding((int)(16*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY), (int)(8*DENSITY));',
                'TextView cancelBtn = new TextView(activity); cancelBtn.setText(lang.get("CLOSE")); cancelBtn.setTextColor(themeColors[3]); cancelBtn.setTextSize(14); cancelBtn.setTypeface(Typeface.DEFAULT_BOLD); cancelBtn.setPadding((int)(15*DENSITY), (int)(15*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY));')

cc = cc.replace('LinearLayout yMain = new LinearLayout(activity); yMain.setOrientation(LinearLayout.VERTICAL); yMain.setPadding(0, (int)(20*DENSITY), 0, (int)(20*DENSITY));\n                GradientDrawable yGd = new GradientDrawable(); yGd.setColor(themeColors[1]); yGd.setCornerRadius(25f * DENSITY); yMain.setBackground(yGd);',
                'LinearLayout yMain = new LinearLayout(activity); yMain.setOrientation(LinearLayout.VERTICAL); yMain.setPadding((int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY), (int)(25*DENSITY));\n                GradientDrawable yGd = new GradientDrawable(); yGd.setColor(themeColors[1]); yGd.setCornerRadius(30f * DENSITY); yGd.setStroke((int)(1.5f*DENSITY), themeColors[4]); yMain.setBackground(yGd);')

cc = cc.replace('if(y == viewHYear) { GradientDrawable bg = new GradientDrawable(); bg.setColor(themeColors[5]); bg.setCornerRadius(15f*DENSITY); yt.setBackground(bg); }',
                '')

open(cp, 'w').write(cc)
print("✅ ALL FINAL POLISHES APPLIED! PDF Table Removed, Alignment Fixed, Image Setup Done!")
