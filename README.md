# My Salah Tracker 🕌✨
### Native Android Daily Prayer & Neumorphic Tasbih Application

**My Salah Tracker** is a modern, privacy-focused native Android application designed to help Muslims effortlessly track their daily five prayers (Fajr, Dhuhr, Asr, Maghrib, Isha), build consistent worship habits, and practice daily dhikr with a tactile Ultra Neumorphic Tasbih counter.

---

## 🌟 Key Features

- **Daily Prayer Monitoring**: Intuitive, responsive tracking for all 5 obligatory prayers with real-time progress indicators.
- **Marble Vein Visual Cards**: Elegant Jetpack Compose UI cards featuring animated gradient aesthetics for each prayer time.
- **Ultra Neumorphic Tasbih**: Electronic digital counter designed with realistic soft-light neumorphic elevation, customized haptic feedback, and customizable target counts.
- **Automated Daily Rollover**: Powered by Android WorkManager for seamless midnight daily resets and historical archival.
- **Offline & Private**: 100% offline-first architecture with local SQLite persistence. Your spiritual records remain strictly private on your device.
- **Companion Web Project**: Includes a standalone responsive web edition inside the `Web Code Project/` directory.

---

## 🏗️ Technical Architecture

- **Platform**: Native Android (API 21+)
- **Language**: Kotlin 1.9
- **UI Toolkit**: Jetpack Compose & Material 3
- **Design System**: Neumorphic Elevation & Custom Canvas Shaders
- **Background Tasks**: AndroidX WorkManager
- **Build System**: Gradle Kotlin DSL (`build.gradle.kts`)

---

## 📂 Project Structure

```
My-Salah-Tracker/
├── app/
│   ├── src/main/
│   │   ├── java/com/my/salah/tracker/app/
│   │   │   ├── MainActivity.kt
│   │   │   ├── SalahDatabase.kt
│   │   │   ├── AppWorkers.kt
│   │   │   └── ui/
│   │   │       ├── PrayerCardNeumorphic.kt
│   │   │       ├── UltraTasbihNeumorphic.kt
│   │   │       ├── HeaderAndControlsNeumorphic.kt
│   │   │       ├── NeumorphicModifiers.kt
│   │   │       └── AppTypography.kt
│   │   ├── res/                  # Vector drawables & typography
│   │   └── AndroidManifest.xml
│   └── build.gradle.kts
├── Web Code Project/             # Standalone Companion Web Edition
├── build.gradle.kts
├── settings.gradle.kts
└── README.md
```

---

## 👤 Author

**Ahmad Hibban**
- GitHub: [@ahmadhibban](https://github.com/ahmadhibban)

---

## 📄 License

Open-source under the MIT License. Copyright © Ahmad Hibban.
