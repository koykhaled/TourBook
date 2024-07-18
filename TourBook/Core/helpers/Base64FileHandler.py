from rest_framework import serializers

from django.core.files.base import ContentFile

import base64
import six
import uuid
import imghdr


class Base64FileField(serializers.FileField):
    """
    A Django REST framework field for handling file-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.
    """
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png', 'pdf']
    MAX_FILE_SIZE = 5 * 1024 * 1024

    def to_internal_value(self, data):
        errors = {}

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to dec ode the file. Return a validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                errors['file'] = "Invalid File"

            # Generate a file name: 12 characters are more than enough.
            file_name = str(uuid.uuid4())[:12]

            # Get the file name extension
            if header.startswith('data:application/pdf'):
                file_extension = "pdf"
            else:
                file_extension = self.get_file_extension(
                    file_name, decoded_file)

            if file_extension not in self.ALLOWED_EXTENSIONS:
                errors['file_type'] = "File type not allowed"

            # Additional validation for file size
            if len(decoded_file) > self.MAX_FILE_SIZE:
                errors['file_size'] = "File size is too big"

            complete_file_name = f"{file_name}.{file_extension}"
            data = ContentFile(decoded_file, name=complete_file_name)

            if len(errors) > 0:
                raise serializers.ValidationError(errors)

        return super().to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        extension = imghdr.what(file_name, decoded_file)
        if extension == "jpeg":
            extension = "jpg"

        return extension
