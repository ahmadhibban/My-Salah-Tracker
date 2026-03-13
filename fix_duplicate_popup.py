import os

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

        # ১. যতগুলো ডুপ্লিকেট showMashallahPopup আছে, সব খুঁজে বের করে মুছে ফেলা হচ্ছে
        while True:
            idx = content.find("private void showMashallahPopup")
            if idx == -1:
                break
            start_brace = content.find('{', idx)
            if start_brace == -1:
                break
            
            brace_count = 1
            end_brace = start_brace + 1
            while brace_count > 0 and end_brace < len(content):
                if content[end_brace] == '{':
                    brace_count += 1
                elif content[end_brace] == '}':
                    brace_count -= 1
                end_brace += 1
            
            # মেথডটি মুছে ফেলা হলো
            content = content[:idx] + content[end_brace:]

        # ২. একদম ফ্রেশ এবং অরিজিনাল ডিজাইনের পপ-আপটি একবার যুক্ত করা হচ্ছে
        perfect_popup = """
    private void showMashallahPopup(String dK) {
        android.content.SharedPreferences sp = getSharedPreferences("salah_pro_final", 0);
        // ওই নির্দিষ্ট দিনের জন্য আগে একবার দেখানো হয়েছে কিনা চেক করা
        if(sp.getBoolean(dK + "_original_popup", false)) return;
        sp.edit().putBoolean(dK + "_original_popup", true).apply();
        
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        String msg = isBn ? "মাশাআল্লাহ! সব সম্পন্ন হয়েছে" : "Ma sha Allah! All completed";
        
        final android.app.Dialog dialog = new android.app.Dialog(this);
        dialog.requestWindowFeature(android.view.Window.FEATURE_NO_TITLE);
        
        android.widget.TextView tv = new android.widget.TextView(this);
        tv.setText(msg);
        tv.setTextSize(18);
        tv.setTextColor(themeColors[2]); 
        tv.setGravity(android.view.Gravity.CENTER);
        tv.setPadding((int)(25*DENSITY), (int)(15*DENSITY), (int)(25*DENSITY), (int)(15*DENSITY));
        tv.setTypeface(null, android.graphics.Typeface.BOLD);
        
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(themeColors[1]); 
        gd.setCornerRadius(30f * DENSITY); 
        gd.setStroke((int)(2*DENSITY), colorAccent); 
        
        android.widget.LinearLayout ll = new android.widget.LinearLayout(this);
        ll.setBackground(gd);
        ll.addView(tv);
        
        dialog.setContentView(ll);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
            dialog.getWindow().clearFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND); 
        }
        
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
        last_brace = content.rfind('}')
        content = content[:last_brace] + perfect_popup + "\n}"

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ ডুপ্লিকেট 'মাশাআল্লাহ' পপ-আপ এরর ফিক্স করা হয়েছে!")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
