import os

java_code = """package com.my.salah.tracker.app;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.LayerDrawable;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.content.SharedPreferences;
import android.os.Vibrator;

public class PremiumTasbihView extends LinearLayout {
    private int count = 0;
    private TextView display;
    private View tapButton;
    private SharedPreferences prefs;

    public PremiumTasbihView(Context context, boolean isDark, int accentColor) {
        super(context);
        setOrientation(LinearLayout.VERTICAL);
        setGravity(Gravity.CENTER);
        setPadding(5, 5, 5, 5);
        
        prefs = context.getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE);
        count = prefs.getInt("premium_tasbih_count", 0);

        // 1. Digital Display Box (Inset/Engraved Look)
        display = new TextView(context);
        updateDisplay();
        display.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        display.setTextSize(16f);
        display.setTextColor(isDark ? Color.parseColor("#E0E0E0") : Color.parseColor("#333333"));
        display.setGravity(Gravity.CENTER);
        display.setPadding(25, 12, 25, 12);
        
        GradientDrawable insetBg = new GradientDrawable();
        insetBg.setColor(isDark ? Color.parseColor("#121212") : Color.parseColor("#D6D6D6"));
        insetBg.setCornerRadius(12f);
        // Inner shadow illusion
        insetBg.setStroke(3, isDark ? Color.parseColor("#000000") : Color.parseColor("#BDBDBD"));
        display.setBackground(insetBg);
        
        addView(display);

        // Spacer
        View space = new View(context);
        space.setLayoutParams(new LinearLayout.LayoutParams(1, 20));
        addView(space);

        // 2. 3D Tap Button (Neumorphic)
        tapButton = new View(context);
        int btnSize = 90;
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(btnSize, btnSize);
        tapButton.setLayoutParams(btnParams);
        
        GradientDrawable btnBg = new GradientDrawable();
        btnBg.setShape(GradientDrawable.OVAL);
        btnBg.setColor(accentColor);
        
        // Shadow for 3D depth
        GradientDrawable shadow = new GradientDrawable();
        shadow.setShape(GradientDrawable.OVAL);
        shadow.setColor(Color.argb(70, 0, 0, 0));
        
        LayerDrawable layerDrawable = new LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, btnBg});
        // Adjusting inset to avoid one side looking excessively high
        layerDrawable.setLayerInset(1, 0, 0, 4, 4); 
        
        tapButton.setBackground(layerDrawable);
        
        tapButton.setOnTouchListener((v, event) -> {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                // Realistic push down animation
                tapButton.animate().translationY(3f).translationX(3f).setDuration(50).start();
                layerDrawable.setLayerInset(1, 2, 2, 2, 2); 
                return true;
            } else if (event.getAction() == MotionEvent.ACTION_UP || event.getAction() == MotionEvent.ACTION_CANCEL) {
                // Button release animation
                tapButton.animate().translationY(0f).translationX(0f).setDuration(50).start();
                layerDrawable.setLayerInset(1, 0, 0, 4, 4); 
                
                if (event.getAction() == MotionEvent.ACTION_UP) {
                    incrementCount();
                    vibrate(context, 30);
                }
                return true;
            }
            return false;
        });
        
        // Long press to reset
        tapButton.setOnLongClickListener(v -> {
            count = 0;
            updateDisplay();
            saveCount();
            vibrate(context, 80);
            return true;
        });

        addView(tapButton);
    }

    private void incrementCount() {
        count++;
        if(count > 999) count = 0;
        updateDisplay();
        saveCount();
    }

    private void updateDisplay() {
        display.setText(String.format("%03d", count));
    }

    private void saveCount() {
        prefs.edit().putInt("premium_tasbih_count", count).apply();
    }
    
    private void vibrate(Context ctx, int duration) {
        try {
            Vibrator v = (Vibrator) ctx.getSystemService(Context.VIBRATOR_SERVICE);
            if (v != null) v.vibrate(duration);
        } catch (Exception e){}
    }
}
"""

def main():
    print("🔍 ফাইলের অবস্থান খোঁজা হচ্ছে...")
    target_dir = None
    search_roots = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for root in search_roots:
        if not os.path.exists(root): continue
        for dirpath, dirnames, filenames in os.walk(root):
            # স্কিপ করা ফোল্ডার যাতে স্পিড বেশি পাওয়া যায়
            if 'Android/data' in dirpath or '.git' in dirpath: continue
            if 'AppConstants.java' in filenames:
                target_dir = dirpath
                break
        if target_dir: break
        
    if target_dir:
        file_path = os.path.join(target_dir, 'PremiumTasbihView.java')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(java_code)
        print(f"✅ সফল হয়েছে! নতুন ফাইল তৈরি হয়েছে এখানে: {file_path}")
    else:
        print("❌ এরর: প্রোজেক্ট ফোল্ডার স্বয়ংক্রিয়ভাবে খুঁজে পাওয়া যায়নি।")

if __name__ == '__main__':
    main()
