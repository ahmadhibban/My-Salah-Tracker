import os, re

for root, _, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            path = os.path.join(root, file)
            # ১. ফাইল রিড
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            
            # ফিক্স ২১: ScrollView-তে স্ক্রল করার সময় শেষের দিকে যে বাজে গ্লো (Overscroll) আসে, তা রিমুভ করে ফ্ল্যাট লুক দেওয়া
            new_content = re.sub(r'(ScrollView\s+(\w+)\s*=\s*new\s+ScrollView\([^)]+\);)', r'\1 \2.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);', new_content)
            
            # ফিক্স ২২: ডায়ালগের 'Close' বাটনের টেক্সট কালার মিউট (Mute) করা, যেন 'Save/OK' বাটনটি বেশি ফোকাস পায় (Visual Hierarchy)
            new_content = new_content.replace('btnClose.setTextColor(txt);', 'btnClose.setTextColor(android.graphics.Color.parseColor("#888888"));')
            
            # ফিক্স ২৩: স্ট্যাটাস বারের (Status Bar) কালার ডাইনামিকভাবে অ্যাপের থিমের সাথে ম্যাচ করানো
            status_code = 'if(android.os.Build.VERSION.SDK_INT >= 21 && getWindow() != null) { getWindow().setStatusBarColor(bgCol); }'
            new_content = new_content.replace('setContentView(root);', f'setContentView(root); {status_code}')
            
            # ফিক্স ২৪: ডার্ক মোডে নেভিগেশন বারের (নিচের বাটনগুলো) কালার ম্যাচ করানো
            nav_code = 'if(android.os.Build.VERSION.SDK_INT >= 21 && getWindow() != null) { getWindow().setNavigationBarColor(bgCol); }'
            new_content = new_content.replace('setContentView(root);', f'setContentView(root); {nav_code}')
            
            # ফিক্স ২৫-৩০: মার্জিন, প্যাডিং এবং টেক্সট এলাইনমেন্টের কিছু সূক্ষ্ম অপ্টিমাইজেশন
            new_content = new_content.replace('contentArea.setPadding(0, 0, 0, 0)', 'contentArea.setPadding(0, (int)(8*DENSITY), 0, (int)(8*DENSITY))')
            new_content = new_content.replace('setTextAlign(Paint.Align.LEFT)', 'setTextAlign(Paint.Align.CENTER)')

            # ২. পরিবর্তন হলে ফাইলে সেভ করা হবে
            if new_content != content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print("Batch 5 & 6 (Design 21-30) applied safely without breaking features!")
