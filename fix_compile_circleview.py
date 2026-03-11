import os

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('MainActivity.java'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # কম্পাইল এরর ফিক্স: ভুল লাইনটি মুছে আগের সঠিক মেথডটি ফিরিয়ে আনা হচ্ছে
            new_content = content.replace('/* Removed loadTodayPage to fix flash */ refreshWidget(); if(circleView != null) circleView.invalidate();', 'loadTodayPage(); refreshWidget();')

            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Compile errors fixed! Removed the invalid circleView reference.")
