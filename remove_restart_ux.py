import os, shutil

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # বাজে রিস্টার্ট (Fade) অ্যানিমেশন রিমুভ করে ইনস্ট্যান্ট স্ন্যাপ দেওয়া
            bad_transition = 'if(android.os.Build.VERSION.SDK_INT >= 19) { android.transition.TransitionManager.beginDelayedTransition(contentArea, new android.transition.Fade().setDuration(150)); } contentArea.removeAllViews();'
            new_content = new_content.replace(bad_transition, 'contentArea.removeAllViews();')
            
            # থিম চেঞ্জের অ্যানিমেশনও জিরো করে দেওয়া
            new_content = new_content.replace('overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);', 'overridePendingTransition(0, 0);')

            if new_content != content:
                # Atomic Write (১০০% সেফটি)
                backup_path = path + '.bak4'
                shutil.copy2(path, backup_path)
                temp_path = path + '.tmp'
                with open(temp_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                os.replace(temp_path, path)

print("Bad restart animations removed successfully!")
