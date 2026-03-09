f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f, 'r', encoding='utf-8').read()
s_idx = c.find("static class ZikrManager {")
e_idx = c.find("private void loadStatsTab()")
if s_idx != -1 and e_idx != -1:
    c = c[:s_idx] + "\n    // ZIKR_MGR_PLACEHOLDER\n    " + c[e_idx:]
    open(f, 'w', encoding='utf-8').write(c)
    print("✅ Step 1: Old broken code removed safely.")
