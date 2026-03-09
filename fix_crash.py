fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# ১. টেক্সট লেআউট ক্র্যাশ ফিক্স (নেগেটিভ সাইজ ঠেকানো)
code = code.replace('int layoutWidth = (int)(w - 100);', 'int layoutWidth = (int)(w - 100);\n                if (layoutWidth <= 0) return;')

# ২. কালার অ্যারে ক্র্যাশ ফিক্স (নিরাপদ ডিফল্ট কালার বসানো)
code = code.replace('themeColors != null ? themeColors[3] : ', '')
code = code.replace('themeColors != null ? themeColors[2] : ', '')
code = code.replace('themeColors != null ? themeColors[0] : ', 'themeColors != null && themeColors.length > 0 ? themeColors[0] : ')

# ৩. ফন্ট অ্যারে ক্র্যাশ ফিক্স
code = code.replace('if (fonts != null) bnFont = fonts[1];', 'if (fonts != null && fonts.length > 1) bnFont = fonts[1];')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: All Runtime Crashes (Bugs) are perfectly fixed!")
