import os
import re

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

        # আগের যেকোনো গ্রেডিয়েন্ট বা ব্যাকগ্রাউন্ড কোড ক্লিন করে নতুনটা বসানো
        start_marker = "PremiumTasbihView tasbihView"
        end_marker = "contentArea.addView(pNeo);"
        
        if start_marker in content and end_marker in content:
            # Finding the block where we add pCard to pNeo
            search_str = "pCard.addView(left);"
            
            if search_str in content:
                beautiful_gradient_code = """
        // --- মাস্টারপিস ডিপ গ্রেডিয়েন্ট ব্যাকগ্রাউন্ড ---
        android.graphics.drawable.GradientDrawable beautifulBg = new android.graphics.drawable.GradientDrawable();
        
        if (!isDarkTheme) {
            // লাইট থিমের জন্য অ্যাকসেন্ট কালারের গাঢ় এবং প্রিমিয়াম ভার্সন
            int r = android.graphics.Color.red(colorAccent);
            int g = android.graphics.Color.green(colorAccent);
            int b = android.graphics.Color.blue(colorAccent);
            
            int color1 = android.graphics.Color.rgb((int)(r * 0.4), (int)(g * 0.4), (int)(b * 0.4)); // ডিপ
            int color2 = android.graphics.Color.rgb((int)(r * 0.2), (int)(g * 0.2), (int)(b * 0.2)); // আরও ডিপ
            
            beautifulBg = new android.graphics.drawable.GradientDrawable(
                android.graphics.drawable.GradientDrawable.Orientation.TL_BR, 
                new int[]{color1, color2}
            );
        } else {
            // ডার্ক থিমের জন্য পিওর স্লিক ডার্ক
            beautifulBg.setColor(android.graphics.Color.parseColor("#151515"));
        }
        
        beautifulBg.setCornerRadius(40f); // এআই ইমেজের মতো সুন্দর রাউন্ডেড
        beautifulBg.setStroke(2, android.graphics.Color.argb(30, 255, 255, 255)); // হালকা গ্লাস বর্ডার
        pCard.setBackground(beautifulBg);
        
        // যেহেতু ব্যাকগ্রাউন্ড ডিপ, তাই পার্সেন্টেজের সব টেক্সট সাদা করে দেওয়া হচ্ছে
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
        
        pCard.addView(left);"""
                
                # Replace the simple addView with the styled one
                # We need to make sure we don't duplicate it if run twice
                if "মাস্টারপিস ডিপ গ্রেডিয়েন্ট" not in content:
                    content = content.replace("pCard.addView(left);", beautiful_gradient_code, 1)
                    
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print("✅ সফল! কার্ডে প্রিমিয়াম ডার্ক গ্রেডিয়েন্ট এবং টেক্সট ফিক্স করা হয়েছে।")
            else:
                print("⚠️ কোড ব্লক পাওয়া যায়নি।")
        else:
            print("❌ ফাইল পাওয়া যায়নি বা কোড ম্যাচ করেনি।")

if __name__ == '__main__': main()
