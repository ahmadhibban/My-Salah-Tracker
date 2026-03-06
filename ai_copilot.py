import os

print("\n🚀 AI Co-Pilot Automation Started...\n")

java_dir = 'app/src/main/java'
fixed_date = False

for root, dirs, files in os.walk(java_dir):
    for file in files:
        if file.endswith('.java'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except:
                continue
            
            modified = False
            for i, line in enumerate(lines):
                # উইজেটের "ই" বা "শে" অটো-ফিক্স করা
                if ('SimpleDateFormat' in line or 'format' in line or 'date' in line.lower()) and ('ই' in line or 'শে' in line):
                    lines[i] = line.replace('ই ', '').replace('ই', '').replace('শে ', '').replace('শে', '')
                    print(f"✅ Date Auto-Fixed in: {file} (Line {i+1})")
                    modified = True
                    fixed_date = True
                
                # Mark All বাটন স্নাইপিং
                if 'markall' in line.lower() or 'mark_all' in line.lower():
                    print(f"🎯 'Mark All' Logic Found in: {file} (Line {i+1})")
                    print(f"   👉 আপনার কাজ: {file} ওপেন করে ঠিক এই ফাংশনটি শেষ হওয়ার আগে আপনার মাশাআল্লাহ দেখানোর কোডটি বসিয়ে দিন!")
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

if not fixed_date:
    print("⚠️ Date format pattern strictly matched not found (might be using a custom logic).")

print("\n🎉 AI Script Finished!")
