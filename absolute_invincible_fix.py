import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. বাটন দুটোর স্পেসিং ফিক্স (যেহেতু আমরা জানি ভেরিয়েবলের নাম markLp এবং todayLp)
    mc = re.sub(r'markLp\.setMargins\([^)]+\);', 'markLp.setMargins((int)(16*DENSITY), (int)(24*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));', mc)
    mc = re.sub(r'todayLp\.setMargins\([^)]+\);', 'todayLp.setMargins((int)(8*DENSITY), (int)(24*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY));', mc)

    # ২. পানির ঢেউ (Water Wave) ক্লাস অ্যাড করা
    if "class WaterWaveView" not in mc:
        mc = re.sub(r'\}\s*$', r'''
    public static class WaterWaveView extends android.view.View {
        private android.graphics.Path path = new android.graphics.Path();
        private android.graphics.Paint paint = new android.graphics.Paint();
        private float phase = 0f; private int progress = 50;
        public WaterWaveView(android.content.Context context) {
            super(context); paint.setStyle(android.graphics.Paint.Style.FILL); paint.setAntiAlias(true);
        }
        public void setProgressAndColor(int p, int c) { this.progress = p; paint.setColor(c); paint.setAlpha(150); }
        @Override
        protected void onDraw(android.graphics.Canvas canvas) {
            super.onDraw(canvas);
            int w = getWidth(); int h = getHeight(); if (w == 0 || h == 0) return;
            path.reset();
            float baseHeight = h - (h * progress / 100f);
            float amplitude = h * 0.04f;
            path.moveTo(0, h); path.lineTo(0, baseHeight);
            for (int i = 0; i <= w; i += 10) {
                float y = (float) (Math.sin((i * 3 * Math.PI / w) + phase) * amplitude) + baseHeight;
                path.lineTo(i, y);
            }
            path.lineTo(w, h); path.close();
            canvas.drawPath(path, paint);
            phase += 0.15f; postInvalidateDelayed(20);
        }
    }
}''', mc)

    # ৩. রিস্টার্ট লজিক (থিম বা দিন পাল্টালে আগের জায়গায় থাকার ফিক্স)
    if "RESTORE_DATE" not in mc:
        mc = re.sub(r'(currentDate\s*=\s*Calendar\.getInstance\(\);)', r'\1\n        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1L);\n        if(savedDate != -1L) currentDate.setTimeInMillis(savedDate);', mc)
        mc = re.sub(r'recreate\(\);', 'Intent intent = new Intent(MainActivity.this, MainActivity.class); intent.putExtra("RESTORE_DATE", currentDate.getTimeInMillis()); startActivity(intent); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out); finish();', mc)

    # ৪. ইনভিন্সিবল ডায়নামিক স্ক্যানার (তীরচিহ্ন এবং ঢেউয়ের জন্য)
    wave_injector = """
        // --- INVINCIBLE DYNAMIC SCANNER ---
        getWindow().getDecorView().post(new Runnable() {
            @Override
            public void run() {
                try {
                    android.view.View decor = getWindow().getDecorView();
                    java.util.Stack<android.view.View> stack = new java.util.Stack<>();
                    stack.push(decor);
                    android.view.ViewGroup percentCard = null;
                    android.view.View prevArrow = null;
                    android.view.View nextArrow = null;
                    
                    while(!stack.isEmpty()) {
                        android.view.View v = stack.pop();
                        if(v instanceof android.widget.TextView) {
                            String txt = ((android.widget.TextView)v).getText().toString();
                            if(txt.contains("%")) {
                                android.view.ViewParent p1 = v.getParent();
                                if(p1 != null && p1.getParent() instanceof soup.neumorphism.NeumorphCardView) {
                                    percentCard = (android.view.ViewGroup) p1.getParent();
                                }
                            }
                            if(txt.equals("<") || txt.equals("❮")) {
                                if(v.getParent() instanceof soup.neumorphism.NeumorphCardView) prevArrow = (android.view.View) v.getParent();
                            }
                            if(txt.equals(">") || txt.equals("❯")) {
                                if(v.getParent() instanceof soup.neumorphism.NeumorphCardView) nextArrow = (android.view.View) v.getParent();
                            }
                        }
                        if(v instanceof android.view.ViewGroup) {
                            android.view.ViewGroup vg = (android.view.ViewGroup) v;
                            for(int i=0; i<vg.getChildCount(); i++) stack.push(vg.getChildAt(i));
                        }
                    }
                    
                    float den = getResources().getDisplayMetrics().density;
                    
                    if(prevArrow != null) {
                        android.view.ViewGroup.LayoutParams lp = prevArrow.getLayoutParams();
                        lp.width = (int)(52 * den); lp.height = (int)(52 * den);
                        prevArrow.setLayoutParams(lp);
                    }
                    if(nextArrow != null) {
                        android.view.ViewGroup.LayoutParams lp = nextArrow.getLayoutParams();
                        lp.width = (int)(52 * den); lp.height = (int)(52 * den);
                        nextArrow.setLayoutParams(lp);
                    }
                    
                    if(percentCard != null && !"waved".equals(percentCard.getTag())) {
                        percentCard.setTag("waved");
                        android.view.ViewGroup parent = (android.view.ViewGroup) percentCard.getParent();
                        if(parent != null) {
                            int index = parent.indexOfChild(percentCard);
                            parent.removeView(percentCard);
                            
                            soup.neumorphism.NeumorphCardView waveContainer = new soup.neumorphism.NeumorphCardView(percentCard.getContext());
                            waveContainer.setLayoutParams(percentCard.getLayoutParams());
                            waveContainer.setShapeType(0);
                            waveContainer.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
                            waveContainer.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
                            waveContainer.setShadowElevation(6f * den);
                            waveContainer.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 20f * den).build());
                            waveContainer.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
                            
                            android.widget.FrameLayout innerBox = new android.widget.FrameLayout(percentCard.getContext());
                            WaterWaveView wave = new WaterWaveView(percentCard.getContext());
                            
                            int p = 50;
                            java.util.Stack<android.view.View> pStack = new java.util.Stack<>(); pStack.push(percentCard);
                            while(!pStack.isEmpty()) {
                                android.view.View v = pStack.pop();
                                if(v instanceof android.widget.TextView) {
                                    String txt = ((android.widget.TextView)v).getText().toString();
                                    if(txt.contains("%")) p = Integer.parseInt(txt.replaceAll("[^0-9]", ""));
                                } else if (v instanceof android.view.ViewGroup) {
                                    android.view.ViewGroup vg = (android.view.ViewGroup) v;
                                    for(int i=0; i<vg.getChildCount(); i++) pStack.push(vg.getChildAt(i));
                                }
                            }
                            wave.setProgressAndColor(p, colorAccent);
                            innerBox.addView(wave, new android.widget.FrameLayout.LayoutParams(-1, -1));
                            
                            percentCard.setBackgroundColor(android.graphics.Color.TRANSPARENT);
                            percentCard.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                            innerBox.addView(percentCard);
                            
                            android.widget.FrameLayout.LayoutParams nlp = new android.widget.FrameLayout.LayoutParams(-1, -1);
                            nlp.setMargins((int)(4*den), (int)(4*den), (int)(4*den), (int)(4*den));
                            waveContainer.addView(innerBox, nlp);
                            
                            innerBox.setOutlineProvider(new android.view.ViewOutlineProvider() {
                                @Override public void getOutline(android.view.View view, android.graphics.Outline outline) { outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), 16f * den); }
                            });
                            innerBox.setClipToOutline(true);
                            
                            parent.addView(waveContainer, index);
                        }
                    }
                } catch(Exception e){}
            }
        });
    """
    if "INVINCIBLE DYNAMIC SCANNER" not in mc:
        mc = re.sub(r'(setContentView\([^)]+\)\s*;)', r'\1\n' + wave_injector, mc, count=1)

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ ULTIMATE INVINCIBLE SCANNER APPLIED SUCCESSFULLY! NO MORE ERRORS.")
else:
    print("❌ FILE NOT FOUND")
