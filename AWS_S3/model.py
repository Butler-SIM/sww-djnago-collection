def upload_image_to_licenceplate(instance, filename):
    name = str(uuid.uuid4())
    filename_base, filename_ext = os.path.splitext(filename)
    return 'event_licenceplate/%s/%s' % (
        now().strftime("%Y%m%d"),
        name
    )

class ScanEventModel(models.Model):
    class Meta:
        db_table = 'scanevent'

    user                      = models.ForeignKey('userapi.UserModel',on_delete=models.CASCADE, null=True, blank=True, verbose_name='스캔한 유저')
    scan_license_plate_image  = models.ImageField(upload_to=upload_image_to_licenceplate, editable=True, null=True, blank=True, verbose_name="번호판 사진")
    scan_license_plate_number = models.CharField(max_length=50, null=True, blank=True, verbose_name='스캔한 번호판 넘버')
    created_at                = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='생성일')
    updated_at                = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='수정일')
    found_user                = models.IntegerField(null=True, blank=True, verbose_name='찾아진 유저')