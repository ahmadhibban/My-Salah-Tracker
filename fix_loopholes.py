import re

def rep(file, old, new):
    c = open(file).read()
    if old in c: open(file,'w').write(c.replace(old, new))

# 1. LanguageEngine
rep('app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java', 
    'bnMap.put("Advanced Statistics", "বিস্তারিত রিপোর্ট (PDF)");', 
    'bnMap.put("Advanced Statistics", "বিস্তারিত রিপোর্ট");')

# 2. MainActivity Loophole Fix
c = open('app/src/main/java/com/my/salah/tracker/app/MainActivity.java').read()
c = c.replace('final String dKey = sdf.format(cal.getTime());\n            final boolean isSel', 
              'final String dKey = sdf.format(cal.getTime()); final boolean isTooOld = cal.get(Calendar.YEAR) < now.get(Calendar.YEAR) - 100;\n            final boolean isSel')
c = c.replace('if(isFuture) { ui.showPremiumLocked(colorAccent); } else { selectedDate[0] = dKey; loadTodayPage(); }',
              'if(isFuture) { ui.showPremiumLocked(colorAccent); } else if(isTooOld) { ui.showSmartBanner(root, lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } else { selectedDate[0] = dKey; loadTodayPage(); }')
open('app/src/main/java/com/my/salah/tracker/app/MainActivity.java','w').write(c)

# 3. CalendarHelper Loophole Fix
c = open('app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java').read()
c = c.replace('final int dayNum = currentDay; temp.set(Calendar.DAY_OF_MONTH, dayNum); final String dKey = sdf.format(temp.getTime()); final boolean isFuture = temp.after(now);',
              'final int dayNum = currentDay; temp.set(Calendar.DAY_OF_MONTH, dayNum); final String dKey = sdf.format(temp.getTime()); final boolean isFuture = temp.after(now); final boolean isTooOld = temp.get(Calendar.YEAR) < now.get(Calendar.YEAR) - 100;')
c = c.replace('if(isFuture) { ui.showPremiumLocked(colorAccent); } else { selectedDate[0] = dKey; dialog.dismiss(); if(onDateSelected!=null) onDateSelected.run(); }',
              'if(isFuture) { ui.showPremiumLocked(colorAccent); } else if(isTooOld) { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); } else { selectedDate[0] = dKey; dialog.dismiss(); if(onDateSelected!=null) onDateSelected.run(); }')
c = c.replace('final String cellDateKey = sdf.format(realGregorian.getTime()); final boolean isSelected = cellDateKey.equals(selectedDate[0]);\n                            final boolean isFutureDate = realGregorian.getTime().after(todayCal.getTime()) && !cellDateKey.equals(sdf.format(todayCal.getTime()));',
              'final String cellDateKey = sdf.format(realGregorian.getTime()); final boolean isSelected = cellDateKey.equals(selectedDate[0]);\n                            final boolean isFutureDate = realGregorian.getTime().after(todayCal.getTime()) && !cellDateKey.equals(sdf.format(todayCal.getTime())); final boolean isTooOld = realGregorian.get(Calendar.YEAR) < todayCal.get(Calendar.YEAR) - 100;')
c = c.replace('if (isFutureDate) ui.showPremiumLocked(colorAccent); \n                                    else { selectedDate[0] = cellDateKey; ad.dismiss(); if(onDateSelected!=null) onDateSelected.run(); }',
              'if (isFutureDate) ui.showPremiumLocked(colorAccent); \n                                    else if(isTooOld) { ui.showSmartBanner((android.widget.FrameLayout)activity.findViewById(android.R.id.content), lang.get("Limit Reached"), lang.get("Cannot go back more than 100 years."), "img_warning", colorAccent, null); }\n                                    else { selectedDate[0] = cellDateKey; ad.dismiss(); if(onDateSelected!=null) onDateSelected.run(); }')
open('app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java','w').write(c)

# 4. UIComponents Custom Font Fix
c = open('app/src/main/java/com/my/salah/tracker/app/UIComponents.java').read()
c = c.replace('TextView title = new TextView(activity); title.setText(lang.get("Patience is Virtue")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(Typeface.DEFAULT_BOLD);',
              'Typeface tfReg = Typeface.DEFAULT, tfBold = Typeface.DEFAULT_BOLD; try { if (sp.getString("app_lang", "en").equals("bn")) { tfReg = Typeface.createFromAsset(activity.getAssets(), "fonts/hind_reg.ttf"); tfBold = Typeface.createFromAsset(activity.getAssets(), "fonts/hind_bold.ttf"); } else { tfReg = Typeface.createFromAsset(activity.getAssets(), "fonts/poppins_reg.ttf"); tfBold = Typeface.createFromAsset(activity.getAssets(), "fonts/poppins_bold.ttf"); } } catch(Exception e){} \n        TextView title = new TextView(activity); title.setText(lang.get("Patience is Virtue")); title.setTextColor(themeColors[2]); title.setTextSize(20); title.setTypeface(tfBold);')
c = c.replace('TextView sub = new TextView(activity); sub.setText(lang.get("You cannot mark future prayers.")); sub.setTextColor(themeColors[3]); sub.setTextSize(14); sub.setGravity(Gravity.CENTER); main.addView(sub);',
              'TextView sub = new TextView(activity); sub.setText(lang.get("You cannot mark future prayers.")); sub.setTextColor(themeColors[3]); sub.setTextSize(14); sub.setGravity(Gravity.CENTER); sub.setTypeface(tfReg); main.addView(sub);')
open('app/src/main/java/com/my/salah/tracker/app/UIComponents.java','w').write(c)
print("✅ Loophole & Font issues fixed!")
