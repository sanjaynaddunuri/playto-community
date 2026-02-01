from rest_framework import serializers
from .models import Post, Comment


class RecursiveCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["id", "author", "content", "replies"]

    def get_replies(self, obj):
        return RecursiveCommentSerializer(obj.replies.all(), many=True).data


class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username")
    comments = RecursiveCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ["id", "author", "content", "comments"]
