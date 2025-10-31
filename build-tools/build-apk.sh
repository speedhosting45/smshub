#!/bin/bash
echo "Building SMS Spy APK..."
./gradlew assembleDebug
echo "APK built in app/build/outputs/apk/debug/"
