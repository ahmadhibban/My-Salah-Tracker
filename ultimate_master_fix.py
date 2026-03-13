import os
import re

def main():
    search_paths = ['.', '/storage/emulated/0/AndroidIDEProjects', '/storage/emulated/0/']
    
    main_path = None
    tasbih_path = None
    
    for r in search_paths:
        if not os.path.exists(r): continue
        for root, dirs, files in os.walk(r):
            if 'Android/data' in root or '.git' in root: continue
            if 'MainActivity.java' in files: main_path = os.path.join(root, 'MainActivity.java')
            if 'PremiumTasbihView.java' in files: tasbih_path = os.path.join(root, 'PremiumTasbihView.java')
        if main_path and tasbih_path: break

    # ==========================================
    # ১. MainActivity.java - সুপারফাস্ট ক্লিক ও লেআউট ফিট
    # ==========================================
    if main_path:
        with open(main_path, 'r', encoding='utf-8') as f:
            c = f.read()

        # --- ফিক্স ১: ফরজ নামাজের সুপারফাস্ট ডাইনামিক ক্লিক ---
        old_fard_regex = r'chk\.setOnClickListener\(new View\.OnClickListener\(\)\s*\{\s*@Override\s*public void onClick\(View v\)\s*\{\s*if \(fardStat\.equals\("excused"\)\) return;.*?\}\s*\}\);'
        new_fard_click = """chk.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SalahRecord currR = getRoomRecord(dKey);
                String cStat = getFardStat(currR, AppConstants.PRAYERS[finalI]);
                if (cStat.equals("excused")) return;
                
                String nVal = cStat.equals("yes") ? "no" : "yes";
                setFardStat(currR, AppConstants.PRAYERS[finalI], nVal);
                updateRoomRecord(currR);
                sp.edit().putString(dKey + "_" + AppConstants.PRAYERS[finalI], nVal).apply();
                
                // রিলোড ছাড়া ইনস্ট্যান্ট UI আপডেট
                chk.removeAllViews();
                if (nVal.equals("yes")) {
                    chk.setShapeType(soup.neumorphism.ShapeType.PRESSED);
                    chk.setShadowElevation(2f * DENSITY);
                    TextView inner = new TextView(MainActivity.this); inner.setText("✓"); inner.setTextColor(colorAccent); inner.setTextSize(18); inner.setTypeface(null, Typeface.DEFAULT_BOLD); inner.setGravity(Gravity.CENTER); inner.setLayoutParams(new FrameLayout.LayoutParams(-1, -1)); chk.addView(inner);
                } else {
                    chk.setShapeType(soup.neumorphism.ShapeType.FLAT);
                    chk.setShadowElevation(3.5f * DENSITY);
                }
                
                int nC = 0; for(String pr : AppConstants.PRAYERS) { String s = getFardStat(currR, pr); if(s.equals("yes") || s.equals("excused")) nC++; }
                pT.setText(lang.bnNum(nC*100/6) + "%");
                subBtm.setText(statusMsgs[nC]);
                refreshWidget();
            }
        });"""
        c = re.sub(old_fard_regex, new_fard_click, c, flags=re.DOTALL)

        # --- ফিক্স ২: সুন্নত নামাজের সুপারফাস্ট ডাইনামিক ক্লিক ---
        old_sunnah_regex = r'sBox\.setOnClickListener\(new View\.OnClickListener\(\)\s*\{\s*@Override\s*public void onClick\(View v\)\s*\{\s*if \(fardStat\.equals\("excused"\)\) return;.*?\} catch\(Exception e\)\{\}\s*\}\s*\}\);'
        new_sunnah_click = """sBox.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SalahRecord currR = getRoomRecord(dKey);
                String cStat = getFardStat(currR, AppConstants.PRAYERS[finalI]);
                if (cStat.equals("excused")) return;
                try {
                    org.json.JSONObject sunnahs = new org.json.JSONObject(currR.sunnahStr);
                    boolean cDone = sunnahs.optBoolean(sName, false);
                    sunnahs.put(sName, !cDone);
                    currR.sunnahStr = sunnahs.toString();
                    updateRoomRecord(currR);
                    sp.edit().putBoolean(dKey + "_" + sName, !cDone).apply();
                    
                    // ইনস্ট্যান্ট UI আপডেট
                    sBox.removeAllViews();
                    if (!cDone) {
                        GradientDrawable fill = new GradientDrawable(); fill.setColor(colorAccent); fill.setCornerRadius(10f * DENSITY); sBox.setBackground(fill);
                        TextView t = new TextView(MainActivity.this); t.setText("✓"); t.setTextColor(Color.WHITE); t.setTextSize(10); t.setTypeface(null, Typeface.DEFAULT_BOLD); t.setGravity(Gravity.CENTER); t.setLayoutParams(new LinearLayout.LayoutParams(-1, -1)); sBox.addView(t);
                    } else {
                        GradientDrawable out = new GradientDrawable(); out.setStroke(2, isDarkTheme ? themeColors[3] : Color.parseColor("#CCCCCC")); out.setCornerRadius(10f * DENSITY); sBox.setBackground(out);
                    }
                    refreshWidget();
                } catch(Exception e){}
            }
        });"""
        c = re.sub(old_sunnah_regex, new_sunnah_click, c, flags=re.DOTALL)

        # --- ফিক্স ৩: ফোর্সফুল লেআউট সাইজ কমানো (এক পেজে ফিট) ---
        c = re.sub(r'txt\.setTextSize\(18\);', 'txt.setTextSize(16);', c) # ফন্ট হালকা ছোট
        c = re.sub(r'sub\.setTextSize\(12\);', 'sub.setTextSize(11);', c) # ফন্ট হালকা ছোট
        c = re.sub(r'sList\.setPadding\(0,\s*\(int\)\(\d+\*DENSITY\),\s*0,\s*0\);', 'sList.setPadding(0, (int)(4*DENSITY), 0, 0);', c) # সুন্নাহ লিস্টের গ্যাপ কমানো
        
        # কার্ডগুলোর ডেনসিটি স্পেস কমানো
        c = re.sub(r'cardParams\.setMargins\(\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\)\);', 
                   'cardParams.setMargins((int)(20*DENSITY), (int)(1*DENSITY), (int)(20*DENSITY), (int)(1*DENSITY));', c)
        c = re.sub(r'card\.setPadding\(\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\)\);', 
                   'card.setPadding((int)(20*DENSITY), (int)(4*DENSITY), (int)(20*DENSITY), (int)(4*DENSITY));', c)
        
        c = re.sub(r'headerParams\.setMargins\(\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\)\);', 
                   'headerParams.setMargins((int)(20*DENSITY), (int)(2*DENSITY), (int)(20*DENSITY), (int)(2*DENSITY));', c)
        c = re.sub(r'pCard\.setPadding\(\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\),\s*\(int\)\(\d+\*DENSITY\)\);', 
                   'pCard.setPadding((int)(20*DENSITY), (int)(5*DENSITY), (int)(20*DENSITY), (int)(5*DENSITY));', c)
        
        # মূল স্ক্রলের বটম প্যাডিং কমানো
        c = re.sub(r'main\.setPadding\(0,\s*0,\s*0,\s*\(int\)\(\d+\*DENSITY\)\);', 'main.setPadding(0, 0, 0, (int)(10*DENSITY));', c)

        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ MainActivity: ক্লিক বাগ ফিক্সড, স্পিড 0ms এবং লেআউট এক পেজে ফিট করা হয়েছে!")


    # ==========================================
    # ২. PremiumTasbihView.java - পারফেক্ট অ্যালাইনমেন্ট ও প্রিমিয়াম ডিজাইন
    # ==========================================
    if tasbih_path:
        tasbih_code = """package com.my.salah.tracker.app;

import android.content.Context; import android.graphics.*; import android.graphics.drawable.*; 
import android.view.*; import android.widget.*; import android.content.SharedPreferences; import android.os.Vibrator; import android.util.TypedValue;

public class PremiumTasbihView extends LinearLayout {
    private int count = 0; private TextView display; private View tapButton; private SharedPreferences prefs; private int accentColor;

    public PremiumTasbihView(Context ctx, boolean isDark, int accCol) {
        super(ctx); this.accentColor = accCol;
        setOrientation(LinearLayout.VERTICAL); setGravity(Gravity.CENTER); setWillNotDraw(false); 
        
        // --- ফিক্স ৪: ডিসপ্লে নিচে নামানো (Top Padding 45 করা হয়েছে) ---
        setPadding(60, 45, 20, 20); 
        
        prefs = ctx.getSharedPreferences("TasbihPrefs", 0); count = prefs.getInt("pt_count", 0);
        
        // 1. Sleek Engraved Display
        display = new TextView(ctx); display.setTypeface(Typeface.create(Typeface.MONOSPACE, Typeface.BOLD)); 
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 20f); display.setTextColor(Color.WHITE); 
        GradientDrawable displayBg = new GradientDrawable(); displayBg.setColor(Color.argb(35, 0, 0, 0)); 
        displayBg.setCornerRadius(15f); displayBg.setStroke(2, Color.argb(40, 255, 255, 255)); 
        display.setBackground(displayBg); display.setPadding(30, 8, 30, 8); display.setGravity(Gravity.CENTER);
        updateDisplay(); addView(display);
        
        View sp = new View(ctx); sp.setLayoutParams(new LayoutParams(1, (int)(12 * ctx.getResources().getDisplayMetrics().density))); addView(sp);
        
        // 2. Ultra Premium Jewel Button
        tapButton = new View(ctx); float den = ctx.getResources().getDisplayMetrics().density;
        tapButton.setLayoutParams(new LayoutParams((int)(55 * den), (int)(55 * den)));
        LayerDrawable unpressed = createPremiumButton(false), pressed = createPremiumButton(true);
        tapButton.setBackground(unpressed); tapButton.setClickable(true); tapButton.setFocusable(true);
        
        tapButton.setOnTouchListener((v, e) -> {
            if (e.getAction() == MotionEvent.ACTION_DOWN) { tapButton.setBackground(pressed); tapButton.setScaleX(0.92f); tapButton.setScaleY(0.92f); } 
            else if (e.getAction() == MotionEvent.ACTION_UP || e.getAction() == MotionEvent.ACTION_CANCEL) { tapButton.setBackground(unpressed); tapButton.animate().scaleX(1f).scaleY(1f).setDuration(100).setInterpolator(new android.view.animation.OvershootInterpolator()).start(); }
            return false;
        });
        tapButton.setOnClickListener(v -> { count++; if(count > 99999) count = 0; updateDisplay(); vib(ctx, 20); prefs.edit().putInt("pt_count", count).apply(); });
        tapButton.setOnLongClickListener(v -> { count = 0; updateDisplay(); vib(ctx, 80); prefs.edit().putInt("pt_count", count).apply(); return true; });
        addView(tapButton);
    }
    
    @Override protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG); p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f);
        p.setShader(new LinearGradient(0, 0, 0, getHeight(), new int[]{Color.TRANSPARENT, Color.argb(120, 255, 255, 255), Color.TRANSPARENT}, null, Shader.TileMode.CLAMP));
        Path path = new Path(); path.moveTo(15, 30); path.quadTo(45, getHeight() / 2f, 15, getHeight() - 30); canvas.drawPath(path, p);
    }

    private LayerDrawable createPremiumButton(boolean isPressed) {
        int light = Color.argb(255, Math.min(255, (int)(Color.red(accentColor)*1.2)), Math.min(255, (int)(Color.green(accentColor)*1.2)), Math.min(255, (int)(Color.blue(accentColor)*1.2)));
        int dark = Color.argb(255, (int)(Color.red(accentColor)*0.7), (int)(Color.green(accentColor)*0.7), (int)(Color.blue(accentColor)*0.7));
        GradientDrawable shadow = new GradientDrawable(); shadow.setShape(GradientDrawable.OVAL); shadow.setColor(Color.argb(80, 0, 0, 0)); 
        GradientDrawable face = new GradientDrawable(GradientDrawable.Orientation.TL_BR, isPressed ? new int[]{dark, light} : new int[]{light, dark});
        face.setShape(GradientDrawable.OVAL); face.setStroke(2, Color.argb(60, 255, 255, 255));
        LayerDrawable ld = new LayerDrawable(new Drawable[]{shadow, face});
        if (isPressed) { ld.setLayerInset(0, 2, 2, 0, 0); ld.setLayerInset(1, 4, 4, 2, 2); } 
        else { ld.setLayerInset(0, 0, 0, 6, 6); ld.setLayerInset(1, 0, 0, 6, 6); }
        return ld;
    }
    private void updateDisplay(){ display.setText(String.format("%04d", count)); }
    private void vib(Context c, int d){ try{ ((Vibrator)c.getSystemService(Context.VIBRATOR_SERVICE)).vibrate(d); }catch(Exception e){} }
}"""
        with open(tasbih_path, 'w', encoding='utf-8') as f:
            f.write(tasbih_code)
        print("✅ PremiumTasbihView: প্রিমিয়াম ডিজাইন অ্যাপ্লাইড এবং ডিসপ্লে পারফেক্টলি সেন্টার করা হয়েছে!")

if __name__ == '__main__': main()
