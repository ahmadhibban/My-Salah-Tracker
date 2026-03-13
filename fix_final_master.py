import os
import re

def main():
    target_main = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: 
                target_main = os.path.join(root, 'MainActivity.java')
                break
        if target_main: break

    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # ==========================================
        # ১. টাচ রেসপন্স রকেটের মতো ফাস্ট করা (০ ল্যাটেন্সি)
        # ==========================================
        # যেকোনো ডিলে (postDelayed) রিমুভ করে সাথে সাথে মেথড কল করা হচ্ছে
        content = re.sub(
            r'v\.postDelayed\(\s*new\s+Runnable\(\)\s*\{\s*@Override\s*public\s+void\s+run\(\)\s*\{\s*loadTodayPage\(\);\s*refreshWidget\(\);\s*\}\s*\}\s*,\s*\d+\s*\);', 
            'loadTodayPage(); refreshWidget();', 
            content
        )
        # লাম্বডা এক্সপ্রেশন থাকলে তার জন্যও ফিক্স
        content = re.sub(
            r'v\.postDelayed\(\s*\(\)\s*->\s*\{\s*loadTodayPage\(\);\s*refreshWidget\(\);\s*\}\s*,\s*\d+\s*\);', 
            'loadTodayPage(); refreshWidget();', 
            content
        )

        # ==========================================
        # ২. এক পেইজে ফিট করা (ফোর্সফুল সাইজ রিডাকশন)
        # ==========================================
        # পার্সেন্টেজ কার্ডের ওপর-নিচের স্পেস একদম মিনিমাম করা হলো
        content = re.sub(r'pCard\.setPadding\([^;]+;', 'pCard.setPadding((int)(20*DENSITY), (int)(5*DENSITY), (int)(20*DENSITY), (int)(5*DENSITY));', content)
        content = re.sub(r'headerParams\.setMargins\([^;]+;', 'headerParams.setMargins((int)(20*DENSITY), (int)(3*DENSITY), (int)(20*DENSITY), (int)(3*DENSITY));', content)
        
        # নামাজের কার্ডগুলোর ওপর-নিচের স্পেস সবচেয়ে বেশি কমানো হলো
        content = re.sub(r'card\.setPadding\([^;]+;', 'card.setPadding((int)(20*DENSITY), (int)(8*DENSITY), (int)(20*DENSITY), (int)(8*DENSITY));', content)
        content = re.sub(r'cardParams\.setMargins\([^;]+;', 'cardParams.setMargins((int)(20*DENSITY), (int)(3*DENSITY), (int)(20*DENSITY), (int)(3*DENSITY));', content)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ শেষ মিশন সফল! টাচ রেসপন্স এখন জিরো-ডিলে এবং অ্যাপটি এক পেইজেই ফিট হবে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
