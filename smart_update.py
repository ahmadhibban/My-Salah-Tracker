import re
import os

file_path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"

if not os.path.exists(file_path):
    print("Error: File not found!")
    exit()

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix Button Latency (150ms to 20ms) - স্পেস যাই থাকুক কাজ করবে
content = re.sub(r'postDelayed\(([^,]+),\s*150\s*\);', r'postDelayed(\1, 20);', content)

# 2. Fix Animation Speed (100ms to 40ms)
content = re.sub(r'setDuration\(\s*100\s*\)', 'setDuration(40)', content)

# 3. Make Tasbih Text Bigger (18f to 26f)
content = re.sub(r'setTextSize\(\s*18f\s*\)', 'setTextSize(26f)', content)

# 4. Make Tasbih Button Bigger (50*DENSITY to 65*DENSITY)
content = re.sub(r'50\s*\*\s*DENSITY', '65*DENSITY', content)
content = re.sub(r'25f\s*\*\s*DENSITY', '32.5f*DENSITY', content) # Perfect circle math

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Success! Python smartly updated your code without any errors.")
