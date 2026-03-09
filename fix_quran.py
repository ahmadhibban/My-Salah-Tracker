import os

fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/QuranFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

old_code = 'boolean isBn = false; try { isBn = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}'
new_code = 'boolean isBnTemp = false; try { isBnTemp = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}\n        final boolean isBn = isBnTemp;'

code = code.replace(old_code, new_code)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: QuranFragment 'isBn' Error Fixed!")
