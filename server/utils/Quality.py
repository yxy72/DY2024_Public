import datetime
import os
from django.conf import settings
from django.core.files import File
import numpy as np
import tensorflow as tf
import json
from app import models
import tensorflow as tf
import pandas as pd
from utils.Global import QM_Result



# QualityModel
class QM():

    url = "%s/models/quality/MODELRESULT.xlsx"%(settings.MEDIA_ROOT)
    QM_DATAURL = "%s/models/quality/QM/QM_result.xlsx" %(settings.MEDIA_ROOT)
    model_onPredicting = False
    predicted_maxThreshold = 0.85
    predicted_minThreshold = 0.60

    data_count = 2
    data_length = 399
    predicted_length = 10


    @staticmethod
    def getModelData():
        # print(QM.url)
        table = pd.read_excel(QM.url)
        data = np.array(table).T.tolist()
        label = list(table)
        return {
            "table":data,"label":label,"predictLen":QM.predicted_length,
            "maxThreshold":QM.predicted_maxThreshold,"minThreshold":QM.predicted_minThreshold}


    # @staticmethod
    # def setModel(uid,file):
    #     try:
    #         filter = models.QualityItem.objects.filter(uid=uid).first()
    #         if(filter.model):
    #             url = "%s/%s"%(settings.MEDIA_ROOT,filter.model)
    #             if(os.path.exists(url)):
    #                 os.remove(url)
    #             filter.model.delete()
    #         filter.model = file
    #         filter.save()
    #         return "ok"
    #     except:
    #         return "error"
        
    # 得到单项预测数据
    @staticmethod
    def getSinglePredictResult(uid):
        return QM_Result[uid]
        # try:
        #     filter = models.QualityItem.objects.filter(uid=uid).first()
        #     df = pd.read_excel(QM.QM_DATAURL,header=None)
        #     index = filter.dataColumn
        #     res = df[int(index)]
        #     return list(res)
        # except:
        #     return "error"

    # 得到单项的阈值
    @staticmethod
    def getSingleTreshold(uid):
        try:
            filter = models.QualityItem.objects.filter(uid=uid).first()
            return {"maxThreshold":filter.maxThreshold,"minThreshold":filter.minThreshold}
        except:
            return "error"

    # 得到单项的输出长度（预测长度）
    @staticmethod
    def getSingleOutputLength(uid):
        try:
            filter = models.QualityItem.objects.filter(uid=uid).first()
            return filter.outputDim
        except:
            return "error"

    # 得到单项的单位
    @staticmethod
    def getSingleUnit(uid):
        try:
            filter = models.QualityItem.objects.filter(uid=uid).first()
            return filter.unit
        except:
            return "error"

    # 检查UID是否存在
    @staticmethod
    def checkUID(uid):
        try:
            return models.QualityItem.objects.filter(uid=uid).count() == 1
        except:
            return False 
        
    # 检查UID所属模型是否正常工作
    @staticmethod
    def checkIfWork(uid):
        try:
            return models.QualityItem.objects.filter(uid=uid).first().onWorking
        except:
            return False 
        
    # 检查UID所属模型是否已经正在预测
    @staticmethod
    def checkIfPredicting(uid):
        try:
            return models.QualityItem.objects.filter(uid=uid).first().onPredicting
        except:
            return False 
        
    # 检查UID所属模型的输入维度
    @staticmethod
    def checkModelInput(uid):
        try:            
            url = "%s/%s"%(settings.MEDIA_ROOT,models.QualityItem.objects.filter(uid=uid).first().model)
            if(not os.path.exists(url)):
                return {"status":False,"content":"no exist"}

            model = tf.keras.models.load_model(url)
            inputsize = str(model.get_layer(index=0).input_shape[1])
            return {"status":True,"content":inputsize}

        except:
            return {"status":False,"content":"error"}


    # 设置单项数据集(准备预测)<重要常用操作>
    @staticmethod
    def PUSH_RAWDATA(uid,data,binary = False):
        try:
            model_url = "%s/%s"%(settings.MEDIA_ROOT,models.QualityItem.objects.filter(uid=uid).first().model)

            if(not os.path.exists(model_url)):
                return {"status":False,"content":"no exist"}
            model = tf.keras.models.load_model(model_url)
            XDATA = np.reshape(data,(1,len(data),1))
            y_pred = model.predict(XDATA)
            x = XDATA.reshape(1,len(data))
            if(binary):
                y_pred_binary = []
                for i in range(len(y_pred)):
                    y_pred_binary.append([0 if i <0.5 else 1  for i in y_pred[i]])
                y_pred = y_pred_binary
                
            x = XDATA.reshape(len(XDATA),len(XDATA[0]))
            # return "success",np.around(np.concatenate((x,y_pred), axis=1),4).tolist()
            return {"status":True,"content":np.around(np.concatenate((x,y_pred), axis=1),4).tolist()}
        except:
            return {"status":False,"content":"error"}
            
        