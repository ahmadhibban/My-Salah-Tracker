import os

java_code = """package com.my.salah.tracker.app;
import android.content.Context; import android.graphics.Color; import android.graphics.Typeface; 
import android.graphics.drawable.*; import android.view.*; import android.widget.*; 
import android.content.SharedPreferences; import android.os.Vibrator; import android.util.TypedValue;

public class PremiumTasbihView extends LinearLayout {
    private int count=0; private TextView display; private View tapButton; private SharedPreferences prefs;
    public PremiumTasbihView(Context ctx, boolean isDark, int accCol) {
        super(ctx); setOrientation(1); setGravity(17);
        prefs=ctx.getSharedPreferences("TasbihPrefs",0); count=prefs.getInt("pt_count",0);
        
        // 1. Casing (Perfect Pill/Capsule Shape)
        GradientDrawable body=new GradientDrawable(); body.setColor(isDark?Color.parseColor("#1C1C1C"):Color.parseColor("#E5E5E5"));
        body.setCornerRadius(150f); // Fully rounded edges
        body.setStroke(3, isDark?Color.parseColor("#0A0A0A"):Color.parseColor("#CCCCCC"));
        setBackground(body); 
        setPadding(15,20,15,20); // Compact padding to save height
        
        // 2. Engraved LCD Display (Larger Text, 5 Digits)
        display=new TextView(ctx); display.setTypeface(Typeface.MONOSPACE,1); 
        display.setTextSize(TypedValue.COMPLEX_UNIT_SP, 21f); // Larger font
        display.setTextColor(isDark?Color.parseColor("#00E676"):Color.parseColor("#212121"));
        display.setPadding(20,12,20,12);
        
        GradientDrawable dTop=new GradientDrawable(); dTop.setColor(isDark?Color.parseColor("#000000"):Color.parseColor("#999999")); dTop.setCornerRadius(15f);
        GradientDrawable dSurf=new GradientDrawable(); dSurf.setColor(isDark?Color.parseColor("#121212"):Color.parseColor("#9EA792")); dSurf.setCornerRadius(15f);
        LayerDrawable dBg=new LayerDrawable(new Drawable[]{dTop, dSurf}); dBg.setLayerInset(1,3,4,0,0); // Engraved depth
        display.setBackground(dBg); updateDisplay(); addView(display);
        
        // Small spacer to reduce height
        View sp=new View(ctx); sp.setLayoutParams(new LayoutParams(1, (int)(10*ctx.getResources().getDisplayMetrics().density))); addView(sp);
        
        // 3. Compact 3D Mechanical Button
        tapButton=new View(ctx); float den=ctx.getResources().getDisplayMetrics().density;
        tapButton.setLayoutParams(new LayoutParams((int)(55*den),(int)(55*den)));
        LayerDrawable unp=btnBg(accCol,isDark,false), prs=btnBg(accCol,isDark,true);
        tapButton.setBackground(unp); tapButton.setClickable(true); tapButton.setFocusable(true);
        
        tapButton.setOnTouchListener((v,e)->{
            if(e.getAction()==0){ tapButton.setBackground(prs); tapButton.setScaleX(0.96f); tapButton.setScaleY(0.96f); }
            else if(e.getAction()==1||e.getAction()==3){ tapButton.setBackground(unp); tapButton.animate().scaleX(1f).scaleY(1f).setDuration(100).start(); }
            return false;
        });
        tapButton.setOnClickListener(v->{ count++; if(count>99999)count=0; updateDisplay(); vib(ctx,30); prefs.edit().putInt("pt_count",count).apply(); });
        tapButton.setOnLongClickListener(v->{ count=0; updateDisplay(); vib(ctx,90); prefs.edit().putInt("pt_count",count).apply(); return true; });
        addView(tapButton);
    }
    private void updateDisplay(){ display.setText(String.format("%04d", count)); }
    private void vib(Context c, int d){ try{ ((Vibrator)c.getSystemService("vibrator")).vibrate(d); }catch(Exception e){} }
    private LayerDrawable btnBg(int c, boolean d, boolean p){
        int l=man(c,1.3f), dk=man(c,0.7f), bT=d?Color.parseColor("#333333"):Color.parseColor("#E0E0E0"), bB=d?Color.parseColor("#0A0A0A"):Color.parseColor("#999999");
        GradientDrawable sh=new GradientDrawable(); sh.setShape(1); sh.setColor(Color.argb(d?180:70,0,0,0));
        GradientDrawable bz=new GradientDrawable(GradientDrawable.Orientation.TL_BR,new int[]{bB,bT}); bz.setShape(1); bz.setStroke(2, d?Color.parseColor("#555555"):Color.parseColor("#BDBDBD"));
        GradientDrawable fc=new GradientDrawable(GradientDrawable.Orientation.TL_BR, p?new int[]{dk,l}:new int[]{l,dk}); fc.setShape(1);
        LayerDrawable ld=new LayerDrawable(new Drawable[]{sh,bz,fc});
        if(p){ ld.setLayerInset(0,2,2,0,0); ld.setLayerInset(1,2,2,2,2); ld.setLayerInset(2,8,8,4,4); }
        else{ ld.setLayerInset(0,0,0,5,5); ld.setLayerInset(1,0,0,6,6); ld.setLayerInset(2,3,3,10,10); }
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
        print("✅ পারফেক্ট! ডিম্বাকার শেপ, বড় খোদাই করা ডিসপ্লে এবং ৯৯৯৯ লিমিট সেট করা হয়েছে।")
    else: print("❌ ফাইল পাওয়া যায়নি।")
if __name__ == '__main__': main()
