from rest_framework import serializers

from api.models import Book


class BookListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "authors", "publish", "author_list", "publish_name",)

        list_serializer_class = BookListSerializer

        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 5,  # 设置最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            },
            "authors": {
                "write_only": True  # 只参与反序列化
            },
            "publish": {
                "write_only": True  # 只参与反序列化
            },
            "author_list": {
                "read_only": True  # 序列化
            },
            "publish_name": {
                "read_only": True  # 序列化
            },
            "pic": {
                "read_only": True  # 序列化
            },
        }

    def validate_book_name(self, value):
        print(self.context.get("request").method)
        return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        book_name = attrs.get("book_name")
        book_obj = Book.objects.filter(book_name=book_name, publish=publish)
        if book_obj:
            raise serializers.ValidationError("该出版社已经发布过该图书")

        return attrs
