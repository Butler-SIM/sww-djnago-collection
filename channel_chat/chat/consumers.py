
import json
from autobahn.exception import Disconnected
from channels.exceptions import InvalidChannelLayerError, StopConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.sessions import *
from channels.db import database_sync_to_async
from chatapi.models import ChatModel, Chat_info, ChatConnectUserModel

from pushapi.models import PushUserModel, AlarmUserModel
from pushapi.views import send_to_ios_firebase_cloud_messaging, send_to_firebase_cloud_messaging
from userapi.models import UserModel


now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class ChatConsumer(AsyncWebsocketConsumer):


    async def websocket_disconnect(self, message):

        """
        Called when a WebSocket connection is closed. Base level so you don't
        need to call super() all the time.
        """
        try:
            for group in self.groups:
                await self.channel_layer.group_discard(group, self.channel_name)
        except AttributeError:
            raise InvalidChannelLayerError(
                "BACKEND is unconfigured or doesn't support groups"
            )
        await self.disconnect(message["code"])
        raise StopConsumer()

    def create_connect_session(self):
        #create
        print("SESSION : ",self.scope['session'])
        ChatConnectUserModel.objects.create(session=self.scope['session'])
        #/create/

        #updtae
        post_connect_user = self.scope['post_connect_user']
        get_connect_user = self.scope['get_connect_user']
        room_check = Chat_info.objects.filter(room_name=get_connect_user + "/" + post_connect_user)
        room_check2 = Chat_info.objects.filter(room_name=post_connect_user + "/" + get_connect_user)
        room_name = ""

        if len(room_check) > 0 :
            room_name = get_connect_user + "/" + post_connect_user
        if len(room_check2) > 0 :
            room_name = post_connect_user + "/" + get_connect_user

        if ChatConnectUserModel.objects.get(session=self.scope['session']).user_name == "":
            ChatConnectUserModel.objects.filter(session=self.scope['session']).update(user_name = self.scope['post_connect_user'],room_name = room_name)

            try :
                chat_info = Chat_info.objects.get(room_name= room_name)
                if chat_info.user_name_1 == post_connect_user :
                    Chat_info.objects.filter(room_name = room_name).update(user_1_status = True)
                elif chat_info.user_name_2 == post_connect_user:
                    Chat_info.objects.filter(room_name = room_name).update(user_2_status = True)

            except Chat_info.DoesNotExist :
                print("DoseNotExist!!!")
                pass
        #/update/

    def delete_connect_session(self):
        #delete
        print("SESSION : ",self.scope['session'])

        try:
            chat_connect_info = ChatConnectUserModel.objects.get(session=self.scope['session'])
            chat_info = Chat_info.objects.get(room_name=chat_connect_info.room_name)

            if chat_info.user_name_1 == chat_connect_info.user_name:
                Chat_info.objects.filter(user_name_1 = chat_connect_info.user_name).update(user_1_status=False)

            elif chat_info.user_name_2 == chat_connect_info.user_name:
                Chat_info.objects.filter(user_name_2 = chat_connect_info.user_name).update(user_2_status=False)


            ChatConnectUserModel.objects.filter(session=self.scope['session']).delete()
            ChatConnectUserModel.objects.filter(user_name="").delete()
            ChatConnectUserModel.objects.filter(user_name= chat_connect_info).delete()

        except Chat_info.DoesNotExist:
            ChatConnectUserModel.objects.filter(session=self.scope['session']).delete()
            ChatConnectUserModel.objects.filter(user_name="").delete()
            print("delete DoesNotExist")
            pass
        except Exception:
            ChatConnectUserModel.objects.filter(session=self.scope['session']).delete()
            ChatConnectUserModel.objects.filter(user_name="").delete()
        #/delete/

    def send_firebase_push(self):
        #send_firebase_push
        post_connect_user = self.scope['post_connect_user']
        get_connect_user = self.scope['get_connect_user']
        print("SESSION : ", self.scope['session'])

        userQuery = UserModel.objects.get(username=get_connect_user)
        get_user_connect_check = ChatConnectUserModel.objects.filter(user_name=userQuery.username)

        if len(get_user_connect_check) < 1:
            try:

                if userQuery.user_alram_sound != None:
                    temp_sound = userQuery.user_alram_sound  # 아이폰 유저 설정 알람음
                else:
                    temp_sound = "default"

                get_user_fcm_token = PushUserModel.objects.get(push_user_id=userQuery.id)
                alarm_model_count = AlarmUserModel.objects.filter(alarm_user_id=userQuery.id).filter(alarm_read_status=0).count()

                # 푸쉬알람 받는 유저 fcm토큰 수정
                send_fcm_token = get_user_fcm_token.fcm_token

                if userQuery.login_os == "Ios":
                    send_to_ios_firebase_cloud_messaging(send_fcm_token, '플리지', post_connect_user + " : 메세지가 왔습니다", temp_sound,
                                                         alarm_model_count, "")  # 받는사람 확인 알림
                else:
                    send_to_firebase_cloud_messaging(send_fcm_token, '플리지', post_connect_user + ' : 메세지가 왔습니다')  # 안드로이드

            except Chat_info.DoesNotExist:
                print("push DoesNotExist")
                pass
            except Exception :
                print("ERROR")
                pass
        #/send_firebase_push/

    async def connect(self):

        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send("connect")
        await self.send(json.dumps({
            'message': "connect"
        }))

        # await self.channel_layer.group_send(
        #     self.room_group_name,
        #     {
        #         'type': 'chat_message',
        #         'message': "connect"
        #     }
        # )



    async def disconnect(self, close_code):

        print("disconnect  /  ",now_time)
        print("disconnect SESSION : ",self.scope['session'])
        print("disconnect", close_code)

        await database_sync_to_async(self.delete_connect_session)()
        await self.send(json.dumps({
            'message': "disconnect"
        }))
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        await self.send(text_data=json.dumps({
            'server pong11': 'server pong test send11'
        }))

        try:

            message = text_data_json['message']

            if message == "pleasy_disconnect":
                print("pleasy_disconnect")
                await self.close()
                return
                # await self.send("disconnect")
                # await self.channel_layer.group_discard(
                #     self.room_group_name,
                #     self.channel_name,
                # )
                # return
            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'chat_message',
                        'message': message
                    }
                )

                if 'android=' in message:



                    android = message
                    android = android.replace("android=", "")
                    post_connect_user = android.split('/')[0]
                    get_connect_user = android.split('/')[1]
                    self.scope['post_connect_user'] = post_connect_user
                    self.scope['session'] = post_connect_user
                    self.scope['get_connect_user'] = get_connect_user
                    await self.send("pong1")

                    await database_sync_to_async(self.create_connect_session)()

                if 'ios=' in message:
                    print(text_data_json)
                    await self.send(text_data=json.dumps({
                        'server pong22': 'server pong test send22'
                    }))

                    ios = message
                    ios = ios.replace("ios=", "")
                    post_connect_user = ios.split('/')[0]
                    get_connect_user = ios.split('/')[1]
                    self.scope['post_connect_user'] = post_connect_user
                    self.scope['session'] = post_connect_user
                    self.scope['get_connect_user'] = get_connect_user

                    await database_sync_to_async(self.create_connect_session)()

        except json.decoder.JSONDecodeError:
            await self.send("pong1")

        except KeyError:
            await self.send("pong2")

        except TypeError:
            await self.send("pong3")

        except Disconnected:
            await self.send("disconnect")
            await self.close()

    async def chat_message(self, event):

        if 'app_send/==' in event['message']:
            message = event['message']

            print(message)
            await self.send(text_data=json.dumps({
                'server pong33': 'server pong test send33'
            }))
            print("메세지 : ", message.split('/==/')[3])
            await database_sync_to_async(self.send_firebase_push)()


        try:

            message = event['message']

            await self.send(text_data=json.dumps({
                'message': message
            }))

        except AttributeError:
            await self.send("pong4")

        except KeyError:
            await self.send("pong5")

        except TypeError:
            await self.send("pong6")
