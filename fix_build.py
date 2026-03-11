import os

def fix_compilation_errors():
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

    # যে মেথডগুলো View-এর জন্য প্রযোজ্য নয় সেগুলো মুছে ফেলা হচ্ছে
    
    # themeToggleBtn এর ফিক্স
    code = code.replace("themeToggleBtn.setIncludeFontPadding(false);", "")
    code = code.replace("themeToggleBtn.setGravity(android.view.Gravity.CENTER);", "")
    
    # offBtn এর ফিক্স
    code = code.replace("offBtn.setIncludeFontPadding(false);", "")
    code = code.replace("offBtn.setGravity(android.view.Gravity.CENTER);", "")
    
    # periodBtn এর ফিক্স
    code = code.replace("periodBtn.setIncludeFontPadding(false);", "")
    code = code.replace("periodBtn.setGravity(android.view.Gravity.CENTER);", "")
    
    # settingsBtn এর ফিক্স
    code = code.replace("settingsBtn.setIncludeFontPadding(false);", "")
    code = code.replace("settingsBtn.setGravity(android.view.Gravity.CENTER);", "")

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
        
    print("✔ Build Errors Fixed Successfully! Invalid method calls removed.")

fix_compilation_errors()
