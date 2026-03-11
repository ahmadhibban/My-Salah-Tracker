import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ FILE NOT FOUND! Check your path.")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

changes = 0

# ১. তীরচিহ্ন (Arrows) পারফেক্ট সাইজ করা (52dp)
mc, count1 = re.subn(r'prevW\.setLayoutParams\([^;]+;', 'prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(52 * DENSITY), (int)(52 * DENSITY)));', mc)
mc, count2 = re.subn(r'nextW\.setLayoutParams\([^;]+;', 'nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(52 * DENSITY), (int)(52 * DENSITY)));', mc)
if count1 > 0 or count2 > 0:
    print("✔ Arrows Resized to 52dp.")
    changes += 1

# ২. আইকনের কালার ফিক্স (সবুজ/নীল করা)
tint_logic = """
        // Icons Color Injector
        getWindow().getDecorView().post(() -> {
            try {
                if(themeToggleBtn instanceof android.widget.TextView) ((android.widget.TextView)themeToggleBtn).setTextColor(colorAccent);
                else if (themeToggleBtn != null && themeToggleBtn.getBackground() != null) themeToggleBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
                if(settingsBtn instanceof android.widget.TextView) ((android.widget.TextView)settingsBtn).setTextColor(colorAccent);
                else if (settingsBtn != null && settingsBtn.getBackground() != null) settingsBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
            } catch(Exception e){}
        });
"""
if "Icons Color Injector" not in mc:
    mc, count = re.subn(r'(setContentView\([^)]+\);)', r'\1\n' + tint_logic, mc, count=1)
    if count > 0:
        print("✔ Icon Colors Injected.")
        changes += 1

# ৩. পানির ঢেউ (Water Wave) ক্লাস অ্যাড করা
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
    print("✔ Wave Engine Added.")
    changes += 1

# ৪. ঢেউয়ের অ্যানিমেশন পার্সেন্টেজ কার্ডে বসানো
wave_wrap = """
        // Wave Animation Injector
        if (pCard != null) {
            pCard.post(() -> {
                try {
                    android.view.ViewGroup parent = (android.view.ViewGroup) pCard.getParent();
                    if (parent != null && !"waved".equals(pCard.getTag())) {
                        pCard.setTag("waved");
                        int index = parent.indexOfChild(pCard);
                        parent.removeView(pCard);
                        soup.neumorphism.NeumorphCardView waveContainer = new soup.neumorphism.NeumorphCardView(pCard.getContext());
                        waveContainer.setLayoutParams(pCard.getLayoutParams());
                        waveContainer.setShapeType(0);
                        waveContainer.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
                        waveContainer.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
                        waveContainer.setShadowElevation(6f * DENSITY);
                        waveContainer.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 20f * DENSITY).build());
                        waveContainer.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
                        android.widget.FrameLayout innerBox = new android.widget.FrameLayout(pCard.getContext());
                        WaterWaveView wave = new WaterWaveView(pCard.getContext());
                        int p = 50;
                        try {
                            java.util.Stack<android.view.View> stack = new java.util.Stack<>(); stack.push(pCard);
                            while(!stack.isEmpty()) {
                                android.view.View v = stack.pop();
                                if(v instanceof android.widget.TextView) {
                                    String txt = ((android.widget.TextView)v).getText().toString();
                                    if(txt.contains("%")) p = Integer.parseInt(txt.replaceAll("[^0-9]", ""));
                                } else if (v instanceof android.view.ViewGroup) {
                                    android.view.ViewGroup vg = (android.view.ViewGroup) v;
                                    for(int i=0; i<vg.getChildCount(); i++) stack.push(vg.getChildAt(i));
                                }
                            }
                        } catch(Exception e){}
                        wave.setProgressAndColor(p, colorAccent);
                        innerBox.addView(wave, new android.widget.FrameLayout.LayoutParams(-1, -1));
                        pCard.setBackgroundColor(android.graphics.Color.TRANSPARENT);
                        pCard.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                        innerBox.addView(pCard);
                        android.widget.FrameLayout.LayoutParams nlp = new android.widget.FrameLayout.LayoutParams(-1, -1);
                        nlp.setMargins((int)(4*DENSITY), (int)(4*DENSITY), (int)(4*DENSITY), (int)(4*DENSITY));
                        waveContainer.addView(innerBox, nlp);
                        innerBox.setOutlineProvider(new android.view.ViewOutlineProvider() {
                            @Override public void getOutline(android.view.View view, android.graphics.Outline outline) { outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), 16f * DENSITY); }
                        });
                        innerBox.setClipToOutline(true);
                        parent.addView(waveContainer, index);
                    }
                } catch(Exception e){}
            });
        }
"""
if "Wave Animation Injector" not in mc:
    mc, count = re.subn(r'(setContentView\([^)]+\);)', r'\1\n' + wave_wrap, mc, count=1)
    if count > 0:
        print("✔ Wave UI Applied to Card.")
        changes += 1

# ৫. রিস্টার্ট করলে আগের তারিখে থাকার ফিক্স
if "RESTORE_DATE" not in mc:
    mc, count1 = re.subn(r'(currentDate\s*=\s*Calendar\.getInstance\(\);)', r'\1\n        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1);\n        if(savedDate != -1) currentDate.setTimeInMillis(savedDate);', mc)
    mc, count2 = re.subn(r'recreate\(\);', 'Intent intent = new Intent(MainActivity.this, MainActivity.class); intent.putExtra("RESTORE_DATE", currentDate.getTimeInMillis()); startActivity(intent); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out); finish();', mc)
    if count1 > 0 or count2 > 0:
        print("✔ Restart State Logic Injected.")
        changes += 1

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

if changes > 0:
    print(f"🚀 {changes} CHANGES INJECTED FORCEFULLY! READY TO BUILD.")
else:
    print("⚠️ WARNING: Nothing was changed. The code might already be applied.")
