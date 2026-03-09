import re
ma = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c = open(ma).read()

# Refactor onCreate Layout
old_layout = '''android.widget.ScrollView scrollView = new android.widget.ScrollView(this); scrollView.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1)); scrollView.setFillViewport(true); scrollView.setOverScrollMode(android.view.View.OVER_SCROLL_NEVER);
        contentArea = new android.widget.LinearLayout(this); contentArea.setOrientation(android.widget.LinearLayout.VERTICAL); scrollView.addView(contentArea, new android.widget.FrameLayout.LayoutParams(-1, -1)); root.addView(scrollView);
        setContentView(root);'''

new_layout = '''android.widget.LinearLayout mainRoot = new android.widget.LinearLayout(this); mainRoot.setOrientation(android.widget.LinearLayout.VERTICAL); mainRoot.setLayoutParams(new android.widget.FrameLayout.LayoutParams(-1, -1));
        fragmentContainer = new android.widget.FrameLayout(this); fragmentContainer.setLayoutParams(new android.widget.LinearLayout.LayoutParams(-1, 0, 1f));
        bottomNav = new android.widget.LinearLayout(this); bottomNav.setOrientation(android.widget.LinearLayout.HORIZONTAL); bottomNav.setGravity(android.view.Gravity.CENTER);
        android.graphics.drawable.GradientDrawable navBg = new android.graphics.drawable.GradientDrawable(); navBg.setColor(themeColors[1]); navBg.setCornerRadii(new float[]{40f*DENSITY,40f*DENSITY, 40f*DENSITY,40f*DENSITY, 0,0,0,0});
        if(android.os.Build.VERSION.SDK_INT >= 21) bottomNav.setElevation(30f); bottomNav.setBackground(navBg);
        mainRoot.addView(fragmentContainer); mainRoot.addView(bottomNav); root.addView(mainRoot); setContentView(root);'''

if 'mainRoot = new' not in c: c = c.replace(old_layout, new_layout)

# Replace direct loadTodayPage calls in onCreate
c = c.replace('loadTodayPage();\n        refreshWidget();\n        setupMidnightRefresh();', 'setupBottomNav(); switchTab(0);\n        refreshWidget();\n        setupMidnightRefresh();')

open(ma, 'w').write(c)
print("✅ Part 2 Done! Base Architecture built.")
