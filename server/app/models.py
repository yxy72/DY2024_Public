import os
from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=32)
    password = models.CharField(verbose_name="密码",max_length=64)
    avatar = models.ImageField(verbose_name="头像",upload_to='users',default="/src/images/users/default.jpeg")
    date_create = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    useradmin = models.BooleanField(verbose_name="用户类型",max_length=16,default=True)
    login = models.BooleanField(verbose_name="登录状态",default=False)
    # token = models.FileField(max_length=255, null=True)

class RegisterSerialNumber(models.Model):
    serial = models.CharField(verbose_name="注册码",max_length=32)
    serialadmin = models.BooleanField(verbose_name="注册码类型",max_length=16,default=True)


def getmodelPathCNN(instance,filename):
    return 'models/users/%s/cnn_%s'%(instance.username,os.path.basename(filename))
def getmodelPathCRNN(instance,filename):
    return 'models/users/%s/crnn_%s'%(instance.username,os.path.basename(filename))
def getmodelPathLSTM(instance,filename):
    return 'models/users/%s/lstm_%s'%(instance.username,os.path.basename(filename))
def getmodelPathTemp(instance,filename):
    return 'models/users/%s/temp_%s'%(instance.username,os.path.basename(filename))



class UserModel(models.Model):
    username = models.CharField(verbose_name="用户名",max_length=32)
    model_cnn = models.FileField(verbose_name="模型",upload_to=getmodelPathCNN,null=True)
    model_crnn = models.FileField(verbose_name="CRNN模型",upload_to=getmodelPathCRNN,null=True)
    model_lstm = models.FileField(verbose_name="LSTM模型",upload_to=getmodelPathLSTM,null=True)
    model_temp = models.FileField(verbose_name="待识别模型",upload_to=getmodelPathTemp,null=True)

class QualityItem(models.Model):

    def getmodelUploadPath(instance,filename):
        return 'models/quality/%s%s'%(instance.uid,os.path.splitext(filename)[-1] )
    uid = models.CharField(verbose_name="属性唯一定位",max_length=4,null=True)
    label = models.CharField(verbose_name="属性中文标签",max_length=64,null=True)
    maxThreshold = models.CharField(verbose_name="属性最大阈值",max_length=16,null=True)
    minThreshold = models.CharField(verbose_name="属性最小阈值",max_length=16,null=True)
    unit = models.CharField(verbose_name="属性单位",max_length=16,null=True)
    maxOrigin = models.CharField(verbose_name="标准化前最大值",max_length=16,null=True)
    minOrigin = models.CharField(verbose_name="标准化前最小值",max_length=16,null=True)
    model = models.FileField(verbose_name="属性所用模型",upload_to=getmodelUploadPath, max_length=64,null=True)
    # dataURL = models.CharField(verbose_name="属性所在表格地址",max_length=64,null=True)
    dataColumn = models.IntegerField(verbose_name="属性所在表格列数",null=True)
    inputDim = models.IntegerField(verbose_name="属性输入维度",null=True)
    outputDim = models.IntegerField(verbose_name="属性预测长度",null=True)
    graphLeft = models.IntegerField(verbose_name="界面图表默认百分比左值区域",null=True)
    graphRight = models.IntegerField(verbose_name="界面图表默认百分比右值区域",null=True)
    outputDim = models.IntegerField(verbose_name="属性预测长度",null=True)
    onPredicting = models.BooleanField(verbose_name="该属性数据正在执行更改",max_length=8,default=False)
    onWorking = models.BooleanField(verbose_name="本属性所有工作模块已可用",max_length=8,default=False)
    nodeType = models.CharField(verbose_name="指标在知识图谱中对应的类别名称",max_length=64,null=True)
    isBinary = models.BooleanField(verbose_name="指标是否是二元相",max_length=8,default=False)

    data = models.TextField(verbose_name="输出数据，长度为inputDim+outputDim",null=True)

class Option(models.Model):
    key = models.CharField(verbose_name="配置项",max_length=16,null=True)
    value = models.CharField(verbose_name="配置值",max_length=24,null=True)

