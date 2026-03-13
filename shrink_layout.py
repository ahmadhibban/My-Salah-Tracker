import os
import re

def scale_down_padding(match):
    v1, v2, v3, v4 = map(int, match.groups())
    # ৪০% সাইজ কমানো হচ্ছে যাতে এক স্ক্রিনে ধরে
    return f"setPadding({max(5, int(v1*0.6))}, {max(5, int(v2*0.6))}, {max(5, int(v3*0.6))}, {max(5, int(v4*0.6))})"

def scale_down_margin(match):
    v1, v2, v3, v4 = map(int, match.groups())
    return f"setMargins({max(0, int(v1*0.6))}, {max(0, int(v2*0.6))}, {max(0, int(v3*0.6))}, {max(0, int(v4*0.6))})"

def main():
    target_dir = None
    for root, dirs, files in os.walk('.'):
        if 'Android/data' in root or '.git' in root: continue
        if 'MainActivity.java' in files: target_dir = root; break
    if not target_dir:
        for root, dirs, files in os.walk('/storage/emulated/0/'):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: target_dir = root; break

    if target_dir:
        file_path = os.path.join(target_dir, 'MainActivity.java')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # প্যাডিং এবং মার্জিন খুঁজে বের করে কমানো
        content = re.sub(r'setPadding\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', scale_down_padding, content)
        content = re.sub(r'setMargins\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', scale_down_margin, content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ চমৎকার! কার্ডগুলোর অতিরিক্ত স্পেস কমিয়ে অ্যাপটিকে এক স্ক্রিনের উপযোগী করা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
