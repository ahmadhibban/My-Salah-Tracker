package com.my.salah.tracker.app;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.*;
import android.graphics.drawable.*;
import android.os.Vibrator;
import android.util.TypedValue;
import android.view.*;
import android.widget.*;

public class PremiumTasbihView extends LinearLayout
{
    private int count = 0;
    private TextView display;
    private View tapButton;
    private SharedPreferences prefs;
    private int accentColor;

    public PremiumTasbihView(Context ctx, boolean isDark, int accCol)
    {
        super(ctx);
        this.accentColor = accCol;
        setOrientation(LinearLayout.VERTICAL);
        setGravity(Gravity.CENTER);
        setWillNotDraw(false);

        // --- ফিক্স ৪: ডিসপ্লে নিচে নামানো (Top Padding 45 করা হয়েছে) ---
        setPadding(60, 45, 20, 20);

        prefs = ctx.getSharedPreferences("TasbihPrefs", 0);
        count = prefs.getInt("pt_count", 0);

        // 1. Sleek Engraved Display
        display = new TextView(ctx);
        display.setTypeface(Typeface.create(Typeface.MONOSPACE, Typeface.BOLD));
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20f);
        display.setTextColor(Color.WHITE);
        GradientDrawable displayBg = new GradientDrawable();
        displayBg.setColor(Color.argb(35, 0, 0, 0));
        displayBg.setCornerRadius(15f);
        displayBg.setStroke(2, Color.argb(40, 255, 255, 255));
        display.setBackground(displayBg);
        display.setPadding(30, 8, 30, 8);
        display.setGravity(Gravity.CENTER);
        updateDisplay();
        addView(display);

        View sp = new View(ctx);
        sp.setLayoutParams(
            new LayoutParams(1, (int) (12 * ctx.getResources().getDisplayMetrics().density)));
        addView(sp);

        // 2. Ultra Premium Jewel Button
        tapButton = new View(ctx);
        float den = ctx.getResources().getDisplayMetrics().density;
        tapButton.setLayoutParams(new LayoutParams((int) (55 * den), (int) (55 * den)));
        LayerDrawable unpressed = createPremiumButton(false), pressed = createPremiumButton(true);
        tapButton.setBackground(unpressed);
        tapButton.setClickable(true);
        tapButton.setFocusable(true);

        tapButton.setOnTouchListener((v, e) -> {
            if (e.getAction() == MotionEvent.ACTION_DOWN) {
                tapButton.setBackground(pressed);
                tapButton.setScaleX(0.92f);
                tapButton.setScaleY(0.92f);
            } else if (e.getAction() == MotionEvent.ACTION_UP
                || e.getAction() == MotionEvent.ACTION_CANCEL) {
                tapButton.setBackground(unpressed);
                tapButton.animate()
                    .scaleX(1f)
                    .scaleY(1f)
                    .setDuration(100)
                    .setInterpolator(new android.view.animation.OvershootInterpolator())
                    .start();
            }
            return false;
        });
        tapButton.setOnClickListener(v -> {
            count++;
            if (count > 99999)
                count = 0;
            updateDisplay();
            vib(ctx, 20);
            prefs.edit().putInt("pt_count", count).apply();
        });
        tapButton.setOnLongClickListener(v -> {
            count = 0;
            updateDisplay();
            vib(ctx, 80);
            prefs.edit().putInt("pt_count", count).apply();
            return true;
        });
        addView(tapButton);
    }

    @Override protected void onDraw(Canvas canvas)
    {
        super.onDraw(canvas);
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        p.setStyle(Paint.Style.STROKE);
        p.setStrokeWidth(4f);
        p.setShader(new LinearGradient(0, 0, 0, getHeight(),
            new int[] {Color.TRANSPARENT, Color.argb(120, 255, 255, 255), Color.TRANSPARENT}, null,
            Shader.TileMode.CLAMP));
        Path path = new Path();
        path.moveTo(15, 30);
        path.quadTo(45, getHeight() / 2f, 15, getHeight() - 30);
        canvas.drawPath(path, p);
    }

    private LayerDrawable createPremiumButton(boolean isPressed)
    {
        int light = Color.argb(255, Math.min(255, (int) (Color.red(accentColor) * 1.2)),
            Math.min(255, (int) (Color.green(accentColor) * 1.2)),
            Math.min(255, (int) (Color.blue(accentColor) * 1.2)));
        int dark = Color.argb(255, (int) (Color.red(accentColor) * 0.7),
            (int) (Color.green(accentColor) * 0.7), (int) (Color.blue(accentColor) * 0.7));
        GradientDrawable shadow = new GradientDrawable();
        shadow.setShape(GradientDrawable.OVAL);
        shadow.setColor(Color.argb(80, 0, 0, 0));
        GradientDrawable face = new GradientDrawable(GradientDrawable.Orientation.TL_BR,
            isPressed ? new int[] {dark, light} : new int[] {light, dark});
        face.setShape(GradientDrawable.OVAL);
        face.setStroke(2, Color.argb(60, 255, 255, 255));
        LayerDrawable ld = new LayerDrawable(new Drawable[] {shadow, face});
        if (isPressed) {
            ld.setLayerInset(0, 2, 2, 0, 0);
            ld.setLayerInset(1, 4, 4, 2, 2);
        } else {
            ld.setLayerInset(0, 0, 0, 6, 6);
            ld.setLayerInset(1, 0, 0, 6, 6);
        }
        return ld;
    }
    private void updateDisplay()
    {
        String numStr = String.format("%04d", count);
        try {
            android.content.SharedPreferences sp =
                getContext().getSharedPreferences("salah_pro_final", 0);
            if (sp.getString("app_lang", "en").equals("bn")) {
                numStr = numStr.replace("0", "০")
                             .replace("1", "১")
                             .replace("2", "২")
                             .replace("3", "৩")
                             .replace("4", "৪")
                             .replace("5", "৫")
                             .replace("6", "৬")
                             .replace("7", "৭")
                             .replace("8", "৮")
                             .replace("9", "৯");
            }
        } catch (Exception e) {
        }
        display.setText(numStr);
    }
    private void vib(Context c, int d)
    {
        try {
            ((Vibrator) c.getSystemService(Context.VIBRATOR_SERVICE)).vibrate(d);
        } catch (Exception e) {
        }
    }
}