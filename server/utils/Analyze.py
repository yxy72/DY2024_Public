import datetime
import os
from django.conf import settings
from django.core.files import File
import numpy as np
import tensorflow as tf
import json
from app.consumers import Client
from app import models
import pandas as pd

def datasetcreat(sequence, windows, col=True):
    datasize = np.shape(sequence)
    m = datasize[0]
    #sequence = np.reshape(sequence, (m,1))
    #datasize = np.shape(sequence)
    #print(datasize)
    if col:
        n = 1
        sequence = np.reshape(sequence,(m,n))
    else:
        n = datasize[1]
    x_data = []
    y_data = []
    for i in range(n):
        coltran = sequence[:,i]
        x_col = []
        y_col = []
        for j in range(m):
            endelem = j + windows
            if endelem > m - 1:
                break
            x_d = coltran[j:endelem-1]
            y_d = coltran[endelem]
            x_col.append(x_d)
            y_col.append(y_d)
        x_data.append(np.transpose(x_col))
        y_data.append(y_col)
    x_data = np.array(np.transpose(x_data), dtype=np.float32)
    y_data = np.array(np.transpose(y_data), dtype=np.float32)
    return x_data,y_data
class modelCallback(tf.keras.callbacks.Callback):
    def __init__(self, username,modelname,EPOCH):
        self.username = username
        self.modelname = modelname
        self.EPOCH = EPOCH
    def on_epoch_end(self, epoch, logs=None):
        info = {
            "epoch":epoch,
            "EPOCH":self.EPOCH,
            "loss":str(round(logs["loss"], 4)),
            "val_loss":str(round(logs["val_loss"], 4)),
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

class CRNN():
    def __init__(self,username):
        self.username = username
    def init_train(self,xdata,windowSize,out,epoch):
        self.windowSize = int(windowSize)
        self.outSize = int(out)
        self.epoch = int(epoch)
        self.dropout_rate = 0.2
        dim = len(xdata[0]) if len(xdata[0]) > len(xdata) else len(xdata)
        self.xdata = np.array(xdata).reshape(dim)
    def build_CRNN(self,x_train,y_train, predict_interval,timesteps, data_dim, hidDim=[50,70]):
        regressor = tf.keras.Sequential()
        regressor.add(tf.keras.layers.Conv1D(hidDim[0], 3, input_shape=(timesteps, data_dim)))
        regressor.add(tf.keras.layers.Conv1D(hidDim[1], 3,))
        regressor.add(tf.keras.layers.MaxPooling1D(2))
        regressor.add(tf.keras.layers.GRU(hidDim[0], return_sequences=True,input_shape=(timesteps, data_dim)))
        regressor.add(tf.keras.layers.GRU(hidDim[0], return_sequences=True))
        regressor.add(tf.keras.layers.GRU(hidDim[1], return_sequences=True))
        regressor.add(tf.keras.layers.GRU(hidDim[0], activation='sigmoid'))
        regressor.add(tf.keras.layers.Dropout(self.dropout_rate))
        regressor.add(tf.keras.layers.Dense(units=predict_interval, kernel_regularizer = tf.keras.regularizers.L2(0.001)))
        regressor.compile(optimizer=tf.keras.optimizers.Adam(3e-4), loss='mean_squared_error')
        regressor.fit(x_train,y_train,epochs=self.epoch, batch_size=64, validation_split=0.1,callbacks=[modelCallback(username=self.username,modelname="crnn",EPOCH=self.epoch)])
        # 训练终止
        # print(self.epoch)
        # print(len(regressor.history.history["loss"]))
        if(len(regressor.history.history["loss"])!=self.epoch):
            return "unfinished"
        return regressor
    def train(self):
        x_train, y_train = datasetcreat(self.xdata,windows=self.windowSize, col=True)
        data_dim = x_train.shape[2]
        timesteps = x_train.shape[1]
        regressor = self.build_CRNN(x_train,y_train, self.outSize,timesteps, data_dim)
        # 训练出错
        if(regressor=="unfinished" and Client[self.username].modelInfo['crnn']['training']):
            Client[self.username].modelInfo['crnn']['training'] = False
            return "error","none","none"
        # 训练被用户中止
        elif(regressor=="unfinished" and not Client[self.username].modelInfo['crnn']['training']):
            return "abort","none","none"
        # 训练正常完成
        elif(regressor!="unfinished" and Client[self.username].modelInfo['crnn']['training']):
            Client[self.username].modelInfo['crnn']['training'] = False
            time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            # 先删除原有crnn模型
            exist = os.listdir("%s/models/users/%s"%(settings.MEDIA_ROOT,self.username))
            for i in exist:
                if(i[0:4]=="crnn"):
                    os.remove("%s/models/users/%s/%s"%(settings.MEDIA_ROOT,self.username,i))
            
            # 保存CRNN模型
            save_url = "%smodels/users/%s/%s.h5" %(settings.MEDIA_ROOT, self.username,time)
            regressor.save(save_url)


            # 保存到数据库
            target = models.UserModel.objects.filter(username=self.username).first()
            target.model_crnn.delete()
            target.model_crnn = File(open(save_url,'rb'))
            target.save()

            # 删除多余的模型（？待优化 2023/04/10）
            os.remove(save_url)

            saveURL = "/models/users/%s/crnn_%s.h5"%(self.username,time)

            name = "crnn_%s"%(time)
            downloadURL = "/src%s"%(saveURL)
            return "success",name,downloadURL
        # 训练被用户中止
        elif(regressor!="unfinished" and not Client[self.username].modelInfo['crnn']['training']):
            return "abort","none","none"
    
    def predict(self,data):
        sub_url = str(models.UserModel.objects.filter(username=self.username).first().model_crnn)
        XDATA = np.array(data).T
        model_url = "%s%s"%(settings.MEDIA_ROOT,sub_url)

        if(not os.path.exists(model_url)):
            return "no exist",None
        try:
            model = tf.keras.models.load_model(model_url)
            XDATA = np.reshape(XDATA,(len(XDATA),len(XDATA[0]),1))
            y_pred = model.predict(XDATA)
            x = XDATA.reshape(len(XDATA),len(XDATA[0]))
            return "success",np.around(np.concatenate((x,y_pred), axis=1),4).tolist()
        except:
            return "error",None
            
class LSTM():
    def __init__(self,username):
        self.username = username
    def init_train(self,xdata,windowSize,out,epoch):
        self.windowSize = int(windowSize)
        self.outSize = int(out)
        self.epoch = int(epoch)
        self.dropout_rate = 0.2
        dim = len(xdata[0]) if len(xdata[0]) > len(xdata) else len(xdata)
        self.xdata = np.array(xdata).reshape(dim)
    def build_LSTM(self,x_train,y_train, predict_interval):
        regressor = tf.keras.Sequential()
        regressor.add(tf.keras.layers.LSTM(units=30, return_sequences=True, input_shape=(x_train.shape[1],x_train.shape[2])))
        regressor.add(tf.keras.layers.LSTM(units=50, return_sequences=True))
        regressor.add(tf.keras.layers.LSTM(units=10, activation='sigmoid'))
        regressor.add(tf.keras.layers.Dense(units=predict_interval,kernel_regularizer = tf.keras.regularizers.L2(0.001)))
        regressor.compile(optimizer=tf.keras.optimizers.Adam(3e-4), loss=tf.keras.losses.MeanSquaredError())
        regressor.fit(x_train, y_train, batch_size=64, epochs=self.epoch,validation_split=0.1,callbacks=[modelCallback(username=self.username,modelname="lstm",EPOCH=self.epoch)])
        if(len(regressor.history.history["loss"])!=self.epoch):
            return "unfinished"
        return regressor
    def train(self):
        x_train, y_train = datasetcreat(self.xdata,windows=self.windowSize, col=True)
        regressor = self.build_LSTM(x_train,y_train, self.outSize)
        # 训练出错
        if(regressor=="unfinished" and Client[self.username].modelInfo['lstm']['training']):
            Client[self.username].modelInfo['lstm']['training'] = False
            return "error","none","none"
        # 训练被用户中止
        elif(regressor=="unfinished" and not Client[self.username].modelInfo['lstm']['training']):
            return "abort","none","none"
        # 训练正常完成
        elif(regressor!="unfinished" and Client[self.username].modelInfo['lstm']['training']):
            Client[self.username].modelInfo['lstm']['training'] = False
            time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

            # 先删除原有lstm模型
            exist = os.listdir("%s/models/users/%s"%(settings.MEDIA_ROOT,self.username))
            for i in exist:
                if(i[0:4]=="lstm"):
                    os.remove("%s/models/users/%s/%s"%(settings.MEDIA_ROOT,self.username,i))
            
            # 保存LSTM模型
            save_url = "%smodels/users/%s/%s.h5" %(settings.MEDIA_ROOT, self.username,time)
            regressor.save(save_url)


            # 保存到数据库
            target = models.UserModel.objects.filter(username=self.username).first()
            target.model_lstm.delete()
            target.model_lstm = File(open(save_url,'rb'))
            target.save()

            # 删除多余的模型（？待优化 2023/04/10）
            os.remove(save_url)

            saveURL = "/models/users/%s/lstm_%s.h5"%(self.username,time)

            name = "lstm_%s"%(time)
            downloadURL = "/src%s"%(saveURL)
            return "success",name,downloadURL
        # 训练被用户中止
        elif(regressor!="unfinished" and not Client[self.username].modelInfo['lstm']['training']):
            return "abort","none","none"
    
    def predict(self,data,binary = False):
        sub_url = str(models.UserModel.objects.filter(username=self.username).first().model_lstm)
        XDATA = np.array(data).T
        model_url = "%s%s"%(settings.MEDIA_ROOT,sub_url)

        if(not os.path.exists(model_url)):
            return "no exist",None
        try:
            model = tf.keras.models.load_model(model_url)
            XDATA = np.reshape(XDATA,(len(XDATA),len(XDATA[0]),1))
            y_pred = model.predict(XDATA)
            if(binary):
                y_pred_binary = []
                for i in range(len(y_pred)):
                    y_pred_binary.append([0 if i <0.5 else 1  for i in y_pred[i]])
                y_pred = y_pred_binary
                print(y_pred)
            x = XDATA.reshape(len(XDATA),len(XDATA[0]))
            return "success",np.around(np.concatenate((x,y_pred), axis=1),4).tolist()
        except:
            return "error",None

