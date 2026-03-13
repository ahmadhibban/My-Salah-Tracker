import os

java_code = """package com.my.salah.tracker.app;

import android.content.Context;
import android.graphics.*;
import android.graphics.drawable.*;
import android.view.*;
import android.widget.*;
import android.content.SharedPreferences;
import android.os.Vibrator;
import android.util.TypedValue;

public class PremiumTasbihView extends LinearLayout {
    private int count = 0;
    private TextView display;
    private View tapButton;
    private SharedPreferences prefs;
    private int accentColor;

    public PremiumTasbihView(Context ctx, boolean isDark, int accCol) {
        super(ctx); 
        this.accentColor = accCol;
        setOrientation(LinearLayout.VERTICAL); 
        setGravity(Gravity.CENTER); 
        setWillNotDraw(false); // বাঁকা দাগ আকার জন্য
        
        // বাম পাশে কার্ভড দাগের জন্য পর্যাপ্ত জায়গা রাখা হলো
        setPadding(60, 20, 20, 20); 
        
        prefs = ctx.getSharedPreferences("TasbihPrefs", 0); 
        count = prefs.getInt("pt_count", 0);
        
        // --- 1. Beautiful Engraved Display ---
        display = new TextView(ctx); 
        display.setTypeface(Typeface.create(Typeface.MONOSPACE, Typeface.BOLD)); 
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 22f); 
        display.setTextColor(Color.WHITE); // ব্যাকগ্রাউন্ড ডিপ থাকবে তাই টেক্সট সাদা
        
        // প্রিমিয়াম ট্রান্সপারেন্ট গ্লাস ইনসেট লুক
        GradientDrawable displayBg = new GradientDrawable();
        displayBg.setColor(Color.argb(40, 0, 0, 0)); // সফট ডার্ক ওভারলে
        displayBg.setCornerRadius(20f);
        displayBg.setStroke(2, Color.argb(40, 255, 255, 255)); // হালকা গ্লাস হাইলাইট
        
        display.setBackground(displayBg);
        display.setPadding(35, 12, 35, 12);
        display.setGravity(Gravity.CENTER);
        updateDisplay(); 
        addView(display);
        
        // Spacer
        View sp = new View(ctx); 
        sp.setLayoutParams(new LayoutParams(1, (int)(18 * ctx.getResources().getDisplayMetrics().density))); 
        addView(sp);
        
        // --- 2. Sleek 3D Jewel Button ---
        tapButton = new View(ctx); 
        float den = ctx.getResources().getDisplayMetrics().density;
        tapButton.setLayoutParams(new LayoutParams((int)(55 * den), (int)(55 * den)));
        
        LayerDrawable unpressed = createPremiumButton(false);
        LayerDrawable pressed = createPremiumButton(true);
        
        tapButton.setBackground(unpressed); 
        tapButton.setClickable(true); 
        tapButton.setFocusable(true);
        
        tapButton.setOnTouchListener((v, e) -> {
            if (e.getAction() == MotionEvent.ACTION_DOWN) { 
                tapButton.setBackground(pressed); 
                tapButton.animate().scaleX(0.92f).scaleY(0.92f).setDuration(50).start(); 
            } else if (e.getAction() == MotionEvent.ACTION_UP || e.getAction() == MotionEvent.ACTION_CANCEL) { 
                tapButton.setBackground(unpressed); 
                tapButton.animate().scaleX(1f).scaleY(1f).setDuration(150).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); 
            }
            return false;
        });
        
        tapButton.setOnClickListener(v -> { 
            count++; if(count > 99999) count = 0; 
            updateDisplay(); vib(ctx, 25); 
            prefs.edit().putInt("pt_count", count).apply(); 
        });
        
        tapButton.setOnLongClickListener(v -> { 
            count = 0; updateDisplay(); vib(ctx, 80); 
            prefs.edit().putInt("pt_count", count).apply(); 
            return true; 
        });
        
        addView(tapButton);
    }
    
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        // --- ৩. প্রিমিয়াম গ্লোয়িং কার্ভড ডিভাইডার (Glowing Curved Divider) ---
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        p.setStyle(Paint.Style.STROKE);
        p.setStrokeWidth(4f);
        
        // ফেইড ইফেক্ট (ওপর নিচে মিলিয়ে যাবে, মাঝখানে উজ্জ্বল)
        p.setShader(new LinearGradient(0, 0, 0, getHeight(), 
            new int[]{Color.TRANSPARENT, Color.argb(120, 255, 255, 255), Color.TRANSPARENT}, 
            null, Shader.TileMode.CLAMP));
            
        Path path = new Path();
        path.moveTo(15, 30); // শুরু
        path.quadTo(50, getHeight() / 2f, 15, getHeight() - 30); // সুন্দর স্মুথ বাঁক
        canvas.drawPath(path, p);
    }

    private LayerDrawable createPremiumButton(boolean isPressed) {
        // বাটনের কালার লজিক
        int light = Color.argb(255, Math.min(255, (int)(Color.red(accentColor)*1.2)), Math.min(255, (int)(Color.green(accentColor)*1.2)), Math.min(255, (int)(Color.blue(accentColor)*1.2)));
        int dark = Color.argb(255, (int)(Color.red(accentColor)*0.7), (int)(Color.green(accentColor)*0.7), (int)(Color.blue(accentColor)*0.7));

        GradientDrawable shadow = new GradientDrawable();
        shadow.setShape(GradientDrawable.OVAL);
        shadow.setColor(Color.argb(100, 0, 0, 0)); // সফট শ্যাডো

        GradientDrawable face = new GradientDrawable(GradientDrawable.Orientation.TL_BR, 
                isPressed ? new int[]{dark, light} : new int[]{light, dark});
        face.setShape(GradientDrawable.OVAL);
        // সফট ইনার হাইলাইট
        face.setStroke(2, Color.argb(60, 255, 255, 255));

        LayerDrawable ld = new LayerDrawable(new Drawable[]{shadow, face});
        if (isPressed) {
            ld.setLayerInset(0, 2, 2, 0, 0);
            ld.setLayerInset(1, 6, 6, 2, 2); // ভেতরে ডেবে যাবে
        } else {
            ld.setLayerInset(0, 0, 0, 8, 8); // শ্যাডো নিচে পড়বে
            ld.setLayerInset(1, 0, 0, 8, 8); // বাটন উঁচুতে থাকবে
        }
        return ld;
    }

    private void updateDisplay(){ display.setText(String.format("%04d", count)); }
    private void vib(Context c, int d){ try{ ((Vibrator)c.getSystemService(Context.VIBRATOR_SERVICE)).vibrate(d); }catch(Exception e){} }
}
"""
def main():
    target_dir = None
    for root, dirs, files in os.walk('.'):
        if 'Android/data' in root or '.git' in root: continue
        if 'PremiumTasbihView.java' in files: target_dir = root; break
    if not target_dir:
        for root, dirs, files in os.walk('/storage/emulated/0/'):
            if 'Android/data' in root or '.git' in root: continue
            if 'PremiumTasbihView.java' in files: target_dir = root; break
            
    if target_dir:
        path = os.path.join(target_dir, 'PremiumTasbihView.java')
        with open(path, 'w', encoding='utf-8') as f: f.write(java_code)
        print("✅ পারফেক্ট! মাস্টারপিস তাসবিহ ভিউ কোড লেখা সম্পন্ন হয়েছে।")
    else: print("❌ ফাইল পাওয়া যায়নি।")
if __name__ == '__main__': main()
