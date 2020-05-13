from rest_framework import serializers, exceptions

from userapp.models import Employee
from demo import settings


class EmployeeModelSerializer(serializers.Serializer):
    """
    需要为每一个model编写一个独立的序列化器
    """
    username = serializers.CharField()
    # password = serializers.CharField()
    # gender = serializers.IntegerField()
    # pic = serializers.ImageField()

    # SerializerMethodField 自定义一个序列化字段
    aaa = serializers.SerializerMethodField()

    # 自定义字段属性名随意，但提供值的方法有一个固定的命令规范
    # get_属性名就是为自定义字段提供值得方法 self是参与序列化的model
    # 返回值就是自定义的值
    def get_aaa(self, obj):
        return "example"

    # 自定义返回的性别
    gender = serializers.SerializerMethodField()

    def get_gender(self, obj):
        # print(self, type(self))
        print(obj.gender, type(obj))
        # 如果获取choices类型解释型的值，可以通过 get_字段名_display()访问
        return obj.get_gender_display()

    # 自定义返回图片的全路径
    pic = serializers.SerializerMethodField()

    def get_pic(self, obj):
        # print(type(obj.pic))
        # print("http://127.0.0.1:8000" + settings.MEDIA_URL + str(obj.pic))
        # http://127.0.0.1:8000/media/pic/1.jpeg/
        return "%s%s%s" % ("http://127.0.0.1:8000", settings.MEDIA_URL, str(obj.pic))


class EmployeeDeserializer(serializers.Serializer):
    """
    反序列化：将前台提交的数据入库
    1. 前台需要提供哪些反序列化的字段
    2. 对字段进行安全校验
    3. 哪些字段需要提供额外的校验
    反序列化有自定义字段  没有
    """

    # 添加反序列化校验规则  与错误信息
    username = serializers.CharField(
        max_length=10,
        min_length=2,
        error_messages={
            "max_length": "长度太长",
            "min_length": "长度太短"
        }
    )
    password = serializers.CharField()
    # phone不是必填参数
    phone = serializers.CharField(required=False)

    # 重复密码
    re_pwd = serializers.CharField()

    # 局部校验钩子 对反序列化器中的某个字段进行校验
    def validate_username(self, value):
        if "1" in value:
            raise exceptions.ValidationError("用户名异常")
        return value

    # 全局的校验钩子，会对反序列化器中所有校验规则进行验证
    def validate(self, attrs):
        print(attrs, "attr")
        password = attrs.get("password")
        re_pwd = attrs.pop("re_pwd")
        if password != re_pwd:
            raise exceptions.ValidationError("两次密码不一致")
        return attrs

    # 完成员工新增需要实现create方法
    # 在create()方法完成保存之前  会先调用局部钩子  全局钩子函数来完成字段的校验
    def create(self, validated_data):
        print(validated_data)
        # 自己实现保存的逻辑 校验数据 校验通过后保存
        return Employee.objects.create(**validated_data)
