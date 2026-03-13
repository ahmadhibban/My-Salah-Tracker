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

        # আগের ভুল পপ-আপ মেথড যদি থাকে, সেটাকে পুরোপুরি মুছে ফেলা হচ্ছে
        content = re.sub(r'private void showMashallahPopup\(String dK\)\s*\{.*?\try \{ \(\(android\.os\.Vibrator\).*?catch\(Exception e\)\{\}\s*\}\s*\}', '', content, flags=re.DOTALL)
        
        # আপনার বর্ণনা অনুযায়ী একদম অরিজিনাল ডিজাইনের পপ-আপ কোড
        perfect_popup = """
    private void showMashallahPopup(String dK) {
        android.content.SharedPreferences sp = getSharedPreferences("salah_pro_final", 0);
        // ওই নির্দিষ্ট দিনের (যেকোনো তারিখের) জন্য আগে একবার দেখানো হয়েছে কিনা চেক করা
        if(sp.getBoolean(dK + "_original_popup", false)) return;
        sp.edit().putBoolean(dK + "_original_popup", true).apply();
        
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        String msg = isBn ? "মাশাআল্লাহ! সব সম্পন্ন হয়েছে" : "Ma sha Allah! All completed";
        
        final android.app.Dialog dialog = new android.app.Dialog(this);
        dialog.requestWindowFeature(android.view.Window.FEATURE_NO_TITLE);
        
        android.widget.TextView tv = new android.widget.TextView(this);
        tv.setText(msg);
        tv.setTextSize(18);
        tv.setTextColor(themeColors[2]); // থিম অনুযায়ী টেক্সট কালার
        tv.setGravity(android.view.Gravity.CENTER);
        tv.setPadding((int)(25*DENSITY), (int)(15*DENSITY), (int)(25*DENSITY), (int)(15*DENSITY));
        tv.setTypeface(null, android.graphics.Typeface.BOLD);
        
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(themeColors[1]); // থিম অনুযায়ী ব্যাকগ্রাউন্ড
        gd.setCornerRadius(30f * DENSITY); // সুন্দর গোল করা বর্ডার
        gd.setStroke((int)(2*DENSITY), colorAccent); // অ্যাপের কালার অনুযায়ী বর্ডার
        
        android.widget.LinearLayout ll = new android.widget.LinearLayout(this);
        ll.setBackground(gd);
        ll.addView(tv);
        
        dialog.setContentView(ll);
        dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
        dialog.getWindow().clearFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND); // পেছনের স্ক্রিন অন্ধকার করবে না
        
        if(!isFinishing()) {
            dialog.show();
            // অটোমেটিক ১.৫ সেকেন্ড পর চলে যাবে
            new android.os.Handler().postDelayed(new Runnable() {
                @Override
                public void run() {
                    if(dialog.isShowing()) {
                        dialog.dismiss();
                    }
                }
            }, 1500);
        }
    }
"""
        # মেথডটি ক্লাসের শেষে যুক্ত করা হচ্ছে
        last_brace = content.rfind('}')
        content = content[:last_brace] + perfect_popup + "\n}"

        # ট্রিগার যুক্ত করা (যদি আগে না থাকে)
        if 'showMashallahPopup(selectedDate[0])' not in content:
            content = re.sub(
                r'(subBtm\.setText\(statusMsgs\[([^\]]+)\]\);)', 
                r'\1\n                if (\2 == 6) { showMashallahPopup(selectedDate[0]); }', 
                content
            )

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ পারফেক্ট! অরিজিনাল 'মাশাআল্লাহ' ডিজাইনের অটো-ক্লোজিং পপ-আপ সফলভাবে রিস্টোর করা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
