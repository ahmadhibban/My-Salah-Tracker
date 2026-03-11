import os, re

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ভুলবশত রয়ে যাওয়া অতিরিক্ত 'else' ব্লকটা খুঁজে মুছে ফেলা হচ্ছে
bad_pattern = r't\.setScaleY\(1\.0f\);\s*\}\s*else\s*\{\s*t\.setScaleX\([^;]+\);\s*t\.setScaleY\([^;]+\);\s*\}'
content = re.sub(bad_pattern, 't.setScaleY(1.0f); }', content, flags=re.DOTALL)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Orphaned 'else' block fixed perfectly!")
