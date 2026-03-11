import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. পিওর জাভায় WaterWaveView ক্লাস তৈরি করা (কোনো লাইব্রেরি ছাড়া)
    wave_class = """
    public static class WaterWaveView extends android.view.View {
        private android.graphics.Path path = new android.graphics.Path();
        private android.graphics.Paint paint = new android.graphics.Paint();
        private float phase = 0f;
        private int progress = 0;
        public WaterWaveView(android.content.Context context) {
            super(context);
            paint.setStyle(android.graphics.Paint.Style.FILL);
            paint.setAntiAlias(true);
        }
        public void setProgressAndColor(int p, int c) {
            this.progress = p;
            paint.setColor(c);
            invalidate();
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
            postInvalidateDelayed(20); // স্মুথ অ্যানিমেশনের জন্য
        }
    }
    """
    if "WaterWaveView" not in mc:
        mc = re.sub(r'\}\s*$', wave_class + '\n}', mc)

    # ২. রানটাইমে পার্সেন্টেজ কার্ডের ভেতরে এই ঢেউটা ঢুকিয়ে দেওয়া
    wave_injector = """
        pCard.post(new Runnable() {
            @Override
            public void run() {
                try {
                    android.view.ViewGroup parent = (android.view.ViewGroup) pCard.getParent();
                    if (parent != null && pCard.getTag() == null) {
                        pCard.setTag("waved");
                        int index = parent.indexOfChild(pCard);
                        parent.removeView(pCard);
                        
                        android.widget.FrameLayout wrapper = new android.widget.FrameLayout(pCard.getContext());
                        wrapper.setLayoutParams(pCard.getLayoutParams());
                        
                        // ব্যাকগ্রাউন্ডের খালি কার্ড
                        applyNeo(wrapper, 0, 20f, 6f, isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"), isDarkTheme);
                        
                        // পানির ঢেউ যুক্ত করা
                        WaterWaveView wave = new WaterWaveView(pCard.getContext());
                        int p = 50;
                        try {
                            if(pCard instanceof android.view.ViewGroup) {
                                android.view.ViewGroup vg = (android.view.ViewGroup) pCard;
                                for(int i=0; i<vg.getChildCount(); i++) {
                                    if(vg.getChildAt(i) instanceof android.view.ViewGroup) {
                                        android.view.ViewGroup inner = (android.view.ViewGroup) vg.getChildAt(i);
                                        for(int j=0; j<inner.getChildCount(); j++) {
                                            if(inner.getChildAt(j) instanceof android.widget.TextView) {
                                                String txt = ((android.widget.TextView)inner.getChildAt(j)).getText().toString();
                                                if(txt.contains("%")) {
                                                    p = Integer.parseInt(txt.replaceAll("[^0-9]", ""));
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        } catch(Exception e){}
                        wave.setProgressAndColor(p, colorAccent);
                        
                        // কার্ডের শেপ অনুযায়ী ঢেউ কাটা
                        wave.setOutlineProvider(new android.view.ViewOutlineProvider() {
                            @Override
                            public void getOutline(android.view.View view, android.graphics.Outline outline) {
                                outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), 20f * DENSITY);
                            }
                        });
                        wave.setClipToOutline(true);
                        
                        wrapper.addView(wave, new android.widget.FrameLayout.LayoutParams(-1, -1));
                        
                        // অরিজিনাল টেক্সটগুলো ঢেউয়ের ওপরে ভাসিয়ে দেওয়া
                        pCard.setBackgroundColor(android.graphics.Color.TRANSPARENT);
                        pCard.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                        wrapper.addView(pCard);
                        
                        parent.addView(wrapper, index);
                    }
                } catch(Exception e){}
            }
        });
    """
    
    if "pCard.setTag(\"waved\");" not in mc:
        mc = re.sub(r'(applyNeo\s*\(\s*pCard\s*,\s*[^;]+;)', r'\1\n' + wave_injector, mc)

    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ LIQUID MAGIC APPLIED!")
else:
    print("❌ FILE NOT FOUND")
