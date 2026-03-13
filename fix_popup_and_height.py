import os
import re

def main():
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    target_main = None
    
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: 
                target_main = os.path.join(root, 'MainActivity.java')
                break
        if target_main: break

    if target_main:
        with open(target_main, 'r', encoding='utf-8') as f:
            content = f.read()

        # ==========================================
        # ১. পাশাপাশি থাকা কার্ডগুলোর উচ্চতা সমান (Equal Height) করা
        # ==========================================
        # লেআউট প্যারামিটার 0, -2 (WRAP_CONTENT) থেকে 0, -1 (MATCH_PARENT) করা হচ্ছে
        content = re.sub(r'new\s+LinearLayout\.LayoutParams\(\s*0\s*,\s*(?:-2|ViewGroup\.LayoutParams\.WRAP_CONTENT|LinearLayout\.LayoutParams\.WRAP_CONTENT|android\.view\.ViewGroup\.LayoutParams\.WRAP_CONTENT)\s*,\s*([0-9.]+f)\s*\)', r'new LinearLayout.LayoutParams(0, -1, \1)', content)

        # ==========================================
        # ২. "মাশাআল্লাহ" পপ-আপ ডায়ালগ তৈরি ও ট্রিগার করা
        # ==========================================
        # পপ-আপ মেথডটি ক্লাসের ভেতরে যুক্ত করা হচ্ছে
        if "private void showMashallahPopup" not in content:
            popup_code = """
    private void showMashallahPopup(String dK) {
        android.content.SharedPreferences sp = getSharedPreferences("salah_pro_final", 0);
        // আজকে একবার দেখানো হলে আর দেখাবে না
        if(sp.getBoolean(dK + "_mashallah_popup", false)) return;
        sp.edit().putBoolean(dK + "_mashallah_popup", true).apply();
        
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        String msg = isBn ? "মাশাআল্লাহ! আজকের সবগুলো নামাজ আপনি আদায় করেছেন।" : "Ma sha Allah! You have offered all your prayers today.";
        
        android.app.AlertDialog.Builder b = new android.app.AlertDialog.Builder(this);
        android.widget.TextView tv = new android.widget.TextView(this);
        tv.setText(msg);
        tv.setTextSize(22);
        tv.setTextColor(colorAccent);
        tv.setGravity(android.view.Gravity.CENTER);
        tv.setPadding((int)(20*DENSITY), (int)(30*DENSITY), (int)(20*DENSITY), (int)(30*DENSITY));
        tv.setTypeface(null, android.graphics.Typeface.BOLD);
        
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(20f * DENSITY);
        gd.setStroke(3, colorAccent);
        
        android.widget.LinearLayout ll = new android.widget.LinearLayout(this);
        ll.setBackground(gd);
        ll.addView(tv, new android.widget.LinearLayout.LayoutParams(-1, -2));
        
        android.app.AlertDialog d = b.setView(ll).create();
        d.getWindow().setBackgroundDrawableResource(android.R.color.transparent);
        if(!isFinishing()) {
            d.show();
            // হালকা ভাইব্রেশন দিয়ে সেলিব্রেট করা
            try { ((android.os.Vibrator) getSystemService(VIBRATOR_SERVICE)).vibrate(100); } catch(Exception e){}
        }
    }
"""
            last_brace = content.rfind('}')
            content = content[:last_brace] + popup_code + "\n}"

        # পপ-আপটি ট্রিগার করা (যখন ৬টি নামাজ সম্পন্ন হবে)
        if 'showMashallahPopup' not in content.split('private void showMashallahPopup')[0]:
            # লাইভ আপডেট মেথডে ট্রিগার যুক্ত করা
            content = re.sub(
                r'(if\s*\(\s*pT\s*!=\s*null\s*\)\s*pT\.setText[^;]+;)', 
                r'\1\n            if(nC == 6) { showMashallahPopup(dK); }', 
                content
            )
            # ডিরেক্ট ক্লিক লিসেনারে ট্রিগার যুক্ত করা (যদি থাকে)
            content = re.sub(
                r'(pT\.setText\([^\)]+\)\s*;[^\n]*\n[^\n]*subBtm\.setText[^\n]*;)', 
                r'\1\n                if(nC == 6) { showMashallahPopup(dKey); }', 
                content
            )

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ মাশাআল্লাহ পপ-আপ রিস্টোর করা হয়েছে এবং কার্ডের উচ্চতা সমান করা হয়েছে!")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
