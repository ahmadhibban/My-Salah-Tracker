import re

f = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# 1. Remove Sunnah Bar setup from Monthly chart
old_bar_setup = r'if\(isWeekly\)\{.*?bd\.setBarWidth\(0\.3f\);.*?\} else \{ bd=new com\.github\.mikephil\.charting\.data\.BarData\(fs\); bd\.setBarWidth\(0\.5f\); bc\.getXAxis\(\)\.setAxisMinimum\(-0\.5f\); bc\.getXAxis\(\)\.setAxisMaximum\(totalDays-0\.5f\); \}'

new_bar_setup = r'''if(isWeekly){ 
            com.github.mikephil.charting.data.BarDataSet ss=new com.github.mikephil.charting.data.BarDataSet(sE, "Sunnah"); 
            ss.setColor(android.graphics.Color.parseColor("#F59E0B")); ss.setDrawValues(false);
            bd=new com.github.mikephil.charting.data.BarData(fs, ss); bd.setBarWidth(0.3f);
            bc.getXAxis().setAxisMinimum(-0.5f); bc.getXAxis().setAxisMaximum(6.5f);
        } else { 
            bd=new com.github.mikephil.charting.data.BarData(fs); bd.setBarWidth(0.5f);
            bc.getXAxis().setAxisMinimum(-0.5f); bc.getXAxis().setAxisMaximum(totalDays-0.5f);
            bc.getXAxis().setGranularity(1f); bc.getXAxis().setCenterAxisLabels(false);
        }'''

c = re.sub(old_bar_setup, new_bar_setup, c, flags=re.DOTALL)

# 2. Fix the Legends (Remove Sunnah legend from monthly)
old_legend = r'String\[\] lN = isBn \? new String\[\]\{"ফরজ", "সুন্নাহ", "ছুটি"\} : new String\[\]\{"Fard", "Sunnah", "Excused"\};\s*int\[\] lC = new int\[\]\{android\.graphics\.Color\.parseColor\("#22C55E"\), android\.graphics\.Color\.parseColor\("#F59E0B"\), android\.graphics\.Color\.parseColor\("#8B5CF6"\)\};'

new_legend = r'''String[] lN = isBn ? (isWeekly ? new String[]{"ফরজ", "সুন্নাহ", "ছুটি"} : new String[]{"ফরজ", "ছুটি"}) : (isWeekly ? new String[]{"Fard", "Sunnah", "Excused"} : new String[]{"Fard", "Excused"});
        int[] lC = isWeekly ? new int[]{android.graphics.Color.parseColor("#22C55E"), android.graphics.Color.parseColor("#F59E0B"), android.graphics.Color.parseColor("#8B5CF6")} : new int[]{android.graphics.Color.parseColor("#22C55E"), android.graphics.Color.parseColor("#8B5CF6")};'''

c = re.sub(old_legend, new_legend, c)

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Monthly Stats Chart (Cleaned & Aligned) FIXED!")
