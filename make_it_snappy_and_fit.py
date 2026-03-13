import os
import re

def main():
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    main_path = None
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: main_path = os.path.join(root, 'MainActivity.java'); break
        if main_path: break

    if main_path:
        with open(main_path, 'r', encoding='utf-8') as f: 
            content = f.read()

        # ==========================================
        # ফিক্স ১: সুপার ফাস্ট টিক চিহ্ন (০ ল্যাটেন্সি)
        # ==========================================
        # যেকোনো postDelayed ডিলে মুছে সরাসরি আপডেট মেথড কল করা হচ্ছে
        content = re.sub(
            r'\w+\.postDelayed\(\s*new\s+Runnable\(\)\s*\{\s*@Override\s*public\s+void\s+run\(\)\s*\{\s*loadTodayPage\(\);\s*refreshWidget\(\);\s*\}\s*\}\s*,\s*\d+\s*\);', 
            'loadTodayPage(); refreshWidget();', 
            content
        )
        # যদি অন্য ফরম্যাটে থাকে, তার জন্যও ব্যাকআপ
        content = re.sub(r'postDelayed\(([^,]+),\s*[1-9]\d*\)', r'postDelayed(\1, 0)', content)

        # ==========================================
        # ফিক্স ২: এক্সট্রিম সাইজ রিডাকশন (এক পেইজে ফিট)
        # ==========================================
        # ১. পার্সেন্টেজ কার্ডের ওপর-নিচের স্পেস কমানো
        content = re.sub(r'headerParams\.setMargins\([^;]+;', 'headerParams.setMargins((int)(15*DENSITY), (int)(5*DENSITY), (int)(15*DENSITY), (int)(5*DENSITY));', content)
        content = re.sub(r'pCard\.setPadding\([^;]+;', 'pCard.setPadding((int)(15*DENSITY), (int)(10*DENSITY), (int)(15*DENSITY), (int)(10*DENSITY));', content)
        
        # ২. ৬টি নামাজের কার্ডের ওপর-নিচের স্পেস সবচেয়ে বেশি কমানো
        content = re.sub(r'cardParams\.setMargins\([^;]+;', 'cardParams.setMargins((int)(15*DENSITY), (int)(3*DENSITY), (int)(15*DENSITY), (int)(3*DENSITY));', content)
        content = re.sub(r'card\.setPadding\([^;]+;', 'card.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY));', content)

        with open(main_path, 'w', encoding='utf-8') as f: 
            f.write(content)
        print("✅ চ্যালেঞ্জ সম্পন্ন! টিক চিহ্ন এখন রকেটের মতো ফাস্ট এবং পুরো অ্যাপ এক পেইজে ফিট।")
    else:
        print("❌ MainActivity.java খুঁজে পাওয়া যায়নি।")

if __name__ == '__main__': main()
