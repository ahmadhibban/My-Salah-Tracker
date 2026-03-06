import os
import re

path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # পুরনো ভুল লজিকটি খুঁজে বের করা
    old_pattern = r'Calendar endCal = Calendar\.getInstance\(\);\s*Calendar startCal = Calendar\.getInstance\(\);\s*if \(isWeekly\) \{\s*startCal\.add\(Calendar\.DATE, -6\);\s*\}\s*else \{\s*startCal\.set\(Calendar\.DAY_OF_MONTH, 1\);\s*endCal\.set\(Calendar\.DAY_OF_MONTH, startCal\.getActualMaximum\(Calendar\.DAY_OF_MONTH\)\);\s*if\(endCal\.after\(Calendar\.getInstance\(\)\)\)\s*endCal = Calendar\.getInstance\(\);\s*\}'

    # নতুন শনিবার-কেন্দ্রিক এবং ডায়ালগ-সিঙ্কড লজিক
    new_code = """Calendar startCal = (Calendar) statsCalPointer.clone();
            Calendar endCal = (Calendar) statsCalPointer.clone();
            if (isWeekly) { 
                while (startCal.get(Calendar.DAY_OF_WEEK) != Calendar.SATURDAY) startCal.add(Calendar.DATE, -1);
                endCal = (Calendar) startCal.clone(); endCal.add(Calendar.DATE, 6);
                if(endCal.after(Calendar.getInstance())) endCal = Calendar.getInstance();
            } else { 
                startCal.set(Calendar.DAY_OF_MONTH, 1); 
                endCal.set(Calendar.DAY_OF_MONTH, startCal.getActualMaximum(Calendar.DAY_OF_MONTH)); 
                if(endCal.after(Calendar.getInstance())) endCal = Calendar.getInstance();
            }"""

    if re.search(old_pattern, c):
        c = re.sub(old_pattern, new_code, c)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ Image Share Logic perfectly fixed! (Synced with Stats Pointer)")
    else:
        print("⚠️ Pattern not found. Please check if already applied.")
else:
    print("❌ StatsHelper.java not found.")
