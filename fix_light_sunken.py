import os, re
java_file = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(java_file, "r", encoding="utf-8") as f:
    mc = f.read()

depth_logic = """
        if (type == 1 && !isDark) {
            bgColor = android.graphics.Color.parseColor("#E2E8F0"); // গর্তের ভেতরটা হালকা ছাই
            d.setShadowColorDark(android.graphics.Color.parseColor("#A0AEC0")); // গাঢ় ছায়া
            d.setShadowColorLight(android.graphics.Color.parseColor("#FFFFFF"));
            elev = elev * 1.5f; // গর্তের গভীরতা বাড়ানো
        }
"""
if "bgColor = android.graphics.Color.parseColor(\"#E2E8F0\");" not in mc:
    mc = re.sub(r'(d\.setShapeType\(type\);)', r'\1\n' + depth_logic, mc)

with open(java_file, "w", encoding="utf-8") as f:
    f.write(mc)
print("✅ ৩. Light Mode Sunken Depth Increased!")
