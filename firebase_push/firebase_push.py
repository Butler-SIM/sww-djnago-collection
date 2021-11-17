# ------------------------------------------------------------------------------------------

# python.exe -m pip install --upgrade pip
# pip install firebase_admin

# ------------------------------------------------------------------------------------------

import firebase_admin
from firebase_admin import credentials, messaging, _messaging_utils

#BASE_DIR = Path(__file__).resolve().parent.parent
#fcm_server_key_path = os.path.join(BASE_DIR, "serviceAccountKey.json")
#cred = credentials.Certificate(fcm_server_key_path)
#firebase_admin.initialize_app(cred)

def send_to_ios_firebase_cloud_messaging(fcm_token, title, message, sound, badge_count, image=""):
    registration_token = fcm_token

    if sound != "" :
        sound=sound
    elif sound == "" :
        sound = "default"
    #apns
    alert = _messaging_utils.ApsAlert(title = title, body= message)
    aps = messaging._messaging_utils.Aps(alert=alert, sound=sound, badge=badge_count+1)
    payload = _messaging_utils.APNSPayload(aps)

    #message
    msg = messaging.Message(
        notification= messaging.Notification(
            title=title,
            body=message,
        ),
        token=registration_token,
        #apns = messaging.APNSConfig(payload= payload)
        apns= messaging._messaging_utils.APNSConfig(payload=payload)
    )
    #send

    res = messaging.send(msg)
    # Response is a message ID string.
    print('Successfully sent message:', res, )

def send_to_firebase_cloud_messaging(fcm_token, title, message, image=""):
    # This registration token comes from the client FCM SDKs.
    registration_token = fcm_token

    # See documentation on defining a message payload.
    message = messaging.Message(
        data={
            'title': title,
            'body': message,
            'sound': 'default'
        },
        token=registration_token,
    )

    response = messaging.send(message)
        # Response is a message ID string.
    print('Successfully sent message:', response, )


#-- 사용 예 --

# if login_os == "Ios":
#     send_to_ios_firebase_cloud_messaging(send_fcm_token, temp_title, temp_message, temp_sound, alarm_model_count,
#                                          temp_image)  # 받는사람 확인 알림
# else:
#     send_to_firebase_cloud_messaging(send_fcm_token, temp_title, temp_message, temp_image)  # 받는사람 확인 알림

#-- /사용 예/--