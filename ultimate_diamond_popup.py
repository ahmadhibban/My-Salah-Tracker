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

        # ১. আগের সব ফালতু/ডুপ্লিকেট showMashallahPopup নিখুঁতভাবে মুছে ফেলা হচ্ছে
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

        # ২. ১০০% পারফেক্ট এবং গ্লোয়িং ডায়মন্ড ইফেক্টসহ প্রিমিয়াম পপ-আপ
        premium_popup = """
    private void showMashallahPopup(String dK) {
        android.content.SharedPreferences sp = getSharedPreferences("salah_pro_final", 0);
        if(sp.getBoolean(dK + "_ultra_premium_popup", false)) return;
        sp.edit().putBoolean(dK + "_ultra_premium_popup", true).apply();
        
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        
        final android.app.Dialog dialog = new android.app.Dialog(this);
        dialog.requestWindowFeature(android.view.Window.FEATURE_NO_TITLE);
        
        android.widget.LinearLayout root = new android.widget.LinearLayout(this);
        root.setOrientation(android.widget.LinearLayout.VERTICAL);
        root.setGravity(android.view.Gravity.CENTER);
        root.setPadding((int)(30*DENSITY), (int)(40*DENSITY), (int)(30*DENSITY), (int)(40*DENSITY));
        
        android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
        gd.setColor(themeColors[1]);
        gd.setCornerRadius(40f * DENSITY); 
        gd.setStroke((int)(3*DENSITY), colorAccent); 
        root.setBackground(gd);
        
        // --- 1. Glowing Diamond Effect ---
        android.widget.FrameLayout iconFrame = new android.widget.FrameLayout(this);
        
        android.view.View glow = new android.view.View(this);
        android.graphics.drawable.GradientDrawable glowBg = new android.graphics.drawable.GradientDrawable();
        glowBg.setGradientType(android.graphics.drawable.GradientDrawable.RADIAL_GRADIENT);
        glowBg.setGradientRadius(150f * DENSITY);
        glowBg.setColors(new int[]{android.graphics.Color.argb(120, android.graphics.Color.red(colorAccent), android.graphics.Color.green(colorAccent), android.graphics.Color.blue(colorAccent)), android.graphics.Color.TRANSPARENT});
        glow.setBackground(glowBg);
        android.widget.FrameLayout.LayoutParams glowLp = new android.widget.FrameLayout.LayoutParams((int)(140*DENSITY), (int)(140*DENSITY));
        glowLp.gravity = android.view.Gravity.CENTER;
        iconFrame.addView(glow, glowLp);
        
        android.widget.TextView diamond = new android.widget.TextView(this);
        diamond.setText("💎");
        diamond.setTextSize(65);
        diamond.setGravity(android.view.Gravity.CENTER);
        diamond.setShadowLayer(20f, 0f, 0f, colorAccent);
        android.widget.FrameLayout.LayoutParams diaLp = new android.widget.FrameLayout.LayoutParams(-2, -2);
        diaLp.gravity = android.view.Gravity.CENTER;
        iconFrame.addView(diamond, diaLp);
        
        root.addView(iconFrame, new android.widget.LinearLayout.LayoutParams(-1, -2));
        
        // --- 2. Main Title ---
        android.widget.TextView title = new android.widget.TextView(this);
        title.setText(isBn ? "মাশাআল্লাহ!" : "Ma sha Allah!");
        title.setTextSize(32);
        title.setTextColor(colorAccent);
        title.setTypeface(null, android.graphics.Typeface.BOLD);
        title.setGravity(android.view.Gravity.CENTER);
        title.setShadowLayer(4f, 0f, 2f, android.graphics.Color.argb(100,0,0,0));
        android.widget.LinearLayout.LayoutParams titleLp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        titleLp.setMargins(0, (int)(10*DENSITY), 0, 0);
        root.addView(title, titleLp);
        
        // --- 3. Subtitle / Message ---
        android.widget.TextView msg1 = new android.widget.TextView(this);
        msg1.setText(isBn ? "আলহামদুলিল্লাহ, আজকের সবগুলো নামাজ আপনি আদায় করেছেন।" : "Alhamdulillah, you have offered all your prayers today.");
        msg1.setTextSize(16);
        msg1.setTextColor(themeColors[2]);
        msg1.setGravity(android.view.Gravity.CENTER);
        android.widget.LinearLayout.LayoutParams msg1Lp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        msg1Lp.setMargins(0, (int)(10*DENSITY), 0, 0);
        root.addView(msg1, msg1Lp);
        
        // --- 4. Streak / Motivation ---
        android.widget.TextView msg2 = new android.widget.TextView(this);
        msg2.setText(isBn ? "✨ দারুণ! এভাবেই স্ট্রিক বজায় রাখুন ✨" : "✨ Awesome! Keep up the daily streak ✨");
        msg2.setTextSize(14);
        msg2.setTextColor(colorAccent);
        msg2.setTypeface(null, android.graphics.Typeface.BOLD);
        msg2.setGravity(android.view.Gravity.CENTER);
        android.widget.LinearLayout.LayoutParams msg2Lp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        msg2Lp.setMargins(0, (int)(15*DENSITY), 0, 0);
        root.addView(msg2, msg2Lp);
        
        dialog.setContentView(root);
        if (dialog.getWindow() != null) {
            dialog.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(android.graphics.Color.TRANSPARENT));
            // ব্যাকগ্রাউন্ড কোনোভাবেই অন্ধকার (Dim) করবে না
            dialog.getWindow().clearFlags(android.view.WindowManager.LayoutParams.FLAG_DIM_BEHIND); 
        }
        
        if(!isFinishing()) {
            dialog.show();
            try { ((android.os.Vibrator) getSystemService(VIBRATOR_SERVICE)).vibrate(100); } catch(Exception e){}
            
            // সুন্দর বাউন্স অ্যানিমেশন দিয়ে স্ক্রিনে আসবে
            root.setScaleX(0.5f); root.setScaleY(0.5f); root.setAlpha(0f);
            root.animate().scaleX(1f).scaleY(1f).alpha(1f).setDuration(500).setInterpolator(new android.view.animation.OvershootInterpolator()).start();
            
            // ঠিক ১.৫ সেকেন্ড পর নিজে নিজেই অ্যানিমেশন হয়ে চলে যাবে
            new android.os.Handler().postDelayed(new Runnable() {
                @Override
                public void run() { 
                    if(dialog.isShowing()) {
                        root.animate().scaleX(0.8f).scaleY(0.8f).alpha(0f).setDuration(300).withEndAction(new Runnable() {
                            @Override
                            public void run() { dialog.dismiss(); }
                        }).start();
                    }
                }
            }, 1500); 
        }
    }
"""
        last_brace = content.rfind('}')
        content = content[:last_brace] + premium_popup + "\n}"

        # ৩. ট্রিগার যুক্ত করা (সাবধানে)
        if 'showMashallahPopup(selectedDate[0])' not in content:
            content = re.sub(
                r'(subBtm\.setText\(statusMsgs\[([^\]]+)\]\);)', 
                r'\1\n                if (\2 == 6) { try { showMashallahPopup(selectedDate[0]); } catch(Exception e){} }', 
                content
            )

        with open(target_main, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ চ্যালেঞ্জ সম্পন্ন! আল্ট্রা-প্রিমিয়াম গ্লোয়িং ডায়মন্ড পপ-আপ ফিক্স করা হয়েছে।")
    else:
        print("❌ MainActivity.java পাওয়া যায়নি।")

if __name__ == '__main__': main()
