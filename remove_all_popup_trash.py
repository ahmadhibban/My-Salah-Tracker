import os
import re

def main():
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    target_main = None
    
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

        # ১. পপ-আপ মেথডটি পুরোপুরি খুঁজে মুছে ফেলা হচ্ছে
        while True:
            idx = content.find("private void showMashallahPopup")
            if idx == -1: break
            start_brace = content.find('{', idx)
            if start_brace == -1: break
            
            brace_count = 1
            end_brace = start_brace + 1
            while brace_count > 0 and end_brace < len(content):
                if content[end_brace] == '{': brace_count += 1
                elif content[end_brace] == '}': brace_count -= 1
                end_brace += 1
            
            content = content[:idx] + content[end_brace:]

        # ২. পপ-আপ কল করার যত ট্রিগার (if nC == 6...) বা try-catch ব্লক আমি বসিয়েছিলাম, সব ক্লিন করা হচ্ছে
        content = re.sub(r'[ \t]*if\s*\([^)]*\)\s*\{[^{}]*showMashallahPopup[^{}]*\}[ \t]*\n?', '', content)
        content = re.sub(r'showMashallahPopup\([^)]*\);', '', content)

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ আপনার নির্দেশ অনুযায়ী সমস্ত ফালতু পপ-আপ কোড এবং ট্রিগার প্রজেক্ট থেকে চিরতরে মুছে ফেলা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
