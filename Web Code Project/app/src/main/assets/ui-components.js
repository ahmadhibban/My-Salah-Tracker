const SoftNoise = `url('data:image/svg+xml;utf8,<svg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"><filter id="n"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="3" stitchTiles="stitch"/></filter><rect width="100%" height="100%" filter="url(%23n)" opacity="0.06"/></svg>')`;

const GlobalCSS = `
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700;900&family=Amiri:wght@700&family=Plus+Jakarta+Sans:wght@500;700;800;900&display=swap');

    .header-top { display: flex; justify-content: space-between; align-items: center; width: 100%; height: 100%; gap: 10px; }
    .english-date-3d { flex: 1.4; background: linear-gradient(135deg, #3A4750 0%, #28313B 100%); padding: 0 10px; border-radius: 12px; font-size: 13px; font-weight: 800; color: #FFF; display: flex; align-items: center; justify-content: center; height: 100%; box-shadow: inset 2px 2px 3px rgba(255,255,255,0.2), inset -1px -1px 3px rgba(0,0,0,0.5), 1px 1px 0px #181C1E, 2px 2px 0px #181C1E, 4px 5px 8px rgba(0,0,0,0.3); border-top: 1px solid rgba(255,255,255,0.3); border-left: 1px solid rgba(255,255,255,0.1); cursor: pointer; transition: transform 0.1s; }
    .english-date-3d:active { transform: scale(0.97); }
    .streak-badge { flex: 0.8; background: linear-gradient(135deg, #1A6D96 0%, #0D415C 100%); padding: 0 10px; border-radius: 12px; font-size: 13px; font-weight: 900; color: #FFF; display: flex; align-items: center; justify-content: center; height: 100%; box-shadow: inset 2px 2px 3px rgba(255,255,255,0.4), inset -1px -1px 3px rgba(0,0,0,0.2), 1px 1px 0px #0D1C33, 2px 2px 0px #0D1C33, 4px 5px 8px rgba(0,0,0,0.3); text-shadow: 1px 2px 2px rgba(0,0,0,0.6); border-top: 1px solid rgba(255,255,255,0.3); border-left: 1px solid rgba(255,255,255,0.15); }
    
    .login-box-3d { flex-shrink: 0; min-width: 42px; width: 42px; height: 42px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: inset 2px 2px 3px rgba(255,255,255,1), inset -1px -1px 3px rgba(0,0,0,0.1), 1px 1px 0px #97A0A5, 2px 2px 0px #97A0A5, 4px 5px 8px rgba(0,0,0,0.2); cursor: pointer; border-top: 1px solid #FFF; border-left: 1px solid #FFF; transition: transform 0.1s; box-sizing: border-box; }
    .login-box-3d:active { transform: translateY(2px); box-shadow: inset 2px 3px 5px rgba(0,0,0,0.2), inset -1px -1px 2px rgba(255,255,255,0.5); }
    .engraved-icon-head { filter: drop-shadow(1px 1px 0px #FFF); width: 20px; height: 20px; }

    .ultra-tasbih-card { width: 100%; height: 100%; border-radius: 20px; padding: 12px 15px; box-sizing: border-box; background: linear-gradient(135deg, #0a4f70 0%, #032b45 100%); box-shadow: inset 3px 4px 6px rgba(255, 255, 255, 0.25), inset -3px -3px 8px rgba(0, 0, 0, 0.6), 1px 1px 0px #021a2a, 2px 2px 0px #021a2a, 4px 6px 15px rgba(3, 43, 69, 0.5); border-top: 1.5px solid rgba(255, 255, 255, 0.35); border-left: 1.5px solid rgba(255, 255, 255, 0.2); display: flex; align-items: center; justify-content: space-between; position: relative; overflow: hidden; font-family: 'Plus Jakarta Sans', sans-serif; }
    .ultra-tasbih-card::before { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%); pointer-events: none; }
    .tasbih-info { flex: 1.2; display: flex; flex-direction: column; justify-content: center; align-items: center; z-index: 2; padding-right: 12px; text-align: center; min-width: 0; }
    .t-arabic { font-family: 'Amiri', serif; font-size: 24px; color: #e2f1f8; direction: rtl; text-shadow: 0 2px 6px rgba(0,0,0,0.6); margin-bottom: 0; padding: 6px 0 2px 0; line-height: 1.4; white-space: nowrap; overflow: visible; width: 100%; text-align: center; }
    .t-divider { width: 70%; height: 1px; background: linear-gradient(90deg, #fff0, #fff3, #fff0); margin: 6px 0; }
    .t-pronounce { font-size: 13px; color: #00fa9a; font-weight: 700; text-shadow: 0 0 5px rgba(0, 250, 154, 0.3); margin-bottom: 2px; letter-spacing: 0.5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; }
    .t-meaning { font-size: 11px; color: #a4c6db; font-weight: 600; margin-bottom: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; width: 100%; }
    
    .t-btn-group { display: flex; gap: 10px; justify-content: center; width: 100%; }
    .t-icon-btn { width: 30px; height: 30px; border-radius: 50%; background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0)); border: 1px solid rgba(255,255,255,0.2); display: flex; justify-content: center; align-items: center; box-shadow: 3px 3px 10px rgba(0,0,0,0.4), -2px -2px 10px rgba(255,255,255,0.05); cursor: pointer; transition: 0.1s; }
    .t-icon-btn:active { transform: scale(0.92); box-shadow: inset 3px 3px 6px rgba(0,0,0,0.6); }
    .t-icon-btn svg { width: 15px; height: 15px; stroke-width: 2.5; fill: none; stroke: currentColor; }
    .t-ring-wrapper { flex-shrink: 0; display: flex; flex-direction: column; align-items: center; z-index: 2; }
    .t-ring-container { position: relative; width: 115px; height: 115px; border-radius: 50%; background: rgba(10, 60, 87, 0.3); border: 1px solid rgba(255,255,255,0.1); box-shadow: 4px 4px 12px rgba(0,0,0,0.4), -4px -4px 12px rgba(255,255,255,0.06); display: flex; justify-content: center; align-items: center; cursor: pointer; transition: transform 0.1s; -webkit-tap-highlight-color: transparent; }
    .t-ring-container:active { transform: scale(0.96); box-shadow: 2px 2px 6px rgba(0,0,0,0.4), -2px -2px 6px rgba(255,255,255,0.06); }
    .t-svg-ring { position: absolute; width: 100%; height: 100%; transform: rotate(-90deg); pointer-events: none; overflow: visible;}
    .t-bg-circle { fill: none; stroke: rgba(255,255,255,0.06); stroke-width: 8; }
    .t-pr-circle { fill: none; stroke: #00fa9a; stroke-width: 8; stroke-linecap: round; stroke-dasharray: 314.16; transition: stroke-dashoffset 0.25s ease; filter: drop-shadow(0 0 6px #00fa9a); }
    .t-marble { position: absolute; width: 26px; height: 26px; border-radius: 50%; background: radial-gradient(circle at 35% 35%,#e6ffff 0%,#80e5ff 15%,#0099cc 40%,#004d66 70%,#001a22 100%); box-shadow: inset -3px -3px 8px rgba(0,0,0,0.8), inset 3px 3px 8px rgba(255,255,255,0.9), 0 4px 10px rgba(0, 255, 255, 0.5); z-index: 10; transform: translate(-50%, -50%); pointer-events: none; transition: left 0.25s ease, top 0.25s ease; }
    
    .t-count-display { position: absolute; display: flex; align-items: baseline; pointer-events: none; }
    .v-num { font-size: 34px; font-weight: 900; color: #FFF; text-shadow: 0 3px 6px rgba(0,0,0,0.7); line-height: 1; font-family: 'Outfit', sans-serif;}
    .t-limit-btn { height: 24px; padding: 0 14px; border-radius: 14px; font-size: 13px; font-weight: 800; background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(0,0,0,0.25)); color: #8ab4cd; display: flex; align-items: center; justify-content: center; cursor:pointer; box-shadow: inset 1px 1px 3px rgba(255,255,255,0.25), inset -1px -1px 3px rgba(0,0,0,0.5), 1px 2px 4px rgba(0,0,0,0.3); text-shadow: 1px 1px 2px rgba(0,0,0,0.8); border-top: 1px solid rgba(255,255,255,0.2); border-left: 1px solid rgba(255,255,255,0.1); margin-top: -8px; z-index: 5; transition: 0.1s; }
    .t-limit-btn:active { transform: scale(0.95); box-shadow: inset 2px 3px 6px rgba(0,0,0,0.6); }

    input[type=number]::-webkit-inner-spin-button, input[type=number]::-webkit-outer-spin-button { -webkit-appearance: none; margin: 0; }
    input[type=number] { -moz-appearance: textfield; }

    .modal-btn { transition: transform 0.1s ease; }
    .modal-btn:active { transform: scale(0.96); box-shadow: inset 2px 3px 6px rgba(0,0,0,0.2) !important; }

    .days-row { display: flex; justify-content: space-between; align-items: center; width: 100%; height: 100%; }
    .day-wrapper { width: 36px; height: 100%; display: flex; justify-content: center; align-items: center; }
    .day-btn { width: 22px; height: 26px; border-radius: 6px; display: flex; justify-content: center; align-items: center; font-size: 10px; font-weight: 800; background: linear-gradient(135deg, #FFFFFF 0%, #DFDBD2 100%); color: #5C5547; box-shadow: inset 2px 2px 3px #FFF, inset -1px -1px 2px rgba(0,0,0,0.05), 1px 1px 0px #BCB4A4, 2px 2px 0px #BCB4A4, 3px 4px 6px rgba(0,0,0,0.12); text-shadow: 1px 1px 1px #FFF; cursor: pointer; border-top: 1px solid rgba(255,255,255,1); border-left: 1px solid rgba(255,255,255,0.7); transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
    .day-btn.active { width: 34px; height: 38px; border-radius: 10px; font-size: 14px; background: linear-gradient(135deg, #5D9DF5 0%, #224E91 100%); color: #FFF; box-shadow: inset 2px 2px 3px rgba(255,255,255,0.5), inset -2px -2px 4px rgba(0,0,0,0.2), 1px 1px 0px #133366, 2px 2px 0px #133366, 4px 5px 10px rgba(0,0,0,0.3); text-shadow: 1px 2px 2px rgba(0,0,0,0.5); border-top: 1px solid rgba(255,255,255,0.3); border-left: 1px solid rgba(255,255,255,0.2); }
    .day-btn:active { transform: scale(0.92); box-shadow: inset 2px 3px 5px rgba(0,0,0,0.15), inset -1px -1px 2px rgba(255,255,255,0.5); }

    .actions-row { display: flex; gap: 12px; width: 100%; height: 100%; }
    .action-btn { flex: 1; height: 100%; border-radius: 8px; display: flex; justify-content: center; align-items: center; gap: 6px; font-size: 12px; font-weight: 850; color: #444E51; text-shadow: 1px 1px 1px #FFF; background: linear-gradient(135deg, #FFFFFF 0%, #E0DED3 100%); box-shadow: inset 2px 3px 4px rgba(255, 255, 255, 1), inset -1px -1px 3px rgba(0,0,0,0.05), 1px 1px 0px #BCB8A7, 2px 2px 0px #BCB8A7, 3px 3px 0px #BCB8A7, 4px 5px 10px rgba(0, 0, 0, 0.15); border-top: 1px solid rgba(255, 255, 255, 1); border-left: 1px solid rgba(255,255,255,0.7); cursor: pointer; transition: all 0.1s; }
    .engraved-icon { filter: drop-shadow(1px 1px 0px rgba(255,255,255,1)) drop-shadow(0px 1px 1px rgba(0,0,0,0.1)); width: 14px; height: 14px; }
    .action-btn:active { transform: translateY(3px) scale(0.98); box-shadow: inset 2px 3px 6px rgba(0,0,0,0.12), inset -2px -2px 4px rgba(255,255,255,0.8), 0px 0px 0px #BCB8A7, 1px 2px 4px rgba(0,0,0,0.1); }

    .prayer-card { width: 100%; flex: 1; min-height: 48px; border-radius: 14px; display: flex; align-items: center; justify-content: space-between; padding: 0 14px; box-sizing: border-box; position: relative; overflow: hidden; box-shadow: inset 2px 3px 5px rgba(255, 255, 255, 0.4), inset -1px -1px 3px rgba(0, 0, 0, 0.1), 1px 1px 0px var(--e3), 2px 2px 0px var(--e3), 3px 3px 0px var(--e3), 4px 4px 0px var(--e3), 6px 8px 15px rgba(0, 0, 0, 0.2); border-top: 1.5px solid rgba(255, 255, 255, 0.6); border-left: 1px solid rgba(255, 255, 255, 0.4); }
    .prayer-card { background-image: var(--bg-gradient), var(--veins), ${SoftNoise}; background-blend-mode: normal, overlay, multiply; }
    
    .fajr { --veins: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="100"><path d="M-20 80 C 100 -20, 200 120, 420 10" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="5" stroke-linecap="round"/><path d="M150 120 C 250 40, 300 80, 400 -10" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="2"/></svg>'); --bg-gradient: linear-gradient(135deg, #7C988F 0%, #5C7B71 100%); --e3: #405C53; }
    .dhuhr { --veins: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="100"><path d="M0 100 C 100 0, 250 100, 400 0" fill="none" stroke="rgba(100,60,30,0.12)" stroke-width="3"/><path d="M80 -20 C 180 80, 250 20, 350 120" fill="none" stroke="rgba(255,255,255,0.85)" stroke-width="4"/></svg>'); --bg-gradient: linear-gradient(135deg, #C2A882 0%, #A38760 100%); --e3: #82663F; }
    .asr { --veins: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="100"><path d="M-50 40 C 100 -10, 200 110, 450 30" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="2"/><path d="M100 120 C 200 20, 300 80, 400 -20" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="5"/></svg>'); --bg-gradient: linear-gradient(135deg, #7A8EAA 0%, #5B6F8C 100%); --e3: #42536B; }
    .maghrib { --veins: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="100"><path d="M-20 50 Q 150 120 420 20" fill="none" stroke="rgba(255,255,255,0.7)" stroke-width="6"/><path d="M50 120 Q 200 -20 350 120" fill="none" stroke="rgba(100,0,20,0.08)" stroke-width="3"/></svg>'); --bg-gradient: linear-gradient(135deg, #B5848C 0%, #94646B 100%); --e3: #73464C; }
    .isha { --veins: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="w"><feTurbulence type="fractalNoise" baseFrequency="0.01 0.4" numOctaves="3" result="n"/><feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 1.5 -0.3"/></filter><rect width="100%" height="100%" filter="url(%23w)" opacity="0.35"/></svg>'); --bg-gradient: linear-gradient(135deg, #574643 0%, #3D2D2A 100%); --e3: #261A17; background-blend-mode: normal, multiply, multiply; }
    .witr { --veins: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="100"><path d="M-20 100 C 150 -40, 250 120, 420 20" fill="none" stroke="rgba(0,0,0,0.06)" stroke-width="3"/><path d="M100 120 C 250 20, 300 80, 450 -20" fill="none" stroke="rgba(255,255,255,0.8)" stroke-width="5"/></svg>'); --bg-gradient: linear-gradient(135deg, #3A4A5A 0%, #253140 100%); --e3: #17202B; }

    .card-inner { display: flex; align-items: center; gap: 14px; z-index: 2; position: relative; }
    .icon-wrapper { width: 30px; height: 30px; border-radius: 8px; background: rgba(0,0,0,0.25); box-shadow: inset 2px 3px 5px rgba(0,0,0,0.5), inset -1px -1px 2px rgba(255,255,255,0.1); display: flex; justify-content: center; align-items: center; }
    .icon-svg { width: 18px; height: 18px; filter: drop-shadow(0px 2px 3px rgba(0,0,0,0.6)); }
    .prayer-name { font-family: 'Outfit', sans-serif; font-size: 16.5px; font-weight: 900; color: #F8FAFC; text-shadow: 0px 1px 0px rgba(0,0,0,0.8), 0px 2px 0px #64748B, 0px 3px 0px #475569, 0px 4px 0px #334155, 0px 6px 5px rgba(0,0,0,0.6); letter-spacing: 0.5px; }
    
    .jamaat-btn { height: 26px; padding: 0 12px; border-radius: 20px; font-size: 11.5px; font-weight: 850; background: rgba(0,0,0,0.3); color: #E2E8F0; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: inset 2px 3px 6px rgba(0,0,0,0.6), inset -1px -1px 3px rgba(255,255,255,0.1), inset 0px 0px 12px rgba(255, 255, 255, 0.15); text-shadow: 1px 1px 2px rgba(0,0,0,0.8); box-sizing: border-box; border-top: 1px solid transparent; border-left: 1px solid transparent; transition: transform 0.1s; user-select: none; }
    .jamaat-btn.jamaat-active { background: #1A365D; color: #90CDF4; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.25), inset -1px -1px 3px rgba(0,0,0,0.4), 1px 1px 0px #102440, 2px 2px 0px #102440, 3px 4px 6px rgba(0,0,0,0.4); border-top: 1px solid rgba(255,255,255,0.25); border-left: 1px solid rgba(255,255,255,0.15); }
    .jamaat-btn:active { transform: scale(0.94); }

    .small-btn { height: 26px; padding: 0 12px; border-radius: 20px; font-size: 11.5px; font-weight: 850; background: rgba(0,0,0,0.3); color: #E2E8F0; display: flex; align-items: center; justify-content: center; cursor:pointer; box-shadow: inset 2px 3px 6px rgba(0,0,0,0.6), inset -1px -1px 3px rgba(255,255,255,0.1), inset 0px 0px 12px rgba(255, 255, 255, 0.15); text-shadow: 1px 1px 2px rgba(0,0,0,0.8); box-sizing: border-box; border-top: 1px solid transparent; border-left: 1px solid transparent; transition: transform 0.1s;}
    .small-btn.completed-btn { background: #1B4332; color: #81C784; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.25), inset -1px -1px 3px rgba(0,0,0,0.4), 1px 1px 0px #132E23, 2px 2px 0px #132E23, 3px 4px 6px rgba(0,0,0,0.4); border-top: 1px solid rgba(255,255,255,0.25); border-left: 1px solid rgba(255,255,255,0.15); }
    .small-btn:active { transform: scale(0.94); }
    
    .radio-ring { width: 20px; height: 20px; border-radius: 50%; background: rgba(0,0,0,0.2); border: 2px solid rgba(0,0,0,0.4); box-shadow: inset 2px 3px 4px rgba(0,0,0,0.5), inset -1px -2px 2px rgba(255,255,255,0.2), 1px 1px 1px rgba(255,255,255,0.1); cursor: pointer; transition: transform 0.1s;}
    .hole { width: 24px; height: 24px; border-radius: 50%; background: rgba(0,0,0,0.25); display: flex; justify-content: center; align-items: center; box-shadow: inset 2px 3px 6px rgba(0,0,0,0.7), inset -1px -2px 2px rgba(255,255,255,0.1), inset 0 0 10px rgba(255,255,255,0.1); cursor: pointer; transition: transform 0.1s;}
    .radio-ring:active, .hole:active { transform: scale(0.85); }

    .checked-lava { width: 16px; height: 16px; border-radius: 50%; background: linear-gradient(135deg, #5DF598 0%, #159C4C 100%); box-shadow: inset 1px 2px 3px rgba(255,255,255,0.9), inset -1px -2px 3px rgba(0,50,20,0.7), 0 0 10px 2px rgba(46, 234, 114, 0.5); display: flex; justify-content: center; align-items: center; }
    .checked-lava::after { content: ''; display: block; width: 3px; height: 7px; border: solid #FFF; border-width: 0 2px 2px 0; transform: rotate(45deg); margin-bottom: 2px; filter: drop-shadow(1px 1px 0px rgba(0,50,0,0.5)); }

    .stat-pill { width: 24px; height: 12px; border-radius: 6px; }
    .stat-pill.empty { background: rgba(0,0,0,0.03); box-shadow: inset 1px 2px 4px rgba(0,0,0,0.15), inset -1px -1px 3px rgba(255,255,255,0.9); }
    .stat-pill.full { box-shadow: 2px 3px 5px rgba(0,0,0,0.25), inset 1px 1px 2px rgba(255,255,255,0.6); border-top: 1px solid rgba(255,255,255,0.6); border-left: 1px solid rgba(255,255,255,0.3); }
    .stat-pill.p-c0 { background: linear-gradient(135deg, #7C988F, #5C7B71); } 
    .stat-pill.p-c1 { background: linear-gradient(135deg, #C2A882, #A38760); } 
    .stat-pill.p-c2 { background: linear-gradient(135deg, #7A8EAA, #5B6F8C); } 
    .stat-pill.p-c3 { background: linear-gradient(135deg, #B5848C, #94646B); } 
    .stat-pill.p-c4 { background: linear-gradient(135deg, #574643, #3D2D2A); } 
    .stat-pill.p-c5 { background: linear-gradient(135deg, #3A4A5A, #253140); } 
    
    .stats-day-lbl { margin-top: 8px; width: 24px; height: 24px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 10px; font-weight: 800; color: #8A9499; background: linear-gradient(135deg, #F9F9F9, #E3E3E3); box-shadow: 2px 3px 5px rgba(0,0,0,0.1), -2px -2px 5px #FFFFFF, inset 1px 1px 2px #FFF; border-top: 1px solid #FFF; }
    .stats-day-lbl.active { background: linear-gradient(135deg, #4A89DF, #1A4B96); color: #FFFFFF; text-shadow: 1px 1px 2px rgba(0,0,0,0.3); box-shadow: 2px 3px 6px rgba(26, 75, 150, 0.4), inset 1px 1px 3px rgba(255,255,255,0.4); border: none; }
</style>
`;

