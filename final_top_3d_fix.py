import os

path = "app/src/main/java/com/my/salah/tracker/app/MainActivity.java"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# ১. Progress Card (pCard) - বিশাল পার্সেন্টেজ ব্যানার
if 'pCard.setBackground(get3DDrawable' not in content:
    content = content.replace('pCard.setBackground(pcBg);', 'pCard.setBackground(get3DDrawable(pcBg, 16f, false)); pCard.setPadding((int)(19.5f*DENSITY), (int)(pCardPadV*DENSITY), (int)(16*DENSITY), (int)((pCardPadV + 3.5f)*DENSITY));')

# ২. Streak Badge - স্ট্রিকের ঘর
if 'streakBadge.setBackground(get3DDrawable' not in content:
    content = content.replace('streakBadge.setBackground(badgeBg);', 'streakBadge.setBackground(get3DDrawable(badgeBg, 16f, false)); streakBadge.setPadding((int)(15.5f*DENSITY), (int)(4*DENSITY), (int)(10*DENSITY), (int)(7.5f*DENSITY));')

# ৩. Theme Toggle Button - থিম বাটন
if 'themeToggleBtn.setBackground(get3DDrawable' not in content:
    content = content.replace('themeToggleBtn.setBackground(tBg);', 'themeToggleBtn.setBackground(get3DDrawable(tBg, 0, true)); themeToggleBtn.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY));')

# ৪. Icons (Period, Settings, Offline) - অন্যান্য গোলাকার আইকনের ঘরগুলো
if 'periodBtn.setBackground(get3DDrawable' not in content:
    content = content.replace('rightHeader.addView(periodBtn);', 'periodBtn.setBackground(get3DDrawable(periodBtn.getBackground(), 0, true)); periodBtn.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY)); rightHeader.addView(periodBtn);')
    content = content.replace('rightHeader.addView(settingsBtn);', 'settingsBtn.setBackground(get3DDrawable(settingsBtn.getBackground(), 0, true)); settingsBtn.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY)); rightHeader.addView(settingsBtn);')
    content = content.replace('rightHeader.addView(offBtn);', 'offBtn.setBackground(get3DDrawable(offBtn.getBackground(), 0, true)); offBtn.setPadding((int)(3.5f*DENSITY), 0, 0, (int)(3.5f*DENSITY)); rightHeader.addView(offBtn);')

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("Remaining top UI elements (Progress Card, Badges, Icons) are now PERFECTLY 3D!")
