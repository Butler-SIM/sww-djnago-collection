#POST가 아닌 PUT인경우 S3에 바로 업로드 되지않아서 직접 해줘야함
def put(self, request, *args, **kwargs):
    s3_client = boto3.client('s3',
                             aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY
                             )
    name = str(uuid.uuid4())
    user = access_id(request.headers["AccessToken"])
    event_model = PointEventModel.objects.get(id=kwargs['id'])
    if user:
        image = request.FILES.get('image')
        image_text = ''
        if event_model.point_type == 'scan':
            image_text = 'event_licenceplate/' + now().strftime("%Y%m%d") + name
            s3_client.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, 'event_licenceplate/%s/%s' % (
                now().strftime("%Y%m%d"), name))

            ScanEventModel.objects.filter(id=event_model.scan_event.id).update(scan_license_plate_image=image_text)
        else:
            image_text = 'event_photo/' + now().strftime("%Y%m%d") + name
            s3_client.upload_fileobj(image, AWS_STORAGE_BUCKET_NAME, 'event_photo/%s/%s' % (
                now().strftime("%Y%m%d"), name))

            PhotoEventModel.objects.filter(id=event_model.photo_event.id).update(event_photo=image_text)

        return JsonResponse(json_success("S0002", {"image": image_text}), status=status.HTTP_200_OK)

    else:
        return JsonResponse(json_error("E0007"), status=status.HTTP_200_OK)