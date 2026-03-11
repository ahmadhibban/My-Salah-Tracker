package com.my.salah.tracker.app.fragments;

import android.animation.ValueAnimator;
import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.graphics.Typeface;
import android.os.Bundle;
import android.text.Layout;
import android.text.StaticLayout;
import android.text.TextPaint;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import androidx.fragment.app.Fragment;
import java.lang.reflect.Field;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import com.my.salah.tracker.app.TasbihDataStore;

public class ZikrFragment extends Fragment {
    class TasbihData {
        String arabic; int target; boolean soundOn;
        TasbihData(String a, int t, boolean s) { this.arabic = a; this.target = t; this.soundOn = s; }
    }

    final ArrayList<TasbihData> tasbihList = new ArrayList<>();
    final int[] currentIdx = {0};
    final int[] individualCounts = new int[200];
    final int[] individualRounds = new int[200];
    final int[] individualTotals = new int[200];
    
    android.media.ToneGenerator toneGen;
    Typeface arabicFont, bnFont;
    float visualBeadPos = 0f; 
    ValueAnimator beadAnim;
    
    final int[][] beadThemes = {
        {Color.parseColor("#111111"), Color.parseColor("#666666")}, 
        {Color.parseColor("#E0E0E0"), Color.parseColor("#FFFFFF")}, 
        {Color.parseColor("#D4AF37"), Color.parseColor("#FFF5C3")}, 
        {Color.parseColor("#B87333"), Color.parseColor("#F5DEB3")}, 
        {Color.parseColor("#5C4033"), Color.parseColor("#8B5A2B")}, 
        {Color.parseColor("#2E8B57"), Color.parseColor("#8FBC8F")}  
    };
    int currentBeadTheme = 2; 

    private Object getField(String name) {
        try { Field f = getActivity().getClass().getDeclaredField(name); f.setAccessible(true); return f.get(getActivity()); } catch (Exception e) { return null; }
    }

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        Context ctx = getContext();
        final int[] themeColors = (int[]) getField("themeColors");
        com.my.salah.tracker.app.LanguageEngine lang = (com.my.salah.tracker.app.LanguageEngine) getField("lang");
        boolean isBnTemp = false; try { isBnTemp = lang.get("Fajr").equals("ফজর"); } catch(Exception e){}
        final boolean isBn = isBnTemp;
        
        final int bgCol = themeColors != null && themeColors.length > 0 ? themeColors[0] : Color.parseColor("#FDFCF0");
        final int cardCol = themeColors != null && themeColors.length > 1 ? themeColors[1] : Color.WHITE;
        final int textCol = themeColors != null && themeColors.length > 2 ? themeColors[2] : Color.BLACK;
        final int accentCol = themeColors != null && themeColors.length > 4 ? themeColors[4] : Color.parseColor("#00BFA5");

        Typeface[] fonts = (Typeface[]) getField("appFonts");
        if (fonts != null && fonts.length > 1) bnFont = fonts[1];

        toneGen = new android.media.ToneGenerator(android.media.AudioManager.STREAM_MUSIC, 100);
        try { arabicFont = Typeface.createFromAsset(ctx.getAssets(), "fonts/al_majeed_quranic_font_shiped.ttf"); } catch (Exception e) {}
        
