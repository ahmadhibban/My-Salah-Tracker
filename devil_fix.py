import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    print("\n=== 🛠️ INJECTION REPORT ===")

    # ১. তীরচিহ্নের (Arrows) সাইজ ঠিক করা
    mc_new = re.sub(r'(prevW\.setLayoutParams\(.*?LayoutParams\()\s*\([^)]+\)\s*,\s*\([^)]+\)\s*(\)\);)', r'\1(int)(52*DENSITY), (int)(52*DENSITY)\2', mc)
    mc_new = re.sub(r'(nextW\.setLayoutParams\(.*?LayoutParams\()\s*\([^)]+\)\s*,\s*\([^)]+\)\s*(\)\);)', r'\1(int)(52*DENSITY), (int)(52*DENSITY)\2', mc_new)
    if mc_new != mc:
        mc = mc_new
        print("✔ 1. Arrows Resized (52dp) - SUCCESS")
    else:
        print("❌ 1. Arrows Resized - FAILED")

    # ২. উপরের আইকনগুলোর (Settings, Theme) কালার সবুজ/নীল করা
    icon_color = """
        try {
            if(themeToggleBtn instanceof android.widget.TextView) ((android.widget.TextView)themeToggleBtn).setTextColor(colorAccent);
            else if (themeToggleBtn != null && themeToggleBtn.getBackground() != null) themeToggleBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
            if(settingsBtn instanceof android.widget.TextView) ((android.widget.TextView)settingsBtn).setTextColor(colorAccent);
            else if (settingsBtn != null && settingsBtn.getBackground() != null) settingsBtn.getBackground().setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
        } catch(Exception e){}
    """
    if "themeToggleBtn instanceof" not in mc:
        # settingsBtn-এ ক্লিক লিসেনার বসানোর ঠিক আগে কালার ইনজেক্ট করা হচ্ছে
        mc_new = re.sub(r'(settingsBtn\.setOnClickListener)', icon_color + r'\n        \1', mc)
        if mc_new != mc:
            mc = mc_new
            print("✔ 2. Icon Colors Applied - SUCCESS")
        else:
            print("❌ 2. Icon Colors Applied - FAILED")
    else:
        print("✔ 2. Icon Colors Applied - ALREADY EXISTS")

    # ৩. রিস্টার্ট করলে আগের তারিখে থাকার ফিক্স
    if "RESTORE_DATE" not in mc:
        mc_new = re.sub(r'(currentDate\s*=\s*Calendar\.getInstance\(\);)', r'\1\n        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1L); if(savedDate != -1L) currentDate.setTimeInMillis(savedDate);', mc)
        mc_new = re.sub(r'recreate\(\);', 'Intent intent = new Intent(this, MainActivity.class); intent.putExtra("RESTORE_DATE", currentDate.getTimeInMillis()); startActivity(intent); overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out); finish();', mc_new)
        if mc_new != mc:
            mc = mc_new
            print("✔ 3. Restart State Fix - SUCCESS")
        else:
            print("❌ 3. Restart State Fix - FAILED")
    else:
        print("✔ 3. Restart State Fix - ALREADY EXISTS")

    # ৪. পানির ঢেউ (Water Wave) ক্লাস ও লজিক ইনজেক্ট করা
    wave_class = """
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
    """
    if "class WaterWaveView" not in mc:
        mc = re.sub(r'\}\s*$', wave_class + '\n}', mc)

    wave_logic = """
        // WAVE ANIMATION INJECTOR
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
    """
    if "WAVE ANIMATION INJECTOR" not in mc:
        # pCard কন্টেন্ট এরিয়াতে অ্যাড হওয়ার ঠিক পরেই ঢেউয়ের লজিক বসানো হচ্ছে
        mc_new = re.sub(r'(contentArea\.addView\(\s*pCard\s*\)\s*;)', r'\1\n' + wave_logic, mc)
        if mc_new != mc:
            mc = mc_new
            print("✔ 4. Water Wave Applied - SUCCESS")
        else:
            print("❌ 4. Water Wave Applied - FAILED")
    else:
        print("✔ 4. Water Wave Applied - ALREADY EXISTS")

    print("===============================\n")

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
else:
    print("❌ FILE NOT FOUND")
