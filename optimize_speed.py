import os
import re

def main():
    target_dir = None
    for root_path in ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']:
        if not os.path.exists(root_path): continue
        for root, dirs, files in os.walk(root_path):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: target_dir = root; break
        if target_dir: break

    if target_dir:
        file_path = os.path.join(target_dir, 'MainActivity.java')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # ১. Latency অপ্টিমাইজেশন (150ms -> 20ms)
        content = re.sub(r'postDelayed\(([^,]+),\s*150\s*\)', r'postDelayed(\1, 20)', content)
        
        # ২. Animation Speed অপ্টিমাইজেশন (100ms -> 35ms)
        content = re.sub(r'setDuration\(\s*100\s*\)', 'setDuration(35)', content)

        # ৩. পার্সেন্টেজ টেক্সট ভিউতে Tag যুক্ত করা
        if 'setTag("PERCENT_TEXT")' not in content:
            # যেখানে পার্সেন্টেজ টেক্সট সেট হচ্ছে, ঠিক সেখানেই ট্যাগ বসিয়ে দেওয়া হবে
            content = re.sub(r'(\w+)\.setText\(([^)]*%\w*[^)]*)\);', r'\1.setText(\2);\n            \1.setTag("PERCENT_TEXT");', content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ স্পিড অপ্টিমাইজড! ল্যাটেন্সি 20ms এবং অ্যানিমেশন 35ms করা হয়েছে। ট্যাগ যুক্ত হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
