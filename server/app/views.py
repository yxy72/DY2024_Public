import os
from django.shortcuts import HttpResponse

from django.http import JsonResponse

from app import models

import json
import hashlib
import jwt
import numpy as np

from django.conf import settings
from PIL import Image

from utils.CNN import preData,Model,calModelLayers,queryModel,Predict
from utils.Embed import CalTrans
import utils.KnowledgeGraph as KG
from utils.Global import QM_Result
from utils.PSO import PSO_RUN
import configs

needLogin = True
tokenKey = "secret"
tokenAlgorithm = "HS256"
serverSuccessResponse = "success"

def cnm(request):
    print(request.GET)
    return HttpResponse(request.GET)

def dev(req):
    exist = os.listdir("E:/ProjectHDD/Vue/DY_TS/server/DY_Server_Py/static/models/users/yxy")
    for i in exist:
        os.remove("E:/ProjectHDD/Vue/DY_TS/server/DY_Server_Py/static/models/users/yxy/%s"%i)
        
    return HttpResponse("helloworld")

# from app import init_mysql
# def SYSTEMINIT(req):
#     init_mysql.RUNINTI()
    
#     return HttpResponse("done")

# 设置头像
def postUserAvatar(req):
    if(needLogin):
        if ("Token" not in dict(req.headers)):
            return JsonResponse({"status":"failed"})
        token = req.headers['Token'];
    else:
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.qQSekbR5BFKQPc3_7gUiDY6Q9y7RojKzvBTLJ9jGtec"

    usernameObj = jwt.decode(token,tokenKey,tokenAlgorithm)
    username = usernameObj['username']


    file = (req.FILES.get('file'))
    jpg = Image.open(file)
    full_name = "%s/images/users/%s.jpg" %(settings.MEDIA_ROOT, username)
    jpg.save(full_name)
    newAvatar = "/src/images/users/%s.jpg"%(username)
    models.UserInfo.objects.filter(username=username).update(avatar=newAvatar)
    return JsonResponse({"status":serverSuccessResponse,"avatar":newAvatar})


# 此处前端为el-upload自动上传
def postModelView(req):
    # print(dict(req.headers))
    username = req.headers['Username']
    target = req.headers['Model-Target']

    file = (req.FILES.get('file'))

    
    filter = models.UserModel.objects.filter(username=username).first()

    if(filter.model_temp):
        filter.model_temp.delete()
    filter.model_temp = file
    filter.save()

    if(target=="cnn"):
        model_url = "%s/%s"%(settings.MEDIA_ROOT,filter.model_temp)
        _,n,s,i,o = queryModel(model_url)
        exist = os.listdir("%s/models/users/%s"%(settings.MEDIA_ROOT,username))
        for id in exist:
            if(id[0:4]=="cnn_"):
                os.remove("%s/models/users/%s/%s"%(settings.MEDIA_ROOT,username,id))
        filter.model_cnn = file
        filter.save()
        return JsonResponse({"status":"success","name":n,"size":s,"in":i,"out":o})
    elif(target=="crnn"):
        model_url = "%s/%s"%(settings.MEDIA_ROOT,filter.model_temp)
        _,n,s,i,o = queryModel(model_url)
        # if(int(o)!=1):
        #     return JsonResponse({"status":"out channels error","out":o})
        # elif(int(o)==1):
        exist = os.listdir("%s/models/users/%s"%(settings.MEDIA_ROOT,username))
        for id in exist:
            if(id[0:5]=="crnn_"):
                os.remove("%s/models/users/%s/%s"%(settings.MEDIA_ROOT,username,id))
        filter.model_crnn = file
        filter.save()
        return JsonResponse({"status":"success","name":n,"size":s,"in":i,"out":o})
    elif(target=="lstm"):
        model_url = "%s/%s"%(settings.MEDIA_ROOT,filter.model_temp)
        _,n,s,i,o = queryModel(model_url)
        # if(int(o)!=1):
        #     return JsonResponse({"status":"out channels error","out":o})
        # elif(int(o)==1):
        exist = os.listdir("%s/models/users/%s"%(settings.MEDIA_ROOT,username))
        for id in exist:
            if(id[0:5]=="lstm_"):
                os.remove("%s/models/users/%s/%s"%(settings.MEDIA_ROOT,username,id))
        filter.model_lstm = file
        filter.save()
        return JsonResponse({"status":"success","name":n,"size":s,"in":i,"out":o})
    # 登录

