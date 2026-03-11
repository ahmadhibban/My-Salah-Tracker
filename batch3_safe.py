import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. নিরাপদে রিড
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ১১: পুরোনো গেমের মতো লাফানো অ্যানিমেশন (Bounce) রিমুভ করা
            new_content = re.sub(r'v\.animate\(\)\.scaleX\(0\.95f\)\.scaleY\(0\.95f\)\.setDuration\(50\)\.start\(\);', '', new_content)
            new_content = re.sub(r'v\.animate\(\)\.scaleX\(1f\)\.scaleY\(1f\)\.setDuration\(50\)\.start\(\);', '', new_content)
            
            # ফিক্স ১২: ডার্ক মোডে সাবটেক্সটের কালার কন্ট্রাস্ট ঠিক করা (পড়তে আরাম হবে)
            new_content = new_content.replace('Color.parseColor("#A0A0A5")', 'Color.parseColor("#B0B0B5")')
            
            # ফিক্স ১৩: ডায়ালগের টাইটেল যেন ভেঙে দুই লাইনে না যায় (Single Line)
            new_content = re.sub(r'(TextView\s+(\w+)\s*=\s*new\s+TextView\([^)]+\);)', r'\1 \2.setSingleLine(true); \2.setEllipsize(android.text.TextUtils.TruncateAt.END);', new_content)
            
            # ফিক্স ১৪: সাকসেস মেসেজের সবুজ কালারটিকে আরও আধুনিক করা (Emerald Green)
            new_content = new_content.replace('Color.parseColor("#22C55E")', 'Color.parseColor("#10B981")')
            
            # ফিক্স ১৫: চেক বক্সের টিক চিহ্নগুলো আরও সেন্টারে আনা
            new_content = new_content.replace('setGravity(Gravity.CENTER)', 'setGravity(Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL)')

            # ২. শুধু পরিবর্তন হলেই রাইট করবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 3 (Design 11-15) applied safely!")
