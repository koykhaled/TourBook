from rest_framework import serializers
from ..models.comments import Comment
from ..serializers.ClientSerializer import ClientSerializer


class CommentSerializer(serializers.ModelSerializer):
    client_object = ClientSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'comment', 'client_object', 'tour')
        extra_kwargs = {
            "tour": {'write_only': True},
            "client_object": {'read_only': True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        errors = {}
        comment = attrs.get('comment')
        if comment and comment.strip() == '':
            errors['comments'] = "Comment  cannot be empty."
        if len(errors) > 0:
            raise serializers.ValidationError(errors)
        return attrs