def getLoginDefaultData(username,token=""):
    return {
        "username" : username,
        "avatar" : str(models.UserInfo.objects.filter(username=username).first().avatar),
        "admin" : models.UserInfo.objects.filter(username=username).first().useradmin,
        "token" :token,
        "tokenExpires":models.Option.objects.filter(key="userTokenExpires").first().value,
        "preData":preData,
    }
# 登录
def loginView(req):
    # models.UserInfo.objects.create(name="admin",password="admin")
    
    data = json.loads(req.body)
    username = data["username"]
    
    password = data["password"]
    if(models.UserInfo.objects.filter(username=username).count()==0):
        return JsonResponse({"status":"username error"})
    else:
        md5 = hashlib.md5()
        md5.update(password.encode(encoding='utf-8'))
        password_md5 = md5.hexdigest()
        if(models.UserInfo.objects.filter(username=username,password=password_md5).count()==0):
            return JsonResponse({"status":"password error"})
        else:
            # 登录成功
            token = jwt.encode({"username":username},tokenKey,algorithm=tokenAlgorithm)
            if(models.UserInfo.objects.filter(username=username).first().login):
                return JsonResponse({"status":"login error","data":getLoginDefaultData(username=username,token=token)})
            models.UserInfo.objects.filter(username=username).update(login=True)
            return JsonResponse({"status":serverSuccessResponse,"data":getLoginDefaultData(username=username,token=token)})

# 获取当前token的用户名
def getUserView(request):
    subs = False
    login = False

    if(models.Option.objects.filter(key="subSystem").first().value!="0"):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.qQSekbR5BFKQPc3_7gUiDY6Q9y7RojKzvBTLJ9jGtec"
        subs = True
    else:
        if ("Token" in dict(request.headers)):
            token = request.headers['Token']
        else:
            return JsonResponse({"status":"failed"})
    usernameObj = jwt.decode(token,tokenKey,tokenAlgorithm)
    username = usernameObj['username']
    if(models.UserInfo.objects.filter(username=username).first().login):
        login = True
    return JsonResponse({"status":serverSuccessResponse,"subsystem":subs,"login":login,"data":getLoginDefaultData(username=username)})

    
# 注销
def logout(req):
    models.UserInfo.objects.filter(username=json.loads(req.body)["username"]).update(login=False)
    return HttpResponse("88"+json.loads(req.body)["username"])

# 注册
def register(req):
    data = json.loads(req.body)
    serial = data["serial"]

    # 验证注册序列号
    serialOBJ = models.RegisterSerialNumber.objects.filter(serial=serial)
    if(serialOBJ.count()==0):
        return HttpResponse("serial error")
    
    # 注册用户
    username = data["username"]
    if(models.UserInfo.objects.filter(username=username).count()==1):
        return HttpResponse("username error")
    password = data["password"]
    md5 = hashlib.md5()
    md5.update(password.encode(encoding='utf-8'))
    password_md5 = md5.hexdigest()
    models.UserInfo.objects.create(username=username,password=password_md5,useradmin=serialOBJ.first().serialadmin)
    models.UserModel.objects.create(username=username)


    return HttpResponse(serverSuccessResponse)

# 管理员注册
def registConfig(req):
    data = json.loads(req.body)


    username = data["username"]
    if(models.UserInfo.objects.filter(username=username).count()==1):
        return JsonResponse({"status":"username error"})
    md5 = hashlib.md5()
    md5.update("123456".encode(encoding='utf-8'))
    password_md5 = md5.hexdigest()
    admin = data["useradmin"]
    models.UserInfo.objects.create(username=username,password=password_md5,useradmin=admin)
    models.UserModel.objects.create(username=username)

    filter = models.UserInfo.objects.all()
    userList = []
    for item in filter:
        userList.append({
           "id":item.id,
           "username":item.username,
           "useradmin":"管理员" if item.useradmin else "用户",
           "date_create":item.date_create.strftime("%Y/%m/%d %H:%M:%S")
        })
    return JsonResponse({"status":serverSuccessResponse,"userList":userList})
    
