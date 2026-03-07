import re
le = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
c = open(le).read()
if '"Add Extra Prayer"' not in c:
    c = c.replace('bnMap.put("Settings & Options", "সেটিংস এবং অপশন");',
                  'bnMap.put("Settings & Options", "সেটিংস এবং অপশন");\n        bnMap.put("Add Extra Prayer", "অতিরিক্ত নফল যুক্ত করুন");\n        bnMap.put("Prayer Name (e.g. Ishraq)", "নামাজের নাম (যেমন: ইশরাক)");\n        bnMap.put("Rakats (e.g. 2)", "রাকাত (যেমন: ২)");\n        bnMap.put("Add Prayer", "যুক্ত করুন");\n        bnMap.put("Delete Extra Prayer?", "এই নফল নামাজটি ডিলিট করবেন?");\n        bnMap.put("This will remove it from your list.", "এটি আপনার লিস্ট থেকে মুছে যাবে।");\n        bnMap.put("Rakats", "রাকাত");')
    open(le,'w').write(c)

sh = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
c = open(sh).read()
get_ext = """private int getTotalExtras(String dKey) {
        int c = 0; for(int p=0; p<prayers.length; p++) { for(String sn : AppConstants.SUNNAHS[p]) if("yes".equals(sp.getString(dKey+"_"+prayers[p]+"_Sunnah_"+sn, "no"))) c++; }
        String cStr = sp.getString("custom_nafl_list", "");
        if(!cStr.isEmpty()) { for(String cN : cStr.split(",")) { if(cN.contains(":")) cN = cN.split(":")[0]; if("yes".equals(sp.getString(dKey+"_Custom_"+cN, "no"))) c++; } }
        return c;
    }\n\n    private void applyFont"""
if "getTotalExtras" not in c: c = c.replace('private void applyFont', get_ext)
c = c.replace('if(rec!=null){for(int p=0;p<prayers.length;p++){String fS=getFardStat(rec,prayers[p]); if(fS.equals("yes"))fD++; else if(fS.equals("excused")){fD++;hB=true;} for(String sN:AppConstants.SUNNAHS[p])if("yes".equals(sp.getString(dK+"_"+prayers[p]+"_Sunnah_"+sN,"no")))sD_cnt++;}}',
              'if(rec!=null){for(int p=0;p<prayers.length;p++){String fS=getFardStat(rec,prayers[p]); if(fS.equals("yes"))fD++; else if(fS.equals("excused")){fD++;hB=true;}} sD_cnt += getTotalExtras(dK);}')
c = c.replace('if(r!=null){for(int p=0;p<prayers.length;p++){String st=getFardStat(r,prayers[p]); if(st.equals("yes")){tDn++;dyDn++;}else if(st.equals("excused")){tE++;dyE++;}else{if(getQazaStat(r,prayers[p]))tQ++;else tM++;} if(isWeekly)for(String sN:AppConstants.SUNNAHS[p])if("yes".equals(sp.getString(dK+"_"+prayers[p]+"_Sunnah_"+sN,"no")))sC_cnt++;}}',
              'if(r!=null){for(int p=0;p<prayers.length;p++){String st=getFardStat(r,prayers[p]); if(st.equals("yes")){tDn++;dyDn++;}else if(st.equals("excused")){tE++;dyE++;}else{if(getQazaStat(r,prayers[p]))tQ++;else tM++;}} if(isWeekly) sC_cnt += getTotalExtras(dK);}')
c = c.replace('if(sR!=null){ for(int j=0; j<6; j++){ String st=getFardStat(sR, prayers[j]); if("yes".equals(st)) d++; else if("excused".equals(st)) e++;\n                if(isWeekly) for(String sn : AppConstants.SUNNAHS[j]) if("yes".equals(sp.getString(dK+"_"+prayers[j]+"_Sunnah_"+sn, "no"))) s++; } }',
              'if(sR!=null){ for(int j=0; j<6; j++){ String st=getFardStat(sR, prayers[j]); if("yes".equals(st)) d++; else if("excused".equals(st)) e++; } \n                if(isWeekly) s += getTotalExtras(dK); }')
open(sh,'w').write(c)
print("✅ Part 1 Done!")
