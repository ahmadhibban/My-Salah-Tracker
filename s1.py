import re
f='app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c=open(f).read()
c=re.sub(r'streakBadge\.setText\((streakCount.*?)\);',r'streakBadge.setText(String.valueOf(\1));',c)
mks=["private ZikrManager zikrMan", "static class ZikrManager", "class ZikrCanvasView", "private void loadZikrTab"]
idx=[c.find(m) for m in mks if c.find(m)!=-1]
if idx: c=c[:min(idx)]
o,x=c.count('{'),c.count('}')
if o>x: c+='}\n'*(o-x)
elif x>o: 
    for _ in range(x-o): c=c[:c.rfind('}')]
l=c.rfind('}')
open(f,'w').write(c[:l]+"\n//_ZIKR_\n}")
print("✅ Step 1: Cleaned & Balanced perfectly!")
