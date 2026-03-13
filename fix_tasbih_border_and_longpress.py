import os

java_code = """package com.my.salah.tracker.app;

import android.content.Context;
import android.graphics.Color;
import android.graphics.Typeface;
import android.graphics.drawable.GradientDrawable;
import android.graphics.drawable.LayerDrawable;
import android.view.GestureDetector;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.content.SharedPreferences;
import android.os.Vibrator;
import android.util.TypedValue;

public class PremiumTasbihView extends LinearLayout {
    private int count = 0;
    private TextView display;
    private View tapButton;
    private SharedPreferences prefs;
    private int accentColor;
    private boolean isDark;
    private GestureDetector gestureDetector;

    public PremiumTasbihView(Context context, boolean isDark, int accentColor) {
        super(context);
        this.isDark = isDark;
        this.accentColor = accentColor;
        setOrientation(LinearLayout.VERTICAL);
        setGravity(Gravity.CENTER);
        
        prefs = context.getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE);
        count = prefs.getInt("premium_tasbih_count", 0);

        // --- 1. Realistic LCD Display Box ---
        display = new TextView(context);
        updateDisplay();
        display.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 17f);
        
        display.setTextColor(isDark ? Color.parseColor("#00E676") : Color.parseColor("#212121"));
        display.setGravity(Gravity.CENTER);
        display.setPadding(25, 15, 25, 15);
        
        GradientDrawable displayBg = new GradientDrawable();
        displayBg.setColor(isDark ? Color.parseColor("#121212") : Color.parseColor("#9EA792"));
        displayBg.setCornerRadius(12f);
        displayBg.setStroke(4, isDark ? Color.parseColor("#000000") : Color.parseColor("#7A8270"));
        
        display.setBackground(displayBg);
        addView(display);

        // Spacer
        View space = new View(context);
        space.setLayoutParams(new LinearLayout.LayoutParams(1, (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 18, context.getResources().getDisplayMetrics())));
        addView(space);

        // --- 2. 3D Physical Button with Distinct Border ---
        tapButton = new View(context);
        float density = context.getResources().getDisplayMetrics().density;
        int btnSize = (int) (70 * density);
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(btnSize, btnSize);
        tapButton.setLayoutParams(btnParams);
        
        LayerDrawable unpressedDrawable = createMechanicalButton(false);
        LayerDrawable pressedDrawable = createMechanicalButton(true);

        tapButton.setBackground(unpressedDrawable);
        
        // --- ফিক্স: GestureDetector দিয়ে ট্যাপ এবং লং প্রেস হ্যান্ডেল করা ---
        gestureDetector = new GestureDetector(context, new GestureDetector.SimpleOnGestureListener() {
            @Override
            public boolean onSingleTapUp(MotionEvent e) {
                incrementCount();
                vibrate(context, 35);
                return true;
            }

            @Override
            public void onLongPress(MotionEvent e) {
                count = 0;
                updateDisplay();
                saveCount();
                vibrate(context, 100); // রিসেট হলে একটু বড় ভাইব্রেশন হবে
            }
        });

        tapButton.setOnTouchListener((v, event) -> {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                tapButton.setBackground(pressedDrawable);
                tapButton.animate().scaleX(0.95f).scaleY(0.95f).setDuration(40).start();
            } else if (event.getAction() == MotionEvent.ACTION_UP || event.getAction() == MotionEvent.ACTION_CANCEL) {
                tapButton.setBackground(unpressedDrawable);
                tapButton.animate().scaleX(1f).scaleY(1f).setDuration(120).setInterpolator(new android.view.animation.OvershootInterpolator()).start();
            }
            
            // ইভেন্টটি GestureDetector এর কাছে পাঠিয়ে দেওয়া হচ্ছে
            gestureDetector.onTouchEvent(event);
            return true;
        });

        addView(tapButton);
    }

    private LayerDrawable createMechanicalButton(boolean isPressed) {
        int lighterAccent = manipulateColor(accentColor, 1.4f);
        int darkerAccent = manipulateColor(accentColor, 0.6f);
        
        int bezelTop = isDark ? Color.parseColor("#333333") : Color.parseColor("#E0E0E0");
        int bezelBottom = isDark ? Color.parseColor("#0A0A0A") : Color.parseColor("#999999");
        
        // নতুন: থিমের সাথে ম্যাচ করে স্পষ্ট বর্ডার কালার
        int borderColor = isDark ? Color.parseColor("#555555") : Color.parseColor("#BDBDBD");

        GradientDrawable shadow = new GradientDrawable();
        shadow.setShape(GradientDrawable.OVAL);
        shadow.setColor(isDark ? Color.argb(200, 0, 0, 0) : Color.argb(90, 0, 0, 0));

        // আউটার রিং (Bezel) এর সাথে Stroke/Border যুক্ত করা হলো
        GradientDrawable bezel = new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{bezelBottom, bezelTop});
        bezel.setShape(GradientDrawable.OVAL);
        bezel.setStroke(4, borderColor); // এই লাইনটি আপনার প্রত্যাশিত বর্ডার তৈরি করবে

        GradientDrawable face = new GradientDrawable(GradientDrawable.Orientation.TL_BR, 
                isPressed ? new int[]{darkerAccent, lighterAccent} : new int[]{lighterAccent, darkerAccent});
        face.setShape(GradientDrawable.OVAL);

        LayerDrawable layerDrawable = new LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, bezel, face});
        
        if (isPressed) {
            layerDrawable.setLayerInset(0, 2, 2, 0, 0); 
            layerDrawable.setLayerInset(1, 2, 2, 4, 4); 
            layerDrawable.setLayerInset(2, 10, 10, 6, 6); 
        } else {
            layerDrawable.setLayerInset(0, 0, 0, 6, 6); 
            layerDrawable.setLayerInset(1, 0, 0, 8, 8); 
            layerDrawable.setLayerInset(2, 4, 4, 12, 12); 
        }
        
        return layerDrawable;
    }

    private int manipulateColor(int color, float factor) {
        int a = Color.alpha(color);
        int r = Math.round(Color.red(color) * factor);
        int g = Math.round(Color.green(color) * factor);
        int b = Math.round(Color.blue(color) * factor);
        return Color.argb(a, Math.min(r, 255), Math.min(g, 255), Math.min(b, 255));
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
    print("🔍 PremiumTasbihView.java আপডেট করা হচ্ছে...")
    target_dir = None
    search_roots = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    for root in search_roots:
        if not os.path.exists(root): continue
        for dirpath, dirnames, filenames in os.walk(root):
            if 'Android/data' in dirpath or '.git' in dirpath: continue
            if 'PremiumTasbihView.java' in filenames:
                target_dir = dirpath
                break
        if target_dir: break
        
    if target_dir:
        file_path = os.path.join(target_dir, 'PremiumTasbihView.java')
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(java_code)
        print(f"✅ পারফেক্ট! বর্ডার এবং লং-প্রেস ফিক্স করা হয়েছে: {file_path}")
    else:
        print("❌ এরর: PremiumTasbihView.java খুঁজে পাওয়া যায়নি।")

if __name__ == '__main__':
    main()
