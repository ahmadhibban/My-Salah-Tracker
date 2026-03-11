import os

def fix_linearlayout_errors():
    target = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files:
            target = os.path.join(root, "MainActivity.java")
            break
    
    if not target:
        print("MainActivity.java খুঁজে পাওয়া যায়নি!")
        return

    with open(target, 'r', encoding='utf-8') as f:
        code = f.read()

    # LinearLayout এর জন্য অবৈধ মেথডগুলো মুছে ফেলা হচ্ছে
    code = code.replace("markAllBtn.setIncludeFontPadding(false);", "")
    code = code.replace("todayBtn.setIncludeFontPadding(false);", "")

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print("✔ Layout errors fixed successfully!")

fix_linearlayout_errors()