document.getElementById('header-container').innerHTML = GlobalCSS + `
<div class="header-top">
    <div class="english-date-3d" @click="openCalendar()" x-text="formattedDate"></div>
    <div class="streak-badge" x-text="streak"></div>
    <div class="login-box-3d" @click="openAuthModal()">
        <svg x-show="!isLoggedIn" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#6C7A80" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="engraved-icon-head"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle></svg>
        <svg x-show="isLoggedIn" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#159C4C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="engraved-icon-head"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path><circle cx="12" cy="7" r="4"></circle><circle cx="19" cy="19" r="5" fill="#159C4C"></circle><polyline points="17 19 18.5 20.5 21 17.5" stroke="#FFF" stroke-width="2.5"></polyline></svg>
    </div>
</div>
`;

document.getElementById('water-card-container').innerHTML = `
<div class="ultra-tasbih-card">
    <div class="tasbih-info">
        <div class="t-arabic" x-text="tItm.ar"></div>
        <div class="t-divider"></div>
        <div class="t-pronounce" x-text="tItm.pr"></div>
        <div class="t-meaning" x-text="tItm.mn"></div>
        <div class="t-btn-group">
            <div class="t-icon-btn" style="color:#2ecc71" @click="tRes()" title="Reset"><svg viewBox="0 0 24 24"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg></div>
            <div class="t-icon-btn" style="color:#ff6b6b" @click="tDec()" title="Minus"><svg viewBox="0 0 24 24"><line x1="5" y1="12" x2="19" y2="12"></line></svg></div>
            <div class="t-icon-btn" style="color:#ff9f43" @click="tSpk()" title="Audio"><svg viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg></div>
            <div class="t-icon-btn" style="color:#a4c6db" @click="tNext()" title="Next"><svg viewBox="0 0 24 24"><polyline points="9 18 15 12 9 6"></polyline></svg></div>
        </div>
    </div>
    <div class="t-ring-wrapper">
        <div class="t-ring-container" @click="tInc()">
            <svg class="t-svg-ring"><circle cx="57.5" cy="57.5" r="50" class="t-bg-circle"/><circle cx="57.5" cy="57.5" r="50" class="t-pr-circle" :style="\`stroke-dashoffset:\${tOff}\`"/></svg>
            <div class="t-marble" :style="tDot"></div>
            <div class="t-count-display"><span class="v-num" x-text="tCur.c"></span></div>
        </div>
        <div class="t-limit-btn" @click="openTasbihModal()" x-text="'/ ' + tLimit"></div>
    </div>
</div>

<div x-show="isTasbihModalOpen" class="modal-overlay" style="display: none;" x-transition>
    <div style="background: linear-gradient(145deg, #F9F9F9, #E3E3E3); border-radius: 22px; padding: 26px; width: 85%; max-width: 320px; box-shadow: 0 20px 45px rgba(0,0,0,0.35), inset 0 2px 5px rgba(255,255,255,1); text-align: center; border: 1.5px solid rgba(255,255,255,0.8);">
        <h3 style="color: #2D3748; margin-top:0; margin-bottom: 22px; font-size:19px; font-weight:900;">Set Target</h3>
        <div style="margin-bottom: 24px;">
            <input type="number" x-model="customLimitInput" style="width: 100%; height: 50px; border-radius: 14px; border: none; background: linear-gradient(135deg, #FFFFFF 0%, #E8E8E8 100%); text-align: center; font-size: 20px; font-weight: 800; color: #4A5568; box-shadow: inset 2px 3px 6px rgba(0,0,0,0.15), inset -1px -1px 3px #FFF; border-top: 1px solid #FFF; border-left: 1px solid #FFF; outline: none; font-family: 'Plus Jakarta Sans', sans-serif;" placeholder="Enter number">
        </div>
        <div style="display: flex; gap: 12px;">
            <button class="modal-btn" @click="isTasbihModalOpen = false" style="flex: 1; height: 48px; border-radius: 14px; border: none; background: linear-gradient(135deg, #FFFFFF 0%, #D4D1C7 100%); color: #5C6568; font-weight: 800; font-size: 15px; cursor: pointer; box-shadow: inset 2px 3px 4px #FFF, 2px 3px 6px rgba(0,0,0,0.15); border-top: 1px solid #FFF; font-family: 'Plus Jakarta Sans', sans-serif;">Cancel</button>
            <button class="modal-btn" @click="saveTasbihLimit()" style="flex: 1; height: 48px; border-radius: 14px; border: none; background: linear-gradient(135deg, #4A89DF 0%, #1A4B96 100%); color: white; font-weight: 800; font-size: 15px; cursor: pointer; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.4), inset -2px -2px 4px rgba(0,0,0,0.2), 0 5px 10px rgba(0,0,0,0.25); border-top: 1px solid rgba(255,255,255,0.4); font-family: 'Plus Jakarta Sans', sans-serif;">Save</button>
        </div>
    </div>
</div>

<div x-show="isMarkModalOpen" class="modal-overlay" style="display: none;" x-transition>
    <div style="background: linear-gradient(145deg, #F9F9F9, #E3E3E3); border-radius: 22px; padding: 26px; width: 85%; max-width: 320px; box-shadow: 0 20px 45px rgba(0,0,0,0.35), inset 0 2px 5px rgba(255,255,255,1); text-align: center; border: 1.5px solid rgba(255,255,255,0.8);">
        <h3 style="color: #2D3748; margin-top:0; margin-bottom: 22px; font-size:19px; font-weight:900;" x-text="markModalType === 'mark' ? 'Mark Prayers' : 'Unmark Prayers'"></h3>
        <div style="display: flex; flex-direction: column; gap: 12px; margin-bottom: 24px;">
            <button class="modal-btn" @click="executeMark(markModalType, markModalType === 'mark' ? 'farz' : 'sunnah')" style="width: 100%; height: 48px; border-radius: 14px; border: none; background: linear-gradient(135deg, #4A89DF 0%, #1A4B96 100%); color: white; font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.4), inset -2px -2px 4px rgba(0,0,0,0.2), 0 5px 10px rgba(0,0,0,0.25); border-top: 1px solid rgba(255,255,255,0.4); font-family: 'Plus Jakarta Sans', sans-serif; text-transform: uppercase;" x-text="markModalType === 'mark' ? 'Mark Farz Only' : 'Unmark Farz Only'"></button>
            <button class="modal-btn" @click="executeMark(markModalType, 'all')" style="width: 100%; height: 48px; border-radius: 14px; border: none; background: linear-gradient(135deg, #4A89DF 0%, #1A4B96 100%); color: white; font-weight: 800; font-size: 14px; cursor: pointer; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.4), inset -2px -2px 4px rgba(0,0,0,0.2), 0 5px 10px rgba(0,0,0,0.25); border-top: 1px solid rgba(255,255,255,0.4); font-family: 'Plus Jakarta Sans', sans-serif; text-transform: uppercase;" x-text="markModalType === 'mark' ? 'Mark Farz + Sunnah (All)' : 'Unmark Farz + Sunnah (All)'"></button>
        </div>
        <button class="modal-btn" @click="isMarkModalOpen = false" style="width: 100%; height: 48px; border-radius: 14px; border: none; background: linear-gradient(135deg, #FFFFFF 0%, #D4D1C7 100%); color: #5C6568; font-weight: 800; font-size: 15px; cursor: pointer; box-shadow: inset 2px 3px 4px #FFF, 2px 3px 6px rgba(0,0,0,0.15); border-top: 1px solid #FFF; font-family: 'Plus Jakarta Sans', sans-serif;">Cancel</button>
    </div>
</div>

<div x-show="isStatsModalOpen" class="modal-overlay" style="display: none;" x-transition>
    <div style="background: linear-gradient(145deg, #F9F9F9, #E3E3E3); border-radius: 26px; padding: 24px; width: 90%; max-width: 360px; box-shadow: 0 25px 50px rgba(0,0,0,0.4), inset 0 2px 5px rgba(255,255,255,0.8); text-align: center; border: 1.5px solid rgba(255,255,255,0.8);">
        <h3 style="color: #364455; margin-top:0; margin-bottom: 20px; font-size:20px; font-weight:900; display:flex; align-items:center; justify-content:center; gap:8px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="#364455"><rect x="4" y="13" width="4" height="9" rx="1.5"/><rect x="10" y="8" width="4" height="14" rx="1.5"/><rect x="16" y="3" width="4" height="19" rx="1.5"/></svg>Weekly Progress
        </h3>
        <div style="display: flex; gap: 10px; margin-bottom: 20px;">
            <div class="option-3d" style="flex: 1; flex-direction: column; justify-content: center; padding: 12px 4px; margin-bottom: 0;"><div style="font-size: 9px; color: #8A9499; font-weight: 800; text-transform: uppercase; margin-bottom: 6px;">Prayers</div><div style="font-size: 18px; font-weight: 900; color: #1C3682; font-family: 'Outfit', sans-serif;" x-text="weeklyStats.prayersStr"></div></div>
            <div class="option-3d" style="flex: 1; flex-direction: column; justify-content: center; padding: 12px 4px; margin-bottom: 0;"><div style="font-size: 9px; color: #8A9499; font-weight: 800; text-transform: uppercase; margin-bottom: 6px;">Jamaat</div><div style="font-size: 18px; font-weight: 900; color: #1C7043; font-family: 'Outfit', sans-serif;" x-text="weeklyStats.jamaatPct"></div></div>
            <div class="option-3d" style="flex: 1; flex-direction: column; justify-content: center; padding: 12px 4px; margin-bottom: 0;"><div style="font-size: 9px; color: #8A9499; font-weight: 800; text-transform: uppercase; margin-bottom: 6px;">Sunnah</div><div style="font-size: 18px; font-weight: 900; color: #A13824; font-family: 'Outfit', sans-serif;" x-text="weeklyStats.sunnahPct"></div></div>
        </div>
        <div style="background: linear-gradient(135deg, #EAECEF, #F4F6F8); border-radius: 20px; padding: 20px 14px; box-shadow: inset 4px 5px 10px rgba(0,0,0,0.1), inset -4px -4px 10px rgba(255,255,255,0.9), 0px 4px 10px rgba(0,0,0,0.05); display: flex; justify-content: space-between; margin-bottom: 22px; border: 1px solid rgba(255,255,255,0.6);">
            <template x-for="(day, idx) in weeklyStats.grid">
                <div style="display: flex; flex-direction: column; gap: 6px; align-items: center;">
                    <template x-for="(pill, pIdx) in day.pills"><div class="stat-pill" :class="pill ? 'full p-c' + pIdx : 'empty'"></div></template>
                    <div class="stats-day-lbl" :class="day.isToday ? 'active' : ''" x-text="['S','M','T','W','T','F','S'][day.date.getDay()]"></div>
                </div>
            </template>
        </div>
        <button class="modal-btn" @click="isStatsModalOpen = false" style="width: 100%; height: 48px; border-radius: 14px; border: none; background: linear-gradient(135deg, #4A89DF 0%, #1A4B96 100%); color: white; font-weight: 800; font-size: 16px; cursor: pointer; box-shadow: inset 2px 2px 4px rgba(255,255,255,0.4), inset -2px -2px 4px rgba(0,0,0,0.2), 0 5px 10px rgba(0,0,0,0.25); border-top: 1px solid rgba(255,255,255,0.4); font-family: 'Plus Jakarta Sans', sans-serif;">Excellent, Keep It Up!</button>
    </div>
</div>
`;

