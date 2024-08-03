from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
import jwt
from app import models
tokenKey = "secret"
tokenAlgorithm = "HS256"
from django.shortcuts import HttpResponse
class AuthenticationMiddleware(MiddlewareMixin):
    """登录信息鉴权"""

    def process_request(self,request):
        # print(request.path_info)

        # return


        if(models.Option.objects.filter(key="subSystem").first().value!="0"):
            return

        if request.path_info == "/register/" or request.path_info == "/login/" or request.path_info == "/logout/" or request.path_info == "/option/isSubsystem/":
            return
        if(request.path_info[0:5] == "/src/"):
            return
        
        



        # 运维接口访问
        if ("Api-Token" in dict(request.headers)):
            token = request.headers['Api-Token']
            if(models.Option.objects.filter(key="APIToken").first().value == token):
                return
            else:
                return HttpResponse({"API token error"})  
        
        # 用户接口访问
        if ("Token" in dict(request.headers)):
            try:
                token = request.headers['Token']
                usernameObj = jwt.decode(token,tokenKey,tokenAlgorithm)
                # print(token)
                if(models.UserInfo.objects.filter(**usernameObj).count()!=0):
                    return
                else:
                    return HttpResponse("token no exist") 
            except:
                return HttpResponse("token error") 
        else:
            return HttpResponse("No Authentication!") 
        
        return
        


    def process_response(self,request,response):

        return response