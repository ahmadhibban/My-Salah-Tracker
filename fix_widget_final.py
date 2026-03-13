import os, re

for r, d, f in os.walk('.'):
    if 'SalahWidget.java' in f and 'build' not in r:
        p = os.path.join(r, 'SalahWidget.java')
        with open(p, 'r', encoding='utf-8') as file: cw = file.read()
        
        # 1. 3টি তারিখ একসাথে সেট করা
        cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)([^,]*getHijri[^)]*)(\s*\);)',
                    r'''try {
            String wg = MainActivity.lang.getGregorian(new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US).parse(dateStr));
            String wb = MainActivity.getBnDateStr(dateStr, sp);
            \1 \2 + " • " + wb + " • " + wg \3
        } catch(Exception e) { \1 \2 \3 }''', cw)
        
        # 2. পার্সেন্টেজের ওপরে স্ট্রিক বসানো
        cw = re.sub(r'(views\.setTextViewText\([^,]+,\s*)(.*?100\s*/\s*6\s*\+\s*"%".*?)(\s*\);)',
                    r'''int wSt = sp.getInt("cached_streak", 0);
        boolean wIsBn = sp.getString("app_lang", "en").equals("bn");
        String wStStr = wSt >= 365 ? (wIsBn ? "১ বছর" : "1 YEAR") : (wIsBn ? String.valueOf(wSt).replace("0","০").replace("1","১").replace("2","২").replace("3","৩").replace("4","৪").replace("5","৫").replace("6","৬").replace("7","৭").replace("8","৮").replace("9","৯") + " দিন" : wSt + " DAYS");
        \1 wStStr + "\\n" + \2 \3''', cw)
        
        with open(p, 'w', encoding='utf-8') as file: file.write(cw)
        print("✅ Widget Patched (3 Dates + Streak)")
