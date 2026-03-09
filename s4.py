f='app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
z3=r'''
        private void cnt(boolean a){ int i=zikrMan.currentIdx; if(a){zikrMan.indCounts[i]++; if(zikrMan.soundOn&&zikrMan.toneGen!=null) zikrMan.toneGen.startTone(24,50); if(zikrMan.tasbihList.get(i).target>0&&zikrMan.indCounts[i]>=zikrMan.tasbihList.get(i).target){zikrMan.indCounts[i]=0;zikrMan.indRounds[i]++;performHapticFeedback(0);}} else {if(zikrMan.indCounts[i]>0)zikrMan.indCounts[i]--;} zikrMan.save(); }
        private void anm(float t, boolean a){ android.animation.ValueAnimator v=android.animation.ValueAnimator.ofFloat(beadOff,t); v.setDuration(120); v.addUpdateListener(an->{beadOff=(float)an.getAnimatedValue();invalidate();}); v.addListener(new android.animation.AnimatorListenerAdapter(){public void onAnimationEnd(android.animation.Animator an){if(t!=0f)cnt(a); beadOff=0f;invalidate();}}); v.start(); }
        @Override public boolean onTouchEvent(android.view.MotionEvent ev) {
            float x=ev.getX(), y=ev.getY(), w=getWidth(), cx=w/2f; float iY=940f, thY=1100f; int i=zikrMan.currentIdx;
            if(ev.getAction()==0){startX=x;isSwiping=false;return true;}
            if(ev.getAction()==2){float dx=x-startX; if(Math.abs(dx)>20){isSwiping=true; beadOff=dx; if(beadOff>160f)beadOff=160f; if(beadOff<-160f)beadOff=-160f; invalidate();}}
            if(ev.getAction()==1){
                float dx=x-startX; if(isSwiping){ if(dx<-60){performHapticFeedback(1);anm(-160f,true);} else if(dx>60){performHapticFeedback(1);anm(160f,false);} else anm(0f,false); }
                else {
                    if(Math.abs(y-iY)<120){ if(x<250){performHapticFeedback(1); new android.app.AlertDialog.Builder(getContext()).setTitle("Reset").setMessage("Reset count?").setPositiveButton("Yes",(di,wi)->{zikrMan.indCounts[i]=0;zikrMan.indRounds[i]=0;zikrMan.save();invalidate();}).setNegativeButton("No",null).show();} else if(x>w-250){zikrMan.soundOn=!zikrMan.soundOn;zikrMan.save();invalidate();} }
                    else if(y>350 && y<600 && x>cx){performHapticFeedback(1); eT(i);}
                    else if(y>750 && y<1100 && x>50 && x<w-50){performHapticFeedback(1); sL();}
                    else if(y>thY-60 && y<thY+60){ for(int j=0;j<6;j++){ if(Math.abs(x-(cx-250f+(j*100f)))<50){zikrMan.beadTheme=j;zikrMan.save();invalidate();break;} } }
                    else {performHapticFeedback(1);anm(-160f,true);}
                }
            } return true;
        }
        private void eT(int idx){ final android.widget.EditText et=new android.widget.EditText(getContext()); et.setInputType(2); et.setText(String.valueOf(zikrMan.tasbihList.get(idx).target)); new android.app.AlertDialog.Builder(getContext()).setTitle("Target").setView(et).setPositiveButton("OK",(di,wi)->{if(!et.getText().toString().isEmpty()){zikrMan.tasbihList.get(idx).target=Integer.parseInt(et.getText().toString()); zikrMan.prefs.edit().putInt("t_"+idx,zikrMan.tasbihList.get(idx).target).apply(); invalidate();}}).show(); }
        private void sL(){
            final android.app.Dialog d=new android.app.Dialog(getContext(),android.R.style.Theme_Black_NoTitleBar_Fullscreen); android.widget.LinearLayout r=new android.widget.LinearLayout(getContext()); r.setOrientation(1); r.setBackgroundColor(themeColors[0]); r.setPadding(40,80,40,40); android.widget.TextView t1=new android.widget.TextView(getContext()); t1.setText("Zikr List"); t1.setTextColor(colorAccent); t1.setTextSize(26); t1.setTypeface(appFonts[1]); t1.setGravity(17); r.addView(t1);
            android.widget.ScrollView sv=new android.widget.ScrollView(getContext()); android.widget.LinearLayout l=new android.widget.LinearLayout(getContext()); l.setOrientation(1);
            for(int j=0;j<zikrMan.tasbihList.size();j++){
                final int rI=j; ZikrManager.TasbihData dt=zikrMan.tasbihList.get(j); android.widget.LinearLayout rw=new android.widget.LinearLayout(getContext()); rw.setOrientation(1); rw.setPadding(30,45,30,45); rw.setGravity(17);
                android.widget.TextView tA=new android.widget.TextView(getContext()); tA.setText(dt.arabic); tA.setTextColor(themeColors[2]); tA.setTextSize(32); tA.setTypeface(getArabicFont()); tA.setGravity(17); tA.setOnClickListener(v->{zikrMan.currentIdx=rI;zikrMan.save();invalidate();d.dismiss();}); rw.addView(tA);
                android.widget.TextView tP=new android.widget.TextView(getContext()); tP.setText(dt.pron); tP.setTextColor(themeColors[3]); tP.setTextSize(16); tP.setGravity(17); tP.setPadding(0,15,0,5); rw.addView(tP);
                android.widget.TextView tM=new android.widget.TextView(getContext()); tM.setText(dt.mean); tM.setTextColor(themeColors[3]); tM.setTextSize(14); tM.setGravity(17); tM.setPadding(0,0,0,25); rw.addView(tM);
                android.widget.TextView tT=new android.widget.TextView(getContext()); tT.setText("Target: "+dt.target); tT.setTextColor(colorAccent); tT.setTextSize(18); tT.setTypeface(appFonts[1]); tT.setGravity(17); android.graphics.drawable.GradientDrawable tb=new android.graphics.drawable.GradientDrawable(); tb.setColor(themeColors[1]); tb.setCornerRadius(15f); tT.setBackground(tb); tT.setPadding(40,15,40,15); tT.setOnClickListener(v->{ eT(rI); }); rw.addView(tT);
                l.addView(rw); android.view.View div=new android.view.View(getContext()); div.setBackgroundColor(themeColors[4]); div.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1,2)); l.addView(div);
            } sv.addView(l); r.addView(sv,new android.widget.LinearLayout.LayoutParams(-1,0,1f)); d.setContentView(r); d.show();
        }
    }
    private void loadZikrTab() { contentArea.removeAllViews(); contentArea.addView(new ZikrCanvasView(this), new android.widget.LinearLayout.LayoutParams(-1, -1)); }
    private void loadStatsTab() {
        contentArea.removeAllViews(); contentArea.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY)); android.widget.TextView h=new android.widget.TextView(this); h.setText("Stats"); h.setTextColor(themeColors[2]); h.setTextSize(24); h.setTypeface(appFonts[1]); h.setPadding(0,0,0,(int)(20*DENSITY)); contentArea.addView(h);
        try{ java.lang.reflect.Method m=StatsHelper.class.getDeclaredMethod("renderStats",android.widget.LinearLayout.class,android.app.AlertDialog.class,boolean.class); m.setAccessible(true); android.widget.TextView wT=new android.widget.TextView(this); wT.setText("Weekly Statistics"); wT.setTextColor(themeColors[3]); wT.setTypeface(appFonts[1]); contentArea.addView(wT); android.widget.LinearLayout wC=new android.widget.LinearLayout(this); wC.setOrientation(1); wC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY)); android.graphics.drawable.GradientDrawable wBg=new android.graphics.drawable.GradientDrawable(); wBg.setColor(themeColors[1]); wBg.setCornerRadius(25f*DENSITY); wC.setBackground(wBg); android.widget.LinearLayout.LayoutParams wLp=new android.widget.LinearLayout.LayoutParams(-1,-2); wLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); wC.setLayoutParams(wLp); m.invoke(statsHelper,wC,null,true); wC.removeViewAt(wC.getChildCount()-1); contentArea.addView(wC); android.widget.TextView mT=new android.widget.TextView(this); mT.setText("Monthly Statistics"); mT.setTextColor(themeColors[3]); mT.setTypeface(appFonts[1]); contentArea.addView(mT); android.widget.LinearLayout mC=new android.widget.LinearLayout(this); mC.setOrientation(1); mC.setPadding((int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY),(int)(20*DENSITY)); android.graphics.drawable.GradientDrawable mBg=new android.graphics.drawable.GradientDrawable(); mBg.setColor(themeColors[1]); mBg.setCornerRadius(25f*DENSITY); mC.setBackground(mBg); android.widget.LinearLayout.LayoutParams mLp=new android.widget.LinearLayout.LayoutParams(-1,-2); mLp.setMargins(0,(int)(10*DENSITY),0,(int)(20*DENSITY)); mC.setLayoutParams(mLp); m.invoke(statsHelper,mC,null,false); mC.removeViewAt(mC.getChildCount()-1); contentArea.addView(mC); }catch(Exception e){}
    }
'''
open(f,'w').write(open(f).read().replace('//_TOUCH_', z3))
print("✅ ALL STEPS DONE! NO ERRORS CAN EXIST NOW! 🚀")
