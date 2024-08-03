from enum import Enum
from app import models
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from tensorflow import keras
from django.conf import settings
from django.core.files import File
import numpy as np
import json
import datetime
import os
from app.consumers import Client


class preProcess(Enum):
    log10 = 1,
    ln = 2,
    mean = 3,
    initial = 4,
    zscore = 5,
    minmax = 6,
    none = 7,
    def enumInit():
        preProcess.log10.name_ = "对数"
        preProcess.ln.name_ = "自然对数"
        preProcess.mean.name_ = "均值"
        preProcess.initial.name_ = "初值"
        preProcess.zscore.name_ = "Z-Score"
        preProcess.minmax.name_ = "Min-max"
        preProcess.none.name_ = "不处理"
preProcess.enumInit()
class lossEnum(Enum):
    categorical_crossentropy = 1,
    # sparse_categorical_crossentropy = 2,
class optimizerEnum(Enum):
    SGD = 1,
    Adam = 2,
preData = {
  "preProcess" : [
    {"val":preProcess.log10.name,"name":preProcess.log10.name_,"expression":'x\'_i\\left(k\\right) =log_{10}x_i\\left(k\\right)'},
    {"val":preProcess.ln.name,"name":preProcess.ln.name_,"expression":'x\'_i\\left(k\\right) =lnx_i\\left(k\\right)'},
    {"val":preProcess.mean.name,"name":preProcess.mean.name_,"expression":'x\'_i\\left(k\\right) =\\frac{x_i\\left(k\\right)}{\\frac{1}{N}\\sum_{i=1}^{N}x_i\\left(k\\right)}'},
    {"val":preProcess.initial.name,"name":preProcess.initial.name_,"expression":'x\'_i\\left(k\\right) =\\frac{x_i\\left(k\\right)}{x_i\\left(0\\right)}'},
    {"val":preProcess.zscore.name,"name":preProcess.zscore.name_,"expression":'x\'_i\\left(k\\right) =\\frac{x_i\\left(k\\right)-\\mu}{\\sigma}'},
    {"val":preProcess.minmax.name,"name":preProcess.minmax.name_,"expression":'x\'_i\\left(k\\right ) =\\frac{x_{i}\\left(k\\right) - \\min x_{i}  }{\\max x_{i}-\\min x_{i}} '},
    {"val":preProcess.none.name,"name":preProcess.none.name_,"expression":'x\'_i\\left(k\\right) =  x_i\\left(k\\right)'},
  ],
  "preProcessVal":preProcess.minmax.name,
  "parameters":{
    "loss":{          "val":lossEnum.categorical_crossentropy.name,"scope":[item.name for item in lossEnum]},
    "optimizer":{     "val":optimizerEnum.SGD.name,"scope":[item.name for item in optimizerEnum]},
    "learning_rate":{ "val":0.01,"scope":[0.001,0.002, 0.005, 0.01, 0.02, 0.05]},
    "epoch":{         "val":10,"scope":[10, 15,30, 45, 60, 75, 90,120,200]},
    "batch_size":{    "val":16,"scope":[16,32, 64, 128]},
  },
}
class modelCallback(keras.callbacks.Callback):
    def __init__(self, username,modelname,EPOCH):
        self.username = username
        self.modelname = modelname
        self.EPOCH = EPOCH
    def on_epoch_end(self, epoch, logs=None):
        info = {
            "epoch":epoch,
            "loss":str(round(logs["loss"],4)),
            "accuracy":str(round(logs["accuracy"],4)),
            "EPOCH":self.EPOCH
        }
        msg = {
            "type":self.modelname,
            "kind":"loss",
            "info":info,
        }
        if(self.username not in Client):
            self.model.stop_training = True
        elif(not Client[self.username].modelInfo[self.modelname]['training']):
            self.model.stop_training = True
            Client[self.username].send(json.dumps({
                "type":self.modelname,
                "kind":"text",
                "info":"服务端已中止训练。",
            }))
        else:
            Client[self.username].send(json.dumps(msg))
