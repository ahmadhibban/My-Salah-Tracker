import os
import re

print("🚀 Installing Super Premium Excel Engine...")

s_path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(s_path):
    with open(s_path, 'r', encoding='utf-8') as f:
        s_data = f.read()

    super_xls = """public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            java.io.File file = new java.io.File(dir, "Salah_Premium_Report_" + System.currentTimeMillis() + ".xls");
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
            String title = (isBn ? "মাসিক রিপোর্ট • " : "Monthly Report • ") + new SimpleDateFormat("MMMM yyyy", Locale.US).format(statsCalPointer.getTime());
            
            StringBuilder xml = new StringBuilder();
            xml.append("<?xml version=\\"1.0\\" encoding=\\"UTF-8\\"?>\\n");
            xml.append("<?mso-application progid=\\"Excel.Sheet\\"?>\\n");
            xml.append("<Workbook xmlns=\\"urn:schemas-microsoft-com:office:spreadsheet\\" xmlns:ss=\\"urn:schemas-microsoft-com:office:spreadsheet\\">\\n");
            
            // 💎 PREMIUM STYLES DEFINITION 💎
            xml.append("<Styles>\\n");
            xml.append("<Style ss:ID=\\"Default\\" ss:Name=\\"Normal\\"><Alignment ss:Vertical=\\"Center\\"/></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sTitle\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"20\\" ss:Bold=\\"1\\" ss:Color=\\"#FFFFFF\\"/><Interior ss:Color=\\"#FF9800\\" ss:Pattern=\\"Solid\\"/></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sSumH\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"12\\" ss:Bold=\\"1\\" ss:Color=\\"#5F6368\\"/><Interior ss:Color=\\"#F8F9FA\\" ss:Pattern=\\"Solid\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Top\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sSumV\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"16\\" ss:Bold=\\"1\\" ss:Color=\\"#202124\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"2\\" ss:Color=\\"#FF9800\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sHead\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"13\\" ss:Bold=\\"1\\" ss:Color=\\"#FFFFFF\\"/><Interior ss:Color=\\"#3C4043\\" ss:Pattern=\\"Solid\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"2\\" ss:Color=\\"#202124\\"/><Border ss:Position=\\"Top\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sDate\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"12\\" ss:Bold=\\"1\\" ss:Color=\\"#3C4043\\"/><Interior ss:Color=\\"#F1F3F4\\" ss:Pattern=\\"Solid\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Top\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sYes\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"12\\" ss:Bold=\\"1\\" ss:Color=\\"#137333\\"/><Interior ss:Color=\\"#E6F4EA\\" ss:Pattern=\\"Solid\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sNo\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"12\\" ss:Bold=\\"1\\" ss:Color=\\"#C5221F\\"/><Interior ss:Color=\\"#FCE8E6\\" ss:Pattern=\\"Solid\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            
            xml.append("<Style ss:ID=\\"sExc\\"><Alignment ss:Horizontal=\\"Center\\" ss:Vertical=\\"Center\\"/><Font ss:FontName=\\"Segoe UI\\" ss:Size=\\"12\\" ss:Bold=\\"1\\" ss:Color=\\"#B80672\\"/><Interior ss:Color=\\"#FCE4EC\\" ss:Pattern=\\"Solid\\"/><Borders><Border ss:Position=\\"Bottom\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Left\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/><Border ss:Position=\\"Right\\" ss:LineStyle=\\"Continuous\\" ss:Weight=\\"1\\" ss:Color=\\"#E0E0E0\\"/></Borders></Style>\\n");
            xml.append("</Styles>\\n");
            
            xml.append("<Worksheet ss:Name=\\"Report\\">\\n<Table>\\n");
            
            // 💎 COLUMN WIDTHS 💎
            xml.append("<Column ss:Width=\\"140\\"/>"); // Date
            for(int i=0; i<6; i++) xml.append("<Column ss:Width=\\"110\\"/>"); // Prayers
            xml.append("<Column ss:Width=\\"150\\"/>\\n"); // Status
            
            // 💎 TITLE 💎
            xml.append("<Row ss:Height=\\"60\\"><Cell ss:MergeAcross=\\"7\\" ss:StyleID=\\"sTitle\\"><Data ss:Type=\\"String\\">" + title + "</Data></Cell></Row>\\n");
            xml.append("<Row ss:Height=\\"20\\"><Cell><Data ss:Type=\\"String\\"></Data></Cell></Row>\\n");
            
            // 💎 SUMMARY HEADER 💎
            xml.append("<Row ss:Height=\\"35\\">\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"মোট দিন":"Total Days") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"আদায়কৃত":"Done") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"কাজা":"Missed") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"অপেক্ষমান কাজা":"Pending Qaza") + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"ছুটি":"Excused") + "</Data></Cell>\\n");
            xml.append("<Cell ss:MergeAcross=\\"2\\" ss:StyleID=\\"sSumH\\"><Data ss:Type=\\"String\\">" + (isBn?"স্ট্রিক":"Streak") + "</Data></Cell>\\n");
            xml.append("</Row>\\n");
            
            // 💎 SUMMARY VALUES 💎
            xml.append("<Row ss:Height=\\"45\\">\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tDays) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tDone) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tMissed) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tQaza) + "</Data></Cell>\\n");
            xml.append("<Cell ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(tExcused) + "</Data></Cell>\\n");
            xml.append("<Cell ss:MergeAcross=\\"2\\" ss:StyleID=\\"sSumV\\"><Data ss:Type=\\"String\\">" + lang.bnNum(streak) + " 🔥</Data></Cell>\\n");
            xml.append("</Row>\\n");
            xml.append("<Row ss:Height=\\"25\\"><Cell><Data ss:Type=\\"String\\"></Data></Cell></Row>\\n");

            // 💎 MAIN DATA HEADERS 💎
            xml.append("<Row ss:Height=\\"40\\">\\n");
            String[] headers = isBn ? new String[]{"তারিখ", "ফজর", "যোহর", "আসর", "মাগরিব", "এশা", "বিতর", "সারসংক্ষেপ"} : new String[]{"Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr", "Status"};
            for(String h : headers) xml.append("<Cell ss:StyleID=\\"sHead\\"><Data ss:Type=\\"String\\">" + h + "</Data></Cell>\\n");
            xml.append("</Row>\\n");
            
            // 💎 GENERATE REPORT ROWS 💎
            Calendar cal = (Calendar) statsCalPointer.clone(); cal.set(Calendar.DAY_OF_MONTH, 1);
            for(int i=1; i<=mDays; i++) {
                cal.set(Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                String dateDisplay = isBn ? lang.bnNum(i) + " " + lang.get(new SimpleDateFormat("MMM", Locale.US).format(cal.getTime())) + ", " + lang.bnNum(cal.get(Calendar.YEAR)) : dKey;
                
                xml.append("<Row ss:Height=\\"35\\">\\n");
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
    }"""
    
    # আগের exportXls মুছে নতুনটা বসানো
    c = re.sub(r'public void exportXls\(\)\s*\{.*?public void showStatsOptionsDialog\(\)\s*\{', super_xls + '\n\n    public void showStatsOptionsDialog() {', s_data, flags=re.DOTALL)
    
    with open(s_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("✅ Super Premium Excel Engine Successfully Installed!")

