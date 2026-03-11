import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. ফাইল রিড
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ৪১: Paint অবজেক্টগুলোতে Anti-Aliasing যুক্ত করা, যেন বৃত্ত বা প্রোগ্রেসবারগুলো পিক্সেল-ফাটা না হয়ে একদম স্মুথ দেখায়
            new_content = new_content.replace('new Paint()', 'new Paint(android.graphics.Paint.ANTI_ALIAS_FLAG)')
            
            # ফিক্স ৪২: প্রোগ্রেসবারের (বা যেকোনো কাস্টম লাইনের) প্রান্তগুলো চারকোনা না হয়ে সুন্দর রাউন্ড (Round) শেপ হবে
            new_content = new_content.replace('Paint.Style.STROKE);', 'Paint.Style.STROKE); p.setStrokeCap(android.graphics.Paint.Cap.ROUND);')
            new_content = new_content.replace('paint.setStyle(android.graphics.Paint.Style.STROKE);', 'paint.setStyle(android.graphics.Paint.Style.STROKE); paint.setStrokeCap(android.graphics.Paint.Cap.ROUND);')
            
            # ফিক্স ৪৩: জিকির/তাসবিহ সেকশনের মূল কাউন্টার টেক্সটকে (বড় সংখ্যাটি) বোল্ড করা, যেন ফোকাস বেশি পড়ে
            new_content = re.sub(r'(\w+)\.setTextSize\(50\);', r'\1.setTextSize(50); \1.setTypeface(null, android.graphics.Typeface.BOLD);', new_content)
            
            # ফিক্স ৪৪: সাফল্যের ইমোজিটিতে (💎) আরেকটু প্যাডিং বা স্পেসিং দেওয়া যেন তা শ্বাস নেওয়ার জায়গা পায়
            new_content = new_content.replace('setText("💎\\n"', 'setPadding(0, (int)(16*DENSITY), 0, (int)(16*DENSITY)); setText("💎\\n"')
            
            # ফিক্স ৪৫: ছুটির মোডের (Excused) টেক্সটটিকে ইটালিক (Italic) করে আলাদা একটি ভিজ্যুয়াল আইডেন্টিটি দেওয়া
            new_content = new_content.replace('setText(isBn ? "আজকের নামাজ মাফ" : "Excused from Salah Today");', 'setText(isBn ? "আজকের নামাজ মাফ" : "Excused from Salah Today"); setTypeface(null, android.graphics.Typeface.ITALIC);')
            
            # ফিক্স ৪৬: ডার্ক মোডের ব্যাকগ্রাউন্ড কালার (`#0A0A0C`) থেকে একদম মিশকালো ভাব কমিয়ে একটি মডার্ন ডার্ক-গ্রে (`#121212`) ভাইব দেওয়া
            new_content = new_content.replace('Color.parseColor("#0A0A0C")', 'Color.parseColor("#121212")')
            
            # ফিক্স ৪৭: 'QAZA' বা 'STREAK' ব্যাজগুলোর ব্যাকগ্রাউন্ড কালারে কিছুটা ট্রান্সপারেন্সি (স্বচ্ছতা) আনা
            new_content = new_content.replace('Color.parseColor("#33FF5252")', 'Color.parseColor("#26EF4444")')
            new_content = new_content.replace('Color.parseColor("#3322C55E")', 'Color.parseColor("#2610B981")')
            
            # ফিক্স ৪৮: ডায়ালগের ভেতরে স্ক্রল ভিউগুলোতে ওভার-স্ক্রল ল্যাগ বন্ধ করা (সব স্ক্রলভিউয়ের জন্য কনফার্ম করা)
            new_content = re.sub(r'(ScrollView\s+(\w+)\s*=\s*new\s+ScrollView\([^)]+\);)', r'\1 \2.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);', new_content)
            
            # ফিক্স ৪৯-৫০: চেক বক্সের ভেতরের টিক চিহ্নটিকে (✓) পজিশনিংয়ের জন্য সামান্য প্যাডিং অ্যাডজাস্ট করা
            new_content = new_content.replace('setPadding((int)(4*DENSITY)', 'setPadding((int)(2*DENSITY)')

            # ২. পরিবর্তন হলে ফাইলে সেভ করা হবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 9 & 10 (Final Design 41-50) applied safely! Ready for final build!")
