import os, re

# 1. Language Engine update
lp = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
lc = open(lp).read()
if '"Invalid Email"' not in lc:
    lc = lc.replace('bnMap.put("Already in Qaza list.", "এই দিনটি আগে থেকেই কাজা লিস্টে যুক্ত আছে।");', 'bnMap.put("Already in Qaza list.", "এই দিনটি আগে থেকেই কাজা লিস্টে যুক্ত আছে।");\n        bnMap.put("Invalid Email", "ভুল ইমেইল");\n        bnMap.put("Please enter a valid email address.", "অনুগ্রহ করে একটি সঠিক ইমেইল অ্যাড্রেস দিন।");')
    open(lp,'w').write(lc)

# 2. Email Validation in BackupHelper
bp = 'app/src/main/java/com/my/salah/tracker/app/BackupHelper.java'
bc = open(bp).read()
bc = re.sub(
    r'String mail = emailIn\.getText\(\)\.toString\(\)\.trim\(\);\s*if \(!mail\.isEmpty\(\)\) \{',
    'String mail = emailIn.getText().toString().trim();\n            if (mail.isEmpty() || !android.util.Patterns.EMAIL_ADDRESS.matcher(mail).matches()) { ui.showSmartBanner(root, lang.get("Invalid Email"), lang.get("Please enter a valid email address."), "img_warning", colorAccent, null); return; }\n            if (!mail.isEmpty()) {',
    bc
)
open(bp,'w').write(bc)

# 3. Empty Catch Blocks Fix (Logging)
files = ['app/src/main/java/com/my/salah/tracker/app/StatsHelper.java', 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java', 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java', 'app/src/main/java/com/my/salah/tracker/app/FirebaseManager.java', 'app/src/main/java/com/my/salah/tracker/app/BackupHelper.java']
for f in files:
    if os.path.exists(f):
        c = open(f).read()
        c = c.replace('catch(Exception e){}', 'catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }')
        c = c.replace('catch (Exception e) {}', 'catch(Exception e){ android.util.Log.e("SalahTracker", "Error", e); }')
        c = c.replace('catch(Exception ex){}', 'catch(Exception ex){ android.util.Log.e("SalahTracker", "Error", ex); }')
        open(f,'w').write(c)

print("✅ Technical Flaws Fixed: Email Validation & Error Logging active!")
