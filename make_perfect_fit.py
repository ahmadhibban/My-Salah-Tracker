import os
import re

def main():
    target_dir = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for root_path in search_paths:
        if not os.path.exists(root_path): continue
        for root, dirs, files in os.walk(root_path):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: 
                target_dir = root
                break
        if target_dir: break

    if target_dir:
        file_path = os.path.join(target_dir, 'MainActivity.java')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # ১. নামাজের কার্ডের মার্জিন (ডানে-বামে ৪৫ থাকবে, ওপর-নিচে ২৫ থেকে কমিয়ে ১৪ করা হলো)
        content = re.sub(r'cardParams\.setMargins\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\);', 'cardParams.setMargins(45, 14, 45, 14);', content)
        
        # ২. নামাজের কার্ডের ভেতরের প্যাডিং (ডানে-বামে ৪০ থাকবে, ওপর-নিচে ৪৫ থেকে কমিয়ে ২৬ করা হলো)
        content = re.sub(r'card\.setPadding\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\);', 'card.setPadding(40, 26, 40, 26);', content)
        
        # ৩. পার্সেন্টেজ কার্ডের মার্জিন (ডানে-বামে ৪৫ থাকবে, ওপর-নিচে ৩০/৪০ থেকে কমিয়ে ২০ করা হলো)
        content = re.sub(r'headerParams\.setMargins\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\);', 'headerParams.setMargins(45, 20, 45, 20);', content)
        
        # ৪. পার্সেন্টেজ কার্ডের ভেতরের প্যাডিং (ডানে-বামে ৫০ থাকবে, ওপর-নিচে ৫০ থেকে কমিয়ে ৩৫ করা হলো)
        content = re.sub(r'pCard\.setPadding\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\);', 'pCard.setPadding(50, 35, 50, 35);', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ পারফেক্ট! লেআউটের ব্যালেন্স ঠিক রেখে শুধুমাত্র ওপর-নিচের স্পেস কমানো হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
