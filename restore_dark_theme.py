import os
import re

def main():
    target_dir = None
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for root_path in search_paths:
        if not os.path.exists(root_path): continue
        for root, dirs, files in os.walk(root_path):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: 
                target_dir = root
                break
        if target_dir: break

    if target_dir:
        file_path = os.path.join(target_dir, 'MainActivity.java')
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # আমার আগের করা ডার্ক থিমের সব ভুল কোড খুঁজে বের করে ডিলিট করা হচ্ছে
        pattern = r'// --- পারফেক্ট কার্ড ব্যাকগ্রাউন্ড.*?pCard\.addView\(left\);'
        
        clean_code = """
        // লাইট থিমের জন্য ব্রাইট গ্রেডিয়েন্ট (ডার্ক থিমে হাত দেওয়া হয়নি, অরিজিনাল থাকবে)
        if (!isDarkTheme) {
            int r = android.graphics.Color.red(colorAccent);
            int g = android.graphics.Color.green(colorAccent);
            int b = android.graphics.Color.blue(colorAccent);
            
            int color1 = android.graphics.Color.rgb((int)(r * 0.9), (int)(g * 0.9), (int)(b * 0.9)); 
            int color2 = android.graphics.Color.rgb((int)(r * 0.75), (int)(g * 0.75), (int)(b * 0.75)); 
            
            android.graphics.drawable.GradientDrawable niceBg = new android.graphics.drawable.GradientDrawable(
                android.graphics.drawable.GradientDrawable.Orientation.TL_BR, 
                new int[]{color1, color2}
            );
            niceBg.setCornerRadius(30f); 
            pCard.setBackground(niceBg);
            
            try {
                for(int i=0; i<left.getChildCount(); i++) {
                    android.view.View v = left.getChildAt(i);
                    if(v instanceof android.widget.TextView) {
                        ((android.widget.TextView)v).setTextColor(android.graphics.Color.WHITE);
                    } else if (v instanceof android.widget.LinearLayout) {
                        android.widget.LinearLayout ll = (android.widget.LinearLayout) v;
                        for(int j=0; j<ll.getChildCount(); j++) {
                            android.view.View innerV = ll.getChildAt(j);
                            if(innerV instanceof android.widget.TextView) {
                                ((android.widget.TextView)innerV).setTextColor(android.graphics.Color.WHITE);
                            }
                        }
                    }
                }
            } catch (Exception e){}
        }
        // ডার্ক থিমের কোনো কোড নেই, তাই আপনার আগের অরিজিনাল ডিজাইনটাই শো করবে!
        pCard.addView(left);"""

        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, clean_code.strip(), content, flags=re.DOTALL)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✅ ডার্ক থিমের কালো ব্যাকগ্রাউন্ড রিমুভ করা হয়েছে! আপনার অরিজিনাল ডিজাইন রিস্টোর হয়েছে।")
        else:
            print("⚠️ আগের কোড ব্লকটি পাওয়া যায়নি।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
