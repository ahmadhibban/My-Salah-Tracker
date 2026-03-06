import os
import re

path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    # আমাদের আগের বসানো ব্লকটি খুঁজে বের করা
    pattern = r'boolean\s+isAllDone\s*=\s*true;\s*SalahRecord\s+dRec\s*=\s*SalahDatabase\.getDatabase\(activity\)\.salahDao\(\)\.getRecordByDate\(dKey\);.*?cell\.addView\(tv\);'
    
    match = re.search(pattern, c, re.DOTALL)
    if match:
        old_block = match.group(0)
        # ডুপ্লিকেট নাম এড়াতে isAllDone কে isDayCompleted দিয়ে রিপ্লেস করা
        new_block = old_block.replace('isAllDone', 'isDayCompleted')
        c = c.replace(old_block, new_block)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ Variable Duplication Fixed (Changed to isDayCompleted)!")
    else:
        print("⚠️ Code block not found! Might be already fixed?")
else:
    print("❌ CalendarHelper.java not found.")
