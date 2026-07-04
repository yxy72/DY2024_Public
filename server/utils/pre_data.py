from enum import Enum


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
