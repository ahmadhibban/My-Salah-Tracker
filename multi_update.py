import re
import os

file_path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. সেটিংস মেনু সর্টিং (A-Z)
settings_pattern = re.compile(r"(MenuRow mr = new MenuRow\(\);)(.*?)(applyFont\(main, appFonts\[0\], appFonts\[1\]\);)", re.DOTALL)
if settings_pattern.search(content):
    sorted_menu = """
        MenuRow mr = new MenuRow();
        mr.addImg("Advanced Statistics", "img_stats", new Runnable() { @Override public void run() { statsHelper.showStatsOptionsDialog(); }});
        mr.addImg("Backup & Sync", "img_cloud", new Runnable() { @Override public void run() { backupHelper.showProfileDialog(null); }});
        mr.addImg("Change Language", "img_lang", new Runnable() { @Override public void run() { /* Language Logic */ }});
        mr.addImg("Choose Theme", "img_theme", new Runnable() { @Override public void run() { /* Theme Logic */ }});
        mr.addImg("Hijri Date Setting", "img_moon", new Runnable() { @Override public void run() { /* Hijri Logic */ }});
        mr.addImg("View Qaza List", "img_custom_qaza", new Runnable() { @Override public void run() { showQazaListDialog(); }});
    """
    content = settings_pattern.sub(r"\1" + sorted_menu + r"\n        \3", content)

# ২. পার্সেন্টেজ কার্ডে গ্রেডিয়েন্ট (Diagonal Orientation)
gradient_logic = """
        GradientDrawable pGrad = new GradientDrawable(GradientDrawable.Orientation.TL_BR, new int[]{colorAccent, themeColors[1]});
        pGrad.setCornerRadius(25f * DENSITY);
        pNeo.setBackground(pGrad);
"""
if "pNeo.setBackgroundColor(themeColors[1]);" in content:
    content = content.replace("pNeo.setBackgroundColor(themeColors[1]);", gradient_logic)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)
print("✅ Settings sorted & Gradient added!")
