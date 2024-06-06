from rest_framework import serializers
from ..models.comments import Comment
from ..serializers.ClientSerializer import ClientSerializer


class CommentSerializer(serializers.ModelSerializer):
    client_object = ClientSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'client_object', 'tour')
        read_only_fields = ('id', 'tour',)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        errors = {}
        comments_field = attrs.get('comment')
        if not comments_field or comments_field.strip() == '':
            errors['comments'] = "Comment  cannot be empty."
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs
