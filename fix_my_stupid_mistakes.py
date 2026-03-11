import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. বাটন দুটোর মার্জিন ফিক্স (নিচে ১৬ ডিপি ফাঁকা দেওয়া হলো এবং ওপরের বিশাল ফাঁকা কমানো হলো)
mc = re.sub(r'markLp\.setMargins\([^)]+\);', 'markLp.setMargins((int)(16*DENSITY), (int)(12*DENSITY), (int)(8*DENSITY), (int)(16*DENSITY));', mc)
mc = re.sub(r'todayLp\.setMargins\([^)]+\);', 'todayLp.setMargins((int)(8*DENSITY), (int)(12*DENSITY), (int)(16*DENSITY), (int)(16*DENSITY));', mc)

# ২. তীরচিহ্নগুলোকে একদম নিখুঁত গোল এবং সপ্তাহের ঘরের সমান (৪৪ ডিপি) করা হলো
arr_prev = 'prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY))); prevW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 22f*DENSITY).build());'
arr_next = 'nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(44*DENSITY), (int)(44*DENSITY))); nextW.setShapeAppearanceModel(new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, 22f*DENSITY).build());'
mc = re.sub(r'prevW\.setLayoutParams\([^)]+\);', arr_prev, mc)
mc = re.sub(r'nextW\.setLayoutParams\([^)]+\);', arr_next, mc)

# ৩. লাইট মোডে সাদা হয়ে যাওয়া লেখাগুলোকে আবার ডার্ক/কালো করা হলো (যাতে স্পষ্ট ফুটে ওঠে)
text_fix = """
        getWindow().getDecorView().post(() -> {
            try {
                int correctTextColor = isDarkTheme ? android.graphics.Color.parseColor("#F1F5F9") : android.graphics.Color.parseColor("#1C1C1E");
                java.util.Stack<android.view.View> stack = new java.util.Stack<>();
                stack.push(getWindow().getDecorView());
                while(!stack.isEmpty()) {
                    android.view.View v = stack.pop();
                    if(v instanceof soup.neumorphism.NeumorphCardView) {
                        soup.neumorphism.NeumorphCardView neo = (soup.neumorphism.NeumorphCardView) v;
                        // যদি কার্ডটি ডেবে থাকে (Sunken) অথবা তীরচিহ্ন হয়, তবে তার ভেতরের লেখার রঙ ঠিক করো
                        if(neo.getShapeType() == 1 || neo == prevW || neo == nextW) { 
                            java.util.Stack<android.view.View> innerStack = new java.util.Stack<>();
                            innerStack.push(neo);
                            while(!innerStack.isEmpty()) {
                                android.view.View iv = innerStack.pop();
                                if(iv instanceof android.widget.TextView) {
                                    String t = ((android.widget.TextView)iv).getText().toString();
                                    if(!t.contains("%")) ((android.widget.TextView)iv).setTextColor(correctTextColor);
                                } else if (iv instanceof android.view.ViewGroup) {
                                    for(int i=0; i<((android.view.ViewGroup)iv).getChildCount(); i++) innerStack.push(((android.view.ViewGroup)iv).getChildAt(i));
                                }
                            }
                        }
                    }
                    if(v instanceof android.view.ViewGroup) {
                        for(int i=0; i<((android.view.ViewGroup)v).getChildCount(); i++) stack.push(((android.view.ViewGroup)v).getChildAt(i));
                    }
                }
            } catch(Exception e){}
        });
"""
if "correctTextColor" not in mc:
    mc = re.sub(r'(setContentView\([^)]+\);)', r'\1\n' + text_fix, mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ৩টি মারাত্মক ভুল ঠিক করা হয়েছে! আর কোনো ঘাড় তেরামি নেই।")
