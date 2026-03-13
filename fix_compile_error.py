import os
import re

def main():
    target_main = None
    for r in ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']:
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

        # অরিজিনাল statusMsgs লিস্টটি খুঁজে বের করা
        match = re.search(r'String\[\]\s+statusMsgs\s*=\s*\{[^}]+\};', content)
        if match:
            decl = match.group(0)
        else:
            decl = 'String[] statusMsgs = {lang.get("0/6 Completed"), lang.get("1/6 Completed"), lang.get("2/6 Completed"), lang.get("3/6 Completed"), lang.get("4/6 Completed"), lang.get("5/6 Completed"), lang.get("Alhamdulillah, all completed!")};'

        # updateLivePercentage মেথডের ভেতরে মিসিং ভেরিয়েবলটি বসিয়ে দেওয়া
        if 'private void updateLivePercentage' in content:
            parts = content.split('private void updateLivePercentage')
            if 'String[] statusMsgs' not in parts[1].split('} catch')[0]:
                parts[1] = re.sub(r'(if\s*\(\s*subBtm\s*!=\s*null\s*\)\s*subBtm\.setText\(\s*statusMsgs\[nC\]\s*\);)', decl + r' \1', parts[1])
                content = parts[0] + 'private void updateLivePercentage' + parts[1]
                with open(target_main, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ কম্পাইল এরর একদম নিখুঁতভাবে ফিক্স করা হয়েছে!")
            else:
                print("⚠️ আগেই ফিক্স করা হয়েছে!")
        else:
            print("❌ updateLivePercentage মেথডটি পাওয়া যায়নি।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
