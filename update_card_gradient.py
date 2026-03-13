import os

def main():
    target_dir = None
    for root, dirs, files in os.walk('.'):
        if 'Android/data' in root or '.git' in root: continue
        if 'MainActivity.java' in files: target_dir = root; break
    if not target_dir:
        for root, dirs, files in os.walk('/storage/emulated/0/'):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: target_dir = root; break

    if target_dir:
        file_path = os.path.join(target_dir, 'MainActivity.java')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        target_code = "pCard.addView(left);"
        if target_code in content and "pCardBg" not in content:
            gradient_code = """
        // --- নতুন: লাইট থিমে গাঢ় গ্রেডিয়েন্ট ---
        android.graphics.drawable.GradientDrawable pCardBg = new android.graphics.drawable.GradientDrawable();
        if (!isDarkTheme) {
            int a = android.graphics.Color.alpha(colorAccent);
            int r1 = Math.max(0, (int)(android.graphics.Color.red(colorAccent) * 0.8f));
            int g1 = Math.max(0, (int)(android.graphics.Color.green(colorAccent) * 0.8f));
            int b1 = Math.max(0, (int)(android.graphics.Color.blue(colorAccent) * 0.8f));
            
            int r2 = Math.max(0, (int)(android.graphics.Color.red(colorAccent) * 0.4f));
            int g2 = Math.max(0, (int)(android.graphics.Color.green(colorAccent) * 0.4f));
            int b2 = Math.max(0, (int)(android.graphics.Color.blue(colorAccent) * 0.4f));
            
            pCardBg = new android.graphics.drawable.GradientDrawable(
                android.graphics.drawable.GradientDrawable.Orientation.TL_BR, 
                new int[]{android.graphics.Color.argb(a, r1, g1, b1), android.graphics.Color.argb(a, r2, g2, b2)}
            );
        } else {
            pCardBg.setColor(android.graphics.Color.parseColor("#1A1A1A")); // ডার্ক থিম
        }
        pCardBg.setCornerRadius(30f); // এআই ডিজাইনের মত রাউন্ডেড
        pCard.setBackground(pCardBg);
        
        // ভেতরের টেক্সট সাদা করার জন্য (যেহেতু লাইট থিমেও কার্ড গাঢ়)
        try {
            for(int i=0; i<left.getChildCount(); i++) {
                android.view.View v = left.getChildAt(i);
                if(v instanceof android.widget.TextView) {
                    ((android.widget.TextView)v).setTextColor(android.graphics.Color.WHITE);
                }
            }
        } catch (Exception e){}
        
        pCard.addView(left);"""
            
            content = content.replace(target_code, gradient_code)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ চমৎকার! পার্সেন্টেজ কার্ডে গাঢ় গ্রেডিয়েন্ট এবং টেক্সট কালার ফিক্স করা হয়েছে।")
        else:
            print("⚠️ হয়তো আগেই পরিবর্তন করা হয়েছে অথবা pCard.addView(left) পাওয়া যায়নি।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
