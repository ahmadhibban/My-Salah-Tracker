import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

new_nav = """
        prevW.setLayoutParams(new LinearLayout.LayoutParams((int)(52*DENSITY), (int)(52*DENSITY)));
        nextW.setLayoutParams(new LinearLayout.LayoutParams((int)(52*DENSITY), (int)(52*DENSITY)));
        weekNavBox.addView(prevW); weekNavBox.addView(weekBox); weekNavBox.addView(nextW);
"""
mc = mc.replace("weekNavBox.addView(prevW); weekNavBox.addView(weekBox); weekNavBox.addView(nextW);", new_nav.strip())

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ২. Arrows Resized to 52dp!")