# 访问鉴权（此时已经过中间件）
def checkauth(req):
    return HttpResponse(serverSuccessResponse)


# 获取用户列表
def getAllUser(req):
    filter = models.UserInfo.objects.all()
    data = []
    for item in filter:
        data.append({
           "id":item.id,
           "username":item.username,
           "useradmin":"管理员" if item.useradmin else "用户",
           "date_create":item.date_create.strftime("%Y/%m/%d %H:%M:%S")
        })
    return JsonResponse({"status":serverSuccessResponse,"userList":data})
# ！删除用户！#
def deleteUser(req):
    username = json.loads(req.body)['username']
    models.UserInfo.objects.filter(username=username).delete()
    return JsonResponse({"status":serverSuccessResponse})

# 更改用户信息
def changeUser(req):

    data = json.loads(req.body)
    # 只更改用户名
    if(data["type"]=="username"):
        username = data["username"]
        token = jwt.encode({"username":username},tokenKey,algorithm = tokenAlgorithm)
        if(not data["changeusername"]):
            return JsonResponse({"status":serverSuccessResponse,"token":token})
        if(models.UserInfo.objects.filter(username=username).count()==1): 
            return JsonResponse({"status":"failed","reason":"用户名已存在。"})
        username_old = jwt.decode(req.headers['Token'],tokenKey,'HS256')["username"]
        models.UserInfo.objects.filter(username=username_old).update(username=username)
        return JsonResponse({"status":serverSuccessResponse,"token":token})
    elif(data["type"]=="password"):
        # 更改密码时当前面输入错误
        md5 = hashlib.md5()
        md5.update(data["password"].encode(encoding='utf-8'))
        password_md5 = md5.hexdigest()
        username_old = jwt.decode(req.headers['Token'],tokenKey,'HS256')["username"]
        if(models.UserInfo.objects.filter(username=username_old,password=password_md5).count()==0):
            return JsonResponse({"status":"failed","reason":"原密码输入错误。"})
        md5_new = hashlib.md5()
        md5_new.update(data["password_new"].encode(encoding='utf-8'))
        password_new_md5 = md5_new.hexdigest()
        # 更改密码时更改了用户名
        if(data["changeusername"]):
            if(models.UserInfo.objects.filter(username=data["username"]).count()==1): 
                return JsonResponse({"status":"failed","reason":"用户名已存在。"})
            models.UserInfo.objects.filter(username=username_old).update(username=data["username"],password=password_new_md5)
            token = jwt.encode({"username":data["username"]},tokenKey,algorithm = tokenAlgorithm)
            return JsonResponse({"status":serverSuccessResponse,"token":token})
        # 更改密码时未更改用户名
        elif(not data["changeusername"]):
            models.UserInfo.objects.filter(username=data["username"]).update(password=password_new_md5)
            token = jwt.encode({"username":data["username"]},tokenKey,algorithm = tokenAlgorithm)
            return JsonResponse({"status":serverSuccessResponse,"token":token})
    return JsonResponse({"status":"failed","reason":"数据包格式不正确。"})



# USERMODELS = {}
# 训练模型
def train(req):
    data = json.loads(req.body)
    model = Model(data["sendData"]["xData"],data["sendData"]["yData"],data["parameters"],data["preProcess"],data["username"])
    # print('='*80)
    # print(data)
    # print('='*80)
    (status,name,url) = model.run()
    return JsonResponse({"status":status,"name":name,"url":url})

def optimizeView(req):
    data = json.loads(req.body)
    username = data["username"]
    parameters = data["parameters"]
    iterations = data["iterations"]
    res = PSO_RUN(username,parameters,iterations)
    if(res['finished']):
        return JsonResponse({"status":serverSuccessResponse,"data":res["data"].tolist(),"maxmin":res["MAXMIN"]})
    else:
        return JsonResponse({"status":'failed'})
    


