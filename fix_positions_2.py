fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# বাটন এবং থিম সিলেক্টরের গ্যাপ অ্যাডজাস্টমেন্ট
code = code.replace('float btnY = boxTop + boxHeight + (h * 0.08f);', 'float btnY = boxTop + boxHeight + (h * 0.10f);')
code = code.replace('float themeY = h - (h * 0.06f);', 'float themeY = h - (h * 0.08f);')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Success: All positions are now perfectly balanced!")
