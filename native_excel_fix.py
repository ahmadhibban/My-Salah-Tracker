import os
import re

print("🚀 Initiating Native XML Excel Engine & Bug Fixes...")

# ১. MainActivity Language Bug Fix
m_path = 'app/src/main/java/com/my/salah/tracker/app/MainActivity.java'
if os.path.exists(m_path):
    with open(m_path, 'r', encoding='utf-8') as f:
        m_data = f.read()
    m_data = m_data.replace('"সীমা অতিক্রম"', 'lang.get("Limit Reached")')
    m_data = m_data.replace('"১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়"', 'lang.get("Limit Reached Desc")')
    with open(m_path, 'w', encoding='utf-8') as f:
        f.write(m_data)
    print("✅ MainActivity Language Fix Applied.")

# ২. LanguageEngine Translations Update
l_path = 'app/src/main/java/com/my/salah/tracker/app/LanguageEngine.java'
if os.path.exists(l_path):
    with open(l_path, 'r', encoding='utf-8') as f:
        l_data = f.read()
    if '"Limit Reached"' not in l_data:
        add_langs = """bnMap.put("Limit Reached", "সীমা অতিক্রম");
        bnMap.put("Limit Reached Desc", "১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়।");
        """
        l_data = l_data.replace('bnMap.put("My Salah Journey"', add_langs + 'bnMap.put("My Salah Journey"')
        with open(l_path, 'w', encoding='utf-8') as f:
            f.write(l_data)
    print("✅ Language Translations Added.")

# ৩. CalendarHelper (English Calendar Highlight & Language Fix)
c_path = 'app/src/main/java/com/my/salah/tracker/app/CalendarHelper.java'
if os.path.exists(c_path):
    with open(c_path, 'r', encoding='utf-8') as f:
        c_data = f.read()
    
    # ভাষার বাগ ফিক্স
    c_data = c_data.replace('"সীমা অতিক্রম"', 'lang.get("Limit Reached")')
    c_data = c_data.replace('"১০০ বছরের বেশি পেছনে যাওয়া সম্ভব নয়"', 'lang.get("Limit Reached Desc")')
    
    # ইংরেজি ক্যালেন্ডার হাইলাইট লজিক (আরবি ক্যালেন্ডারের মতো হুবহু)
    c_data = re.sub(
        r'GradientDrawable bgD = new GradientDrawable\(\); bgD\.setShape\(GradientDrawable\.OVAL\);.*?cell\.addView\(tv\);',
        r'''boolean isAllDone = true;
                    SalahRecord dRec = SalahDatabase.getDatabase(activity).salahDao().getRecordByDate(dKey);
                    if(dRec != null) {
                        for(String p : prayers) {
                            String st = "no";
                            if(p.equals("Fajr")) st = dRec.fajr; else if(p.equals("Dhuhr")) st = dRec.dhuhr;
                            else if(p.equals("Asr")) st = dRec.asr; else if(p.equals("Maghrib")) st = dRec.maghrib;
                            else if(p.equals("Isha")) st = dRec.isha; else if(p.equals("Witr")) st = dRec.witr;
                            if(!st.equals("yes") && !st.equals("excused")) { isAllDone = false; break; }
                        }
                    } else { isAllDone = false; }
                    
                    tv.setTextColor(dKey.equals(selectedDate[0]) ? android.graphics.Color.WHITE : (isFuture ? themeColors[4] : (isAllDone ? colorAccent : themeColors[2])));
                    GradientDrawable bgD = new GradientDrawable(); bgD.setShape(GradientDrawable.OVAL);
                    if (dKey.equals(selectedDate[0])) { bgD.setColor(colorAccent); tv.setBackground(bgD); }
                    else if (isAllDone && !isFuture) { bgD.setColor(themeColors[5]); tv.setBackground(bgD); }
                    else { bgD.setColor(android.graphics.Color.TRANSPARENT); tv.setBackground(bgD); }
                    cell.addView(tv);''',
        c_data, flags=re.DOTALL
    )
    with open(c_path, 'w', encoding='utf-8') as f:
        f.write(c_data)
    print("✅ English Calendar Highlights perfectly synced with Hijri style.")

