import os

def main():
    print("🔍 MainActivity.java খোঁজা হচ্ছে...")
    target_dir = None
    search_roots = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    # MainActivity ফাইলটি খোঁজার কাজ
    for root in search_roots:
        if not os.path.exists(root): continue
        for dirpath, _, filenames in os.walk(root):
            if 'Android/data' in dirpath or '.git' in dirpath: continue
            if 'MainActivity.java' in filenames:
                target_dir = dirpath
                break
        if target_dir: break

    if target_dir:
        file_path = os.path.join(target_dir, 'MainActivity.java')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # চাঁদ/সূর্যের কোড ব্লকটি টার্গেট করা
        marker1 = "TextView artDisplay = new TextView(this);"
        marker2 = "artDisplay.setText(isDayTime ? \"☀️\" : \"🌙\");"
        marker3 = "contentArea.addView(pNeo);"

        if marker1 in content and marker2 in content and marker3 in content:
            start_idx = content.find(marker1)
            end_idx = content.find(marker3, start_idx) + len(marker3)
            
            old_block = content[start_idx:end_idx]
            
            # নতুন 3D তাসবিহ কাউন্টার বসানোর কোড
            new_block = """PremiumTasbihView tasbihView = new PremiumTasbihView(this, isDarkTheme, colorAccent);
        tasbihView.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 0.8f));
        pCard.addView(left); 
        pCard.addView(tasbihView); 
        contentArea.addView(pNeo);"""
            
            new_content = content.replace(old_block, new_block)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✅ সফল হয়েছে! MainActivity.java তে চাঁদ/সূর্যের জায়গায় প্রিমিয়াম ৩ডি তাসবিহ কাউন্টার বসানো হয়েছে।")
        else:
            print("❌ এরর: MainActivity.java তে নির্দিষ্ট কোড ব্লক পাওয়া যায়নি। হয়তো আগেই পরিবর্তন করা হয়েছে।")
    else:
        print("❌ এরর: MainActivity.java ফাইলটি পাওয়া যায়নি।")

if __name__ == '__main__':
    main()
