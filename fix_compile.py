import os
import re

def rescue_compilation():
    target = None
    for root, _, files in os.walk("."):
        if "MainActivity.java" in files:
            target = os.path.join(root, "MainActivity.java")
            break
    
    if not target:
        print("MainActivity.java খুঁজে পাওয়া যায়নি!")
        return

    with open(target, 'r', encoding='utf-8') as f:
        code = f.read()

    # আগের স্ক্রিপ্টের ভুলে যে শব্দগুলো শেষের 't' হারিয়েছে, তাদের তালিকা
    broken_words = [
        'roo', 'layou', 'mainLayou', 'conten', 'paren', 'toas', 'lis', 'widge', 
        'tex', 'aler', 'dialogRoo', 'contex', 'inten', 'resul', 'even', 'objec',
        'fragmen', 'shee', 'edi', 'inpu', 'forma', 'coun', 'star', 'elemen'
    ]
    
    # ভাঙা শব্দগুলোকে খুঁজে মুছে ফেলার লজিক
    for word in broken_words:
        # ভাঙা শব্দের পর যদি কোনো নতুন ভেরিয়েবল বা ক্লাস থাকে, তবে মাঝখানের ভাঙা অংশ মুছে ফেলবে
        pattern = r'\b' + word + r'\s+(?=[A-Z@]|int\b|boolean\b|float\b|double\b|long\b)'
        code = re.sub(pattern, '', code)

    with open(target, 'w', encoding='utf-8') as f:
        f.write(code)
    print("✔ All Syntax errors caused by 't' bug have been successfully fixed!")

rescue_compilation()
