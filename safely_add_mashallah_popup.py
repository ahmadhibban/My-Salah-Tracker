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

        # ১. পপ-আপ উইন্ডো মেথডটি ক্লাসের একদম শেষে (নিরাপদে) যুক্ত করা হচ্ছে
        if "private void showMashallahPopup" not in content:
            popup_code = """
    private void showMashallahPopup(String dK) {
        android.content.SharedPreferences sp = getSharedPreferences("salah_pro_final", 0);
        // আজকে একবার দেখানো হলে আর বারবার দেখিয়ে বিরক্ত করবে না
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
            // পপ-আপ আসলে হালকা ভাইব্রেশন হবে
            try { ((android.os.Vibrator) getSystemService(VIBRATOR_SERVICE)).vibrate(100); } catch(Exception e){}
        }
    }
"""
            last_brace = content.rfind('}')
            content = content[:last_brace] + popup_code + "\n}"

        # ২. পপ-আপ ট্রিগারটি অত্যন্ত সাবধানে শুধু স্ট্যাটাস আপডেট হওয়ার জায়গায় বসানো হচ্ছে
        # এটি অন্য কোনো কোড পরিবর্তন করবে না
        if 'showMashallahPopup(selectedDate[0])' not in content:
            # সাবধানে রিজেক্স ব্যবহার করে যেখানে countCompleted বা nC ব্যবহার হয়েছে, সেখানে বসানো হচ্ছে
            content = re.sub(
                r'(subBtm\.setText\(statusMsgs\[([^\]]+)\]\);)', 
                r'\1\n                if (\2 == 6) { showMashallahPopup(selectedDate[0]); }', 
                content
            )

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ পারফেক্ট! 'মাশাআল্লাহ' পপ-আপ নিরাপদে যুক্ত করা হয়েছে। অন্য কোনো লেআউট বা ডিজাইনে বিন্দুমাত্র হাত দেওয়া হয়নি।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
