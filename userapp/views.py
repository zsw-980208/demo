from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer, TemplateHTMLRenderer, MultiPartRenderer
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework import serializers
from userapp.models import UserInfo, Student, Employee
from userapp.serializers import EmployeeModelSerializer, EmployeeDeserializer

"""
FBV: function base view  函数视图
CBV: class base view 类视图
"""


def user(request):
    if request.method == "GET":
        print("GET 查询")
        return HttpResponse("GET SUCCESS")
    elif request.method == "POST":
        print("POST 添加")
        return HttpResponse("POST SUCCESS")
    elif request.method == "PUT":
        print("PUT 修改")
        return HttpResponse("PUT SUCCESS")
    elif request.method == "DELETE":
        print("DELETE 删除")
        return HttpResponse("DELETE SUCCESS")


"""
单个接口：获取单条 获取所有 新增单条 删除单条 整体更新单条 局部更新单条
群体接口：群体增加   群体删除    整体群改  局部群改
"""


# csrf_exempt: 可以免除某个方法的csrf认证
# csrf_protect：可以为某个视图单独添加csrf认证
@method_decorator(csrf_exempt, name="dispatch")
class UserView(View):

    def get(self, request, *args, **kwargs):
        """提供查询单个  多个用户的API"""
        user_id = kwargs.get("pk")
        if user_id:  # 查询单个
            user_values = UserInfo.objects.filter(pk=user_id).values("username", "password", "gender").first()
            if user_values:
                return JsonResponse({
                    "status": 200,
                    "message": "获取用户成功",
                    "results": user_values
                })
        else:  # 如果用户id不存且发的是get请求  代表是获取全部用户信息
            user_list = UserInfo.objects.all().values("username", "password", "gender")
            if user_list:
                return JsonResponse({
                    "status": 201,
                    "message": "获取用户列表成功",
                    "results": list(user_list)
                })

        return JsonResponse({
            "status": 400,
            "message": "获取用户不存在",
        })

    def post(self, request, *args, **kwargs):
        """完成新增单个用户的操作"""
        print(request.POST)
        # 对post传递过来的参数进行校验
        try:
            user_obj = UserInfo.objects.create(**request.POST.dict())
            if user_obj:
                return JsonResponse({
                    "status": 200,
                    "message": "新增用户成功",
                    "results": {"username": user_obj.username, "gender": user_obj.gender}
                })
            else:
                return JsonResponse({
                    "status": 500,
                    "message": "新增用户失败",
                })
        except:
            return JsonResponse({
                "status": 501,
                "message": "参数有误",
            })

    def put(self, request, *args, **kwargs):
        print("PUT 修改")
        print(request.put)
        return HttpResponse("CLASS PUT SUCCESS")

    def delete(self, request, *args, **kwargs):
        print("DELETE 删除")
        return HttpResponse("CLASS DELETE SUCCESS")


class StudentView(APIView):
    # renderer_classes = [MultiPartRenderer]
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        """DRF获取get请求参数的方式"""
        # print(request._request.GET)  # 原生django request对象
        # print(request.GET)  # DRF request 对象
        # print(request.query_params)  # DRF 扩展的get请求参数
        # return Response("GET SUCCESS")

        user_id = kwargs.get("pk")
        if user_id:  # 查询单个
            stu = Student.objects.filter(pk=user_id).values("name", "age").first()
            if stu:
                return JsonResponse({
                    "status": 200,
                    "message": "获取用户成功",
                    "results": stu
                })
        else:  # 如果用户id不存且发的是get请求  代表是获取全部用户信息
            stu_list = Student.objects.all().values("name", "age")
            if stu_list:
                return JsonResponse({
                    "status": 201,
                    "message": "获取用户列表成功",
                    "results": list(stu_list)
                })

        return JsonResponse({
            "status": 400,
            "message": "获取用户不存在",
        })

    def post(self, request, *args, **kwargs):
        """DRF 获取POST请求参数的方式"""
        # POST传递参数的形式 formdata urlencoding Json
        # print(request._request.POST)  # 原生django request对象
        # print(request.POST)  # DRF request 对象
        # print(request.data)  # DRF 扩展post请求参数   兼容性最强
        #
        # return Response("POST SUCCESS")
        print(123)
        print(request._request.POST)  # 原生django request对象
        # print(request.POST)  # DRF request 对象
        # print(request.data)  # DRF 扩展post请求参数   兼容性最强
        # # 对post传递过来的参数进行校验
        data=request._request.POST
        print(data)
        if data:
            try:
                stu1 = Student.objects.create(**data.dict())
                if stu1:
                    return JsonResponse({
                        "status": 200,
                        "message": "新增用户成功",
                        "results": {"name": stu1.name, "age": stu1.age}
                    })
                else:
                    return JsonResponse({
                        "status": 500,
                        "message": "新增用户失败",
                    })
            except:
                return JsonResponse({
                    "status": 501,
                    "message": "参数有误",
                })
        else:
            return JsonResponse({
                "status":502,
                "message":"参数不能为空"
            })


class EmployeeAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """查询可以查单个以及多个"""
        emp_id = kwargs.get("id")

        if emp_id:
            try:
                emp_obj = Employee.objects.get(pk=emp_id)
                # print(emp_obj, type(emp_obj))
                # 在员工信息查询完成后需要手动的进行序列化，转成可识别的python类型
                emp_ser = EmployeeModelSerializer(emp_obj).data
                return Response({
                    "status": 200,
                    "message": "用户查询成功",
                    "results": emp_ser,
                })
            except:
                return Response({
                    "status": 500,
                    "message": "用户不存在"
                })
        # 查询全部
        else:
            # 也需要将查询出的员工集进行序列化
            emp_list = Employee.objects.all()
            emp_ser = EmployeeModelSerializer(emp_list, many=True).data
            return Response({
                "status": 200,
                "message": "用户列表查询成功",
                "results": emp_ser,
            })

    def post(self, request, *args, **kwargs):
        """反序列化暂时只考虑新增单个"""
        # 接受参数
        request_data = request.data

        # TODO 验证数据是否合法
        if not isinstance(request_data, dict) or request_data == {}:
            return Response({
                "status": 500,
                "message": "数据有误"
            })

        # 校验数据的内容是否合法  传入序列化数据的时候需要指定关键字参数 data
        deserializer = EmployeeDeserializer(data=request_data)
        # print(deserializer)
        # 使用is_valid()进行数据校验  校验成功返回True  失败则错误会保存在 .errors中
        if deserializer.is_valid():
            # 通过save()方法完成新增
            emp_obj = deserializer.save()
            print(emp_obj)
            return Response({
                "status": 200,
                "message": "用户创建成功",
                # 将保存的数据响应到前台  是序列化而不是反序列化
                "results": EmployeeModelSerializer(emp_obj).data
            })
        else:
            return Response({
                "status": 500,
                "message": "用户创建失败",
                "results": deserializer.errors
            })