        android.content.SharedPreferences prefs = ctx.getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE);
        tasbihList.clear();
        ArrayList<TasbihData> allData = new ArrayList<>();
        
        String[] duas = TasbihDataStore.getDuas();
        for(int i=3; i<duas.length; i++) {
            String[] p = duas[i].split("\\|");
            allData.add(new TasbihData(p[0], Integer.parseInt(p[1]), true));
        }
        Collections.sort(allData, (d1, d2) -> Integer.compare(d1.arabic.length(), d2.arabic.length()));
        for(int i=0; i<3; i++) {
            String[] p = duas[i].split("\\|");
            tasbihList.add(new TasbihData(p[0], Integer.parseInt(p[1]), true));
        }
        tasbihList.addAll(allData);
        
        int customCount = prefs.getInt("custom_dua_count", 0);
        for(int i=0; i<customCount; i++) {
            String cDua = prefs.getString("custom_dua_" + i, "");
            int cTarg = prefs.getInt("custom_target_" + i, 33);
            if(!cDua.isEmpty()) tasbihList.add(new TasbihData(cDua, cTarg, true));
        }
        
        for (int i = 0; i < tasbihList.size(); i++) {
            individualCounts[i] = prefs.getInt("ind_" + i, 0);
            individualRounds[i] = prefs.getInt("round_" + i, 0);
            individualTotals[i] = prefs.getInt("total_" + i, 0);
            tasbihList.get(i).target = prefs.getInt("target_custom_" + i, tasbihList.get(i).target);
            tasbihList.get(i).soundOn = prefs.getBoolean("sound_" + i, true);
        }
        
        currentIdx[0] = prefs.getInt("lastIdx", 0);
        if (currentIdx[0] >= tasbihList.size() || currentIdx[0] < 0) currentIdx[0] = 0;
        currentBeadTheme = prefs.getInt("bead_theme", 2);
        visualBeadPos = individualCounts[currentIdx[0]];

        final View circleView = new View(ctx) {
            private String formatNum(int num) {
                String out = String.valueOf(num);
                if (!isBn) return out;
                String[] eng = {"0","1","2","3","4","5","6","7","8","9"}, bng = {"০","১","২","৩","৪","৫","৬","৭","৮","৯"};
                for(int i=0; i<10; i++) out = out.replace(eng[i], bng[i]); return out;
            }
            
            int lastDrawnIdx = -1;

            @Override protected void onDraw(Canvas canvas) {
                super.onDraw(canvas);
                float w = getWidth(), h = getHeight();
                if (w <= 0 || h <= 0) return; 
                float centerX = w / 2.0f;
                Paint p = new Paint(Paint.ANTI_ALIAS_FLAG);
                int idx = currentIdx[0]; 
                TasbihData d = tasbihList.get(idx); int curVal = individualCounts[idx];
                
                if (lastDrawnIdx != idx) { visualBeadPos = curVal; lastDrawnIdx = idx; }

                float boxTop = h * 0.04f, boxHeight = h * 0.17f;
                float circleY = boxTop + boxHeight + (h * 0.22f), radius = w * 0.29f;
                float beadY = circleY + radius + (h * 0.09f);
                float totalBoxY = beadY + (h * 0.14f);
                float themeY = h - (h * 0.05f);

                // --- 1. Salah Tab Style Day/Night Dua Box ---
                RectF boxRect = new RectF(40, boxTop, w - 40, boxTop + boxHeight);
                int hour = java.util.Calendar.getInstance().get(java.util.Calendar.HOUR_OF_DAY);
                boolean isDayTime = (hour >= 6 && hour < 18);
                int[] cardColors = isDayTime ? new int[]{Color.parseColor("#FFB75E"), Color.parseColor("#ED8F03")} 
                                             : new int[]{Color.parseColor("#00C9FF"), Color.parseColor("#1A2980")};
                android.graphics.LinearGradient lg = new android.graphics.LinearGradient(
                    40, boxTop, w-40, boxTop+boxHeight, cardColors[0], cardColors[1], android.graphics.Shader.TileMode.CLAMP);
                p.setShader(lg); p.setShadowLayer(15f, 0, 10f, Color.argb(60, 0, 0, 0));
                canvas.drawRoundRect(boxRect, 50f, 50f, p); p.clearShadowLayer(); p.setShader(null);

                TextPaint tp = new TextPaint(Paint.ANTI_ALIAS_FLAG);
                if(arabicFont != null) tp.setTypeface(arabicFont); 
                tp.setColor(Color.WHITE); tp.setShadowLayer(5f, 0f, 2f, Color.argb(150, 0,0,0));
                int layoutWidth = (int)(w - 100); 
                if (layoutWidth > 0) {
                    float autoFontSize = 95f; android.text.StaticLayout sl;
                    while (true) {
                        tp.setTextSize(autoFontSize);
                        sl = new android.text.StaticLayout(d.arabic, tp, layoutWidth, android.text.Layout.Alignment.ALIGN_CENTER, 1.1f, 0.0f, false);
                        if (sl.getHeight() <= (boxHeight - 40f) || autoFontSize <= 35f) break; autoFontSize -= 2f; 
                    }
                    canvas.save(); canvas.translate(centerX - (layoutWidth / 2f), boxTop + (boxHeight - sl.getHeight()) / 2f);
                    sl.draw(canvas); canvas.restore(); tp.clearShadowLayer();
                }

                // --- 2. Dynamic 3D Progress Ring & Ball ---
                int themeMain = accentCol;
                float sweep = (d.target > 0) ? ((float)curVal / d.target) * 360f : 0f;
                float rOuter = radius + 25f;
                
                // বৃত্তের বর্ডার (গ্রে কালার মুছে থিমের কালার বসানো হয়েছে)
                android.graphics.SweepGradient themeRing = new android.graphics.SweepGradient(centerX, circleY, new int[]{cardCol, themeMain, cardCol, themeMain, cardCol}, null);
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(30f); p.setShader(themeRing); p.setShadowLayer(20f, 0, 15f, Color.argb(120,0,0,0));
                canvas.drawCircle(centerX, circleY, rOuter, p); p.clearShadowLayer(); p.setShader(null);
                
                p.setStrokeWidth(15f); p.setColor(Color.argb(40, 0,0,0)); canvas.drawCircle(centerX, circleY, radius, p);
                
                // প্রোগ্রেস লাইন
                p.setStrokeWidth(22f); p.setStrokeCap(Paint.Cap.ROUND); p.setColor(themeMain);
                canvas.drawArc(new RectF(centerX-radius, circleY-radius, centerX+radius, circleY+radius), -90, sweep, false, p);
                
                // ৩ডি বল (সাদা থেকে থিম কালারের গ্রেডিয়েন্ট)
                double angle = Math.toRadians(sweep - 90);
                float ballX = (float) (centerX + radius * Math.cos(angle)), ballY = (float) (circleY + radius * Math.sin(angle));
                p.setStyle(Paint.Style.FILL); 
                android.graphics.RadialGradient ballRg = new android.graphics.RadialGradient(ballX-5, ballY-5, 30f, Color.WHITE, themeMain, android.graphics.Shader.TileMode.CLAMP);
                p.setShader(ballRg); p.setShadowLayer(10, 0, 5, Color.argb(100,0,0,0));
                canvas.drawCircle(ballX, ballY, 24f, p); p.clearShadowLayer(); p.setShader(null);

                p.setStyle(Paint.Style.FILL); if(bnFont != null) p.setTypeface(bnFont); p.setColor(textCol); 
                String mainCountStr = formatNum(curVal); String targetPart = " / " + formatNum(d.target); 
                p.setTextSize(260f); float mainTextWidth = p.measureText(mainCountStr);
                Paint targetPaint = new Paint(p); targetPaint.setTextSize(55f); targetPaint.setColor(themeMain); 
                targetPaint.setUnderlineText(true); 
                float targetWidth = targetPaint.measureText(targetPart); float startX = centerX - ((mainTextWidth + targetWidth) / 2f);
                p.setTextAlign(Paint.Align.LEFT); canvas.drawText(mainCountStr, startX, circleY + 85f, p);
                targetPaint.setTextAlign(Paint.Align.LEFT); canvas.drawText(targetPart, startX + mainTextWidth, circleY + 85f, targetPaint);

                // --- 3. 3D Premium U-Curve Beads ---
                float bRad = 45f, spacing = 85f, gapSize = 150f, dip = 110f;
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(8f); p.setColor(Color.parseColor("#C19A6B"));
                Path sPath = new Path(); sPath.moveTo(-50, beadY); sPath.quadTo(centerX, beadY + dip * 2.1f, w + 50, beadY);
                canvas.drawPath(sPath, p);

                for(int i = curVal - 15; i <= curVal + 15; i++) {
                    float rel = i - visualBeadPos; 
                    float bx;
                    if (rel <= 0) bx = centerX - gapSize/2f - Math.abs(rel) * spacing; 
                    else if (rel >= 1) bx = centerX + gapSize/2f + (rel - 1f) * spacing; 
                    else bx = centerX + gapSize/2f - (1f - rel) * gapSize; 

                    if (bx < -50 || bx > w + 50) continue;
                    float dx = bx - centerX; float maxDx = w / 2f;
                    float by = beadY + dip * (1f - (dx * dx) / (maxDx * maxDx)); 

                    p.setStyle(Paint.Style.FILL);
                    android.graphics.RadialGradient woodRg = new android.graphics.RadialGradient(bx - 12f, by - 12f, bRad * 1.5f, new int[]{beadThemes[currentBeadTheme][1], beadThemes[currentBeadTheme][0], Color.BLACK}, new float[]{0f, 0.6f, 1f}, android.graphics.Shader.TileMode.CLAMP);
                    p.setShader(woodRg); p.setShadowLayer(20f, 5f, 10f, Color.argb(150, 0, 0, 0)); 
                    canvas.drawCircle(bx, by, bRad, p); p.clearShadowLayer(); p.setShader(null);
                    p.setColor(Color.argb(160, 255, 255, 255)); canvas.drawOval(new RectF(bx - 18f, by - 35f, bx + 8f, by - 12f), p);
                }

                // --- 4. Dynamic Themed Total Box ---
                String totalTxt = (isBn ? "সর্বমোট: " : "Total: ") + formatNum(individualTotals[idx]) + "  |  " + (isBn ? "রাউন্ড: " : "Loop: ") + formatNum(individualRounds[idx]);
                p.setTextSize(40f); float boxW = p.measureText(totalTxt) + 80; if(bnFont != null) p.setTypeface(bnFont);
                
                RectF totalRect = new RectF(centerX - boxW/2, totalBoxY - 40, centerX + boxW/2, totalBoxY + 40);
                // themeMain আগেই তৈরি করা আছে, তাই এখানে নতুন করে লেখার দরকার নেই
                
                // থিম কালারে হালকা ফিল (Background)
                p.setStyle(Paint.Style.FILL); p.setColor(themeMain); p.setAlpha(30);
                canvas.drawRoundRect(totalRect, 40f, 40f, p); p.setAlpha(255);
                
                // থিম কালারে স্পষ্ট বর্ডার
                p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(4f); p.setColor(themeMain);
                canvas.drawRoundRect(totalRect, 40f, 40f, p);
                
                // লেখা মাঝখানে রাখা
                p.setStyle(Paint.Style.FILL); p.setColor(textCol); p.setTextAlign(Paint.Align.CENTER);
                canvas.drawText(totalTxt, centerX, totalBoxY + 12, p);

                // --- 5. Theme Selector ---
                float themeSpacing = w / 7f, themeRadius = 30f;
                for(int i = 0; i < beadThemes.length; i++) {
                    float tx = themeSpacing * (i + 1); p.setStyle(Paint.Style.FILL);
                    android.graphics.RadialGradient trg = new android.graphics.RadialGradient(tx - 10f, themeY - 10f, themeRadius*1.5f, new int[]{beadThemes[i][1], beadThemes[i][0], Color.BLACK}, new float[]{0f, 0.7f, 1f}, android.graphics.Shader.TileMode.CLAMP);
                    p.setShader(trg); if (currentBeadTheme == i) p.setShadowLayer(15f, 0f, 0f, accentCol); else p.setShadowLayer(8f, 2f, 5f, Color.argb(100,0,0,0));
                    canvas.drawCircle(tx, themeY, themeRadius, p); p.clearShadowLayer(); p.setShader(null);
                    p.setColor(Color.argb(120, 255, 255, 255)); canvas.drawOval(new RectF(tx-12, themeY-20, tx+5, themeY-8), p);
                    if (currentBeadTheme == i) { p.setStyle(Paint.Style.STROKE); p.setStrokeWidth(5f); p.setColor(accentCol); canvas.drawCircle(tx, themeY, themeRadius + 10f, p); }
                }
            }
            private float getColorHue(int color) { float[] hsv = new float[3]; Color.colorToHSV(color, hsv); return hsv[0]; }
        };

        circleView.setOnTouchListener(new View.OnTouchListener() {
            float startX, startY; boolean isDraggingBeads = false;
            long downTime = 0;

            private void triggerBeadAnimation(final View v, float target) {
                if (beadAnim != null) beadAnim.cancel();
                beadAnim = ValueAnimator.ofFloat(visualBeadPos, target);
                beadAnim.setDuration(300); 
                beadAnim.setInterpolator(new android.view.animation.DecelerateInterpolator());
                beadAnim.addUpdateListener(anim -> { visualBeadPos = (float) anim.getAnimatedValue(); v.invalidate(); });
                beadAnim.start();
            }

            @Override public boolean onTouch(final View v, MotionEvent event) {
                float x = event.getX(), y = event.getY(), w = v.getWidth(), h = v.getHeight(), centerX = w / 2.0f;
                float boxTop = h * 0.04f, boxHeight = h * 0.17f, circleY = boxTop + boxHeight + (h * 0.18f), radius = w * 0.32f, beadY = circleY + radius + (h * 0.09f), themeY = h - (h * 0.05f);
                final int idx = currentIdx[0];

                if (event.getAction() == MotionEvent.ACTION_DOWN) { 
                    startX = x; startY = y; downTime = System.currentTimeMillis();
                    if (y > beadY - 120 && y < beadY + 150) { isDraggingBeads = true; return true; }
                    return true; 
                }
                if (event.getAction() == MotionEvent.ACTION_UP) {
                    long pressDuration = System.currentTimeMillis() - downTime;
                    float deltaX = x - startX, deltaY = y - startY;

                    // 1. Multi-Bead Drag Logic
                    if (isDraggingBeads) {
                        isDraggingBeads = false;
                        int beadsMoved = Math.round(Math.abs(deltaX) / 85f);
                        if (beadsMoved == 0 && Math.abs(deltaX) < 20) beadsMoved = 1; 
                        
                        if (deltaX < -30) incrementCount(idx, v, beadsMoved); 
                        else if (deltaX > 30) decrementCount(idx, v, beadsMoved); 
                        else incrementCount(idx, v, 1); 
                        return true;
                    }
                    
                    if (y > themeY - 60) {
                        float themeSpacing = w / 7f;
                        for(int i = 0; i < beadThemes.length; i++) {
                            if (Math.abs(x - (themeSpacing * (i + 1))) < 50) {
                                currentBeadTheme = i; v.getContext().getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE).edit().putInt("bead_theme", i).apply(); v.invalidate(); return true;
                            }
                        }
                    }
                    
                    // 2. Long Press Reset & Target Click
                    if (Math.sqrt(Math.pow(x - centerX, 2) + Math.pow(y - circleY, 2)) <= radius + 30) { 
                        if (pressDuration > 600 && Math.abs(deltaX) < 30 && Math.abs(deltaY) < 30) {
                            showModernResetDialog(v, idx, isBn, cardCol, textCol); 
                        } else {
                            if (x > centerX && y > circleY && y < circleY + 140) {
                                showEditTargetDialog(v, idx, isBn, cardCol, textCol, accentCol); 
                            } else {
                                incrementCount(idx, v, 1); 
                            }
                        }
                        return true; 
                    }
                    
                    // 3. Swipe Dua Box for Settings
                    if (y > boxTop && y < boxTop + boxHeight) {
                        if (Math.abs(deltaX) > 100) {
                            if (deltaX < 0) currentIdx[0] = (currentIdx[0] + 1) % tasbihList.size();
                            else currentIdx[0] = (currentIdx[0] - 1 + tasbihList.size()) % tasbihList.size();
                            v.getContext().getSharedPreferences("TasbihPrefs", 0).edit().putInt("lastIdx", currentIdx[0]).apply();
                            v.invalidate(); return true;
                        } else if (Math.abs(deltaX) < 20 && Math.abs(y - startY) < 20) { showModernSettingsDialog(v, isBn, bgCol, cardCol, textCol, accentCol); return true; }
                    }
                } return true;
            }

            private void incrementCount(int idx, View v, int amount) {
                if (idx >= tasbihList.size() || amount <= 0) return;
                individualCounts[idx] += amount; individualTotals[idx] += amount;
                if (tasbihList.get(idx).soundOn && toneGen != null) toneGen.startTone(android.media.ToneGenerator.TONE_PROP_BEEP, 100);
                v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                if (individualCounts[idx] >= tasbihList.get(idx).target && tasbihList.get(idx).target > 0) { 
                    individualCounts[idx] = individualCounts[idx] % tasbihList.get(idx).target; 
                    individualRounds[idx]++; 
                }
                v.getContext().getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE).edit().putInt("ind_" + idx, individualCounts[idx]).putInt("total_" + idx, individualTotals[idx]).putInt("round_" + idx, individualRounds[idx]).apply();
                triggerBeadAnimation(v, individualCounts[idx]);
            }

            private void decrementCount(int idx, View v, int amount) {
                if (idx >= tasbihList.size() || amount <= 0) return;
                if (individualCounts[idx] >= amount) {
                    individualCounts[idx] -= amount; if (individualTotals[idx] >= amount) individualTotals[idx] -= amount;
                    v.performHapticFeedback(android.view.HapticFeedbackConstants.VIRTUAL_KEY);
                    v.getContext().getSharedPreferences("TasbihPrefs", Context.MODE_PRIVATE).edit().putInt("ind_" + idx, individualCounts[idx]).putInt("total_" + idx, individualTotals[idx]).apply();
                    triggerBeadAnimation(v, individualCounts[idx]);
                }
            }

            private void showModernResetDialog(final View v, int idx, boolean isBn, int card, int txt) {
                final android.app.Dialog d = new android.app.Dialog(v.getContext());
                d.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));
                LinearLayout root = new LinearLayout(v.getContext()); root.setOrientation(LinearLayout.VERTICAL); root.setPadding(80, 80, 80, 80);
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
                gd.setColor(card); gd.setCornerRadius(60f); root.setBackground(gd);
                
                TextView t = new TextView(v.getContext()); t.setText(isBn ? "রিসেট করতে চান?" : "Reset Tasbih?"); t.setTextSize(22f); t.setTextColor(android.graphics.Color.WHITE); t.setTypeface(Typeface.DEFAULT_BOLD); t.setGravity(Gravity.CENTER); root.addView(t);
                
                LinearLayout btns = new LinearLayout(v.getContext()); btns.setOrientation(LinearLayout.HORIZONTAL); btns.setPadding(0, 60, 0, 0);
                Button bNo = new Button(v.getContext()); bNo.setText(isBn ? "না" : "No"); bNo.setBackgroundColor(Color.TRANSPARENT); bNo.setTextColor(Color.GRAY); bNo.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
                Button bYes = new Button(v.getContext()); bYes.setText(isBn ? "হ্যাঁ" : "Yes"); bYes.setBackgroundColor(Color.TRANSPARENT); bYes.setTextColor(Color.RED); bYes.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 1f));
                
                bNo.setOnClickListener(v2 -> d.dismiss());
                bYes.setOnClickListener(v2 -> {
                    individualCounts[idx] = 0; individualTotals[idx] = 0; individualRounds[idx] = 0; triggerBeadAnimation(v, 0); 
                    v.getContext().getSharedPreferences("TasbihPrefs", 0).edit().putInt("ind_"+idx, 0).putInt("total_"+idx, 0).putInt("round_"+idx, 0).apply(); d.dismiss();
                });
                btns.addView(bNo); btns.addView(bYes); root.addView(btns); d.setContentView(root); d.show();
            }

            private void showEditTargetDialog(final View v, int idx, boolean isBn, int card, int txt, int acc) {
                final android.app.Dialog d = new android.app.Dialog(v.getContext());
                d.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));
                LinearLayout root = new LinearLayout(v.getContext()); root.setOrientation(LinearLayout.VERTICAL); root.setPadding(80, 80, 80, 80);
                android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable();
                gd.setColor(card); gd.setCornerRadius(60f); root.setBackground(gd);
                
                TextView t = new TextView(v.getContext()); t.setText(isBn ? "নতুন টার্গেট দিন" : "Edit Target"); t.setTextSize(20f); t.setTextColor(android.graphics.Color.WHITE); t.setGravity(Gravity.CENTER); root.addView(t);
                final EditText et = new EditText(v.getContext()); et.setInputType(2); et.setText(String.valueOf(tasbihList.get(idx).target)); et.setTextColor(android.graphics.Color.WHITE); root.addView(et);
                
                Button bOk = new Button(v.getContext()); bOk.setText(isBn ? "সেভ করুন" : "Save"); bOk.setBackgroundColor(acc); bOk.setTextColor(android.graphics.Color.WHITE);
                bOk.setOnClickListener(v2 -> {
                    if(!et.getText().toString().isEmpty()){
                        tasbihList.get(idx).target = Integer.parseInt(et.getText().toString());
                        v.getContext().getSharedPreferences("TasbihPrefs", 0).edit().putInt("target_custom_"+idx, tasbihList.get(idx).target).apply();
                        v.invalidate(); d.dismiss();
                    }
                });
                root.addView(bOk); d.setContentView(root); d.show();
            }

            private void showModernSettingsDialog(final View v, boolean isBn, int bg, int card, int txt, int acc) {
                final android.app.Dialog d = new android.app.Dialog(v.getContext(), android.R.style.Theme_Black_NoTitleBar_Fullscreen);
                LinearLayout rootDia = new LinearLayout(v.getContext()); rootDia.setOrientation(LinearLayout.VERTICAL); rootDia.setBackgroundColor(bg); rootDia.setPadding(40, 80, 40, 40);

                TextView t1 = new TextView(v.getContext()); t1.setText(isBn ? "তাসবিহ সেটিংস" : "Tasbih Settings"); t1.setTextColor(acc); t1.setTextSize(28); t1.setGravity(Gravity.CENTER); t1.setTypeface(Typeface.DEFAULT_BOLD); rootDia.addView(t1);

                LinearLayout head = new LinearLayout(v.getContext()); head.setPadding(10, 40, 10, 20); head.setWeightSum(10f);
                TextView hDua = new TextView(v.getContext()); hDua.setText(isBn?"দোয়া":"Dua"); hDua.setTextColor(Color.GRAY); hDua.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 6f)); hDua.setGravity(Gravity.CENTER);
                TextView hTarg = new TextView(v.getContext()); hTarg.setText(isBn?"টার্গেট":"Target"); hTarg.setTextColor(Color.GRAY); hTarg.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 2f)); hTarg.setGravity(Gravity.CENTER);
                TextView hSnd = new TextView(v.getContext()); hSnd.setText(isBn?"সাউন্ড":"Sound"); hSnd.setTextColor(Color.GRAY); hSnd.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 2f)); hSnd.setGravity(Gravity.CENTER);
                head.addView(hDua); head.addView(hTarg); head.addView(hSnd); rootDia.addView(head);

                ScrollView sv = new ScrollView(v.getContext());
                LinearLayout listBody = new LinearLayout(v.getContext()); listBody.setOrientation(LinearLayout.VERTICAL);

                for (int i = 0; i < tasbihList.size(); i++) {
                    final int rowIdx = i;
                    LinearLayout row = new LinearLayout(v.getContext()); row.setPadding(20, 40, 20, 40); row.setWeightSum(10f); row.setGravity(Gravity.CENTER_VERTICAL);
                    android.graphics.drawable.GradientDrawable rowBg = new android.graphics.drawable.GradientDrawable(); rowBg.setColor(card); rowBg.setCornerRadius(30f); row.setBackground(rowBg);
                    LinearLayout.LayoutParams rowParams = new LinearLayout.LayoutParams(-1, -2); rowParams.setMargins(0, 0, 0, 20); row.setLayoutParams(rowParams);

                    TextView tvDua = new TextView(v.getContext()); tvDua.setText(tasbihList.get(rowIdx).arabic); tvDua.setTextColor(android.graphics.Color.WHITE); tvDua.setTextSize(24); tvDua.setGravity(Gravity.CENTER); tvDua.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 6f));
                    if(arabicFont != null) tvDua.setTypeface(arabicFont);
                    tvDua.setOnClickListener(v2 -> { currentIdx[0] = rowIdx; v.invalidate(); d.dismiss(); });

                    TextView tvTarg = new TextView(v.getContext()); tvTarg.setText(String.valueOf(tasbihList.get(rowIdx).target)); tvTarg.setTextColor(acc); tvTarg.setTextSize(20); tvTarg.setGravity(Gravity.CENTER); tvTarg.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 2f));
                    tvTarg.setOnClickListener(v3 -> { d.dismiss(); showEditTargetDialog(v, rowIdx, isBn, card, txt, acc); });
                    
                    TextView tvSnd = new TextView(v.getContext()); tvSnd.setText(tasbihList.get(rowIdx).soundOn ? "🔊" : "🔇"); tvSnd.setTextSize(22); tvSnd.setGravity(Gravity.CENTER); tvSnd.setLayoutParams(new LinearLayout.LayoutParams(0, -2, 2f));
                    tvSnd.setOnClickListener(v3 -> {
                        tasbihList.get(rowIdx).soundOn = !tasbihList.get(rowIdx).soundOn; tvSnd.setText(tasbihList.get(rowIdx).soundOn ? "🔊" : "🔇");
                        v.getContext().getSharedPreferences("TasbihPrefs", 0).edit().putBoolean("sound_"+rowIdx, tasbihList.get(rowIdx).soundOn).apply();
                    });
                    row.addView(tvDua); row.addView(tvTarg); row.addView(tvSnd); listBody.addView(row);
                }
                
                Button btnAddNew = new Button(v.getContext()); btnAddNew.setText(isBn ? "+ নতুন দোয়া যুক্ত করুন" : "+ Add New Tasbih"); btnAddNew.setBackgroundColor(Color.TRANSPARENT); btnAddNew.setTextColor(acc);
                btnAddNew.setOnClickListener(v2 -> {
                    d.dismiss();
                    final android.app.Dialog dAdd = new android.app.Dialog(v.getContext()); dAdd.getWindow().setBackgroundDrawable(new android.graphics.drawable.ColorDrawable(Color.TRANSPARENT));
                    LinearLayout rootAdd = new LinearLayout(v.getContext()); rootAdd.setOrientation(LinearLayout.VERTICAL); rootAdd.setPadding(80, 80, 80, 80);
                    android.graphics.drawable.GradientDrawable gd = new android.graphics.drawable.GradientDrawable(); gd.setColor(card); gd.setCornerRadius(60f); rootAdd.setBackground(gd);
                    
                    EditText etDua = new EditText(v.getContext()); etDua.setHint(isBn?"আরবী দোয়া লিখুন":"Enter Arabic Dua"); etDua.setTextColor(android.graphics.Color.WHITE); etDua.setHintTextColor(Color.GRAY); rootAdd.addView(etDua);
                    EditText etTarget = new EditText(v.getContext()); etTarget.setHint(isBn?"টার্গেট (ঐচ্ছিক)":"Target (Optional)"); etTarget.setInputType(2); etTarget.setTextColor(android.graphics.Color.WHITE); etTarget.setHintTextColor(Color.GRAY); rootAdd.addView(etTarget);
                    
                    Button bSave = new Button(v.getContext()); bSave.setText(isBn?"সেভ":"Save"); bSave.setBackgroundColor(acc); bSave.setTextColor(android.graphics.Color.WHITE);
                    bSave.setOnClickListener(v3 -> {
                        String newDua = etDua.getText().toString(); String tStr = etTarget.getText().toString();
                        if(!newDua.isEmpty()){
                            int newTarg = tStr.isEmpty() ? 0 : Integer.parseInt(tStr);
                            android.content.SharedPreferences p = v.getContext().getSharedPreferences("TasbihPrefs", 0);
                            int cCount = p.getInt("custom_dua_count", 0);
                            p.edit().putString("custom_dua_"+cCount, newDua).putInt("custom_target_"+cCount, newTarg).putBoolean("sound_"+tasbihList.size(), true).putInt("custom_dua_count", cCount+1).apply();
                            tasbihList.add(new TasbihData(newDua, newTarg, true)); currentIdx[0] = tasbihList.size()-1; p.edit().putInt("lastIdx", currentIdx[0]).apply();
                            v.invalidate(); dAdd.dismiss();
                        }
                    });
                    rootAdd.addView(bSave); dAdd.setContentView(rootAdd); dAdd.show();
                });
                listBody.addView(btnAddNew);
                sv.addView(listBody); rootDia.addView(sv, new LinearLayout.LayoutParams(-1, 0, 1f));

                Button btnClose = new Button(v.getContext()); btnClose.setText(isBn ? "বন্ধ করুন" : "Close"); btnClose.setBackgroundColor(card); btnClose.setTextColor(android.graphics.Color.WHITE);
                btnClose.setOnClickListener(v4 -> d.dismiss()); rootDia.addView(btnClose);
                
                d.setContentView(rootDia); d.show();
            }
        });

        LinearLayout root = new LinearLayout(ctx);
        root.setLayoutParams(new ViewGroup.LayoutParams(-1, -1));
        root.setBackgroundColor(bgCol);
        root.addView(circleView, new LinearLayout.LayoutParams(-1, -1));
        return root;
    }
}
