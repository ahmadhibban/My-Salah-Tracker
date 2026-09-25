const PremiumLight = `<defs><linearGradient id="premLight" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#FFFFFF"/><stop offset="100%" stop-color="#E2E8F0"/></linearGradient></defs>`;

document.addEventListener('alpine:init', () => {
    Alpine.data('prayerApp', function() { return {
        // === Import External Auth Logic ===
        ...window.getAuthLogic(),

        selectedDate: new Date(), today: new Date(),
        db: JSON.parse(localStorage.getItem('prayer_db')) || {},
        
        isModalOpen: false, modalType: '', modalPrayer: '', modalTitle: '',
        isCalendarOpen: false, currentMonthDate: new Date(), isFutureModalOpen: false,
        isMarkModalOpen: false, markModalType: '', isStatsModalOpen: false,

        // === TASBIH SYSTEM LOGIC ===
        tasbihIdx: 0,
        defaultDuas: [
            {ar:"سُبْحَانَ اللّٰهِ", pr:"Subhan Allah", mn:"Glory be to Allah", lm:33},
            {ar:"الْحَمْدُ لِلّٰهِ", pr:"Alhamdulillah", mn:"All praise is due to Allah", lm:33},
            {ar:"اللّٰهُ أَكْبَرُ", pr:"Allahu Akbar", mn:"Allah is the Greatest", lm:34},
            {ar:"لَا إِلٰهَ إِلَّا اللّٰهُ", pr:"La ilaha illallah", mn:"There is no deity but Allah", lm:100},
            {ar:"أَسْتَغْفِرُ اللّٰهَ", pr:"Astaghfirullah", mn:"I seek forgiveness from Allah", lm:100},
            {ar:"سُبْحَانَ اللّٰهِ وَبِحَمْدِهِ", pr:"Subhan Allahi wa bihamdihi", mn:"Glory be to Allah and His is the praise", lm:100},
            {ar:"سُبْحَانَ اللّٰهِ الْعَظِيمِ", pr:"Subhan Allahil Azeem", mn:"Glory be to Allah, the Magnificent", lm:100}
        ],
        tasbihState: JSON.parse(localStorage.getItem('tasbih_data')) || [],
        isTasbihModalOpen: false, customLimitInput: '',

        get tCur() { return this.tasbihState[this.tasbihIdx] || {c:0, y:0, t:0, lm: null}; },
        get tItm() { return this.defaultDuas[this.tasbihIdx]; },
        get tLimit() { return this.tCur.lm || this.tItm.lm; }, 
        get tOff() { return 314.16 - (this.tCur.c / this.tLimit) * 314.16; },
        get tDot() { let a = (this.tCur.c / this.tLimit) * 2 * Math.PI - Math.PI/2; return `left:${57.5 + 50 * Math.cos(a)}px; top:${57.5 + 50 * Math.sin(a)}px`; },

        initApp() { 
            window.appRef = this; 
            this.initAuth(); 
            this.getDayData(this.getDateKey(this.selectedDate)); 
            if(this.tasbihState.length === 0 || this.tasbihState.length !== this.defaultDuas.length) {
                this.tasbihState = this.defaultDuas.map(() => ({c:0, y:0, t:0, lm: null}));
                localStorage.setItem('tasbih_data', JSON.stringify(this.tasbihState));
            }
            this.$watch('tasbihState', val => localStorage.setItem('tasbih_data', JSON.stringify(val)), {deep: true});
        },

        tBp(f=600, d=.05) { try { let c = new(window.AudioContext||window.webkitAudioContext)(), o = c.createOscillator(), g = c.createGain(); o.type = 'sine'; o.frequency.value = f; g.gain.setValueAtTime(.05, c.currentTime); g.gain.exponentialRampToValueAtTime(.001, c.currentTime+d); o.connect(g); g.connect(c.destination); o.start(); o.stop(c.currentTime+d); } catch(e) {} },
        tInc() { if(this.tCur.c >= this.tLimit) { this.tCur.c = 1; this.tCur.y++; this.tBp(800,.15); } else { this.tCur.c++; this.tBp(); } this.tCur.t++; },
        tDec() { if(this.tCur.t > 0) { this.tCur.t--; this.tBp(450,.1); if(this.tCur.c === 1 && this.tCur.y > 0) { this.tCur.c = this.tLimit; this.tCur.y--; } else if(this.tCur.c === 0 && this.tCur.y > 0) { this.tCur.c = this.tLimit; this.tCur.y--; } else if(this.tCur.c > 0) this.tCur.c--; } },
        tRes() { this.tCur.c = 0; this.tCur.y = 0; this.tBp(300,.3); },
        tNext() { this.tasbihIdx = (this.tasbihIdx + 1) % this.defaultDuas.length; this.tBp(700,.05); },
        tSpk() { let audio = new Audio("https://translate.googleapis.com/translate_tts?client=gtx&ie=UTF-8&tl=ar&q=" + encodeURIComponent(this.tItm.ar)); audio.play().catch(e => alert('Please check your internet connection to play audio.')); },
        openTasbihModal() { this.customLimitInput = this.tLimit; this.isTasbihModalOpen = true; },
        saveTasbihLimit() { let val = parseInt(this.customLimitInput); if(val && val > 0) { this.tCur.lm = val; this.tasbihState = [...this.tasbihState]; this.isTasbihModalOpen = false; this.tBp(500, 0.1); } else { alert("Please enter a valid number!"); } },

        get formattedDate() { return this.selectedDate.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' }); },
        get streak() { let count = 0; Object.values(this.db).forEach(day => { if (day && day.core && Object.values(day.core).every(v => v === true)) { count++; } }); return count + ' Days'; },
        get weekDays() { let startOfWeek = new Date(this.selectedDate); let dayOffset = startOfWeek.getDay() === 6 ? 0 : startOfWeek.getDay() + 1; startOfWeek.setDate(startOfWeek.getDate() - dayOffset); const daysList = ['S', 'S', 'M', 'T', 'W', 'T', 'F']; return daysList.map((day, i) => { let d = new Date(startOfWeek); d.setDate(startOfWeek.getDate() + i); return { label: day, date: d, isSelected: d.toDateString() === this.selectedDate.toDateString() }; }); },
        getDateKey(date) { const offset = date.getTimezoneOffset() * 60000; return (new Date(date.getTime() - offset)).toISOString().split('T')[0]; },
        
        getDayData(dateStr) {
            if (!this.db[dateStr]) {
                this.db[dateStr] = {
                    core: { fajr: false, dhuhr: false, asr: false, maghrib: false, isha: false, witr: false },
                    jamaat: { fajr: true, dhuhr: true, asr: true, maghrib: true, isha: true, witr: true },
                    sunnah: { fajr: false, dhuhr_before: false, dhuhr_after: false, asr: false, maghrib: false, isha: false, witr: false },
                    extras: { fajr: { sunnah_before: false, ishraq: false, chasht: false }, dhuhr: { sunnah_before: false, sunnah_after: false }, maghrib: { sunnah_after: false, awabin: false } }
                };
                this.saveDB();
            } else {
                if (!this.db[dateStr].sunnah.hasOwnProperty('asr')) {
                    this.db[dateStr].sunnah.asr = false;
                    this.saveDB();
                }
                if (!this.db[dateStr].jamaat) {
                    this.db[dateStr].jamaat = { fajr: true, dhuhr: true, asr: true, maghrib: true, isha: true, witr: true };
                    this.saveDB();
                }
            }
            return this.db[dateStr];
        },
        
        saveDB() { 
            localStorage.setItem('prayer_db', JSON.stringify(this.db)); 
            if(typeof this.forceCloudSync === 'function') this.forceCloudSync();
        },
        
        toggleCore(prayer) { const key = this.getDateKey(this.selectedDate); this.db[key].core[prayer] = !this.db[key].core[prayer]; this.db = { ...this.db }; this.saveDB(); },
        isCoreCompleted(prayer) { return this.getDayData(this.getDateKey(this.selectedDate)).core[prayer]; },
        isJamaat(prayer) { return this.getDayData(this.getDateKey(this.selectedDate)).jamaat[prayer]; },
        toggleJamaat(prayer) { const key = this.getDateKey(this.selectedDate); this.db[key].jamaat[prayer] = !this.db[key].jamaat[prayer]; this.db = { ...this.db }; this.saveDB(); },

        get markStats() {
            let dayData = this.getDayData(this.getDateKey(this.selectedDate));
            let fCount = Object.values(dayData.core).filter(Boolean).length;
            let sCount = 0;
            Object.values(dayData.sunnah).forEach(v => { if(v) sCount++; });
            Object.values(dayData.extras).forEach(p => Object.values(p).forEach(v => { if(v) sCount++; }));
            return { fCount, sCount };
        },

        handleMarkBtn() {
            let stats = this.markStats;
            if (stats.fCount === 0 && stats.sCount === 0) { this.markModalType = 'mark'; this.isMarkModalOpen = true; } 
            else { if (stats.sCount === 0 && stats.fCount > 0) { this.executeMark('unmark', 'farz'); } else if (stats.fCount === 0 && stats.sCount > 0) { this.executeMark('unmark', 'sunnah'); } else { this.markModalType = 'unmark'; this.isMarkModalOpen = true; } }
        },

        executeMark(action, scope) {
            let key = this.getDateKey(this.selectedDate); let dayData = this.getDayData(key); let state = action === 'mark';
            if (scope === 'farz' || scope === 'all') { Object.keys(dayData.core).forEach(p => dayData.core[p] = state); }
            if (scope === 'sunnah' || scope === 'all') { Object.keys(dayData.sunnah).forEach(p => dayData.sunnah[p] = state); Object.keys(dayData.extras).forEach(p => Object.keys(dayData.extras[p]).forEach(e => dayData.extras[p][e] = state)); }
            this.db = { ...this.db }; this.saveDB(); this.isMarkModalOpen = false;
        },

        navigateWeek(dir) { 
            let target = new Date(this.selectedDate); target.setDate(target.getDate() + (dir * 7)); 
            let tw = new Date(this.today); tw.setDate(tw.getDate() - (tw.getDay()===6?0:tw.getDay()+1)); tw.setHours(0,0,0,0); 
            let tgtW = new Date(target); tgtW.setDate(tgtW.getDate() - (tgtW.getDay()===6?0:tgtW.getDay()+1)); tgtW.setHours(0,0,0,0); 
            if (tgtW > tw) { this.isFutureModalOpen = true; } else { this.selectedDate = target; } 
        },
        openCalendar() { this.currentMonthDate = new Date(this.selectedDate); this.isCalendarOpen = true; },
        get calendarMonthName() { return this.currentMonthDate.toLocaleDateString('en-US', {month: 'long', year: 'numeric'}); },
        
        changeMonth(offset) { 
            let d = new Date(this.currentMonthDate); d.setMonth(d.getMonth() + offset); 
            let tm = d.getFullYear() * 12 + d.getMonth(); let cm = this.today.getFullYear() * 12 + this.today.getMonth(); 
            if(tm > cm) { 
                this.isCalendarOpen = false; 
                setTimeout(() => { this.isFutureModalOpen = true; }, 200);
                return; 
            } 
            this.currentMonthDate = d;
        },
        get calendarDays() { let year = this.currentMonthDate.getFullYear(); let month = this.currentMonthDate.getMonth(); let firstDay = new Date(year, month, 1).getDay(); let daysInMonth = new Date(year, month + 1, 0).getDate(); let days = []; for(let i=0; i<firstDay; i++) days.push(null); for(let i=1; i<=daysInMonth; i++) days.push(new Date(year, month, i)); return days; },
        
        selectCalendarDate(d) { 
            if(!d) return; 
            if(d > this.today) { 
                this.isCalendarOpen = false; 
                setTimeout(() => { this.isFutureModalOpen = true; }, 200);
                return; 
            } 
            this.selectedDate = d; this.isCalendarOpen = false;
        },
        
        openModal(type, prayerName) { this.modalType = type; this.modalPrayer = prayerName.toLowerCase(); this.modalTitle = prayerName + (type === 'sunnah' ? ' Sunnah' : ' Extras'); this.isModalOpen = true; },
        getSubChecked(type, prayer, subKey) { const key = this.getDateKey(this.selectedDate); return type === 'sunnah' ? this.getDayData(key).sunnah[subKey] : this.getDayData(key).extras[prayer][subKey]; },
        toggleSub(type, prayer, subKey) { const key = this.getDateKey(this.selectedDate); if (type === 'sunnah') this.db[key].sunnah[subKey] = !this.db[key].sunnah[subKey]; else this.db[key].extras[prayer][subKey] = !this.db[key].extras[prayer][subKey]; this.db = { ...this.db }; this.saveDB(); },
        getExtrasKeys(prayer) { return Object.keys(this.getDayData(this.getDateKey(this.selectedDate)).extras[prayer] || {}); },
        formatLabel(str) { return str.replace('_', ' ').toUpperCase(); },
        getSubBtnStatus(prayerId, type) { const data = this.getDayData(this.getDateKey(this.selectedDate)); if(type === 'sunnah') { const isDone = data.sunnah[prayerId] || false; return { isAllDone: isDone, text: prayerId === 'witr' ? 'Tahajjud' : 'Sunnah' }; } else { const items = data.extras[prayerId] || {}; const total = Object.keys(items).length; const done = Object.values(items).filter(Boolean).length; const isAllDone = total > 0 && done === total; return { isAllDone, text: `Extras (${total > 0 ? done : 0}/${total})` }; } },

        get weeklyStats() {
            let start = new Date(this.selectedDate); let dayOffset = start.getDay() === 6 ? 0 : start.getDay() + 1; start.setDate(start.getDate() - dayOffset);
            let totalPrayers = 0; let donePrayers = 0; let doneJamaat = 0; let totalSunnah = 0; let doneSunnah = 0; let grid = [];
            for(let i=0; i<7; i++) {
                let d = new Date(start); d.setDate(start.getDate() + i); let k = this.getDateKey(d); let data = this.getDayData(k); let isPastOrToday = d <= this.today; let dayPills = [];
                const pKeys = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha', 'witr'];
                pKeys.forEach(p => { if (isPastOrToday) { totalPrayers++; if (data.core[p]) { donePrayers++; if (data.jamaat[p]) doneJamaat++; } dayPills.push(data.core[p]); } else { dayPills.push(false); } });
                if (isPastOrToday) { Object.values(data.sunnah).forEach(v => { totalSunnah++; if(v) doneSunnah++; }); Object.values(data.extras).forEach(p => Object.values(p).forEach(v => { totalSunnah++; if(v) doneSunnah++; })); }
                grid.push({ date: d, isToday: k === this.getDateKey(this.today), pills: dayPills });
            }
            return { prayersStr: `${donePrayers}/${totalPrayers}`, jamaatPct: donePrayers > 0 ? Math.round((doneJamaat/donePrayers)*100) + '%' : '0%', sunnahPct: totalSunnah > 0 ? Math.round((doneSunnah/totalSunnah)*100) + '%' : '0%', grid };
        },

        prayersList: [
            { id: 'fajr', name: 'Fajr', type: 'extras', icon: `<svg class="icon-svg" viewBox="0 0 24 24">${PremiumLight}<path fill="url(#premLight)" d="M12 1L13.5 8.5L21 10L13.5 11.5L12 19L10.5 11.5L3 10L10.5 8.5Z M5 4L5.5 5.5L7 6L5.5 6.5L5 8L4.5 6.5L3 6L4.5 5.5Z M19 16L19.5 17.5L21 18L19.5 18.5L19 20L18.5 18.5L17 18L18.5 17.5Z"/></svg>` },
            { id: 'dhuhr', name: 'Dhuhr', type: 'extras', icon: `<svg class="icon-svg" viewBox="0 0 24 24">${PremiumLight}<circle cx="12" cy="12" r="5" fill="url(#premLight)"/><path fill="url(#premLight)" d="M12 1L14 5H10Z M12 23L14 19H10Z M1 12L5 10V14Z M23 12L19 10V14Z M4.22 4.22L8.46 5.64L5.64 8.46Z M19.78 19.78L15.54 18.36L18.36 15.54Z M4.22 19.78L5.64 15.54L8.46 18.36Z M19.78 4.22L18.36 8.46L15.54 5.64Z"/></svg>` },
            { id: 'asr', name: 'Asr', type: 'sunnah', icon: `<svg class="icon-svg" viewBox="0 0 24 24">${PremiumLight}<path d="M17.5 19C19.98 19 22 16.98 22 14.5C22 12.18 20.25 10.28 18 10.05C17.43 7.2 15.1 5 12.25 5C9.36 5 6.94 7.04 6.36 9.8C3.89 10.1 2 12.19 2 14.75C2 17.37 4.13 19 6.75 19H17.5Z" fill="none" stroke="url(#premLight)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>` },
            { id: 'maghrib', name: 'Maghrib', type: 'extras', icon: `<svg class="icon-svg" viewBox="0 0 24 24">${PremiumLight}<path fill="url(#premLight)" d="M12 5a7 7 0 0 0-7 7h14a7 7 0 0 0-7-7z M2 14h20v2H2z M4 18h16v2H4z"/></svg>` },
            { id: 'isha', name: 'Isha', type: 'sunnah', icon: `<svg class="icon-svg" viewBox="0 0 24 24">${PremiumLight}<path fill="url(#premLight)" d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/><path fill="url(#premLight)" d="M18 4L18.5 5.5L20 6L18.5 6.5L18 8L17.5 6.5L16 6L17.5 5.5Z"/></svg>` },
            { id: 'witr', name: 'Witr', type: 'sunnah', icon: `<svg class="icon-svg" viewBox="0 0 24 24">${PremiumLight}<rect x="10" y="11" width="4" height="10" rx="1" fill="url(#premLight)"/><path fill="url(#premLight)" d="M12 2C10.5 4.5 9 6.5 12 9C15 6.5 13.5 4.5 12 2Z"/><rect x="7" y="21" width="10" height="2" rx="1" fill="url(#premLight)"/><line x1="12" y1="9" x2="12" y2="11" stroke="url(#premLight)" stroke-width="2"/></svg>` }
        ]
    };});
});
