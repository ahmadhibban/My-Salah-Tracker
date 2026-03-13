import os

filepath = None
for r, d, f in os.walk('.'):
    if 'MainActivity.java' in f and 'build' not in r:
        filepath = os.path.join(r, 'MainActivity.java')
        break

if filepath:
    with open(filepath, 'r', encoding='utf-8') as f:
        c = f.read()

    # ১. ডাবল android.widget ফিক্স করা
    c = c.replace('android.widget.android.widget.', 'android.widget.')
    
    # ২. applyFont এরর ফিক্স করা
    c = c.replace('applyFont(yWrap);', 'applyFont(yWrap, appFonts[0], appFonts[1]);')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Build Errors Fixed!")
else:
    print("❌ MainActivity.java Not Found!")
