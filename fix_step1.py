import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# Fix ambiguous setText
c = re.sub(r'streakBadge\.setText\((streakCount\s*>=\s*365\s*\?.*?)\);', r'streakBadge.setText(String.valueOf(\1));', c)

# Find where the mess starts
markers = ["static class ZikrManager", "class ZikrCanvasView", "private void loadZikrTab()", "private void loadStatsTab()", "private ZikrManager zikrMan"]
idx_list = [c.find(m) for m in markers if c.find(m) != -1]

if idx_list:
    cut_off = min(idx_list)
    c = c[:cut_off]

c = c.rstrip()
while c.endswith('}'): c = c[:-1].rstrip()

with open(f, 'w', encoding='utf-8') as file:
    file.write(c + "\n\n    // ZIKR_PLACEHOLDER\n}\n")
print("✅ Step 1: Cleanup Done.")
