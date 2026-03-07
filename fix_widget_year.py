f = 'app/src/main/java/com/my/salah/tracker/app/SalahWidget.java'
c = open(f).read()

old_bn = 'gregText = bnDays[c.get(Calendar.DAY_OF_WEEK) - 1] + ", " + lang.bnNum(gD) + getBnSuffix(gD) + " " + bnMonths[c.get(Calendar.MONTH)];'
new_bn = 'gregText = bnDays[c.get(Calendar.DAY_OF_WEEK) - 1] + ", " + lang.bnNum(gD) + getBnSuffix(gD) + " " + bnMonths[c.get(Calendar.MONTH)] + " " + lang.bnNum(c.get(Calendar.YEAR));'
c = c.replace(old_bn, new_bn)

old_en = 'SimpleDateFormat sdfGreg = new SimpleDateFormat("EEEE, MMM dd", Locale.US);'
new_en = 'SimpleDateFormat sdfGreg = new SimpleDateFormat("EEEE, MMM dd, yyyy", Locale.US);'
c = c.replace(old_en, new_en)

open(f,'w').write(c)
print("✅ Widget Year added successfully!")