class Model():
    def __init__(self,xData,yData,parameters,preprocess,username):
        self.username = username
        self.xData = np.array(xData)
        self.yData = np.array(yData)
        self.preProcessName = preprocess
        self.lossName = parameters["loss"]
        self.optimizerName = parameters["optimizer"]
        self.lr = float(parameters["learning_rate"])
        self.epoch = int(parameters["epoch"])
        self.batchSize = int(parameters["batch_size"])
        self.model = None
        self.optimizer = None
        self.statusInfo = ""
        self.statusInfoChanged = False

        self.preProcess()
        self.optimizerInit()
        self.modelInit()

    def getParameters(self):
        return {
            "preProcessName":self.preProcessName,
            "epoch":self.epoch,
            "optimizerName":self.optimizerName,
            "batchSize":self.batchSize,
            "xData":self.xData,
        }
    def preProcess(self):
        if(self.preProcessName == preProcess.log10.name):
            self.xData = np.log10(self.xData+1)
            self.yData = np.log10(self.yData+1)
        elif(self.preProcessName == preProcess.ln.name):
            self.xData = np.log(self.xData+1)
            self.yData = np.log(self.yData+1)
        elif(self.preProcessName == preProcess.mean.name):
            self.xData = self.xData / self.xData.mean(axis=0)
            self.yData = self.yData / self.yData.mean(axis=0)
        elif(self.preProcessName == preProcess.initial.name):
            self.xData = self.xData / self.xData[0]
            self.yData = self.yData / self.yData[0]
        elif(self.preProcessName == preProcess.zscore.name):
            self.xData = StandardScaler().fit(self.xData).transform(self.xData)
            self.yData = StandardScaler().fit(self.yData).transform(self.yData)
        elif(self.preProcessName == preProcess.minmax.name):
            self.xData = MinMaxScaler().fit(self.xData).transform(self.xData)
            self.yData = MinMaxScaler().fit(self.yData).transform(self.yData)
        elif(self.preProcessName == preProcess.none.name):

            pass
    def modelInit(self):
        # 在前端已经规定xDim <= 32
        xDim = len(self.xData[0])
        yDim = len(self.yData[0])

        model = keras.Sequential()
        model.add(keras.layers.Reshape((xDim,1),input_shape=(xDim,)))
        model.add(keras.layers.Conv1D(4,1,strides=1,activation='relu',input_shape=(xDim,1)))
        
        if(model.output.type_spec.shape[1]>4):
            model.add(keras.layers.Conv1D(64,4,strides=1,activation='relu'))
        elif(model.output.type_spec.shape[1]>2):
            model.add(keras.layers.Conv1D(64,2,strides=1,activation='relu'))

        if(model.output.type_spec.shape[1]>4):
            model.add(keras.layers.Conv1D(256,4,strides=1,activation='relu'))
        elif(model.output.type_spec.shape[1]>2):
            model.add(keras.layers.Conv1D(256,2,strides=1,activation='relu'))
            
        if(model.output.type_spec.shape[1]>2):
            model.add(keras.layers.Conv1D(512,2,strides=1,activation='relu'))  
              
        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dropout(0.3))
        model.add(keras.layers.Dense(yDim,activation='softmax'))
        model.summary()
        model.compile(loss=self.lossName,optimizer=self.optimizer,metrics=['accuracy'])
        self.model = model

    def optimizerInit(self):
        if(self.optimizerName == optimizerEnum.SGD.name):
            self.optimizer = keras.optimizers.SGD(learning_rate=self.lr,nesterov=True, momentum=0.9)
        elif(self.optimizerName == optimizerEnum.Adam.name):
            self.optimizer = keras.optimizers.Adam(learning_rate=self.lr)
    def run(self):
      
        # def updateInfo(epoch):
        # self.statusInfo = str(epoch)+"哈哈哈哈"
        # print("="*80)
        # print(self.xData.shape)
        # print("="*80)
        # print("="*80)
        # print(Client)
        # print("="*80)
        self.model.fit(self.xData, self.yData,validation_split=0.0, epochs = self.epoch,  batch_size = self.batchSize,callbacks=[modelCallback(username=self.username,modelname="cnn",EPOCH=self.epoch)])
        
        # 训练出错
        if(len(self.model.history.history["loss"])!=self.epoch and Client[self.username].modelInfo['cnn']['training']):
            Client[self.username].modelInfo['cnn']['training'] = False
            return "error","none","none"
        # 训练被用户中止
        elif(len(self.model.history.history["loss"])!=self.epoch and not Client[self.username].modelInfo['cnn']['training']):
            return "abort","none","none"
        # 训练正常完成
        elif(len(self.model.history.history["loss"])==self.epoch and Client[self.username].modelInfo['cnn']['training']):
            Client[self.username].modelInfo['cnn']['training'] = False
            time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            # 先删除原有cnn模型
            if(os.path.exists("%s/models/users/%s"%(settings.MEDIA_ROOT,self.username))):
                exist = os.listdir("%s/models/users/%s"%(settings.MEDIA_ROOT,self.username))
                for i in exist:
                    if(i[0:4]=="cnn_"):
                        os.remove("%s/models/users/%s/%s"%(settings.MEDIA_ROOT,self.username,i))
          
            # 保存CNN模型
            save_url = "%smodels/users/%s/%s.h5" %(settings.MEDIA_ROOT, self.username,time)
            self.model.save(save_url)

            # 保存到数据库
            target = models.UserModel.objects.filter(username=self.username)
            if(target.count()==0):
                models.UserModel.objects.create(username=self.username)
                target = models.UserModel.objects.filter(username=self.username).first()
            else:
                target = target.first()
            target.model_cnn.delete()
            target.model_cnn = File(open(save_url,'rb'))
            target.save()

            # 删除多余的模型（？待优化 2023/04/12）
            os.remove(save_url)
            saveURL = "/models/users/%s/cnn_%s.h5"%(self.username,time)
            name = "cnn_%s"%(time)
            downloadURL = "/src%s"%(saveURL)
            return "success",name,downloadURL
        # 训练被用户中止
        elif(len(self.model.history.history["loss"])==self.epoch and not Client[self.username].modelInfo['cnn']['training']):
            return "abort","none","none"
    
    def getStatus(self):
        return self.statusInfoChanged,self.statusInfo
