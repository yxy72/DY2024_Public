import json
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from utils.Quality import QM
# from app.views import USERMODELS

from app import models
Client = {}
class DYConsumer(WebsocketConsumer):
    
    def websocket_connect(self, message):
        # 有客户端发来请求时触发
        self.username = self.scope['url_route']['kwargs']['group']
        self.modelInfo = {
            "cnn":{
                'training':False
            },
            "crnn":{
                'training':False
            },
            "lstm":{
                'training':False
            }     
        }
        Client[self.username] = self
        models.UserInfo.objects.filter(username=self.username).update(login=True)
        self.accept()
    def websocket_receive(self, message):
        # 客户端发信息时触发
        # print((message)["text"])
        obj = json.loads(message["text"])
        if('type' in obj and obj['type']=="settings"):
            self.modelInfo[obj['model']][obj['parameter']] = obj['parameter_val']
        
              
    
    def websocket_disconnect(self, message):
        # 断开连接时触发
        models.UserInfo.objects.filter(username=self.username).update(login=False)
        del Client[self.username]
        raise StopConsumer()

class DY_UploadRawDataConsumer(WebsocketConsumer):
    
    def websocket_connect(self, message):
        # 有客户端发来请求时触发
        self.accept()
    def websocket_receive(self, message):
        # 客户端发信息时触发
        obj = json.loads((message)["text"])
        # obj = json.loads(message["text"])
        # if('type' in obj and obj['type']=="settings"):
        #     self.modelInfo[obj['model']][obj['parameter']] = obj['parameter_val']
        if(not QM().checkUID(obj["targetUID"])):
           self.send("UID不存在。")
           return
        
        if(not QM().checkIfWork(obj["targetUID"])):
           self.send("该指标后台数据不完整，无法正常工作。")
           return
        
        if(QM().checkIfPredicting(obj["targetUID"])):
           self.send("该指标已经有数据正在预测，请等待数据预测完成。")
           return
        
        data = obj["data"]
        o = QM().checkModelInput(obj["targetUID"])
        if(not o["status"]):
            self.send(o["content"])
            return
        
        if(int(o["content"])!=len(data)):
            self.send("源数据维度%s与模型输入维度%s不匹配，请修改源数据或上传新模型"%(len(data),o["content"]))
            return
        self.send(str(QM().PUSH_RAWDATA(obj["targetUID"],data)["content"]))
        # if():
        #    self.send("该指标已经有数据正在预测，请等待数据预测完成。")
        #    return


    def websocket_disconnect(self, message):
        # 断开连接时触发
        raise StopConsumer()

