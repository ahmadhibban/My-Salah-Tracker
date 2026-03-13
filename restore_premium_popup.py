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

        # ১. আগের সব ফালতু/ডুপ্লিকেট showMashallahPopup মুছে ফেলা হচ্ছে
        while True:
            idx = content.find("private void showMashallahPopup")
            if idx == -1: break
            start_brace = content.find('{', idx)
            if start_brace == -1: break
            
            brace_count = 1
            end_brace = start_brace + 1
            while brace_count > 0 and end_brace < len(content):
                if content[end_brace] == '{': brace_count += 1
                elif content[end_brace] == '}': brace_count -= 1
                end_brace += 1
            content = content[:idx] + content[end_brace:]

        # ২. একদম হুবহু আপনার ছবির মতো প্রিমিয়াম পপ-আপ তৈরি করা হচ্ছে
        premium_popup = """
    private void showMashallahPopup(String dK) {
        android.content.SharedPreferences sp = getSharedPreferences("salah_pro_final", 0);
        if(sp.getBoolean(dK + "_premium_popup", false)) return;
        sp.edit().putBoolean(dK + "_premium_popup", true).apply();
        
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        
        final android.app.Dialog dialog = new android.app.Dialog(this);
        dialog.requestWindowFeature(android.view.Window.FEATURE_NO_TITLE);
        
        android.widget.LinearLayout root = new android.widget.LinearLayout(this);
        root.setOrientation(android.widget.LinearLayout.VERTICAL);
        root.setGravity(android.view.Gravity.CENTER);
        root.setPadding((int)(30*DENSITY), (int)(40*DENSITY), (int)(30*DENSITY), (int)(40*DENSITY));
        
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(themeColors[1]); // ডার্ক/লাইট মোড ব্যাকগ্রাউন্ড
        gd.setCornerRadius(30f * DENSITY); 
        gd.setStroke((int)(2*DENSITY), colorAccent); // অ্যাপের কালার অনুযায়ী বর্ডার
        root.setBackground(gd);
        
        // ১. ডায়মন্ড আইকন (গ্লোয়িং ইফেক্ট সহ)
        android.widget.TextView icon = new android.widget.TextView(this);
        icon.setText("💎");
        icon.setTextSize(50);
        icon.setGravity(android.view.Gravity.CENTER);
        icon.setShadowLayer(30f, 0f, 0f, colorAccent); // আইকনের চারপাশে সুন্দর গ্লো
        root.addView(icon, new android.widget.LinearLayout.LayoutParams(-2, -2));
        
        // ২. বড় টাইটেল (মাশাআল্লাহ!)
        android.widget.TextView title = new android.widget.TextView(this);
        title.setText(isBn ? "মাশাআল্লাহ!" : "Ma sha Allah!");
        title.setTextSize(26);
        title.setTextColor(colorAccent);
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        title.setGravity(android.view.Gravity.CENTER);
        android.widget.LinearLayout.LayoutParams titleLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        titleLp.setMargins(0, (int)(15*DENSITY), 0, 0);
        root.addView(title, titleLp);
        
        // ৩. সাবটাইটেল (আজকের সবগুলো নামাজ...)
        android.widget.TextView msg = new android.widget.TextView(this);
        msg.setText(isBn ? "আজকের সবগুলো নামাজ আপনি আদায় করেছেন।" : "You have offered all your prayers today.");
        msg.setTextSize(15);
        msg.setTextColor(themeColors[2]);
        msg.setGravity(android.view.Gravity.CENTER);
        android.widget.LinearLayout.LayoutParams msgLp = new android.widget.LinearLayout.LayoutParams(-2, -2);
        msgLp.setMargins(0, (int)(10*DENSITY), 0, 0);
        root.addView(msg, msgLp);
        
        dialog.setContentView(root);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
            dialog.getWindow().clearFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND); 
        }
        
        if(!isFinishing()) {
            dialog.show();
            try { ((android.os.Vibrator) getSystemService(VIBRATOR_SERVICE)).vibrate(100); } catch(Exception e){}
            
            // ঠিক ১.২ সেকেন্ড পর নিজে নিজে চলে যাবে
            new android.os.Handler().postDelayed(new Runnable() {
                @Override
                public void run() { if(dialog.isShowing()) dialog.dismiss(); }
            }, 1200); 
        }
    }
"""
        last_brace = content.rfind('}')
        content = content[:last_brace] + premium_popup + "\n}"

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ আপনার অরিজিনাল ডায়মন্ড ডিজাইনের প্রিমিয়াম পপ-আপটি নিখুঁতভাবে রিস্টোর করা হয়েছে!")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
