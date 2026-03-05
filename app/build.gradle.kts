plugins {
    id("com.android.application")
}

android {
    namespace = "com.my.salah.tracker.app"
    compileSdk = 33
    
    defaultConfig {
        applicationId = "com.my.salah.tracker.app"
        minSdk = 21
        targetSdk = 33
        versionCode = 1
        versionName = "1.0"
        
        vectorDrawables { 
            useSupportLibrary = true
        }
    }
    
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = true
            isShrinkResources = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
            signingConfig = signingConfigs.getByName("debug")
        }
        getByName("debug") {
            isMinifyEnabled = false
        }
    }
} // <-- এই ব্র্যাকেটটাই মিসিং ছিল!

dependencies {
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.9.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("com.airbnb.android:lottie:6.3.0")
    implementation("com.github.PhilJay:MPAndroidChart:v3.1.0")
    implementation("cn.pedant.sweetalert:library:1.3")
    
    // Room Database
    implementation("androidx.room:room-runtime:2.5.2")
    annotationProcessor("androidx.room:room-compiler:2.5.2")
    
    // WorkManager (For midnight refresh)
    implementation("androidx.work:work-runtime:2.8.1")
}

configurations.all {
    resolutionStrategy {
        force("org.xerial:sqlite-jdbc:3.41.2.2")
    }
}