# 保存模型到这里
# def trainSaveView(req):
#     data = json.loads(req.body)
#     username = data["username"]
#     filename = data["filename"]
#     if( models.UserModel.objects.filter(username=username).count()==1):
#         models.UserModel.objects.filter(username=username).update(model_defalut='models/users/%s/%s.h5'%(username,filename))
#     else:
#         models.UserModel.objects.create(username=username,model_defalut='models/users/%s/%s.h5'%(username,filename))
    
#     return JsonResponse({"status":"success"})




def calModelLayer(req):
    data = json.loads(req.body)
    dimX = data["dimX"]
    dimY = data["dimY"]
    layers = calModelLayers(dimX,dimY)
    return JsonResponse({"status":"success","layers":layers})

# 获取模型信息
def queryModelInfo(req):

    target = json.loads(req.body)["username"]
    type = json.loads(req.body)["type"]
    # filter = models.UserModel.objects.filter(username=target)
    # if(filter.count()==0):
    #     return JsonResponse({"status":"failed","reason":"no exist"});
        
    
    if(type == "cnn"):
        model_url = "%s%s"%(settings.MEDIA_ROOT,models.UserModel.objects.filter(username=target).first().model_cnn) if models.UserModel.objects.filter(username=target).first().model_cnn else ""
    elif(type == "crnn"):
        model_url = "%s%s"%(settings.MEDIA_ROOT,models.UserModel.objects.filter(username=target).first().model_crnn) if models.UserModel.objects.filter(username=target).first().model_crnn else ""
    elif(type == "lstm"):
        model_url = "%s%s"%(settings.MEDIA_ROOT,models.UserModel.objects.filter(username=target).first().model_lstm) if models.UserModel.objects.filter(username=target).first().model_lstm else ""

    if(model_url == ""):
        return JsonResponse({"status":"failed","reason":"no exist"});

    status,n,s,i,o = queryModel(model_url)
    if(status=="no exist"):
        # 服务端有人手动删除了文件（ZGS！！！
        target = models.UserModel.objects.filter(username=target).first()
        if(type == "cnn"):
            target.model_cnn.delete()
            target.save()
        if(type == "crnn"):
            target.model_crnn.delete()
            target.save()
        if(type == "lstm"):
            target.model_lstm.delete()
            target.save()
        return JsonResponse({"status":"failed","reason":"no exist"});
    else:
        return JsonResponse({"status":serverSuccessResponse,"name":n,"size":s,"in":i,"out":o});

# 预测数据
def predictView(req):
    target = json.loads(req.body)
    username = target["username"]
    data = target["data"]

    model_url = "%s%s"%(settings.MEDIA_ROOT,models.UserModel.objects.filter(username=username).first().model_cnn)
  
    pre = Predict(username,data,model_url)
    res = pre.predict()

    return JsonResponse({"status":serverSuccessResponse,"result":res})



def embedView(req):
    target = json.loads(req.body)
    username = target["username"]
    entities = target["entities"]
    edges = target["edges"]
    triplets = target["triplets"]
    dim = target["dim"]
    kind = target["kind"]
    EmbedE,EmbedR,E_label,R_label = CalTrans(username,entities,edges,triplets,dim,kind)

    # print(target)
    return JsonResponse({"status":serverSuccessResponse,"result":{"EmbedE":EmbedE,"EmbedR":EmbedR,"E_label":E_label,"R_label":R_label}})

def kgInitView(req):
    
    # address = ""
    # if("address" in target):
    #     address = target["address"]
    obj = KG.getGrphInfo()
    if(obj["status"]):
        return JsonResponse({"status":serverSuccessResponse,"obj":obj})
    else:
        return JsonResponse({"status":"failed","obj":{"url":obj["url"]}})

def kgQueryView(req):
    target = json.loads(req.body)
    return JsonResponse({"status":serverSuccessResponse,"list":KG.query(target["label"])})
        