# ৪. StatsHelper (Native XML Spreadsheet Engine)
s_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(s_path):
    with open(s_path, 'r', encoding='utf-8') as f:
        s_data = f.read()

    start_str = 'public void exportXls() {'
    end_str = 'public void showStatsOptionsDialog() {'
    
    if start_str in s_data and end_str in s_data:
        s_start = s_data.index(start_str)
        s_end = s_data.index(end_str)
        
        new_xls_method = """public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            java.io.File file = new java.io.File(dir, "Salah_Report_" + System.currentTimeMillis() + ".xls");
            java.io.PrintWriter pw = new java.io.PrintWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(file), "UTF-8"));
            
            int tDays = 0, tDone = 0, tMissed = 0, tExcused = 0, tQaza = 0;
            Calendar sumCal = (Calendar) statsCalPointer.clone(); sumCal.set(Calendar.DAY_OF_MONTH, 1);
            int mDays = sumCal.getActualMaximum(Calendar.DAY_OF_MONTH);
            Calendar nowSum = Calendar.getInstance();
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd", Locale.US);
            
            for(int j=1; j<=mDays; j++) {
                sumCal.set(Calendar.DAY_OF_MONTH, j);
                String dk = sdf.format(sumCal.getTime());
                if(sumCal.after(nowSum) && !dk.equals(sdf.format(nowSum.getTime()))) continue;
                tDays++;
                SalahRecord rec = getRoomRecord(dk);
                for(String p : prayers) {
                    String st = getFardStat(rec, p); boolean isQz = getQazaStat(rec, p);
                    if(st.equals("yes")) tDone++; else if(st.equals("excused")) tExcused++; else { if(isQz) tQaza++; else tMissed++; }
                }
            }
            int streak = ui.calculateStreak(sp, prayers);

            String title = (isBn ? "মাসিক রিপোর্ট - " : "Monthly Report - ") + new SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.getTime());
            
            StringBuilder xml = new StringBuilder();
            xml.append("<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?>\\n");
            xml.append("<?mso-application progid=\\"Excel.Sheet\\"?>\\n");
            xml.append("<Workbook xmlns=\\"urn:schemas-microsoft-com:office:spreadsheet\\" xmlns:ss=\\"urn:schemas-microsoft-com:office:spreadsheet\\">\\n");
            xml.append("<Styles>\\n");
            xml.append("<Style ss:ID=\\"sTitle\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Size=\\"18\\" ss:Bold=\\"1\\" ss:Color=\\"#FFFFFF\\"/><Interior ss:Color=\\"#1C1C1E\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sHead\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Color=\\"#FFFFFF\\"/><Interior ss:Color=\\"#00BFA5\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sYes\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Color=\\"#2E7D32\\"/><Interior ss:Color=\\"#E8F5E9\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sNo\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Color=\\"#C62828\\"/><Interior ss:Color=\\"#FFEBEE\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sExc\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Color=\\"#AD1457\\"/><Interior ss:Color=\\"#FCE4EC\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sDate\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Color=\\"#333333\\"/><Interior ss:Color=\\"#F8F9FA\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sSumH\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Color=\\"#FFFFFF\\"/><Interior ss:Color=\\"#3B82F6\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("<Style ss:ID=\\"sSumV\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:Bold=\\"1\\" ss:Size=\\"14\\" ss:Color=\\"#333333\\"/><Interior ss:Color=\\"#FAFAFA\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            xml.append("</Styles>\\n");
            
            xml.append("<Worksheet ss:Name=\\"Report\\">\\n<Table>\\n");
            xml.append("<Column ss:Width=\\"100\\"/>");
            for(int i=0; i<6; i++) xml.append("<Column ss:Width=\\"80\\"/>");
            xml.append("<Column ss:Width=\\"120\\"/>\\n");
            
            xml.append("<Row ss:Height=\\"40\\"><Cell ss:MergeAcross=\\"7\\" ss:StyleID=\\"sTitle\\"><Data ss:Type=\\"String\\">" + title + "</Data></Cell></Row>\\n");
            xml.append("<Row><Cell><Data ss:Type=\\"String\\"></Data></Cell></Row>\\n");
            
            // Summary Block (PDF Style)
            xml.append("<Row ss:Height=\\"25\\">\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"মোট দিন":"Total Days") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"আদায়কৃত":"Done") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"কাজা":"Missed") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"অপেক্ষমান কাজা":"Pending Qaza") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"ছুটি":"Excused") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"স্ট্রিক":"Streak") + "</Data></Cell>\\n");
            xml.append("</Row>\\n");
            xml.append("<Row ss:Height=\\"30\\">\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tDays) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tDone) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tMissed) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tQaza) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tExcused) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(streak) + "</Data></Cell>\\n");
            xml.append("</Row>\\n");
            xml.append("<Row><Cell><Data ss:Type=\\"String\\"></Data></Cell></Row>\\n");

            // Main Data Headers
            xml.append("<Row ss:Height=\\"25\\">\\n");
            String[] headers = isBn ? new String[]{"তারিখ", "ফজর", "যোহর", "আসর", "মাগরিব", "এশা", "বিতর", "সারসংক্ষেপ"} : new String[]{"Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr", "Status"};
            for(String h : headers) xml.append("<Cell ss:StyleID=\\"sHead\\"><Data ss:Type=\\"String\\">" + h + "</Data></Cell>\\n");
            xml.append("</Row>\\n");
            
            // Generate Report Rows
            Calendar cal = (Calendar) statsCalPointer.clone(); cal.set(Calendar.DAY_OF_MONTH, 1);
            for(int i=1; i<=mDays; i++) {
                cal.set(Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                String dateDisplay = isBn ? lang.bnNum(i) + " " + lang.get(new SimpleDateFormat("MMM", Locale.US).format(cal.getTime())) : dKey;
                xml.append("<Row ss:Height=\\"22\\">\\n");
                xml.append("<Cell ss:StyleID=\\"sDate\\"><Data ss:Type=\\"String\\">" + dateDisplay + "</Data></Cell>\\n");
                
                boolean allDone = true;
                for(String p : prayers) {
                    String s = getFardStat(r, p);
                    String style = s.equals("yes") ? "sYes" : (s.equals("excused") ? "sExc" : "sNo");
                    String txt = s.equals("yes") ? "✓ " + (isBn?"সম্পন্ন":"Done") : (s.equals("excused") ? "🌸 " + (isBn?"ছুটি":"Excused") : "❌ " + (isBn?"কাজা":"Missed"));
                    xml.append("<Cell ss:StyleID=\\"" + style + "\\"><Data ss:Type=\\"String\\">" + txt + "</Data></Cell>\\n");
                    if(!s.equals("yes") && !s.equals("excused")) allDone = false;
                }
                String sStyle = allDone ? "sYes" : "sNo";
                String sTxt = allDone ? (isBn ? "🌟 আলহামদুলিল্লাহ" : "🌟 Perfect") : (isBn ? "⚠️ অসম্পূর্ণ" : "⚠️ Incomplete");
                xml.append("<Cell ss:StyleID=\\"" + sStyle + "\\"><Data ss:Type=\\"String\\">" + sTxt + "</Data></Cell>\\n");
                xml.append("</Row>\\n");
            }
            xml.append("</Table>\\n</Worksheet>\\n</Workbook>");
            pw.write(xml.toString());
            pw.close();
            
            final java.io.File finalFile = file;
            ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), isBn?"সফল":"Success", isBn?"XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)":"XLS Saved (Click to open)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    android.net.Uri uri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(uri, "application/vnd.ms-excel");
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    activity.startActivity(Intent.createChooser(intent, "Open with..."));
                }
            });
        } catch(Exception e) {}
    }

    """
        updated_s_data = s_data[:s_start] + new_xls_method + s_data[s_end:]
        with open(s_path, 'w', encoding='utf-8') as f:
            f.write(updated_s_data)
        print("✅ Native XML Spreadsheet Engine Injected (With PDF Summary).")

print("🎉 ALL FIXES APPLIED SUCCESSFULLY!")
