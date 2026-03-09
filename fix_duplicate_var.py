fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# onTouch মেথডের ভেতরের ডুপ্লিকেট float রিমুভ করা হচ্ছে
parts = code.split("public boolean onTouch")
if len(parts) > 1:
    parts[1] = parts[1].replace("float sideMargin = w * 0.15f;", "sideMargin = w * 0.15f;")
    code = "public boolean onTouch".join(parts)

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ Success: Duplicate 'sideMargin' error fixed!")
