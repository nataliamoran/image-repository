from .models import Image
from rest_framework import serializers
from django.core.files.base import ContentFile

import base64
import six
import uuid
import imghdr

'''
---------- The following code snippet is taken from StackOverflow ----------
Source: https://stackoverflow.com/questions/31690991/uploading-base64-images-using-modelserializers-in-django-django-rest-framework
'''


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, six.string_types):
            try:
                decoded_file = base64.b64decode(bytes(data, encoding='utf8'))
            except TypeError:
                self.fail('invalid_image')

            file_name = str(uuid.uuid4())[:12]
            file_extension = self.get_file_extension(file_name, decoded_file)
            complete_file_name = "%s.%s" % (file_name, file_extension,)
            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension if extension is not None else 'jpg'


'''---------- End of StackOverflow code snippet ---------- '''


class ImageCreateSerializer(serializers.ModelSerializer):
    """
    Serializes POST API Request JSON to get data for creation of a new image.
    JSON fields:
                "image": .png or .jpeg image encoded in base64
                "public": true / false
    """
    image = Base64ImageField(max_length=None, use_url=True)
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Image
        fields = ['image', 'owner', 'public', ]


class ImageSerializer(serializers.ModelSerializer):
    """
    Default serializer not expecting any request body.
    """

    class Meta:
        model = Image
        fields = ['id', 'owner', 'image', 'public', ]
