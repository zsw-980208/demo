from rest_framework.response import Response


class MYResponse(Response):

    def __init__(self, data_status=100, data_message=0, results=None, http_status=None, headers=None, exception=False,
                 **kwargs):
        # 返回数据的初始状态
        data = {
            "status": data_status,
            "message": data_message
        }

        # 判断result是否有结果
        if results is not None:
            data['results'] = results

        # 如果有其他参数  r如果有参数就更新进去  没有不做任何操作
        data.update(kwargs)
        # if kwargs is not None:
        #     for key, value in kwargs.items():
        #         setattr(data, key, value)

        # 获取response对象， 将自定后的对象响应回去  调用父类的Response
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)

"""
Response({
    "status": 200,
    "message": "更新成功",
    "results": []
        }, status=http_status, headers, exception)
        
MYResponse()  => Response()
"""
