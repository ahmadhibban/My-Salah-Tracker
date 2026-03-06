import os

def replace_content(path, old_text, new_text):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        if old_text in content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content.replace(old_text, new_text))
            return True
    return False

# ১. ইংরেজি ক্যালেন্ডারে হাইলাইট এবং কাস্টম ফন্ট (CalendarHelper.java)
cal_path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'

# ফন্ট অ্যাপ্লাই করার লজিক আপডেট
old_apply_font_cal = 'if (tv.getTypeface() != null && tv.getTypeface().isBold()) tv.setTypeface(bold);'
new_apply_font_cal = 'tv.setTypeface(tv.getTypeface() != null && tv.getTypeface().isBold() ? bold : reg);'

# ইংরেজি ক্যালেন্ডারে হাইলাইট লজিক (Rainbow বর্ডার)
old_greg_bg = 'tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : ui.getRainbowBorder(dKey, 3)));'
new_greg_bg = """SalahRecord dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey);
                    boolean isAllDone = true;
                    if(dRec != null){
                        for(String pName : prayers){
                            String s = "no";
                            if(pName.equals("Fajr")) s=dRec.fajr; else if(pName.equals("Dhuhr")) s=dRec.dhuhr;
                            else if(pName.equals("Asr")) s=dRec.asr; else if(pName.equals("Maghrib")) s=dRec.maghrib;
                            else if(pName.equals("Isha")) s=dRec.isha; else if(pName.equals("Witr")) s=dRec.witr;
                            if(!s.equals("yes") && !s.equals("excused")){ isAllDone = False; break; }
                        }
                    } else { isAllDone = False; }
                    tv.setBackground(isFuture ? bgD : (dKey.equals(selectedDate[0]) ? bgD : (isAllDone ? ui.getRainbowBorder(dKey, 3) : bgD)));"""

replace_content(cal_path, old_apply_font_cal, new_apply_font_cal)
replace_content(cal_path, old_greg_bg, new_greg_bg)

# ২. অনবোর্ডিং স্ক্রিন আপডেট (সবগুলো ফিচার যুক্ত করা)
onboarding_path = 'app/src/main/java/com/my/salah/tracker/app/OnboardingHelper.java'
is_bn = 'sp.getString("app_lang", "en").equals("bn")'

new_onboarding_pages = """        final String[][] pages = {
                { "img_moon", isBn ? "স্বাগতম" : "Welcome", isBn ? "আপনার ব্যক্তিগত বিজ্ঞাপন-মুক্ত সালাহ ট্র্যাকার।" : "Your personal ad-free Salah companion." },
                { "img_calender", isBn ? "সহজ ট্র্যাকিং" : "Easy Tracking", isBn ? "প্রতিদিনের নামাজ ও কাজা নামাজের হিসাব রাখুন সহজে।" : "Track daily prayers and Qaza with ease." },
                { "img_cloud", isBn ? "ক্লাউড ব্যাকআপ" : "Cloud Sync", isBn ? "আপনার ডাটা কখনোই হারাবে না, গুগল ক্লাউডে সেভ থাকবে।" : "Never lose data; sync securely with Google Cloud." },
                { "img_stats", isBn ? "বিস্তারিত রিপোর্ট" : "Advanced Stats", isBn ? "সাপ্তাহিক ও মাসিক প্রগতি দেখুন আকর্ষণীয় চার্টে।" : "Analyze your progress with weekly & monthly charts." },
                { "img_settings", isBn ? "কাস্টমাইজেশন" : "Customization", isBn ? "ডার্ক মোড, একাধিক থিম এবং বাংলা ভাষা ব্যবহারের সুবিধা।" : "Dark mode, multiple themes, and Bengali support." }
        };"""

old_onboarding_pages_start = 'final String[][] pages = {'
# এই অংশটি একটু জটিল তাই পুরো ভেরিয়েবল রিপ্লেস করা হচ্ছে
if os.path.exists(onboarding_path):
    with open(onboarding_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(onboarding_path, 'w', encoding='utf-8') as f:
        skip = False
        for line in lines:
            if 'final String[][] pages = {' in line:
                f.write(new_onboarding_pages + "\n")
                skip = True
            elif skip and '};' in line:
                skip = False
                continue
            if not skip:
                f.write(line)

print("✅ অল-ইন-ওয়ান অটোমেশন সম্পন্ন!")
