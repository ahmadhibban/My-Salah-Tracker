import re
f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f, 'r', encoding='utf-8').read()

# Fix setText error
c = re.sub(r'streakBadge\.setText\((streakCount\s*>=\s*365\s*\?.*?)\);', r'streakBadge.setText(String.valueOf(\1));', c)

# Find end of loadQuranTab to safely cut
q_idx = c.find('private void loadQuranTab()')
if q_idx != -1:
    b = 0; in_m = False; e_idx = q_idx
    for i in range(q_idx, len(c)):
        if c[i] == '{': b += 1; in_m = True
        elif c[i] == '}': b -= 1
        if in_m and b == 0: 
            e_idx = i + 1; break
    c = c[:e_idx] + "\n"

open(f, 'w', encoding='utf-8').write(c)
print("✅ Step 1: Cleaned successfully!")
