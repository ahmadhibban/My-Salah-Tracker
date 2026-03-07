import re
f4 = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c4 = open(f4).read()
c4 = c4.replace('setLabelCount(6, true)', 'setLabelCount(7, true)')
# Weekly Double Bar Logic injection
old_bar = "float total = count + excCount; entries.add(new com.github.mikephil.charting.data.BarEntry((float)i, total));"
new_bar = """float total = count + excCount; int sCount = 0; if(isWeekly && r!=null) { for(String p : prayers) { for(String sN : AppConstants.SUNNAHS[java.util.Arrays.asList(prayers).indexOf(p)]) { if(sp.getString(dK+"_"+p+"_Sunnah_"+sN, "no").equals("yes")) sCount++; } } } 
            entries.add(new com.github.mikephil.charting.data.BarEntry(isWeekly ? i - 0.2f : (float)i, total));"""
c4 = c4.replace(old_bar, new_bar)
open(f4,'w').write(c4)
print("✅ Part 4 Done!")
