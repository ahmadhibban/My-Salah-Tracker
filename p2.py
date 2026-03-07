f2 = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
c2 = open(f2).read()
ob = """GradientDrawable dayBg = new GradientDrawable(); dayBg.setShape(GradientDrawable.OVAL); \n            if(isSel) { dayBg.setColor(colorAccent); t.setTextColor(Color.WHITE);\n            } else if (isAllDone && !isFuture) { dayBg.setColor(themeColors[5]); t.setTextColor(colorAccent); } else { dayBg.setColor(themeColors[1]); dayBg.setStroke((int)(1.5f*DENSITY), themeColors[4]); t.setTextColor(isFuture ? themeColors[4] : themeColors[3]);\n            } \n            t.setBackground(dayBg);"""
nb = """t.setTextColor(isSel ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : themeColors[3]));\n            t.setBackground(getProgressBorder(dKey, isSel));"""
if ob in c2: open(f2,'w').write(c2.replace(ob, nb))
print("✅ Part 2 Done!")
