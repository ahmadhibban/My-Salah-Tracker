f3 = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
c3 = open(f3).read()
c3 = c3.replace('tv.setBackground(bgD);', 'tv.setBackground(((MainActivity)activity).getProgressBorder(dKey, dKey.equals(selectedDate[0])));')
c3 = c3.replace('dTv.setBackground(sBg);', 'dTv.setBackground(((MainActivity)activity).getProgressBorder(cellDateKey, isSelected));')
open(f3,'w').write(c3)
print("✅ Part 3 Done!")
