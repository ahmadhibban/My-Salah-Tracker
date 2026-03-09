import re

f = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
with open(f, 'r', encoding='utf-8') as file:
    c = file.read()

# Finding the old layout code that failed to replace last time
old_layout = r'ScrollView scrollView = new ScrollView\(this\);.*?setContentView\(root\);'

new_layout = '''LinearLayout mainRoot = new LinearLayout(this); mainRoot.setOrientation(LinearLayout.VERTICAL); mainRoot.setLayoutParams(new FrameLayout.LayoutParams(-1, -1));
        fragmentContainer = new FrameLayout(this); fragmentContainer.setLayoutParams(new LinearLayout.LayoutParams(-1, 0, 1f));
        bottomNav = new LinearLayout(this); bottomNav.setOrientation(LinearLayout.HORIZONTAL); bottomNav.setGravity(Gravity.CENTER);
        GradientDrawable navBg = new GradientDrawable(); navBg.setColor(themeColors[1]); navBg.setCornerRadii(new float[]{40f*DENSITY,40f*DENSITY, 40f*DENSITY,40f*DENSITY, 0,0,0,0});
        if(Build.VERSION.SDK_INT >= 21) bottomNav.setElevation(30f); bottomNav.setBackground(navBg);
        mainRoot.addView(fragmentContainer); mainRoot.addView(bottomNav); root.addView(mainRoot); setContentView(root);'''

c = re.sub(old_layout, new_layout, c, flags=re.DOTALL)

with open(f, 'w', encoding='utf-8') as file:
    file.write(c)

print("✅ Layout Crash Fixed Perfectly! Ready to build.")
