from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.models import Book


class BookAPIVIew(APIView):

    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookModelSerializer(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.all()
            book_data = serializers.BookModelSerializer(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })

    def post(self, request, *args, **kwargs):
        """只考虑增加单个"""
        request_data = request.data
        # 反序列化的时候需要将参数赋值关键字 data
        book_ser = serializers.BookModelDeSerializer(data=request_data)
        # 校验数据是否合法
        # raise_exception=True: 当校验失败的时候，马上终止当前视图方法，抛出异常到前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.BookModelSerializer(book_obj).data
        })


class BookAPIVIew2(APIView):

    def get(self, request, *args, **kwargs):
        """想要同时查询图书对应出版社的信息"""
        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id)
                book_ser = serializers.BookModelSerializer(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.all()
            book_data = serializers.BookModelSerializer(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })


class BookAPIVIewV2(APIView):
    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id, is_delete=False)
                book_ser = serializers.BookModelSerializerV2(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_data = serializers.BookModelSerializerV2(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })

    def post(self, request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):
            # 代表单增
            # book_ser = serializers.BookModelSerializerV2(data=request_data)
            many = False
        elif isinstance(request_data, list):
            # 代表秦增
            # book_ser = serializers.BookModelSerializerV2(data=request_data, many=True)
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })

        # 反序列化的时候需要将参数赋值关键字 data
        book_ser = serializers.BookModelSerializerV2(data=request_data, many=many)
        # 校验数据是否合法
        # raise_exception=True: 当校验失败的时候，马上终止当前视图方法，抛出异常到前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            # 报错
            "results": serializers.BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个以及删除多个
        :param request: 请求的DRF对象
        # 单个删除：  有id  且是通过路径传参  v2/books/1/
        # 多个删除： 有多个id json传参 {"ids": [1,2,3]}
        """
        book_id = kwargs.get("id")
        if book_id:
            # 单删
            ids = [book_id]
        else:
            # 群删
            ids = request.data.get("ids")

        # 判断id是否图书存在 且未删除
        res = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if res:
            return Response({
                "status": 200,
                "message": "删除成功",
            })

        return Response({
            "status": 500,
            "message": "删除失败或者已删除",
        })

    def put(self, request, *args, **kwargs):
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            # 通过获取的id来找到要修改的对象
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "图书不存在",
            })

        book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)

        # 如果校验通过 则保存
        book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            # 则修改完成的对象返回到前台，需要经过序列化器序列化
            "results": serializers.BookModelSerializerV2(book_obj).data
        })

    # def patch(self, request, *args, **kwargs):
    #
    #     request_data = request.data
    #     book_id = kwargs.get("id")
    #
    #     try:
    #         book_obj = Book.objects.get(pk=book_id, is_delete=False)
    #     except:
    #         return Response({
    #             "status": 500,
    #             "message": "图书不存在",
    #         })
    #     # partial=True  指定序列化器为更新部分字段  有哪个字段的值就修改哪个字段  没有不修改
    #     book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
    #     # 在数据校验之前告诉序列化器我要修改的是部分字段
    #     book_ser.is_valid(raise_exception=True)
    #
    #     # 如果校验通过 则保存
    #     book_ser.save()
    #
    #     return Response({
    #         "status": 200,
    #         "message": "更新成功",
    #         # 则修改完成的对象返回到前台，需要经过序列化器序列化
    #         "results": serializers.BookModelSerializerV2(book_obj).data
    #     })

    def patch(self, request, *args, **kwargs):

        request_data = request.data
        book_id = kwargs.get("id")

        # 如果pk存在且传递的参数是字典  单改  [{pk:1, publish: 4}]
        if book_id and isinstance(request_data, dict):
            # 单改转换成 群改一个
            book_ids = [book_id, ]
            request_data = [request_data, ]
        # 如果pk不存在且传递的参数是列表  群改
        elif not book_id and isinstance(request_data, list):
            # 群改
            book_ids = []
            # 从获取的数据中将pk拿出来放进book_ids
            for dic in request_data:
                pk = dic.pop("pk", None)
                if pk:
                    book_ids.append(pk)
                else:
                    return Response({
                        "status": 500,
                        "message": "ID不存在"
                    })
        else:
            return Response({
                "status": 500,
                "message": "数据不存或格式有误"
            })

        print(request_data)
        print(book_ids)

        # 对book_ids与request_data数据进行筛选
        # 对不存在的对象pk进行移除 request_data 也移除  如果存在  查询出对应的对象
        book_list = []
        # TODO 不要循环中对列表的长度做操作
        new_data = []
        #  [ {pk:1, publish: 4}, {pk:2, price: 88.8}, {pk:3, boo_name: 123} ]
        for index, pk in enumerate(book_ids):
            try:
                book_obj = Book.objects.get(pk=pk)
                book_list.append(book_obj)
                # 对应的索引的数据保存
                new_data.append(request_data[index])
                # print(request_data[index])
            except:
                # 不存在则移除  错误示范
                # index = book_ids.index(pk)
                # request_data.pop(index)
                continue

        book_ser = serializers.BookModelSerializerV2(data=new_data, instance=book_list, partial=True, many=True)
        book_ser.is_valid(raise_exception=True)
        book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.BookModelSerializerV2(book_list, many=True).data
        })

