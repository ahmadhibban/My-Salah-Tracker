import os

file_path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Change Activity to FragmentActivity to support Fragments
code = code.replace("public class MainActivity extends Activity {", "public class MainActivity extends androidx.fragment.app.FragmentActivity {")

nav_code = """
        // --- HYBRID FRAGMENT CONTAINER & BOTTOM NAV (PROGRAMMATIC) ---
        final FrameLayout fragContainer = new FrameLayout(this);
        fragContainer.setId(888888); // Unique ID for fragments
        FrameLayout.LayoutParams fLp = new FrameLayout.LayoutParams(-1, -1);
        fLp.bottomMargin = (int)(56 * DENSITY);
        fragContainer.setLayoutParams(fLp);
        fragContainer.setVisibility(View.GONE);
        root.addView(fragContainer);

        com.google.android.material.bottomnavigation.BottomNavigationView bNav = new com.google.android.material.bottomnavigation.BottomNavigationView(this);
        FrameLayout.LayoutParams nLp = new FrameLayout.LayoutParams(-1, -2);
        nLp.gravity = Gravity.BOTTOM;
        bNav.setLayoutParams(nLp);
        bNav.setBackgroundColor(themeColors[1]);
        
        android.content.res.ColorStateList iconColorStates = new android.content.res.ColorStateList(
            new int[][]{
                new int[]{-android.R.attr.state_checked},
                new int[]{android.R.attr.state_checked}
            },
            new int[]{ themeColors[3], colorAccent }
        );
        bNav.setItemIconTintList(iconColorStates);
        bNav.setItemTextColor(iconColorStates);

        try {
            bNav.inflateMenu(getResources().getIdentifier("bottom_nav_menu", "menu", getPackageName()));
        } catch(Exception e) {}
        
        FrameLayout.LayoutParams sLp = new FrameLayout.LayoutParams(-1, -1);
        sLp.bottomMargin = (int)(56 * DENSITY);
        scrollView.setLayoutParams(sLp);
        root.addView(bNav);
        
        bNav.setOnNavigationItemSelectedListener(new com.google.android.material.bottomnavigation.BottomNavigationView.OnNavigationItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(android.view.MenuItem item) {
                String title = item.getTitle().toString();
                if(title.equals("Salah")) {
                    fragContainer.setVisibility(View.GONE);
                    scrollView.setVisibility(View.VISIBLE);
                } else {
                    scrollView.setVisibility(View.GONE);
                    fragContainer.setVisibility(View.VISIBLE);
                    androidx.fragment.app.Fragment frag = null;
                    if(title.equals("Quran")) frag = new com.my.salah.tracker.app.fragments.QuranFragment();
                    else if(title.equals("Zikr")) frag = new com.my.salah.tracker.app.fragments.ZikrFragment();
                    else if(title.equals("Stats")) frag = new com.my.salah.tracker.app.fragments.StatsFragment();
                    else if(title.equals("Fasting")) frag = new com.my.salah.tracker.app.fragments.FastingFragment();
                    
                    if(frag != null) {
                        getSupportFragmentManager().beginTransaction().replace(888888, frag).commit();
                    }
                }
                return true;
            }
        });
        // ------------------------------------------------------------
"""

if "fragContainer.setId(888888);" not in code:
    code = code.replace("setContentView(root);", nav_code + "\n        setContentView(root);")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    print("✅ SUCCESS: Bottom Navigation & Fragment Logic successfully added to MainActivity.java!")
else:
    print("✅ ALREADY INJECTED!")

