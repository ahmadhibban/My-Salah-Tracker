#!/bin/bash
# ==============================================================================
# CLI Build Script for My Salah Tracker (No Gradle Required)
# Author: Ahmad Hibban
# ==============================================================================

set -e

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}====================================================${NC}"
echo -e "${CYAN}   My Salah Tracker - Standalone CLI Builder (No Gradle) ${NC}"
echo -e "${CYAN}====================================================${NC}"

# Directories
PROJECT_ROOT="$(pwd)"
APP_DIR="$PROJECT_ROOT/app"
BUILD_DIR="$PROJECT_ROOT/build_cli"
GEN_DIR="$BUILD_DIR/gen"
CLASSES_DIR="$BUILD_DIR/classes"
DEX_DIR="$BUILD_DIR/dex"
RES_COMPILED="$BUILD_DIR/compiled_res.zip"
BASE_APK="$BUILD_DIR/app-base.apk"
ALIGNED_APK="$BUILD_DIR/app-aligned.apk"
FINAL_APK="$PROJECT_ROOT/MySalahTracker-debug.apk"

# 1. Locate Android SDK & android.jar
echo -e "${YELLOW}[1/6] Detecting SDK and Build Tools...${NC}"

if [ -n "$ANDROID_HOME" ] && [ -f "$ANDROID_HOME/platforms/android-34/android.jar" ]; then
    SDK_DIR="$ANDROID_HOME"
elif [ -d "/data/user/0/com.tom.rv2ide/files/home/android-sdk" ]; then
    SDK_DIR="/data/user/0/com.tom.rv2ide/files/home/android-sdk"
elif [ -d "/data/data/com.itsaky.androidide/files/android-sdk" ]; then
    SDK_DIR="/data/data/com.itsaky.androidide/files/android-sdk"
elif [ -d "$HOME/android-sdk" ]; then
    SDK_DIR="$HOME/android-sdk"
elif [ -d "/data/data/com.termux/files/home/android-sdk" ]; then
    SDK_DIR="/data/data/com.termux/files/home/android-sdk"
else
    echo -e "${RED}Error: Android SDK not found! Please set ANDROID_HOME.${NC}"
    exit 1
fi

ANDROID_JAR=$(find "$SDK_DIR/platforms" -name "android.jar" 2>/dev/null | sort -V | tail -n 1)
if [ -z "$ANDROID_JAR" ]; then
    echo -e "${RED}Error: android.jar not found under $SDK_DIR/platforms!${NC}"
    exit 1
fi
echo -e "  -> Using Android JAR: ${GREEN}$ANDROID_JAR${NC}"

# Find build tools (aapt2, d8, zipalign, apksigner)
AAPT2=$(which aapt2 2>/dev/null || find "$SDK_DIR" -name "aapt2" -type f 2>/dev/null | head -n 1)
D8=$(which d8 2>/dev/null || find "$SDK_DIR" -name "d8" -type f 2>/dev/null | head -n 1)
ZIPALIGN=$(which zipalign 2>/dev/null || find "$SDK_DIR" -name "zipalign" -type f 2>/dev/null | head -n 1)
APKSIGNER=$(which apksigner 2>/dev/null || find "$SDK_DIR" -name "apksigner" -type f 2>/dev/null | head -n 1)
KOTLINC=$(which kotlinc 2>/dev/null || true)

if [ -z "$AAPT2" ]; then echo -e "${RED}Error: aapt2 not found!${NC}"; exit 1; fi
if [ -z "$D8" ]; then echo -e "${RED}Error: d8 not found!${NC}"; exit 1; fi
if [ -z "$KOTLINC" ]; then
    echo -e "${YELLOW}Warning: kotlinc not in PATH, checking AndroidIDE/Termux paths...${NC}"
    KOTLINC=$(find /data/user/0/ /data/data/ /usr/ $HOME -name "kotlinc" -type f 2>/dev/null | head -n 1 || true)
fi

echo -e "  -> aapt2:    ${GREEN}$AAPT2${NC}"
echo -e "  -> d8:       ${GREEN}$D8${NC}"
echo -e "  -> kotlinc:  ${GREEN}${KOTLINC:-Not Found}${NC}"

# Clean build directory
rm -rf "$BUILD_DIR"
mkdir -p "$GEN_DIR" "$CLASSES_DIR" "$DEX_DIR" "$BUILD_DIR/libs"

# Extract classes.jar from neumorphism.aar if present
if [ -f "$APP_DIR/libs/neumorphism.aar" ]; then
    unzip -q -o "$APP_DIR/libs/neumorphism.aar" "classes.jar" -d "$BUILD_DIR/libs/neumorphism" 2>/dev/null || true
    if [ -f "$BUILD_DIR/libs/neumorphism/classes.jar" ]; then
        mv "$BUILD_DIR/libs/neumorphism/classes.jar" "$BUILD_DIR/libs/neumorphism.jar"
        rm -rf "$BUILD_DIR/libs/neumorphism"
    fi
