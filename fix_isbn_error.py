import os

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

        start_idx = content.find('// --- ROZA TRACKER START ---')
        end_idx = content.find('// --- ROZA TRACKER END ---')

        if start_idx != -1 and end_idx != -1:
            roza_block = content[start_idx:end_idx]
            # নাম পরিবর্তন করে isBnRoza করা হচ্ছে যাতে আগের কোডের সাথে কনফ্লিক্ট না করে
            roza_block = roza_block.replace('final boolean isBn =', 'final boolean isBnRoza =')
            roza_block = roza_block.replace('isBn ?', 'isBnRoza ?')
            roza_block = roza_block.replace('b.setTitle(isBn', 'b.setTitle(isBnRoza')
            
            content = content[:start_idx] + roza_block + content[end_idx:]

            with open(target_main, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ 'isBn' নামের কনফ্লিক্ট (ডুপ্লিকেট) ফিক্স করা হয়েছে!")
        else:
            print("❌ রোজার কোড ব্লকটি খুঁজে পাওয়া যায়নি।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