def kgExportView(req):
    success,obj = KG.getAllTriples()
    if(success):
        return JsonResponse({"status":success,"obj":obj})
    else:
        return JsonResponse({"status":success})
def kgSendView(req):
    tar = json.loads(req.body)


    s = KG.autoTriplesToKG(tar["target"],tar["tripletList"])["status"]
    if(s):
        return JsonResponse({"status":serverSuccessResponse})
    else:
        return JsonResponse({"status":"failed"})
        
def setKGIPView(req):
    target = json.loads(req.body)
    newURL = target["new_url"]
    
    configs.neo4j_url = newURL
   
    return JsonResponse({"status": "success"})





from utils.Analyze import CRNN,LSTM
# CRNN & LSTM
def analyzeTrainView(req):
    target = json.loads(req.body)
    username = target['username']
    data = target['data']
    win = target['window']
    epoch = target['epoch']
    out = target['outsize']
    modelname = target['model']
    
    if(modelname=="crnn"):
        model = CRNN(username)
    elif(modelname=="lstm"):
        model = LSTM(username)
    # print(np.shape(data))
    model.init_train(data,win,out,epoch)
    (status,name,url) = model.train()
    return JsonResponse({"status":status,"res":{"name":name,"url":url}})

def analyzePredictView(req):
    target = json.loads(req.body)
    username = target['username']
    data = target['data']
    modelname = target['model']
    if(modelname=="crnn"):
        model = CRNN(username)
    elif(modelname=="lstm"):
        model = LSTM(username)
    (status,res) = model.predict(data)
    return JsonResponse({"status":status,"res":res})

from utils.Quality import QM
def getAnalyzeView(req):
    # model_onPredicting = models.Option.objects.filter(option="model_onPredicting").first().value
    # model_onPredicted = models.Option.objects.filter(option="model_onPredicted").first().value
    # if(model_onPredicted == "false"):
    #     if(model_onPredicting == "true"):
    #         return JsonResponse({"status":"onPredicting"})
    #     elif(model_onPredicting == "false"):
    #         return JsonResponse({"status":"error"})
    #     else:
    #         return JsonResponse({"status":"failed"})
    # elif(model_onPredicted == "true"):
    #     return JsonResponse({"status":"success",
    #         "sd":model_onPredicting,"sad":model_onPredicted})
    # else:
    #     return JsonResponse({"status":"failed"})

    data = QM().getModelData()
    return JsonResponse({"status":serverSuccessResponse,"data":data})

def fakeView(req):
    print("接收到采集系统信息：")
    print(req.body)
    return JsonResponse({"status":"done"})


# 执行QM预测
# 这部分函数我放在了websocket里。

# 获得QM模型中所有的列标签
def QM_GET_ITEMS_VIEW(req):
    items = []
    for item in models.QualityItem.objects.filter().all():
        items.append({"label":item.label,"uid":item.uid,"minOrigin":item.minOrigin,"maxOrigin":item.maxOrigin,"maxThreshold":item.maxThreshold,"minThreshold":item.minThreshold,"inputDim":item.inputDim,"outputDim":item.outputDim,"unit":item.unit})
    return JsonResponse({"status":serverSuccessResponse,"items":items})

# 按照QM.uid获得QM模型图表数据
def QM_GET_CHART_VIEW(req):
    uid = json.loads(req.body)['uid']
    if(models.QualityItem.objects.filter(uid=uid).count()==0):
        return JsonResponse({"status":"failed"})
    if(models.QualityItem.objects.filter(uid=uid).first().onWorking == False):
        return JsonResponse({"status":"not working"})
    if(models.QualityItem.objects.filter(uid=uid).first().onPredicting == True):
        return JsonResponse({"status":"predicting"})
    
    target = models.QualityItem.objects.filter(uid=uid).first()
    neighbors = KG.getNeighborNode(label=target.nodeType,name=target.label)["data"]

    # if(uid not in QM_Result):
    #     return JsonResponse({"status":"当前指标暂无数据。"})
    # else:
    #     return JsonResponse({"status":serverSuccessResponse,"data":QM_Result[uid],"threshold":QM().getSingleTreshold(uid),"outputDim":QM().getSingleOutputLength(uid),"unit":QM().getSingleUnit(uid)})
    
    return JsonResponse({
        "status":serverSuccessResponse,
        "data":target.data,
        "neighbors":neighbors,
        "threshold":{"maxThreshold":target.maxThreshold,"minThreshold":target.minThreshold},
        "outputDim":target.outputDim,
        "inputDim":target.inputDim,
        "graphLeft":target.graphLeft,
        "graphRight":target.graphRight,
        "label":target.label,


        "unit":target.unit})