fi

# Gather library jars from Gradle cache if available
GRADLE_CACHE="$HOME/.gradle/caches"
if [ -d "$GRADLE_CACHE" ]; then
    echo -e "  -> Scanning dependency JARs from Gradle cache..."
    find "$GRADLE_CACHE" -name "*.jar" -not -name "*sources*" -not -name "*javadoc*" -exec cp -u {} "$BUILD_DIR/libs/" 2>/dev/null \; || true
fi

# Build classpath string
CLASSPATH="$ANDROID_JAR"
for jar in "$BUILD_DIR/libs"/*.jar; do
    [ -f "$jar" ] && CLASSPATH="$CLASSPATH:$jar"
done

# 2. Compile Resources with AAPT2
echo -e "${YELLOW}[2/6] Compiling Resources (AAPT2)...${NC}"
"$AAPT2" compile --dir "$APP_DIR/src/main/res" -o "$RES_COMPILED"

# 3. Link Resources & Generate R.java
echo -e "${YELLOW}[3/6] Linking Resources & Generating R.java...${NC}"
"$AAPT2" link \
    -o "$BASE_APK" \
    -I "$ANDROID_JAR" \
    --manifest "$APP_DIR/src/main/AndroidManifest.xml" \
    --java "$GEN_DIR" \
    --auto-add-overlay \
    "$RES_COMPILED"

# 4. Compile Kotlin Sources with kotlinc
echo -e "${YELLOW}[4/6] Compiling Kotlin Source Files...${NC}"
KOTLIN_FILES=$(find "$APP_DIR/src/main/java" -name "*.kt")
JAVA_GEN_FILES=$(find "$GEN_DIR" -name "*.java" 2>/dev/null || true)

if [ -n "$KOTLINC" ]; then
    "$KOTLINC" \
        -cp "$CLASSPATH" \
        -d "$CLASSES_DIR" \
        -jvm-target 17 \
        $KOTLIN_FILES $JAVA_GEN_FILES
else
    echo -e "${RED}Error: kotlinc is required to compile Kotlin files. Please install kotlinc or use AndroidIDE.${NC}"
    exit 1
fi

# 5. Convert Classes to DEX using d8
echo -e "${YELLOW}[5/6] Converting to Dalvik Executable (D8)...${NC}"
CLASS_FILES=$(find "$CLASSES_DIR" -name "*.class")
JAR_FILES=$(find "$BUILD_DIR/libs" -name "*.jar" 2>/dev/null || true)

"$D8" \
    --lib "$ANDROID_JAR" \
    --output "$DEX_DIR" \
    --min-api 21 \
    $CLASS_FILES $JAR_FILES

# Package classes.dex into base APK
cd "$DEX_DIR"
for dex in classes*.dex; do
    [ -f "$dex" ] && zip -u "$BASE_APK" "$dex"
done
cd "$PROJECT_ROOT"

# Add assets to APK if present
if [ -d "$APP_DIR/src/main/assets" ]; then
    cd "$APP_DIR/src/main"
    zip -r -u "$BASE_APK" "assets"
    cd "$PROJECT_ROOT"
fi

# 6. Zipalign and Sign APK
echo -e "${YELLOW}[6/6] Aligning and Signing APK...${NC}"
if [ -n "$ZIPALIGN" ]; then
    "$ZIPALIGN" -f 4 "$BASE_APK" "$ALIGNED_APK"
else
    cp "$BASE_APK" "$ALIGNED_APK"
fi

# Keystore check/creation
KEYSTORE="$PROJECT_ROOT/debug.keystore"
if [ ! -f "$KEYSTORE" ]; then
    echo -e "  -> Generating debug keystore..."
    keytool -genkey -v \
        -keystore "$KEYSTORE" \
        -storepass android \
        -alias androiddebugkey \
        -keypass android \
        -keyalg RSA \
        -keysize 2048 \
        -validity 10000 \
        -dname "CN=Android Debug,O=Android,C=US" 2>/dev/null
fi

if [ -n "$APKSIGNER" ]; then
    "$APKSIGNER" sign \
        --ks "$KEYSTORE" \
        --ks-pass pass:android \
        --key-pass pass:android \
        --ks-key-alias androiddebugkey \
        --out "$FINAL_APK" \
        "$ALIGNED_APK"
else
    echo -e "${YELLOW}Warning: apksigner not found, using aligned APK.${NC}"
    cp "$ALIGNED_APK" "$FINAL_APK"
fi

echo -e "${GREEN}====================================================${NC}"
echo -e "${GREEN} BUILD SUCCESSFUL!${NC}"
echo -e "${GREEN} Output APK: $FINAL_APK${NC}"
echo -e "${GREEN}====================================================${NC}"
