import os, re

backup = "all_code.txt"
for r, d, f in os.walk("."):
    if "all_code.txt" in f:
        backup = os.path.join(r, "all_code.txt")
        break

with open(backup, 'r', encoding='utf-8') as f:
    raw = f.read()

# 'package' কিওয়ার্ড ধরে প্রতিটি ফাইলকে আলাদা করার স্মার্ট লজিক
matches = list(re.finditer(r'package\s+([a-zA-Z0-9_.]+)\s*;', raw))

for i in range(len(matches)):
    start = matches[i].start()
    end = matches[i+1].start() if i + 1 < len(matches) else len(raw)
    
    file_content = raw[start:end].strip()
    pkg_name = matches[i].group(1)
    
    # ফাইলের ভেতর থেকে ক্লাসের নাম খুঁজে বের করা
    class_match = re.search(r'(?:public\s+|abstract\s+|final\s+)*(?:class|interface|enum)\s+([A-Za-z0-9_]+)', file_content)
    if class_match:
        class_name = class_match.group(1)
        
        # প্যাকেজের নাম অনুযায়ী সঠিক ফোল্ডার তৈরি করে ফাইলটি সেভ করা
        rel_path = pkg_name.replace('.', '/')
        save_dir = os.path.join("app/src/main/java", rel_path)
        os.makedirs(save_dir, exist_ok=True)
        
        file_path = os.path.join(save_dir, f"{class_name}.java")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content + "\n")

print("✔ PROJECT COMPLETELY RESTORED FROM BACKUP! 🚀")
