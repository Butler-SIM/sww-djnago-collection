import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from chatapi.models import ChatModel, Chat_info
from chatapi.serializer import ChatSerializer, ChatBackupSerializer
from json_response import *
from jwtapi.views import validation, access_id, simple_validation
from userapi.models import UserModel, UserBlockModel


def ajax_chat(request):
    if request.method == "POST":
        message_list = []
        user_list = []

        try:
            user_list = str(request.POST["user_list"]).replace("[", "").replace("]", "").replace('"', "").split(",")
        except MultiValueDictKeyError as e:
            pass

        for us in range(0, len(user_list)):
            try:
                post_user = user_list[us].split("/")[0]
                get_user = user_list[us].split("/")[1]
                reverse_user_list = get_user + "/" + post_user
            except IndexError:
                post_user = ""
                get_user = ""
                reverse_user_list = get_user + "/" + post_user

            read_user_model = ChatModel.objects.filter(read=user_list[us]).filter(
                post_send_status=False) | ChatModel.objects.filter(read=user_list[us]).filter(get_send_status=False)
            reverse_read_user_model = ChatModel.objects.filter(read=reverse_user_list).filter(
                post_send_status=False) | ChatModel.objects.filter(read=reverse_user_list).filter(get_send_status=False)
            for jk in read_user_model:
                message_list.append(user_list[us] + "=" + jk.send_message)
                if jk.post_username == post_user:
                    jk.post_send_status = True
                else:
                    jk.get_send_status = True
                jk.save()

            for rever in reverse_read_user_model:
                message_list.append(reverse_user_list + "=" + rever.send_message)
                if rever.post_username == post_user:
                    rever.post_send_status = True
                else:
                    rever.get_send_status = True
                rever.save()

        context = {"message": message_list}

        return HttpResponse(json.dumps(context), content_type="application/json")

    if request.method == "GET":
        return redirect("https://pleasy.co.kr/realchat/room/")


class ChatView(generics.ListCreateAPIView):
    queryset = ChatModel.objects.all().order_by("-id")
    serializer_class = ChatSerializer
    ordering = ['-id']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', "chatNo", "post_username", "get_username", 'read', 'send_message', 'post_send_status',
                        'get_send_status', 'post_hidden_status', 'get_hidden_status']

    def get(self, request, *args, **kwargs):
        try:
            if request.headers["PleasyPrivatKey"] != "PleasyDevGroup":
                return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

            if request.headers["PleasyPhoneGroup"] == "Android" or request.headers["PleasyPhoneGroup"] == "Ios":
                pass
            else:
                return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

            return JsonResponse(json_success("E0004", self.list(request, *args, **kwargs).data["results"]))

        except KeyError:
            if request.user.is_authenticated:
                if request.user.is_admin != 0:
                    return self.list(request, *args, **kwargs)
                else:
                    return redirect(reverse("accountapp:login"))
            else:
                return redirect(reverse("accountapp:login"))

    def post(self, request, *args, **kwargs):
        # if validation(request.headers):
        #     pass
        # else:
        #     return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)
        # check_chat = []
        # check_username_one = ChatModel.objects.none()

        #채팅방 존재 여부 확인 
        # if ChatModel.objects.filter(post_username=request.data["post_username"]).filter(get_username=request.data["get_username"]).exists():
        #     check_username_one = ChatModel.objects.filter(post_username=request.data["post_username"]).filter(get_username=request.data["get_username"])
        #     for vss in check_username_one:
        #         check_chat = vss.read.split('/')

        # #송수신인 반대 상황도 포함된 경우를 확인 
        # elif ChatModel.objects.filter(post_username=request.data["get_username"]).filter(get_username=request.data["post_username"]).exists():
        #     check_username_two = ChatModel.objects.filter(post_username=request.data["get_username"]).filter(get_username=request.data["post_username"])
        #     for vss in check_username_two:
        #         check_chat = vss.read.split('/')

        check_username_one = ChatModel.objects.filter(post_username=request.data["post_username"]).filter(
            get_username=request.data["get_username"])
        check_username_two = ChatModel.objects.filter(post_username=request.data["get_username"]).filter(
            get_username=request.data["post_username"])

        check_chat = []

        if len(check_username_one) != 0:
            for vss in check_username_one:
                check_chat = vss.read.split('/')
        elif len(check_username_two) != 0:
            for vss in check_username_two:
                check_chat = vss.read.split('/')

        #채팅방이 존재한다면 
        # if check_chat:
        #     request.data.update(chatNo=check_username_one.latest("pk").chatNo)
        if len(check_chat) != 0:
            check_chat_one = check_chat[0].replace(" ", "") + "/" + check_chat[1].replace(" ", "")
            check_chat_two = check_chat[1].replace(" ", "") + "/" + check_chat[0].replace(" ", "")
            check_one = ChatModel.objects.filter(read=check_chat_one).count()
            check_two = ChatModel.objects.filter(read=check_chat_two).count()

            if check_one > 0:
                temp_chat_no = ChatModel.objects.filter(read=check_chat_one).latest("pk").chatNo

                request.data.update(chatNo=temp_chat_no)
            elif check_two > 0:
                temp_chat_no = ChatModel.objects.filter(read=check_chat_two).latest("pk").chatNo

                request.data.update(chatNo=temp_chat_no)


        #채팅방이 존재하지 않는다면! 
        else:
            if ChatModel.objects.count() == 0:
                temp_chat_no = "1"
            else:
                temp_chat_no = str(ChatModel.objects.latest("id").pk + 1)

            request.data.update(chatNo=temp_chat_no)

        # chat_info 추가
        chat_no_check = Chat_info.objects.filter(chatNo=temp_chat_no)
        if len(chat_no_check) > 0:
            print(chat_no_check)
        else:
            Chat_info.objects.create(chatNo=temp_chat_no, user_name_1=request.data["post_username"], user_name_2=request.data["get_username"], room_name=request.data["post_username"] + "/" + request.data["get_username"])

        request.data.update(read=request.data["post_username"] + "/" + request.data["get_username"])
        serializer = ChatSerializer(data=request.data)                      #채팅 저장
        serializerBackup = ChatBackupSerializer(data=request.data)          #백업 채팅 저장

        if serializer.is_valid():#채팅 저장
            serializer.save()
            if serializerBackup.is_valid():#백업 채팅 저장
                serializerBackup.save()
            return JsonResponse(json_success("S0005", serializer.data), status=status.HTTP_200_OK)

        return JsonResponse(json_error("E0400"), status=status.HTTP_400_BAD_REQUEST)


