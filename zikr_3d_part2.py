fpath = "app/src/main/java/com/my/salah/tracker/app/fragments/ZikrFragment.java"
with open(fpath, "r", encoding="utf-8") as f:
    code = f.read()

# পজিশনগুলো আরও নিখুঁত করা
code = code.replace('float circleY = btnY + (h * 0.18f);', 'float circleY = btnY + (h * 0.20f);')
code = code.replace('float beadY = circleY + radius + (h * 0.09f);', 'float beadY = circleY + radius + (h * 0.12f);')
code = code.replace('float totalBoxY = beadY + (h * 0.07f);', 'float totalBoxY = beadY + (h * 0.12f);')
code = code.replace('canvas.drawRoundRect(new RectF(centerX - boxW/2, totalBoxY - 50, centerX + boxW/2, totalBoxY + 40), 25f, 25f, p);', 
                    'canvas.drawRoundRect(new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 60), 30f, 30f, p);')
code = code.replace('canvas.drawText(totalTxt, centerX, totalBoxY + 12, p);', 'canvas.drawText(totalTxt, centerX, totalBoxY + 22, p);')

with open(fpath, "w", encoding="utf-8") as f:
    f.write(code)
print("✅ Part 2: Loop Box repositioned and balanced!")
