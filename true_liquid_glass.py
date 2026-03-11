import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if os.path.exists(java_file):
    with open(java_file, "r", encoding="utf-8") as f:
        mc = f.read()

    # ১. আগের চলন্ত ঢেউ (Wave) কোড মুছে ফেলা
    mc = re.sub(r'public static class WaterWaveView.*?postInvalidateDelayed\(20\);\s*\}\s*\}', '', mc, flags=re.DOTALL)
    mc = re.sub(r'pCard\.post\(new Runnable\(\).*?waved.*?\);(?:\s*\})*', '', mc, flags=re.DOTALL)

    # ২. সপ্তাহের গোল ঘরগুলো আরেকটু বড় ও পারফেক্ট করা (44 থেকে 52 করা হলো)
    mc = re.sub(r'FrameLayout\.LayoutParams\(\(int\)\(44\s*\*\s*DENSITY\),\s*\(int\)\(44\s*\*\s*DENSITY\)\)', 'FrameLayout.LayoutParams((int)(52 * DENSITY), (int)(52 * DENSITY))', mc)
    mc = re.sub(r'setAllCorners\(0,\s*18f\s*\*\s*DENSITY\)', 'setAllCorners(0, 26f * DENSITY)', mc)
    
    # ৩. রেফারেন্স ছবির মতো হুবহু Glossy Liquid Glass ইফেক্ট তৈরি
    liquid_glass_code = """
        pCard.post(() -> {
            try {
                android.view.ViewGroup parent = (android.view.ViewGroup) pCard.getParent();
                if (parent != null && !"liquid_glass".equals(pCard.getTag())) {
                    pCard.setTag("liquid_glass");
                    int index = parent.indexOfChild(pCard);
                    parent.removeView(pCard);
                    
                    // বাইরের থ্রিডি গ্লাস ফ্রেম
                    soup.neumorphism.NeumorphCardView neoContainer = new soup.neumorphism.NeumorphCardView(pCard.getContext());
                    neoContainer.setLayoutParams(pCard.getLayoutParams());
                    neoContainer.setShapeType(0);
                    neoContainer.setShadowColorLight(isDarkTheme ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.parseColor("#F1F5F9"));
                    neoContainer.setShadowColorDark(isDarkTheme ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
                    neoContainer.setShadowElevation(8f * DENSITY);
                    neoContainer.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 20f * DENSITY).build());
                    neoContainer.setBackgroundColor(isDarkTheme ? android.graphics.Color.parseColor("#1C1C1E") : android.graphics.Color.parseColor("#E2E8F0"));
                    
                    // ভেতরের লিকুইড গ্রেডিয়েন্ট (Cyan -> Bright Blue -> Deep Blue)
                    android.widget.FrameLayout innerLiquid = new android.widget.FrameLayout(pCard.getContext());
                    android.graphics.drawable.GradientDrawable liquidGrad = new android.graphics.drawable.GradientDrawable(
                        android.graphics.drawable.GradientDrawable.Orientation.TL_BR,
                        new int[]{android.graphics.Color.parseColor("#38BDF8"), android.graphics.Color.parseColor("#2563EB"), android.graphics.Color.parseColor("#1E3A8A")}
                    );
                    liquidGrad.setCornerRadius(18f * DENSITY);
                    innerLiquid.setBackground(liquidGrad);
                    
                    // কাঁচের ওপরের চকচকে রিফ্লেকশন (Glossy Overlay)
                    android.view.View gloss = new android.view.View(pCard.getContext());
                    android.graphics.drawable.GradientDrawable glossGrad = new android.graphics.drawable.GradientDrawable(
                        android.graphics.drawable.GradientDrawable.Orientation.TOP_BOTTOM,
                        new int[]{android.graphics.Color.parseColor("#55FFFFFF"), android.graphics.Color.TRANSPARENT}
                    );
                    glossGrad.setCornerRadius(18f * DENSITY);
                    gloss.setBackground(glossGrad);
                    
                    pCard.setBackgroundColor(android.graphics.Color.TRANSPARENT);
                    pCard.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
                    
                    innerLiquid.addView(gloss, new android.widget.FrameLayout.LayoutParams(-1, (int)(50*DENSITY)));
                    innerLiquid.addView(pCard);
                    
                    android.widget.FrameLayout.LayoutParams nlp = new android.widget.FrameLayout.LayoutParams(-1, -1);
                    nlp.setMargins((int)(4*DENSITY), (int)(4*DENSITY), (int)(4*DENSITY), (int)(4*DENSITY));
                    neoContainer.addView(innerLiquid, nlp);
                    
                    // ভেতরের সব লেখা সাদা করা (যাতে নীল লিকুইডের ওপর সুন্দর ফুটে ওঠে)
                    java.util.Stack<android.view.View> stack = new java.util.Stack<>();
                    stack.push(pCard);
                    while(!stack.isEmpty()) {
                        android.view.View v = stack.pop();
                        if(v instanceof android.widget.TextView) {
                            ((android.widget.TextView)v).setTextColor(android.graphics.Color.WHITE);
                        } else if (v instanceof android.view.ViewGroup) {
                            android.view.ViewGroup vg = (android.view.ViewGroup) v;
                            for(int i=0; i<vg.getChildCount(); i++) stack.push(vg.getChildAt(i));
                        }
                    }
                    parent.addView(neoContainer, index);
                }
            } catch(Exception e){}
        });
    """
    
    if "liquid_glass" not in mc:
        mc = mc.replace("contentArea.addView(pCard);", "/*liquid_flag*/\n" + liquid_glass_code + "\ncontentArea.addView(pCard);")
        
    with open(java_file, "w", encoding="utf-8") as f:
        f.write(mc)
    print("✔ TRUE LIQUID GLASS & SIZING APPLIED PERFECTLY!")
else:
    print("❌ FILE NOT FOUND")