# 运维接口
OMFailedStr = "failed"
OMSuccessStr = "success"
failedCode = ["000","001","002","003","004","005","006","007","008","009","010"]
# 访问注册码
def RegisCodeView(req):
    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
        
    # 确保为application/json
    if(dict(req.headers)['Content-Type']!="application/json"):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})
    
    data = json.loads(req.body)
    # 确保有关键键名
    if "type" not in data:
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})

    # serialOBJ = models.RegisterSerialNumber.objects.filter(serial=data["serial"])
    # if(serialOBJ.count()==0):
    #     return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"注册码错误。"})
    # if(not serialOBJ.first().serialadmin):
    #     return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"注册码类型必须为管理员。"})
    
    # 确保键值合法
    if(data["type"]=="add"):
        if "object" not in data or "admin" not in data:
            return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
        if(not isinstance(data["admin"], bool)):
            return JsonResponse({"status":OMFailedStr,"code":failedCode[4]})
        models.RegisterSerialNumber.objects.create(serial=data["object"],serialadmin=data["admin"])
        return JsonResponse({"status":OMSuccessStr,"code":failedCode[0]})
    elif(data["type"]=="delete"):
        if "object" not in data:
            return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
        models.RegisterSerialNumber.objects.filter(serial=data["object"]).delete()
        return JsonResponse({"status":OMSuccessStr,"code":failedCode[0]})

    elif(data["type"]=="get"):
        items = []
        for item in models.RegisterSerialNumber.objects.filter().all():
            items.append({"注册码":item.serial,"管理员":item.serialadmin})
        return JsonResponse({"status":OMSuccessStr,"code":failedCode[0],"data":items})
    else:
        return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"type键值错误。"})

# 修改Token有效期
def TokenExpiresView(req):
    
    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
    # 确保为application/json
    if(dict(req.headers)['Content-Type']!="application/json"):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})
    
    data = json.loads(req.body)
    # 确保有关键键名
    if "expires" not in data:
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
    if (not isinstance(data["expires"],int)):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[4]})
    
    
    models.Option.objects.filter(key="userTokenExpires").update(value = data["expires"])
    return JsonResponse({"status":OMSuccessStr,"code":failedCode[0]})
def IsSubsystemView(req):
    return JsonResponse({"res":False if models.Option.objects.filter(key="subSystem").first().value=="0" else True})

 
def GraphTimeView(req):
    
    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers) and "Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
    # 确保为application/json
    if(dict(req.headers)['Content-Type']!="application/json"):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})
    
    data = json.loads(req.body)
    # 确保有关键键名
    if ("type" not in data):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
    if (data["type"]=="get"):
        return JsonResponse({"status":OMSuccessStr,"code":failedCode[0],"time": models.Option.objects.filter(key="GraphRefreshTime").first().value})
    elif (data["type"]=="set"):
        if (data["type"]=="set" and "time" not in data):
            return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
        if (data["type"]=="set" and "time" in data and not isinstance(data["time"],int)):
            return JsonResponse({"status":OMFailedStr,"code":failedCode[4]})
        
        if (data["type"]=="set" and "time" in data and isinstance(data["time"],int)) and data["time"]<2:
            return JsonResponse({"status":OMFailedStr,"code":failedCode[3]})

        models.Option.objects.filter(key="GraphRefreshTime").update(value = data["time"])
        return JsonResponse({"status":OMSuccessStr,"code":failedCode[0]})
    else:
        return JsonResponse({"status":OMSuccessStr,"code":failedCode[3]})

def ClearLoginView(req):
    
    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers) and "Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
    models.UserInfo.objects.filter(login=1).update(login = 0)
    return JsonResponse({"status":OMSuccessStr,"code":failedCode[0]})




# 设置QM[uid]预测数据的模型<不常用>
def QM_POST_MODEL_VIEW(req):

    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
    # 检查请求格式
    if(dict(req.headers)['Content-Type'].split(";")[0]!="multipart/form-data"):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})

    # 检查有无缺失键值对
    keyList = ["uid","label","maxThreshold","minThreshold","unit","maxOrigin","minOrigin","nodeType","inputDim","outputDim","graphLeft","graphRight"]
    keyOK = 0
    for i in keyList:
        if(i in req.POST):
            keyOK += 1
    if(keyOK != len(keyList)):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2],"text":'缺少关键键值对，应包含[uid,label,maxThreshold,minThreshold,unit,maxOrigin,minOrigin,dataURL,dataColumn,inputDim,outputDim,nodeType,graphLeft,graphRight]。'})
    else:
        file = req.FILES.get('model')
        if(file == None):
            return JsonResponse({"status":OMFailedStr,"code":failedCode[2],"text":"缺少关键键值对，请检查模型文件的参数名是否为[model]。"})
    # 只接受h5模型
    if(file.name.split('.')[-1]!='h5'):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"请检查模型文件，仅支持.h5格式。"})
    
    # 检查值的类型是否正确
    keyTypeOK = 0
    for key in keyList[0:-4]:
        if(isinstance(req.POST[key],str)):
            keyTypeOK += 1
    for key in keyList[-4:]:
        if(req.POST[key].isdigit()):
            keyTypeOK += 1
    if(keyTypeOK != len(keyList)):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[4],"text":"请检查变量类型。"})

    if(req.POST['graphRight']<=req.POST['graphLeft'] or req.POST['graphRight']>100 or req.POST['graphLeft']<0):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"if(req.POST['graphRight']<=req.POST['graphLeft'] or req.POST['graphRight']>100 or req.POST['graphLeft']<0): return JsonResponse({'status':OMFailedStr,'code':failedCode[3],'text':'李在赣神魔'})"})
        


    # 确认新增还是修改
    target = models.QualityItem.objects.filter(uid=req.POST['uid'])
    if(target.count()==0):
        models.QualityItem.objects.create(uid=req.POST['uid'])
        target = models.QualityItem.objects.filter(uid=req.POST['uid']).first()
    else:
        target = target.first()

    # 知识图谱同样新增节点
    try:
        if(KG.ifNodeExist(label = req.POST['nodeType'], name =  req.POST['label'])):
            pass
        else:
            KG.addNode(label=req.POST['nodeType'], name=req.POST['label'])
        KG_status = "新增指标项成功"
    except:
        KG_status = "新增指标项出错"


    # 修改属性
    target.uid = req.POST['uid']
    target.label = req.POST['label']
    target.maxThreshold = req.POST['maxThreshold']
    target.minThreshold = req.POST['minThreshold']
    target.unit = req.POST['unit']
    target.maxOrigin = req.POST['maxOrigin']
    target.minOrigin = req.POST['minOrigin']
    target.inputDim = req.POST['inputDim']
    target.outputDim = req.POST['outputDim']
    target.graphLeft = req.POST['graphLeft']
    target.graphRight = req.POST['graphRight']
    target.nodeType = req.POST['nodeType']
    target.onWorking = True
    # 删除本地模型
    if(target.model):
        url = "%s/%s"%(settings.MEDIA_ROOT,target.model)
        if(os.path.exists(url)):
            os.remove(url)
    target.model = file
    target.save()
   
    return JsonResponse({"status":OMSuccessStr,"KG-status":KG_status,"code":failedCode[0]})