def check_chatNo(request):
    if validation(request.headers):
        pass
    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        request = request.GET
        temp_chatno_list = []

        if request["post_username"]:
            temp_post_username = ChatModel.objects.filter(post_username=request["post_username"])
            temp_get_username = ChatModel.objects.filter(get_username=request["post_username"])
            for te1 in temp_post_username:
                temp_chatno_list.append(te1.chatNo)
            for te2 in temp_get_username:
                temp_chatno_list.append(te2.chatNo)
            return JsonResponse([{"chatNo": list(set(temp_chatno_list))}], status=201, safe=False)

        else:
            return JsonResponse({"Error": "post_username 또는 get_username 파라미터로 보내주세요."}, status=400, safe=False)


@csrf_exempt
@api_view(["POST"])
def chat_delete(request):
    if validation(request.headers):
        pass
    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        print(request.body)
        data = JSONParser().parse(request)
        try:
            temp_chat_id = data["chat_id"]
        except KeyError:
            return JsonResponse(json_error("E0002"), status=status.HTTP_400_BAD_REQUEST)

        try:
            chat_model = ChatModel.objects.get(id=temp_chat_id)
            content = {"id": chat_model.id, "chatNo": chat_model.chatNo, "send_message": chat_model.send_message}
            chat_model.delete()
            return JsonResponse(json_success("S0003", content), status=status.HTTP_200_OK)
        except ChatModel.DoesNotExist:
            return JsonResponse(json_error("E0010"), status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
def chatNo_delete(request):
    if validation(request.headers):
        pass
    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        print(request.body)
        data = JSONParser().parse(request)
        try:
            temp_chat_no = data["chatNo"]
        except KeyError:
            return JsonResponse(json_error("E0002"), status=status.HTTP_400_BAD_REQUEST)

        try:
            chat_model = ChatModel.objects.filter(chatNo=temp_chat_no)
            if chat_model.count() < 1:
                return JsonResponse(json_error("E0010"), status=status.HTTP_400_BAD_REQUEST)
            Chat_info.objects.filter(chatNo = temp_chat_no).delete()
            for ch in chat_model:
                ch.delete()
            content = {"chatNo": data["chatNo"]}
            return JsonResponse(json_success("S0011", content), status=status.HTTP_200_OK)
        except ChatModel.DoesNotExist:
            return JsonResponse(json_error("E0010"), status=status.HTTP_400_BAD_REQUEST)


def user_chat_data(request):
    if simple_validation(request.headers):
        pass
    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    try:
        temp_request_access_token = request.headers["AccessToken"]
        user_id = access_id(temp_request_access_token)

        if user_id is False:
            return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        chat_model = ChatModel.objects.all()
        get_chat_list = chat_model.filter(post_username=user_id) | chat_model.filter(get_username=user_id)

        get_all_temp_data = []
        get_chat_no = set()
        get_chat_no_other = {}
        temp_sort_array = {}

        for ka in get_chat_list:
            get_chat_no.add(ka.chatNo)
            get_chat_no_other_model = chat_model.filter(chatNo=ka.chatNo)
            for kb in get_chat_no_other_model:
                if str(kb.post_username) == str(user_id):
                    get_chat_no_other[ka.chatNo] = kb.get_username
                else:
                    get_chat_no_other[ka.chatNo] = kb.post_username

        get_chat_no = list(get_chat_no)
        get_chat_no = sorted(get_chat_no)

        unread_count_dic = []

        for kp in get_chat_no:
            mkg = chat_model.filter(chatNo=kp)
            get_read_status_count = 0
            for kd in mkg:
                if kd.read.split("/")[0] == str(user_id):
                    if kd.post_send_status == 0:
                        get_read_status_count += 1
                elif kd.read.split("/")[1] == str(user_id):
                    if kd.get_send_status == 0:
                        get_read_status_count += 1
            unread_chat_no_push = {"chatNo": kp, "unread_count": get_read_status_count}
            unread_count_dic.append(unread_chat_no_push)

        for kc in range(0, len(get_chat_no)):
            try:
                get_other_profil_model = UserModel.objects.get(username=get_chat_no_other[get_chat_no[kc]])
                get_other_profil = str(get_other_profil_model.profile_image)
                if get_other_profil == "":
                    get_other_profil = None
            except UserModel.DoesNotExist:
                get_other_profil = "프로필 에러"
                # return JsonResponse(json_error("E0010"), status=status.HTTP_400_BAD_REQUEST)

            last_chat_model = chat_model.filter(chatNo=get_chat_no[kc]).latest("id")
            last_chat_model_push = {"chatNo": get_chat_no[kc], "other_user": get_chat_no_other[get_chat_no[kc]],
                                    "other_profile": get_other_profil, "last_message": last_chat_model.send_message,
                                    "datetime": last_chat_model.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                                    "unread_count": unread_count_dic[kc].get("unread_count")}
            temp_sort_array[last_chat_model.id] = last_chat_model_push

        sort_array_index = sorted(temp_sort_array, reverse=True)

        for ja in sort_array_index:
            get_all_temp_data.append(temp_sort_array[ja])

        count = 0
        for ev in unread_count_dic:
            count += int(ev["unread_count"])

        total_data = {"all_chatNo_size": len(get_chat_no), "chatNo_list": get_chat_no,
                      "chatNo_lasted_data": get_all_temp_data}

        return JsonResponse(json_success("S0004", total_data), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def get_chat_detail(request):
    if simple_validation(request.headers):
        pass
    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    try:
        temp_request_access_token = request.headers["AccessToken"]
        user_id = access_id(temp_request_access_token)
        if user_id is False:
            return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        data = JSONParser().parse(request)
        try:
            chat_no_data = data["chatNo"]
        except KeyError:
            return JsonResponse(json_error("E0002"), status=status.HTTP_400_BAD_REQUEST)

        chat_model = ChatModel.objects.all()
        chat_detail_list = chat_model.filter(chatNo=chat_no_data)
        all_dict = []

        for xa in chat_detail_list:
            if xa.post_username == str(user_id) and xa.post_hidden_status == 0:
                temp_owner = {"id": xa.id, "owner": str(user_id), "message": xa.send_message,
                              "created_at": xa.created_at.strftime("%Y-%m-%d %H:%M")}
                all_dict.append(temp_owner)
                xa.post_send_status = True
                xa.save()

            elif xa.get_username == str(user_id) and xa.get_hidden_status == 0:
                other_user = xa.read.split("/")[0]
                temp_owner = {"id": xa.id, "owner": other_user, "message": xa.send_message,
                              "created_at": xa.created_at.strftime("%Y-%m-%d %H:%M")}
                all_dict.append(temp_owner)
                xa.get_send_status = True
                xa.save()

        return JsonResponse(json_success("S0004", all_dict), status=status.HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
def hidden_chat(request):
    if simple_validation(request.headers):
        pass
    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    try:
        temp_request_access_token = request.headers["AccessToken"]
        ck = access_id(temp_request_access_token)
        if ck is False:
            return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JsonResponse(json_error("E0007"), status=status.HTTP_400_BAD_REQUEST)

    if request.method == "POST":
        print(request.body)
        data = JSONParser().parse(request)
        try:
            chat_no_data = data["chatNo"]
        except KeyError:
            return JsonResponse(json_error("E0002"), status=status.HTTP_400_BAD_REQUEST)

        chat_model = ChatModel.objects.all()
        chat_detail_list = chat_model.filter(chatNo=chat_no_data)

        for knkn in chat_detail_list:
            if knkn.post_username == ck.username:
                knkn.post_hidden_status = 1
            elif knkn.get_username == ck.username:
                knkn.get_hidden_status = 1
            knkn.save()

        return JsonResponse(json_success("S0004", "success"), status=status.HTTP_200_OK)

    else:
        return JsonResponse(json_error("E0006"), status=status.HTTP_400_BAD_REQUEST)