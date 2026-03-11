f = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c = open(f).read()
old = "float total = count + excCount; int sCount = 0; if(isWeekly && r!=null)"
new = "SalahRecord r = getRoomRecord(dK); float total = count + excCount; int sCount = 0; if(isWeekly && r!=null)"
open(f,'w').write(c.replace(old, new))
print("✅ Fixed! Now build your app.")