document.getElementById('days-row-container').innerHTML = `
<div class="days-row">
    <div class="day-wrapper"><div class="day-btn" style="width: 20px; font-size:12px;" @click="navigateWeek(-1)">&lt;</div></div>
    <template x-for="day in weekDays"><div class="day-wrapper"><div class="day-btn" :class="day.isSelected ? 'active' : ''" x-text="day.label" @click="selectCalendarDate(day.date)"></div></div></template>
    <div class="day-wrapper"><div class="day-btn" style="width: 20px; font-size:12px;" @click="navigateWeek(1)">&gt;</div></div>
</div>
`;

document.getElementById('actions-row-container').innerHTML = `
<div class="actions-row">
    <div class="action-btn" @click="handleMarkBtn()">
        <template x-if="markStats.fCount === 0 && markStats.sCount === 0"><div style="display:contents"><svg class="engraved-icon" viewBox="0 0 24 24" fill="none" stroke="#444E51" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-6-8.5" /><polyline points="22 4 12 14 8 10" /></svg><span>Mark All</span></div></template>
        <template x-if="markStats.fCount > 0 || markStats.sCount > 0"><div style="display:contents"><svg class="engraved-icon" viewBox="0 0 24 24" fill="none" stroke="#444E51" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="15" y1="9" x2="9" y2="15"></line><line x1="9" y1="9" x2="15" y2="15"></line></svg><span>Unmark All</span></div></template>
    </div>
    <div class="action-btn" @click="getDateKey(selectedDate) === getDateKey(today) ? isStatsModalOpen = true : selectCalendarDate(new Date(today))">
        <template x-if="getDateKey(selectedDate) === getDateKey(today)"><div style="display:contents"><svg class="engraved-icon" viewBox="0 0 24 24" fill="none" stroke="#444E51" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg><span>Statistics</span></div></template>
        <template x-if="getDateKey(selectedDate) !== getDateKey(today)"><div style="display:contents"><svg class="engraved-icon" viewBox="0 0 24 24" fill="none" stroke="#444E51" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="3" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="9" x2="21" y2="9" /><circle cx="15" cy="15" r="3" /><polyline points="15 13.8 15 15 16 15" /></svg><span>Today</span></div></template>
    </div>
</div>
`;

