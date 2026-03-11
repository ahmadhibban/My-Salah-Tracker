import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

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
            path.reset(); float baseHeight = h - (h * progress / 100f); float amplitude = h * 0.04f;
            path.moveTo(0, h); path.lineTo(0, baseHeight);
            for (int i = 0; i <= w; i += 10) { float y = (float) (Math.sin((i * 3 * Math.PI / w) + phase) * amplitude) + baseHeight; path.lineTo(i, y); }
            path.lineTo(w, h); path.close(); canvas.drawPath(path, paint);
            phase += 0.15f; postInvalidateDelayed(20);
        }
    }
"""
if "class WaterWaveView" not in mc:
    mc = re.sub(r'\}\s*$', wave_class + '\n}', mc)

wave_inject = """
        pCard.addView(left); pCard.addView(artDisplay);
        android.widget.FrameLayout innerBox = new android.widget.FrameLayout(this);
        WaterWaveView wave = new WaterWaveView(this);
        wave.setProgressAndColor(countCompleted * 100 / 6, colorAccent);
        innerBox.addView(wave, new android.widget.FrameLayout.LayoutParams(-1, -1));
        innerBox.addView(pCard, new android.widget.FrameLayout.LayoutParams(-1, -2));
        innerBox.setOutlineProvider(new android.view.ViewOutlineProvider() {
            @Override public void getOutline(android.view.View view, android.graphics.Outline outline) { outline.setRoundRect(0, 0, view.getWidth(), view.getHeight(), 16f * DENSITY); }
        });
        innerBox.setClipToOutline(true);
        android.widget.LinearLayout.LayoutParams nlp = new android.widget.LinearLayout.LayoutParams(-1, -2);
        nlp.setMargins((int)(4*DENSITY), (int)(4*DENSITY), (int)(4*DENSITY), (int)(4*DENSITY));
        innerBox.setLayoutParams(nlp);
        pNeo.removeAllViews(); pNeo.addView(innerBox); contentArea.addView(pNeo);
"""
if "WaterWaveView wave = new WaterWaveView" not in mc:
    mc = mc.replace("pCard.addView(left); pCard.addView(artDisplay); contentArea.addView(pNeo);", wave_inject.strip())

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ৫. Water Wave Injected to Percentage Card!")
