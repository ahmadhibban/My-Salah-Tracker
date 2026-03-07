import re

ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()

# 1. মেইন পেজ থেকে কাস্টম নফল বাটন মুছে ফেলা
c = re.sub(r'// CUSTOM NAFL.*?contentArea\.addView\(cardsContainer\);', 'contentArea.addView(cardsContainer);', c, flags=re.DOTALL)

# 2. মেইন পেজের সুন্নাহ কাউন্টারে নতুন নফলের হিসাব যুক্ত করা
new_sunnah_logic = '''int doneSunnahs = 0; int totalS = AppConstants.SUNNAHS[i].length; 
                for(String sName : AppConstants.SUNNAHS[i]) { if (sp.getString(selectedDate[0]+"_"+name+"_Sunnah_"+sName, "no").equals("yes")) doneSunnahs++; }
                String cStr = sp.getString("custom_nafl_" + name, "");
                if(!cStr.isEmpty()) { for(String cN : cStr.split(",")) { if(cN.contains(":")) cN = cN.split(":")[0]; totalS++; if("yes".equals(sp.getString(selectedDate[0]+"_"+name+"_Custom_"+cN, "no"))) doneSunnahs++; } }
                String sText = totalS > 1 ? (lang.get("Extras") + " (" + lang.bnNum(doneSunnahs) + "/" + lang.bnNum(totalS) + ")") : (i == 5 ? lang.get("Tahajjud") : lang.get("Sunnah"));'''

s_idx = c.find('int doneSunnahs = 0;')
e_idx = c.find('sunnahBtn.setText(sText);', s_idx)
if s_idx != -1 and e_idx != -1:
    c = c[:s_idx] + new_sunnah_logic + "\n                " + c[e_idx:]

open(ma, 'w').write(c)

# 3. StatsHelper ফিক্স
shF = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
sh = open(shF).read()
old_get = r'private int getTotalExtras\(String dKey\) \{.*?return c;\s*\}'
new_get = '''private int getTotalExtras(String dKey) {
        int c = 0; for(int p=0; p<prayers.length; p++) { 
            String pr = prayers[p];
            for(String sn : AppConstants.SUNNAHS[p]) if("yes".equals(sp.getString(dKey+"_"+pr+"_Sunnah_"+sn, "no"))) c++; 
            String cStr = sp.getString("custom_nafl_" + pr, "");
            if(!cStr.isEmpty()) { for(String cN : cStr.split(",")) { if(cN.contains(":")) cN = cN.split(":")[0]; if("yes".equals(sp.getString(dKey+"_"+pr+"_Custom_"+cN, "no"))) c++; } }
        }
        return c;
    }'''
sh = re.sub(old_get, new_get, sh, flags=re.DOTALL)
open(shF, 'w').write(sh)

print("✅ Part 1 Done!")
