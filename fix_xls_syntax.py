import os

path = 'app/src/main/java/com/my/salah/tracker/app/StatsHelper.java'
if os.path.exists(path):
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()

    start_sig = "public void exportXls() {"
    end_sig = "public void showStatsOptionsDialog() {"
    
    if start_sig in c and end_sig in c:
        start_idx = c.find(start_sig)
        end_idx = c.find(end_sig)
        
        # Raw string without explicit newlines inside Java strings
        clean_xls = r"""public void exportXls() {
        boolean isBn = sp.getString("app_lang", "en").equals("bn");
        try {
            java.io.File dir = android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_DOWNLOADS);
            if (!dir.exists()) dir.mkdirs();
            java.io.File file = new java.io.File(dir, "Salah_Premium_Report_" + System.currentTimeMillis() + ".xls");
            java.io.PrintWriter pw = new java.io.PrintWriter(new java.io.OutputStreamWriter(new java.io.FileOutputStream(file), "UTF-8"));
            
            int tDays = 0, tDone = 0, tMissed = 0, tExcused = 0, tQaza = 0;
            java.util.Calendar sumCal = (java.util.Calendar) statsCalPointer.clone(); sumCal.set(java.util.Calendar.DAY_OF_MONTH, 1);
            int mDays = sumCal.getActualMaximum(java.util.Calendar.DAY_OF_MONTH);
            java.util.Calendar nowSum = java.util.Calendar.getInstance();
            java.text.SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd", java.util.Locale.US);
            
            for(int j=1; j<=mDays; j++) {
                sumCal.set(java.util.Calendar.DAY_OF_MONTH, j);
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
            String title = (isBn ? "মাসিক রিপোর্ট • " : "Monthly Report • ") + new java.text.SimpleDateFormat("MMMM yyyy", java.util.Locale.US).format(statsCalPointer.getTime());
            
            StringBuilder xml = new StringBuilder();
            xml.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>");
            xml.append("<?mso-application progid=\"Excel.Sheet\"?>");
            xml.append("<Workbook xmlns=\"urn:schemas-microsoft-com:office:spreadsheet\" xmlns:ss=\"urn:schemas-microsoft-com:office:spreadsheet\">");
            
            xml.append("<Styles>");
            xml.append("<Style ss:ID=\"Default\" ss:Name=\"Normal\"><Alignment ss:Vertical=\"Center\"/></Style>");
            xml.append("<Style ss:ID=\"sTitle\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"20\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#FF9800\" ss:Pattern=\"Solid\"/></Style>");
            xml.append("<Style ss:ID=\"sSumH\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#5F6368\"/><Interior ss:Color=\"#F8F9FA\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sSumV\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"16\" ss:Bold=\"1\" ss:Color=\"#202124\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#FF9800\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sHead\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"13\" ss:Bold=\"1\" ss:Color=\"#FFFFFF\"/><Interior ss:Color=\"#3C4043\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"2\" ss:Color=\"#202124\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sDate\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#3C4043\"/><Interior ss:Color=\"#F1F3F4\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Top\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sYes\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#137333\"/><Interior ss:Color=\"#E6F4EA\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sNo\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#C5221F\"/><Interior ss:Color=\"#FCE8E6\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("<Style ss:ID=\"sExc\"><Alignment ss:Horizontal=\"Center\" ss:Vertical=\"Center\"/><Font ss:FontName=\"Segoe UI\" ss:Size=\"12\" ss:Bold=\"1\" ss:Color=\"#B80672\"/><Interior ss:Color=\"#FCE4EC\" ss:Pattern=\"Solid\"/><Borders><Border ss:Position=\"Bottom\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Left\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/><Border ss:Position=\"Right\" ss:LineStyle=\"Continuous\" ss:Weight=\"1\" ss:Color=\"#E0E0E0\"/></Borders></Style>");
            xml.append("</Styles>");
            
            xml.append("<Worksheet ss:Name=\"Report\"><Table>");
            
            xml.append("<Column ss:Width=\"140\"/>");
            for(int i=0; i<6; i++) xml.append("<Column ss:Width=\"110\"/>");
            xml.append("<Column ss:Width=\"150\"/>");
            
            xml.append("<Row ss:Height=\"60\"><Cell ss:MergeAcross=\"7\" ss:StyleID=\"sTitle\"><Data ss:Type=\"String\">" + title + "</Data></Cell></Row>");
            xml.append("<Row ss:Height=\"20\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>");
            
            xml.append("<Row ss:Height=\"35\">");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"মোট দিন":"Total Days") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"আদায়কৃত":"Done") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"কাজা":"Missed") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"অপেক্ষমান কাজা":"Pending Qaza") + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"ছুটি":"Excused") + "</Data></Cell>");
            xml.append("<Cell ss:MergeAcross=\"2\" ss:StyleID=\"sSumH\"><Data ss:Type=\"String\">" + (isBn?"স্ট্রিক":"Streak") + "</Data></Cell>");
            xml.append("</Row>");
            
            xml.append("<Row ss:Height=\"45\">");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tDays) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tDone) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tMissed) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tQaza) + "</Data></Cell>");
            xml.append("<Cell ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(tExcused) + "</Data></Cell>");
            xml.append("<Cell ss:MergeAcross=\"2\" ss:StyleID=\"sSumV\"><Data ss:Type=\"String\">" + lang.bnNum(streak) + " ★</Data></Cell>");
            xml.append("</Row>");
            xml.append("<Row ss:Height=\"25\"><Cell><Data ss:Type=\"String\"></Data></Cell></Row>");

            xml.append("<Row ss:Height=\"40\">");
            String[] headers = isBn ? new String[]{"তারিখ", "ফজর", "যোহর", "আসর", "মাগরিব", "এশা", "বিতর", "সারসংক্ষেপ"} : new String[]{"Date", "Fajr", "Dhuhr", "Asr", "Maghrib", "Isha", "Witr", "Status"};
            for(String h : headers) xml.append("<Cell ss:StyleID=\"sHead\"><Data ss:Type=\"String\">" + h + "</Data></Cell>");
            xml.append("</Row>");
            
            java.util.Calendar cal = (java.util.Calendar) statsCalPointer.clone(); cal.set(java.util.Calendar.DAY_OF_MONTH, 1);
            for(int i=1; i<=mDays; i++) {
                cal.set(java.util.Calendar.DAY_OF_MONTH, i);
                String dKey = sdf.format(cal.getTime());
                SalahRecord r = getRoomRecord(dKey);
                
                String dateDisplay = isBn ? lang.bnNum(i) + " " + lang.get(new java.text.SimpleDateFormat("MMM", java.util.Locale.US).format(cal.getTime())) + ", " + lang.bnNum(cal.get(java.util.Calendar.YEAR)) : dKey;
                
                xml.append("<Row ss:Height=\"35\">");
                xml.append("<Cell ss:StyleID=\"sDate\"><Data ss:Type=\"String\">" + dateDisplay + "</Data></Cell>");
                
                boolean allDone = true;
                for(String p : prayers) {
                    String s = getFardStat(r, p);
                    String style = s.equals("yes") ? "sYes" : (s.equals("excused") ? "sExc" : "sNo");
                    String txt = s.equals("yes") ? "\u2713 " + (isBn?"সম্পন্ন":"Done") : (s.equals("excused") ? "\u273F " + (isBn?"ছুটি":"Excused") : "\u2715 " + (isBn?"কাজা":"Missed"));
                    xml.append("<Cell ss:StyleID=\"" + style + "\"><Data ss:Type=\"String\">" + txt + "</Data></Cell>");
                    if(!s.equals("yes") && !s.equals("excused")) allDone = false;
                }
                String sStyle = allDone ? "sYes" : "sNo";
                String sTxt = allDone ? (isBn ? "★ আলহামদুলিল্লাহ" : "★ Perfect") : (isBn ? "⚠ অসম্পূর্ণ" : "⚠ Incomplete");
                xml.append("<Cell ss:StyleID=\"" + sStyle + "\"><Data ss:Type=\"String\">" + sTxt + "</Data></Cell>");
                xml.append("</Row>");
            }
            xml.append("</Table></Worksheet></Workbook>");
            pw.write(xml.toString());
            pw.close();
            
            final java.io.File finalFile = file;
            ui.showSmartBanner((android.widget.FrameLayout) activity.findViewById(android.R.id.content), isBn?"সফল":"Success", isBn?"XLS ফাইল সেভ হয়েছে (ওপেন করতে ক্লিক)":"XLS Saved (Click to open)", "img_tick", colorAccent, new Runnable() {
                @Override public void run() {
                    android.content.Intent intent = new android.content.Intent(android.content.Intent.ACTION_VIEW);
                    android.net.Uri uri = androidx.core.content.FileProvider.getUriForFile(activity, activity.getPackageName() + ".provider", finalFile);
                    intent.setDataAndType(uri, "application/vnd.ms-excel");
                    intent.addFlags(android.content.Intent.FLAG_GRANT_READ_URI_PERMISSION);
                    activity.startActivity(android.content.Intent.createChooser(intent, "Open with..."));
                }
            });
        } catch(Exception e) {}
    }"""
        
        c = c[:start_idx] + clean_xls + '\n\n    ' + c[end_idx:]
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("✅ Syntax Fixed! All newlines safely removed and emojis replaced with safe stars/symbols.")
    else:
        print("⚠️ Targets not found. Already fixed?")
