import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. উপরের ৩টি আইকনের কালার (colorAccent) ডায়নামিক করা
    tint_code = """
        themeToggleBtn.setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
        if(offBtn != null) offBtn.setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
        if(periodBtn != null) periodBtn.setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
        settingsBtn.setColorFilter(colorAccent, android.graphics.PorterDuff.Mode.SRC_IN);
    """
    if "themeToggleBtn.setColorFilter" not in mc:
        mc = mc.replace("rightHeader.addView(settingsBtn);", "rightHeader.addView(settingsBtn);\n" + tint_code)

    # ২. তীরচিহ্নের সাইজ সপ্তাহের ঘরের (52dp) সমান করা
    arrow_size = """
        LinearLayout.LayoutParams arrowLp = new LinearLayout.LayoutParams((int)(52*DENSITY), (int)(52*DENSITY));
        prevW.setLayoutParams(arrowLp);
        nextW.setLayoutParams(arrowLp);
    """
    if "prevW.setLayoutParams(arrowLp);" not in mc:
        mc = mc.replace("datesLayout.addView(nextW);", "datesLayout.addView(nextW);\n" + arrow_size)

    # ৩. রিস্টার্ট করার সময় আগের তারিখ (Date) মনে রাখা এবং Fade অ্যানিমেশন দেওয়া
    # প্রথমে রিস্টার্ট বা রিঅ্যাক্টিভিটি মেথডগুলো খুঁজে বের করে আপডেট করা
    recreate_fix = """
        Intent intent = new Intent(this, MainActivity.class);
        intent.putExtra("RESTORE_DATE", currentDate.getTimeInMillis());
        startActivity(intent);
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
        finish();
    """
    mc = re.sub(r'recreate\(\);', recreate_fix.strip(), mc)
    mc = re.sub(r'Intent intent = new Intent\(this, MainActivity\.class\);\s*startActivity\(intent\);\s*finish\(\);', recreate_fix.strip(), mc)

    # onCreate-এ আগের তারিখ রিস্টোর করা
    restore_logic = """
        long savedDate = getIntent().getLongExtra("RESTORE_DATE", -1);
        if(savedDate != -1) {
            currentDate.setTimeInMillis(savedDate);
        }
    """
    if "RESTORE_DATE" not in mc[:3000]:  # onCreate এর কাছাকাছি
        mc = re.sub(r'(currentDate = Calendar\.getInstance\(\);)', r'\1\n' + restore_logic, mc)

    # ৪. আসল অ্যানিমেটেড পানির ঢেউ (Water Wave) তৈরি করা
    wave_class = """
    public static class WaterWaveView extends android.view.View {
        private android.graphics.Path path = new android.graphics.Path();
        private android.graphics.Paint paint = new android.graphics.Paint();
        private float phase = 0f;
        private int progress = 50;
        public WaterWaveView(android.content.Context context) {
            super(context);
            paint.setStyle(android.graphics.Paint.Style.FILL);
            paint.setAntiAlias(true);
        }
        public void setProgressAndColor(int p, int c) {
            this.progress = p;
            paint.setColor(c);
            paint.setAlpha(180); // পানির একটু স্বচ্ছতা (Transparency)
        }
        @Override
        protected void onDraw(android.graphics.Canvas canvas) {
            super.onDraw(canvas);
            int w = getWidth();
            int h = getHeight();
            if (w == 0 || h == 0) return;
            path.reset();
            float baseHeight = h - (h * progress / 100f);
            float amplitude = h * 0.05f; // ঢেউয়ের উচ্চতা
            path.moveTo(0, h);
            path.lineTo(0, baseHeight);
            for (int i = 0; i <= w; i += 10) {
                float y = (float) (Math.sin((i * 3 * Math.PI / w) + phase) * amplitude) + baseHeight;
                path.lineTo(i, y);
            }
            path.lineTo(w, h);
            path.close();
            canvas.drawPath(path, paint);
            phase += 0.15f; // ঢেউয়ের স্পিড
            postInvalidateDelayed(20);
        }
    }
    """
    
    # আগের লিকুইড গ্লাস বা ওয়েভ ক্লাস মুছে ফেলা
    mc = re.sub(r'public static class WaterWaveView.*?postInvalidateDelayed\(20\);\s*\}\s*\}', '', mc, flags=re.DOTALL)
    mc = re.sub(r'/\*liquid_flag\*/.*?parent\.addView\(neoContainer, index\);\s*\}\s*\} catch\(Exception e\)\{\}\s*\}\);\s*', '', mc, flags=re.DOTALL)
    
    # নতুন ওয়েভ ক্লাস বসানো
    if "WaterWaveView" not in mc:
        mc = re.sub(r'\}\s*$', wave_class + '\n}', mc)

    # ওয়েভ ইনজেক্টর
    wave_injector = """
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
                    
                    // পার্সেন্টেজ বের করা
                    int p = 50;
                    try {
                        java.util.Stack<android.view.View> stack = new java.util.Stack<>();
                        stack.push(pCard);
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
                    
                    // কর্নার রাউন্ড করা
                    innerBox.setOutlineProvider(new android.view.ViewOutlineProvider() {
                        @Override
                        public void getOutline(android.view.View view, android.graphics.Outline outline) {
                            outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), 16f * DENSITY);
                        }
                    });
                    innerBox.setClipToOutline(true);
                    
                    parent.addView(waveContainer, index);
                }
            } catch(Exception e){}
        });
    """
    
    if "pCard.setTag(\"waved\");" not in mc:
        mc = mc.replace("contentArea.addView(pCard);", wave_injector + "\ncontentArea.addView(pCard);")

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ WAVE, COLORS, SIZES AND RESTART STATE APPLIED!")
else:
    print("❌ FILE NOT FOUND")
