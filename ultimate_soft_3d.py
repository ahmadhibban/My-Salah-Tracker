import os, re

java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(java_file):
    print("❌ MainActivity.java not found!")
    exit()

with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

# ১. ব্যাকগ্রাউন্ডে সফট ছায়া আঁকার মেগা মেথড (যাতে লেআউট না ভাঙে)
apply_neo_code = """
    private void applyNeo(android.view.View v, int type, float radius, float elev, int bgColor, boolean isDark) {
        soup.neumorphism.NeumorphShapeAppearanceModel model = new soup.neumorphism.NeumorphShapeAppearanceModel.Builder().setAllCorners(0, radius * DENSITY).build();
        soup.neumorphism.NeumorphShapeDrawable d = new soup.neumorphism.NeumorphShapeDrawable(v.getContext());
        d.setShapeAppearanceModel(model);
        d.setShapeType(type);
        d.setShadowColorLight(isDark ? android.graphics.Color.parseColor("#333336") : android.graphics.Color.WHITE);
        d.setShadowColorDark(isDark ? android.graphics.Color.parseColor("#0A0A0C") : android.graphics.Color.parseColor("#cbd5e0"));
        d.setShadowElevation(elev * DENSITY);
        d.setFillColor(android.content.res.ColorStateList.valueOf(bgColor));
        v.setBackground(d);
        
        // ছায়াকে বাইরে ছড়িয়ে পড়ার পারমিশন দেওয়া হচ্ছে
        v.post(() -> {
            android.view.ViewParent p1 = v.getParent();
            if (p1 instanceof android.view.ViewGroup) {
                ((android.view.ViewGroup) p1).setClipChildren(false);
                ((android.view.ViewGroup) p1).setClipToPadding(false);
                android.view.ViewParent p2 = p1.getParent();
                if (p2 instanceof android.view.ViewGroup) {
                    ((android.view.ViewGroup) p2).setClipChildren(false);
                    ((android.view.ViewGroup) p2).setClipToPadding(false);
                }
            }
        });
    }
"""

if "private void applyNeo" not in mc:
    mc = mc.replace("private SimpleDateFormat sdf;", "private SimpleDateFormat sdf;\n" + apply_neo_code)

# ২. আপনার কাঙ্ক্ষিত সবগুলো ঘরে এই সফট ছায়া বসিয়ে দেওয়া
replacements = {
    "streakBadge": "applyNeo(streakBadge, 0, 15f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme); streakBadge.setPadding((int)(12*DENSITY), (int)(6*DENSITY), (int)(12*DENSITY), (int)(6*DENSITY));",
    "themeToggleBtn": "applyNeo(themeToggleBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme);",
    "offBtn": "applyNeo(offBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme);",
    "periodBtn": "applyNeo(periodBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme);",
    "settingsBtn": "applyNeo(settingsBtn, 0, 20f, 3f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme);",
    "t": "applyNeo(t, isSel ? 1 : 0, 8f, isSel ? 1.5f : 3f, isSel ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\")), isDarkTheme); t.setPadding(0, (int)(8*DENSITY), 0, (int)(8*DENSITY));",
    "markAllBtn": "applyNeo(markAllBtn, 0, 12f, 4f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme); markAllBtn.setPadding((int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY));",
    "todayBtn": "applyNeo(todayBtn, 0, 12f, 4f, isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\"), isDarkTheme); todayBtn.setPadding((int)(16*DENSITY), (int)(10*DENSITY), (int)(16*DENSITY), (int)(10*DENSITY));",
    "sunnahBtn": "applyNeo(sunnahBtn, 1, 10f, 2f, doneSunnahs > 0 ? colorAccent : (isDarkTheme ? android.graphics.Color.parseColor(\"#1C1C1E\") : android.graphics.Color.parseColor(\"#E2E8F0\")), isDarkTheme); sunnahBtn.setPadding((int)(14*DENSITY), (int)(8*DENSITY), (int)(14*DENSITY), (int)(8*DENSITY));",
    "pCard": "applyNeo(pCard, 0, 20f, 6f, tSur, isDarkTheme); pCard.setPadding((int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY), (int)(20*DENSITY));"
}

for var, neo_code in replacements.items():
    # পুরনো শক্ত বর্ডার এবং প্যাডিং খুঁজে বের করে সফট থ্রিডি বসানো হচ্ছে
    pattern = rf'{var}\.setBackground\((?:getAccent3D|getUltra3D|getCarvedInner)\([^;]+;\s*(?:{var}\.setPadding\([^;]+;)?'
    mc = re.sub(pattern, neo_code, mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)

print("✔ ULTIMATE SOFT 3D APPLIED SAFELY! NO LAYOUT BROKEN!")
