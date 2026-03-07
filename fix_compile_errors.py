import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(f).read()

# 1. ডাবল @Override ফিক্স
c = re.sub(r'@Override\s*@Override\s*protected\s+void\s+onResume', r'@Override protected void onResume', c)

# 2. ডায়ালগগুলোকে ক্লাসের ব্র্যাকেটের ভেতরে ঢোকানো
idx = c.find("private void showAddCustomPrayerDialog()")
if idx != -1:
    pre = c[:idx]
    post = c[idx:]
    
    # ভুলে বসে যাওয়া অতিরিক্ত '}' মুছে ফেলা
    last_brace = pre.rfind('}')
    if last_brace != -1:
        pre = pre[:last_brace] + pre[last_brace+1:]
        
    c = pre + post
    
    # ফাইলের শেষে ক্লাসের জন্য একটি '}' নিশ্চিত করা
    c = c.rstrip()
    if not c.endswith('}'):
        c += '\n}'

open(f, 'w').write(c)
print("✅ All 3 Build Errors Fixed! Ready to hit Play (▶️)!")
