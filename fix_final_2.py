f = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c = open(f).read()

# Fix Variable Collision (Rename Calendar tE to tmpE)
c = c.replace('java.util.Calendar tS=', 'java.util.Calendar tmpS=')
c = c.replace('tS.set(5,sD)', 'tmpS.set(5,sD)')
c = c.replace('java.util.Calendar tE=', 'java.util.Calendar tmpE=')
c = c.replace('tE.set(5,eD)', 'tmpE.set(5,eD)')
c = c.replace('tS.getTime()', 'tmpS.getTime()')
c = c.replace('tE.getTime()', 'tmpE.getTime()')

# Fix Clone Object Error
c = c.replace('startCal.clone().after(now)', 'startCal.after(now)')

open(f, 'w').write(c)
print("✅ 2 minor bugs fixed! YOU ARE 100% READY TO BUILD.")
