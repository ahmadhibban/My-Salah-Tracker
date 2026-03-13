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
import android.util.TypedValue;

public class PremiumTasbihView extends LinearLayout {
    private int count = 0;
    private TextView display;
    private View tapButton;
    private SharedPreferences prefs;
    private int accentColor;
    private boolean isDark;

    public PremiumTasbihView(Context context, boolean isDark, int accentColor) {
        super(context);
        this.isDark = isDark;
        this.accentColor = accentColor;
        setOrientation(LinearLayout.VERTICAL);
        setGravity(Gravity.CENTER);
        
        prefs = context.getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE);
        count = prefs.getInt("premium_tasbih_count", 0);

        // --- 1. Digital Display Box (Perfectly Engraved Look) ---
        display = new TextView(context);
        updateDisplay();
        display.setTypeface(Typeface.MONOSPACE, Typeface.BOLD);
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 16f);
        display.setTextColor(isDark ? Color.parseColor("#E0E0E0") : Color.parseColor("#333333"));
        display.setGravity(Gravity.CENTER);
        display.setPadding(25, 12, 25, 12);
        
        // Inner shadow illusion (Engraved)
        GradientDrawable displaySurface = new GradientDrawable();
        displaySurface.setColor(isDark ? Color.parseColor("#121212") : Color.parseColor("#D6D6D6"));
        displaySurface.setCornerRadius(15f);

        GradientDrawable displayTopShadow = new GradientDrawable();
        displayTopShadow.setColor(isDark ? Color.parseColor("#000000") : Color.parseColor("#9E9E9E"));
        displayTopShadow.setCornerRadius(15f);
        
        LayerDrawable displayBg = new LayerDrawable(new android.graphics.drawable.Drawable[]{displayTopShadow, displaySurface});
        // Shifting the surface down-right to reveal the dark shadow on top-left (engraved effect)
        displayBg.setLayerInset(1, 3, 3, 0, 0); 
        
        display.setBackground(displayBg);
        addView(display);

        // Spacer
        View space = new View(context);
        space.setLayoutParams(new LinearLayout.LayoutParams(1, (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 15, context.getResources().getDisplayMetrics())));
        addView(space);

        // --- 2. Realistic 3D Tap Button (Like the Black Design) ---
        tapButton = new View(context);
        float density = context.getResources().getDisplayMetrics().density;
        int btnSize = (int) (65 * density); // Perfect size
        LinearLayout.LayoutParams btnParams = new LinearLayout.LayoutParams(btnSize, btnSize);
        tapButton.setLayoutParams(btnParams);
        
        // Create Highlight (lighter) and Shadow (darker) versions of your Accent Color
        int lighterAccent = manipulateColor(accentColor, 1.3f);
        int darkerAccent = manipulateColor(accentColor, 0.7f);

        // Normal State (Pillowed out)
        LayerDrawable unpressedDrawable = create3DButtonDrawable(lighterAccent, darkerAccent, accentColor, false);
        // Pressed State (Pushed in)
        LayerDrawable pressedDrawable = create3DButtonDrawable(lighterAccent, darkerAccent, accentColor, true);

        tapButton.setBackground(unpressedDrawable);
        
        tapButton.setOnTouchListener((v, event) -> {
            if (event.getAction() == MotionEvent.ACTION_DOWN) {
                tapButton.setBackground(pressedDrawable);
                tapButton.animate().scaleX(0.96f).scaleY(0.96f).setDuration(50).start();
                return true;
            } else if (event.getAction() == MotionEvent.ACTION_UP || event.getAction() == MotionEvent.ACTION_CANCEL) {
                tapButton.setBackground(unpressedDrawable);
                tapButton.animate().scaleX(1f).scaleY(1f).setDuration(100).start();
                
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

    private LayerDrawable create3DButtonDrawable(int lightColor, int darkColor, int baseColor, boolean isPressed) {
        // Drop Shadow (Outer ring)
        GradientDrawable shadow = new GradientDrawable();
        shadow.setShape(GradientDrawable.OVAL);
        shadow.setColor(isDark ? Color.argb(150, 0, 0, 0) : Color.argb(60, 0, 0, 0));

        // Main Surface with Gradient to give that realistic rounded/pillowed 3D look
        GradientDrawable surface = new GradientDrawable();
        surface.setShape(GradientDrawable.OVAL);
        if (isPressed) {
            // Reverse gradient when pressed
            surface.setColors(new int[]{darkColor, baseColor});
        } else {
            surface.setColors(new int[]{lightColor, darkColor});
        }
        surface.setGradientType(GradientDrawable.LINEAR_GRADIENT);
        surface.setOrientation(GradientDrawable.Orientation.TL_BR);

        LayerDrawable layerDrawable = new LayerDrawable(new android.graphics.drawable.Drawable[]{shadow, surface});
        
        if (isPressed) {
            layerDrawable.setLayerInset(1, 3, 3, 0, 0); // Pushed in (moves down-right)
        } else {
            layerDrawable.setLayerInset(1, 0, 0, 8, 8); // Popped out (thick shadow on bottom-right)
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
    print("🔍 PremiumTasbihView.java খোঁজা হচ্ছে...")
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
        print(f"✅ সফল হয়েছে! ফাইলটি আপডেট করা হয়েছে: {file_path}")
    else:
        print("❌ এরর: PremiumTasbihView.java খুঁজে পাওয়া যায়নি।")

if __name__ == '__main__':
    main()
