import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. ফাইল রিড
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ১৬: টেলিগ্রামের মতো স্মুথ ফেড অ্যানিমেশন (রিস্টার্ট বা লাফানো হাইড করা)
            theme_switch = 'finish(); android.content.Intent tIntent = getIntent(); tIntent.addFlags(android.content.Intent.FLAG_ACTIVITY_NO_ANIMATION); startActivity(tIntent); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);'
            new_content = re.sub(r'finish\(\);\s*(?:overridePendingTransition[^;]+;\s*)?startActivity\(getIntent\(\)\);\s*(?:overridePendingTransition[^;]+;)?', theme_switch, new_content)
            
            # ফিক্স ১৭: কার্ড এবং বাটনের বর্ডার রেডিয়াস সমান এবং মডার্ন (16f) করা
            new_content = re.sub(r'setCornerRadius\(\s*[0-9]+f\s*\*\s*DENSITY\s*\)', 'setCornerRadius(16f * DENSITY)', new_content)
            
            # ফিক্স ১৮: ছোট স্ক্রিনের জন্য মার্জিন/প্যাডিং অপ্টিমাইজেশন (20 থেকে 16 করা হলো)
            new_content = new_content.replace('20 * DENSITY', '16 * DENSITY').replace('20*DENSITY', '16*DENSITY')
            
            # ফিক্স ১৯: লম্বা লিস্টে (যেমন ইয়ার পিকার) সুন্দর স্ক্রলবার ভিজিবল করা
            new_content = re.sub(r'(ScrollView\s+(\w+)\s*=\s*new\s+ScrollView\([^)]+\);)', r'\1 \2.setVerticalScrollBarEnabled(true); \2.setScrollbarFadingEnabled(false);', new_content)
            
            # ফিক্স ২০: ইনপুট ফিল্ড (EditText) এর পুরোনো দাগ মুছে আধুনিক গ্রে-বক্স (Gray Box) স্টাইল করা
            et_modern = r'\1 { android.graphics.drawable.GradientDrawable gdEt = new android.graphics.drawable.GradientDrawable(); gdEt.setColor(android.graphics.Color.parseColor("#1A888888")); gdEt.setCornerRadius(12f * android.content.res.Resources.getSystem().getDisplayMetrics().density); \2.setBackground(gdEt); \2.setPadding((int)(16*android.content.res.Resources.getSystem().getDisplayMetrics().density), (int)(16*android.content.res.Resources.getSystem().getDisplayMetrics().density), (int)(16*android.content.res.Resources.getSystem().getDisplayMetrics().density), (int)(16*android.content.res.Resources.getSystem().getDisplayMetrics().density)); }'
            new_content = re.sub(r'(EditText\s+(\w+)\s*=\s*new\s+EditText\([^)]+\);)', et_modern, new_content)

            # ২. পরিবর্তন হলে ফাইলে সেভ করা হবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 4 (Design 16-20) applied safely!")
