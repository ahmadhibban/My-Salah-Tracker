import re
with open("app/src/main/java/com/my/salah/tracker/app/MainActivity.java", "r", encoding="utf-8") as f: mc = f.read()

safe_color_fix = """
        getWindow().getDecorView().post(() -> {
            try {
                if (!isDarkTheme) {
                    int darkColor = android.graphics.Color.parseColor("#1C1C1E");
                    java.util.Stack<android.view.View> stack = new java.util.Stack<>();
                    stack.push(getWindow().getDecorView());
                    while(!stack.isEmpty()) {
                        android.view.View v = stack.pop();
                        if(v instanceof soup.neumorphism.NeumorphCardView) {
                            soup.neumorphism.NeumorphCardView neo = (soup.neumorphism.NeumorphCardView) v;
                            boolean isTarget = neo.getShapeType() == 1 || (neo.getLayoutParams() != null && neo.getLayoutParams().width == (int)(44 * DENSITY));
                            if(isTarget) {
                                java.util.Stack<android.view.View> innerStack = new java.util.Stack<>();
                                innerStack.push(neo);
                                while(!innerStack.isEmpty()) {
                                    android.view.View iv = innerStack.pop();
                                    if(iv instanceof android.widget.TextView) {
                                        String t = ((android.widget.TextView)iv).getText().toString();
                                        if(!t.contains("%")) ((android.widget.TextView)iv).setTextColor(darkColor);
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
                }
            } catch(Exception e){}
        });
"""
if "darkColor" not in mc:
    mc = re.sub(r'(setContentView\([^)]+\);)', r'\1\n' + safe_color_fix, mc)

with open("app/src/main/java/com/my/salah/tracker/app/MainActivity.java", "w", encoding="utf-8") as f: f.write(mc)
print("✅ ৩. লাইট মোডের টেক্সট কালার ঠিক করা হয়েছে!")