def QM_DELETE_MODEL_VIEW(req):
    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
    # 检查请求格式
    if(dict(req.headers)['Content-Type'].split(";")[0]!="application/json"):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})
    # 检查有无缺失键值对
    data = json.loads(req.body)
    if("uid" not in data):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
    if(models.QualityItem.objects.filter(uid = data["uid"]).count()==0):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[3]})
    
    target = models.QualityItem.objects.filter(uid = data["uid"])
    try:
        if(KG.ifNodeExist(label = target.first().nodeType, name =  target.first().label)):
            KG.delNode(label=target.first().nodeType, name=target.first().label)
        KG_status = "删除指标项成功"
    except:
        KG_status = "删除指标项出错"
    target.delete()


temp_predict_data = []
def predictDataView(req):
    
    global temp_predict_data

    # 检查请求格式
    try:
        if(dict(req.headers)['Content-Type'].split(";")[0]!="application/json"):
            return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})
        # 检查有无缺失键值对
        data = json.loads(req.body)
    except:
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})

    if("type" not in data):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
    if(data["type"]!="set" and data["type"]!="get" ):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"msg":"type字段只能为set或get"})
    
    if(data["type"]=="get"):
        return JsonResponse({"status":serverSuccessResponse,"data":temp_predict_data})
    if(data["type"]=="set"):
        if("data" not in data):
            return JsonResponse({"status":OMFailedStr,"code":failedCode[2],"msg":"缺失data字段。"})
        try:
            temp_predict_data = data["data"]
        except:
            return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"msg":"data无法转化为json。"})

        return JsonResponse({"status":OMSuccessStr,"code":failedCode[0],"msg":"设置成功。"})
    


# 上传质量待预测数据
def QM_POST_DATA_VIEW(req):
    # 普通用户没有访问权限。
    if ("Api-Token" not in dict(req.headers)):
        return HttpResponse("没有操作权限。")
    # 检查请求格式
    # print(dict(req.headers)['Content-Type'].split(";")[0])
    if(dict(req.headers)['Content-Type'].split(";")[0]!="application/json"):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[1]})
     # 检查有无缺失键值对
    data = json.loads(req.body)
    
    if("uid" not in data or "data" not in data):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[2]})
    if(models.QualityItem.objects.filter(uid = data["uid"]).count()==0):
        return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"uid不存在。"})
    modelInputLength = int(QM().checkModelInput(data["uid"])["content"])
    if(modelInputLength != len(data["data"])):
       return JsonResponse({"status":OMFailedStr,"code":failedCode[3],"text":"模型的输入长度%s与data长度%s不符。"%(modelInputLength,len(data["data"]))})
    
    obj = QM().PUSH_RAWDATA(data["uid"],data["data"],models.QualityItem.objects.filter(uid=data["uid"]).first().isBinary)
    
    if(obj["status"]):
        
        target = models.QualityItem.objects.filter(uid = data["uid"])
        #print(obj["content"][0])
        
        max = target.first().maxOrigin
        min = target.first().minOrigin
        target.update (data= str(list(
            np.round(np.array(obj["content"][0])*(float(max)-float(min))+float(min),2)
            )))
    return JsonResponse({"status":OMSuccessStr,"res":{data["uid"]:target.first().data}})


# 数据接口
def ErrorCauseView(req):
    print(1)
    data = req.GET.get('exception')
    if((data) != None):
        return HttpResponse(json.dumps({
            "code":200,
            "msg":"查询异常原因["+data+"]，操作成功",
            "data":["产品摆差错误"]
        }))
        
        
    else:
        return JsonResponse({
            "code":203,
            "msg":"关键键名缺失",
        })

    if('Content-Type' not in dict(req.headers) or dict(req.headers)['Content-Type']!="application/json"):
        return JsonResponse({
            "code":201,
            "msg":"接口类型不一致",
        })
    try:
        data = json.loads(req.body)
    except:
        return JsonResponse({
            "code":202,
            "msg":"JSON转译错误",
        })
    data = json.loads(req.body)
    if('exception' not in data):
        return JsonResponse({
            "code":203,
            "msg":"关键键名缺失",
        })
    
    print(3)
    exception = data['exception']
    return JsonResponse({
        "code":200,
        "msg":"查询异常原因["+exception+"]，操作成功",
        "data":["产品摆差错误"]
    })
