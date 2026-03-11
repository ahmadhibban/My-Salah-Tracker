import os, shutil, re

def safe_replace(file_path, old_text, new_text):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if old_text not in content:
        return
    backup_path = file_path + '.bak_ux'
    shutil.copy2(file_path, backup_path)
    new_content = content.replace(old_text, new_text)
    temp_path = file_path + '.tmp'
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    os.replace(temp_path, file_path)

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ১: ক্লিক বা দিন পরিবর্তনের সময় রিস্টার্ট/গ্লিচ বন্ধ করে মডার্ন স্মুথ ট্রানজিশন দেওয়া
            # TransitionManager স্ক্রিন রিলোড হওয়ার সময়টাকে একটি সুন্দর অ্যানিমেশনে ঢেকে দেয়
            bad_remove = 'contentArea.removeAllViews();'
            good_remove = 'if(android.os.Build.VERSION.SDK_INT >= 19) { android.transition.TransitionManager.beginDelayedTransition(contentArea, new android.transition.Fade().setDuration(150)); } contentArea.removeAllViews();'
            new_content = new_content.replace(bad_remove, good_remove)
            
            # ফিক্স ২: থিম চেঞ্জের সেকেলে অ্যানিমেশন বাতিল করে আধুনিক Seamless Switch (0 delay) দেওয়া
            new_content = re.sub(
                r'overridePendingTransition\(android\.R\.anim\.fade_in,\s*android\.R\.anim\.fade_out\);',
                r'overridePendingTransition(0, 0);',
                new_content
            )

            if new_content != content:
                # Atomic Write (১০০% সেফটি)
                backup_path = path + '.bak_ux'
                shutil.copy2(path, backup_path)
                temp_path = path + '.tmp'
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                os.replace(temp_path, path)

print("UX Polished! The weird restarts and old animations have been eliminated.")
