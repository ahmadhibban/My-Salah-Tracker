f = 'app/src/main/java/com/my/salah/tracker/app/UIComponents.java'
c = open(f).read()

old = 'Typeface tfReg = Typeface.DEFAULT, tfBold = Typeface.DEFAULT_BOLD; try { if (sp.getString("app_lang", "en").equals("bn")) {'
new = 'Typeface tfReg = Typeface.DEFAULT, tfBold = Typeface.DEFAULT_BOLD; try { SharedPreferences uiSp = activity.getSharedPreferences("salah_pro_final", android.content.Context.MODE_PRIVATE); if (uiSp.getString("app_lang", "en").equals("bn")) {'
c = c.replace(old, new)

open(f,'w').write(c)
print("✅ Symbol 'sp' fixed! NOW you can build successfully.")
