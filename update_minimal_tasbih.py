import os

java_code = """package com.my.salah.tracker.app;
import android.content.Context; import android.graphics.*; import android.graphics.drawable.*; 
import android.view.*; import android.widget.*; import android.content.SharedPreferences; import android.os.Vibrator; import android.util.TypedValue;

public class PremiumTasbihView extends LinearLayout {
    private int count=0; private TextView display; private View tapButton; private SharedPreferences prefs;
    private boolean isDark; private int accentColor;

    public PremiumTasbihView(Context ctx, boolean isDark, int accCol) {
        super(ctx); this.isDark = isDark; this.accentColor = accCol;
        setOrientation(1); setGravity(17); setWillNotDraw(false); // বাঁকা দাগ আঁকার জন্য
        setPadding(40, 10, 10, 10); // বামে জায়গা রাখা হয়েছে দাগের জন্য
        setBackgroundColor(Color.TRANSPARENT); // ব্যাকগ্রাউন্ড কার্ড থেকে নেবে
        
        prefs=ctx.getSharedPreferences("TasbihPrefs",0); count=prefs.getInt("pt_count",0);
        
        // 1. Minimalist Display
        display=new TextView(ctx); display.setTypeface(Typeface.MONOSPACE, 1); 
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 22f); 
        // কার্ড যেহেতু লাইট থিমেও গাঢ় হবে, তাই টেক্সট সাদা হবে
        display.setTextColor(Color.WHITE); 
        display.setPadding(10,5,10,5);
        updateDisplay(); addView(display);
        
        View sp=new View(ctx); sp.setLayoutParams(new LayoutParams(1, (int)(15*ctx.getResources().getDisplayMetrics().density))); addView(sp);
        
        // 2. Sleek Modern Tap Button
        tapButton=new View(ctx); float den=ctx.getResources().getDisplayMetrics().density;
        tapButton.setLayoutParams(new LayoutParams((int)(55*den),(int)(55*den)));
        LayerDrawable unp=btnBg(false), prs=btnBg(true);
        tapButton.setBackground(unp); tapButton.setClickable(true); tapButton.setFocusable(true);
        
        tapButton.setOnTouchListener((v,e)->{
            if(e.getAction()==0){ tapButton.setBackground(prs); tapButton.setScaleX(0.95f); tapButton.setScaleY(0.95f); }
            else if(e.getAction()==1||e.getAction()==3){ tapButton.setBackground(unp); tapButton.animate().scaleX(1f).scaleY(1f).setDuration(100).start(); }
            return false;
        });
        tapButton.setOnClickListener(v->{ count++; if(count>99999)count=0; updateDisplay(); vib(ctx,30); prefs.edit().putInt("pt_count",count).apply(); });
        tapButton.setOnLongClickListener(v->{ count=0; updateDisplay(); vib(ctx,90); prefs.edit().putInt("pt_count",count).apply(); return true; });
        addView(tapButton);
    }
    
    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        // --- এআই ছবির মতো বাঁকা দাগ (Curved Divider) ---
        Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
        p.setStyle(Paint.Style.STROKE);
        p.setStrokeWidth(4f);
        // কার্ড গাঢ় তাই দাগটি হালকা সাদা/স্বচ্ছ হবে
        p.setColor(Color.argb(80, 255, 255, 255)); 
        
        Path path = new Path();
        path.moveTo(10, 20); // শুরু
        path.quadTo(40, getHeight() / 2f, 10, getHeight() - 20); // বাঁকা অংশ
        canvas.drawPath(path, p);
    }

    private void updateDisplay(){ display.setText(String.format("%04d", count)); }
    private void vib(Context c, int d){ try{ ((Vibrator)c.getSystemService("vibrator")).vibrate(d); }catch(Exception e){} }
    
    private LayerDrawable btnBg(boolean p){
        GradientDrawable sh=new GradientDrawable(); sh.setShape(1); sh.setColor(Color.argb(90,0,0,0));
        GradientDrawable fc=new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{man(accentColor, 1.2f), man(accentColor, 0.8f)}); fc.setShape(1);
        LayerDrawable ld=new LayerDrawable(new Drawable[]{sh,fc});
        if(p){ ld.setLayerInset(0,2,2,0,0); ld.setLayerInset(1,6,6,2,2); }
        else{ ld.setLayerInset(0,0,0,4,4); ld.setLayerInset(1,2,2,6,6); }
        return ld;
    }
    private int man(int c, float f){ return Color.argb(Color.alpha(c), Math.min(Math.round(Color.red(c)*f),255), Math.min(Math.round(Color.green(c)*f),255), Math.min(Math.round(Color.blue(c)*f),255)); }
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
        print("✅ পারফেক্ট! নতুন মিনিমালিস্ট তাসবিহ এবং বাঁকা দাগ সেট করা হয়েছে।")
    else: print("❌ ফাইল পাওয়া যায়নি।")
if __name__ == '__main__': main()
