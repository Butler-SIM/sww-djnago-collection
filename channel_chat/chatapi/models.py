from django.db import models


class ChatModel(models.Model):
    class Meta:
        verbose_name = "메세지"
        verbose_name_plural = "메세지 목록"

    chatNo = models.CharField(max_length=255, null=False, blank=True, verbose_name="채팅방 번호")
    read = models.CharField(max_length=255, null=False, blank=True, verbose_name="읽기 가능한 계정")
    post_username = models.CharField(max_length=50, null=False, blank=False, verbose_name="보내는 아이디")
    get_username = models.CharField(max_length=50, null=False, blank=False, verbose_name="받는 아이디")
    send_message = models.TextField(null=False, blank=False, verbose_name="메세지 내용")
    post_send_status = models.BooleanField(null=False, blank=True, default=False, verbose_name="보내는 사람 읽음 여부")
    get_send_status = models.BooleanField(null=False, blank=True, default=False, verbose_name="받는 사람 읽음 여부")
    post_hidden_status = models.BooleanField(null=True, blank=True, default=False, verbose_name="보내는 사람 숨김 여부")
    get_hidden_status = models.BooleanField(null=True, blank=True, default=False, verbose_name="받는 사람 숨김 여부")
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="생성 날짜")


class ChatBackupModel(models.Model):    #채팅 백업
    class Meta:
        verbose_name = "백업 메세지"
        verbose_name_plural = "백업 메세지 목록"

    chatNo = models.CharField(max_length=255, null=False, blank=True, verbose_name="채팅방 번호")
    read = models.CharField(max_length=255, null=False, blank=True, verbose_name="읽기 가능한 계정")
    post_username = models.CharField(max_length=50, null=False, blank=False, verbose_name="보내는 아이디")
    get_username = models.CharField(max_length=50, null=False, blank=False, verbose_name="받는 아이디")
    send_message = models.TextField(null=False, blank=False, verbose_name="메세지 내용")
    post_send_status = models.BooleanField(null=False, blank=True, default=False, verbose_name="보내는 사람 읽음 여부")
    get_send_status = models.BooleanField(null=False, blank=True, default=False, verbose_name="받는 사람 읽음 여부")
    post_hidden_status = models.BooleanField(null=True, blank=True, default=False, verbose_name="보내는 사람 숨김 여부")
    get_hidden_status = models.BooleanField(null=True, blank=True, default=False, verbose_name="받는 사람 숨김 여부")
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=True, verbose_name="생성 날짜")


class Chat_info(models.Model):
    class Meta:
        verbose_name = "채팅 정보"
        verbose_name_plural = "채팅 정보 목록"

    chatNo = models.CharField(max_length=255, null=False, blank=True, verbose_name="채팅방 번호")
    room_name = models.CharField(max_length=255, null=False, blank=True, verbose_name="채팅방 이름")
    user_name_1 = models.TextField(max_length=100, null=False, blank=True, verbose_name="유저_1")
    user_name_2 = models.TextField(max_length=100, null=False, blank=True, verbose_name="유저_2")
    user_1_status = models.BooleanField(null=False, blank=True, default=False, verbose_name="유저1 입장상태")
    user_2_status = models.BooleanField(null=False, blank=True, default=False, verbose_name="유저2 입장상태")
    
class ChatConnectUserModel(models.Model):
    class Meta:
        verbose_name = "웹소켓 연결 유저 목록"
        verbose_name_plural = "웹소켓 연결 유저 목록"

    room_name = models.CharField(max_length=255, null=False, blank=True, verbose_name="채팅방 이름")
    user_name = models.CharField(max_length=100, null=False, blank=True, verbose_name="유저")
    session = models.TextField(null=False,blank=True, verbose_name="접속 세션")

