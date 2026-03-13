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

        def shrink_vertical(match):
            func = match.group(1)
            l, t, r, b = int(match.group(2)), int(match.group(3)), int(match.group(4)), int(match.group(5))
            
            # ডানে-বামে (l, r) একদম ঠিক থাকবে। শুধু ওপর-নিচে (t, b) কমানো হচ্ছে
            new_t = max(2, int(t * 0.45))
            new_b = max(2, int(b * 0.45))
            
            return f"{func}({l}, {new_t}, {r}, {new_b})"

        # স্বয়ংক্রিয়ভাবে সমস্ত setPadding এবং setMargins এ অ্যাপ্লাই হবে
        content = re.sub(r'(setPadding|setMargins)\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', shrink_vertical, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ পারফেক্ট! লেআউটের ডানে-বামের ব্যালেন্স ১০০% ঠিক রেখে ওপর-নিচের জায়গা কমানো হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