def calModelLayers(dimX,dimY):
    layers = []
    dimX = int(dimX)
    dimY = int(dimY)
    def add(layer,output,channels,size,stride,activation,parameters):
        layers.append({
            "layer":layer,
            "output":output,
            "channels":channels,
            "size":size,
            "stride":stride,
            "activation":activation,
            "parameters":parameters,
        }) 

    model = keras.Sequential()
    model.add(keras.layers.Reshape((dimX,1),input_shape=(dimX,1)))
    add("Reshape",str(model.output.type_spec.shape),"-","-","-","-",0)
    
    model.add(keras.layers.Conv1D(4,1,strides=1,activation='relu',input_shape=(dimX,1)))
    add("Conv1D",str(model.output.type_spec.shape),4,1,1,"relu",4*(1+1))


    size = 0
    channels = 64
    input = 4
    if(model.output.type_spec.shape[1]>4):
        size = 4
        model.add(keras.layers.Conv1D(channels,size,strides=1,activation='relu'))
        add("Conv1D",str(model.output.type_spec.shape),channels,size,1,"relu",(size * input + 1) * channels)
    elif(model.output.type_spec.shape[1]>2):
        size = 2
        model.add(keras.layers.Conv1D(channels,size,strides=1,activation='relu'))
        add("Conv1D",str(model.output.type_spec.shape),channels,size,1,"relu",(size * input + 1) * channels)

    channels = 256
    input = 64
    if(model.output.type_spec.shape[1]>4):
        size = 4
        model.add(keras.layers.Conv1D(channels,size,strides=1,activation='relu'))
        add("Conv1D",str(model.output.type_spec.shape),channels,size,1,"relu",(size * input + 1) * channels)
    elif(model.output.type_spec.shape[1]>2):
        size = 2
        model.add(keras.layers.Conv1D(channels,size,strides=1,activation='relu'))
        add("Conv1D",str(model.output.type_spec.shape),channels,size,1,"relu",(size * input + 1) * channels)
    
    channels = 512
    input = 256
    if(model.output.type_spec.shape[1]>2):
        size = 2
        model.add(keras.layers.Conv1D(channels,size,strides=1,activation='relu'))
        add("Conv1D",str(model.output.type_spec.shape),channels,size,1,"relu",(size * input + 1) * channels)
  
    model.add(keras.layers.Flatten())
    layers.append({
        "layer":"Flatten",
        "output":str(model.output.type_spec.shape),
        "channels":"-",
        "size":"-",
        "stride":"-",
        "activation":'-',
        "parameters":0,   
    }) 
    model.add(keras.layers.Dropout(0.3))
    out = model.output.type_spec.shape
    layers.append({
        "layer":"Dropout",
        "output":str(out),
        "channels":"-",
        "size":"-",
        "stride":"-",
        "activation":'-',
        "parameters":0,   
    })  
    model.add(keras.layers.Dense(dimY,activation='softmax'))
    layers.append({
        "layer":"Dense",
        "output":str(model.output.type_spec.shape),
        "channels":dimY,
        "size":"-",
        "stride":"-",
        "activation":'-',
        "parameters":(int(out[1])+1)*dimY,
        })
    return layers
def queryModel(url):
    if(not os.path.exists(url)):
        return "no exist",None,None,None,None
    size = os.path.getsize(url)
    name = os.path.basename(url)
    if(size>1024*1024):
        size = str(round(size/1024/1024,2)) + "MB"
    elif(size>1024):
        size = str(round(size/1024,2)) + "kB"
    else:
        size = str(round(size,2)) + "Bytes"
    model = keras.models.load_model(url)
    inputsize = str(model.get_layer(index=0).input_shape[1])
    outputsize = str(model.get_layer(index=-1).output_shape[1])
    return "success",name,size,inputsize,outputsize
class Predict():
    def __init__(self,username,data,model_url):
        self.data = np.array(data)
        self.username = username
        self.model = keras.models.load_model(model_url)
    def predict(self):
        # print(self.model.get_layer(index=0).input_shape) 
        # print(self.model.get_layer(index=0).input_shape)
        pred = self.model.predict(self.data)
        return pred.tolist()