document.getElementById('prayer-cards-container').innerHTML = `
<template x-for="prayer in prayersList" :key="prayer.id">
    <div class="prayer-card" :class="prayer.id">
        <div class="card-inner">
            <div class="icon-wrapper"><div style="display:contents" x-html="prayer.icon"></div></div>
            <span class="prayer-name" x-text="prayer.name"></span>
        </div>
        <div class="card-inner" style="gap:10px;">
            <div class="jamaat-btn" :class="isJamaat(prayer.id) ? 'jamaat-active' : ''" @click="toggleJamaat(prayer.id)" x-text="isJamaat(prayer.id) ? 'Jamaat' : 'Alone'"></div>
            <div class="small-btn" :class="getSubBtnStatus(prayer.id, prayer.type).isAllDone ? 'completed-btn' : ''" @click="openModal(prayer.type, prayer.name)" x-text="getSubBtnStatus(prayer.id, prayer.type).text"></div>
            <div style="cursor:pointer; margin-left: 2px;" @click="toggleCore(prayer.id)">
                <div x-show="isCoreCompleted(prayer.id)" class="hole" style="display:none;"><div class="checked-lava"></div></div>
                <div x-show="!isCoreCompleted(prayer.id)" class="radio-ring"></div>
            </div>
        </div>
    </div>
</template>
`;
