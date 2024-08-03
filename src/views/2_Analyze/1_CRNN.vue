<template>
  <div class="page">
    <el-card class="mainCard">
      <el-tabs @tab-change="tabOnChange" class="tabs" type="card"  v-model="d.tabPanel">
        <el-tab-pane label="时序预测" name="1" class="tabplane">
          <div class="modelRow">
            <div class="modelColumn">
              <div class="titleRow">
                <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><money /></el-icon>
                模型信息
                <el-upload
                  v-if="(d.hasModel)"
                  ref="uploadModelRef"
                  class="upload-demo"
                  :action="store.state.server.address+'/postmodel/'"
                  :show-file-list = "false"
                  :auto-upload="true"
                  :headers="getHeaders(modelName)"
                  :beforeUpload="handleCheck"
                  :on-success="handleUploadSuccess"
                  accept=".h5"
                  >
                  <template #trigger>
                    <el-button disabled text type="primary" style="margin-top: 0px;;margin-left: 8px;"><div style="font-size: 15px;">重新上传</div></el-button>
                  </template>
              
                </el-upload>
              </div>
              <div class="msgRow"
                  v-loading="pd.modelInfoOnLoading"
                  element-loading-text="获取数据中...">
                <el-empty
                  v-if="!d.hasModel && !pd.modelInfoOnLoading"
                  :image-size="64"
                  style="height: 100%; background: #fafafa"
                  description="当前没有可用模型。">
                  <div style="display: flex;margin-top: -15px;">
                    <el-upload
                      ref="uploadModelRef"
                      class="upload-demo"
                      :action="store.state.server.address+'/postmodel/'"
                      :show-file-list = "false"
                      :auto-upload="true"
                      :headers="getHeaders(modelName)"
                      :beforeUpload="handleCheck"
                      :on-success="handleUploadSuccess"
                      accept=".h5"
                      >
                      <template #trigger>
                        <el-button disabled class="littleBtn" text type="primary" style="margin-top: -15px;;">上传</el-button>
                      </template>
                    </el-upload>
                    或
                    <el-button class="littleBtn" size="small" text type="primary" @click="d.tabPanel = '2'">
                      训练{{modelName.toUpperCase()}}模型
                    </el-button>
                  </div>

                </el-empty>


                <el-descriptions
                  v-else-if="!pd.modelInfoOnLoading"
                  class="margin-top"
                  :column="1"
                  style="margin-left: 0px;"
                  border>
                  <el-descriptions-item :width="100" v-for="(item,index) in pd.modelInfo" :key="index">
                    <template #label>
                        <div class="cell-item">
                          <i :class=item.icon />
                          {{item.name}}
                        </div>
                      </template>
                      {{ item.val }}
                  </el-descriptions-item>
                </el-descriptions>
                
                




              </div>

            </div>

            <div class="modelColumn" style="padding-right: 0px;border-right: none;">
              <div class="titleRow">
                <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><money /></el-icon>
                样本信息
                <el-upload
                  v-if="d.hasSample"
                  class="upload-demo"
                  :show-file-list = "false"
                  :auto-upload="false"
                  :on-change="handleSampleChange"
                  >
                  <template #trigger>
                    <el-button text type="primary" style="margin-top: 0px;;margin-left: 8px;padding-left:4px;padding-right:4px;;"><div style="font-size: 15px;">重载</div></el-button>
                  </template>
              
                </el-upload>
                <el-button @click="pd.onDialog = true;pd.dialogContent=1" link style="margin-left: 10px;">
                  <div style='font-family: "Times New Roman";font-size: 14px;font-weight: default;color: gray;'>查看范例</div>
                </el-button>
              </div>
              <div class="msgRow">
                <el-empty
                  v-if="!d.hasSample"
                  :image-size="72"
                  style="height: 100%; background: #fcfcfc"
                  description="请载入数据。">
                  <div style="display: flex;margin-top: -15px;">
                    <el-upload
                      ref="uploadModelRef"
                      class="upload-demo"
                      :show-file-list = "false"
                      :auto-upload="false"
                      :on-change="handleSampleChange"
                      >
                      <template #trigger>
                        <el-button   class="littleBtn"  text type="primary" style="margin-top: -15px;;">载入</el-button>
                      </template>
                      
                    </el-upload>
                   
                  </div>

                </el-empty>


                <el-descriptions
                  v-else
                  class="margin-top"
                  :column="1"
                  style="margin-left: 0px;height: 100%;"
                  border
                >
                  <el-descriptions-item :width="100" v-for="(item,index) in d.sampleInfo" :key="index">
                    <template #label>
                        <div class="cell-item">
                          <i :class=item.icon />
                          {{item.name}}
                        </div>
                      </template>
                      {{ item.val }}
                  </el-descriptions-item>
                </el-descriptions>




              </div>
            </div>

            <div class="modelColumn" style="width: calc(100% - 720px);padding-right: 0px;margin-right: 0px;border-right: none;">
              <div style="background: ;width: 100%;margin-top: 2px;;height: calc(100% - 26px);">
                <el-auto-resizer v-if="d.hasSample">
                  <template #default="{ height, width }">
                    <el-table-v2
                      :row-height="35"
                      scrollbar-always-on
                      :width="width"
                      :height="height"
                      fixed
                      :columns="d.sampleDataColumns"
                      :data="d.sampleData"
                    >
                    </el-table-v2>
                  </template>
                </el-auto-resizer>

              </div>
              
            </div>
          </div>
         
          <div style="display: flex;justify-content:center ;height: 54px;">
            <el-button
              @click="PREDICT()"
              style="margin-top: 10px;width: 100%;"
              type="success"
              plain
              :disabled="!d.hasSample || !d.hasModel"
              :loading="d.onPredicting"
            >
            <div style="margin-left: 4px; margin-right: 8px">运行模型</div>
          </el-button>

          </div>


          <div class="displayRow">
            <div class="titleRow" style="border-top: 1px solid #dcdfe670;border-bottom:none;background: ;">
              <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><money /></el-icon>
              时序预测
            </div>
            <div class="echartRow">
              <el-empty
                  v-if="!d.onPredicted"
                  v-loading="d.onPredicting"
                  element-loading-text="数据加载中..."
                  :image-size="96"
                  style="height: calc(100% - 20px);width: 100%; background: #fefefe"
                  description="等待预测">
              </el-empty>
              <div v-loading="d.onPredicting" element-loading-text="模型运行中..." v-show="d.onPredicted" class="chart" id="chart" ref="chartRef"></div>
            </div>
            <div class="btnRow">
              <el-button :disabled="!d.onPredicted" type="primary" @click="DOWNLOADPREDICT" plain>下载预测数据</el-button>
              <el-button :disabled="!d.onPredicted" type="primary" @click="SAVEPREDICT" plain>保存图片</el-button>

            </div>
          </div>

        </el-tab-pane>

        <el-tab-pane label="训练模型" name="2" class="tabplane">
          <div class="titleRow" style="border: 0;">
            <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><money /></el-icon>
            训练模型
            <el-upload
              action=""
              :on-change="handleDatasetChange"
              :show-file-list="false"
              :auto-upload="false">
              <el-button text style="padding: 5px;margin-left: 4px;" type="primary">
                <div style="font-size: 15px;">上传数据集</div>
              </el-button>
            </el-upload>
            <el-button @click="pd.onDialog = true;pd.dialogContent = 2" link style="margin-left: 5px;">
              <div style='color: gray;font-size: 15px;'>说明</div>
            </el-button>
          </div>
          <div style="width: 100%;min-width: 840px;max-width: 1160px;margin-top: 5px;margin-left: 0;">
            <el-descriptions
              :column="4"
              border>
              <el-descriptions-item :width="50" v-for="(item,index) in d.datasetInfo" :key="index" >
                <template #label>
                  <div class="cell-item">
                    <i :class=item.icon />
                    {{item.name}}
                  </div>
                </template>
                {{ (()=>{if(item.name!='序列长度') return ""; else return item.val})() }}
                <el-input type="number"  :disabled="!d.dataSetOnloaded" v-if="item.name=='窗口大小'" :placeholder="d.dataSetOnloaded?'模型的输入长度':'请加载数据集'" v-model="item.val"></el-input>
                <el-input type="number"  :disabled="!d.dataSetOnloaded" v-if="item.name=='预测长度'" :placeholder="d.dataSetOnloaded?'模型的输出长度':'请加载数据集'" v-model="item.val"></el-input>
                <el-input type="number"  :disabled="!d.dataSetOnloaded" v-if="item.name=='训练轮次'" :placeholder="d.dataSetOnloaded?'1 ~ 100':'请加载数据集'" v-model="item.val"></el-input>
              </el-descriptions-item>
            </el-descriptions>
            <div v-if="d.dataSetOnloaded" style="color: gray;font-size: 14px;height: 24px;line-height: 24px;background: ;">*注意：请确保您的训练数据已经按照<el-button @click="$router.replace({path:store.state.router.page_tool_preprocess})" link type="primary" ><div style="font-size: 14px;">Min-max</div></el-button>方式初始化。</div>
            <div v-else style="color: gray;font-size: 14px;height: 8px;line-height: 24px;background: ;"></div>

          </div>

          <div class="titleRow" style=";border-top: 1px solid #dcdfe670;">


            <el-button :loading="d.onTraining"  @click="TRAIN()"
            :style='"padding: 7px;margin-left: 10px;border-radius:"+store.state.option.style.el_button_border_radius+";"'

            type="success" plain>
              <div style="font-size: 16px;">{{d.onTraining?"训练中":"开始训练"}}</div>
            </el-button>
            <el-button  @click="ABORT()" v-if="d.onTraining" style="padding: 7px;margin-left: 10px;" type="danger" plain>
              <div style="font-size: 16px;">中止训练</div>
            </el-button>
            <el-button  @click="DOWNLOAD()" :disabled="!d.onTrained"
            :style='"padding: 7px;margin-left: 10px;border-radius:"+store.state.option.style.el_button_border_radius+";"'

            type="primary" plain>
              <div style="font-size: 16px;">下载模型</div>
            </el-button>
          </div>

          
          <div style="height: 40px;color: gray;line-height: 40px;font-size: 16px;margin-left: 10px;">
            <div>训练状态</div>
          </div>
          <div class="TrainInfoArea" :style="`height:calc(100% - 140px - ${d.dataSetOnloaded?81:65}px)`">
            <el-scrollbar >
              <ul style="margin-left: 10px;margin-top: 8px;">
                <li style="height: 25px;font-size: 16px;color: rgba(100, 100, 100, 0.774);" v-for="item,index in d.trainingInfo" :key="index">
                  {{ item }}
                </li>
              </ul>
            </el-scrollbar>
            
          </div>

        </el-tab-pane>

      </el-tabs>
      <!-- <el-button @click="test"></el-button> -->
    </el-card>


    <el-dialog
      v-model="pd.onDialog"
      append-to-body
      align-center
      :width="pd.dialogContent == 2?640:780"
      >
      <template #header>
        <div style="margin-bottom: -20px;display: flex;">
          <div style="margin-left: 0px;font-size: 23px;margin-top: 0px;"><el-icon><Setting /></el-icon></div>
          <div style="margin-left: 4px;font-size: 20px;">接收文件说明</div>
        </div>
      </template>
      <div v-if="pd.dialogContent==1">
        <div v-if="!d.hasModel" class="dialogRow">请先载入一个{{modelName.toUpperCase()}}模型。</div>
        <div v-if="d.hasModel" class="dialogRow">载入样本的行数或列数应与模型输入维度:{{ pd.modelInfo[2].val }}相同。</div>
        <div class="dialogRow2">1. 您上传的表格文件的列数或行数应与模型的输入维度相符。</div>
        <div class="dialogRow2">2. 当表格行数（列数）与模型输入维度相同时，则不同列（行）会被视作不同的样本。</div>
        <div class="dialogRow2">3. 文件<div style="color: darkred;">不含</div>表头。</div>
        <el-divider style="margin-top: 15px;margin-bottom: 20px;"><div style="color: gray;">示例</div></el-divider>
        <div class="centerrow">
          <div class="centercolumn" style="width: 38.2%;">
            <el-image :src="store.state.server.address+'/src/images/pages/sample1_crnn_predict.png'"></el-image>
            <div style="font-size: 16px;margin-top: 5px;">输入维度 = 10，样本数量 = 2</div>
          </div>
          <div class="centercolumn" style="width: 61.8%;">
            <el-image :src="store.state.server.address+'/src/images/pages/sample2_crnn_predict.png'"></el-image>
            <div style="font-size: 16px;margin-top: 5px;">输入维度 = 10，样本数量 = 3</div>
          </div>
        </div>
      </div>

      <div v-else-if="pd.dialogContent == 2">
        <div  class="dialogRow">{{modelName.toUpperCase()}}模型接收一维数据进行训练。</div>
        <div class="dialogRow2">1. 您上传的表格文件的列数或行数应为1。注意： 文件<div style="color: darkred;">不含</div>表头。</div>
        <div class="dialogRow2">2. 窗口大小：设置模型训练和预测时的输入序列长度；训练轮次：模型训练迭代的次数。</div>
        <el-divider style="margin-top: 15px;margin-bottom: 20px;"><div style="color: gray;">示例</div></el-divider>
        <div class="centerrow" style="background-color: ;">
          <div class="centercolumn" style="width: 50%; background: ;">
            <el-image  :src="store.state.server.address+'/src/images/pages/sample1_crnn_train.png'"></el-image>
            <div style="font-size: 16px;margin-top: 5px;">单行数据集，序列长度 = 5</div>
          </div>
          <div class="centercolumn" style="width: 50%;">
            <el-image :src="store.state.server.address+'/src/images/pages/sample2_crnn_train.png'"></el-image>
            <div style="font-size: 16px;margin-top: 5px;">单列数据集，序列长度 = 5</div>
          </div>
        </div>
      </div>
      
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import * as global from '@/utils/global'
import { onBeforeMount, onMounted, onUnmounted, reactive, ref } from 'vue';
import { useStore } from 'vuex';
import { ElMessage, UploadProps, UploadRawFile } from "element-plus";
import { json } from 'neo4j-driver-core';
import * as echarts from 'echarts';
import * as XLSX from "xlsx";
type EChartsType = echarts.EChartsType;

const store = useStore()
const modelName:string = 'crnn';
let d = reactive(store.state.analyze.crnn);
let pd = reactive({
  modelInfo:[
    {name:"模型名",   icon:"iconfont icon-24gl-tags2",val:""},
    {name:"文件大小", icon:"iconfont icon-shiti1",val:""},
    {name:"输入维度", icon:"iconfont icon-shuchu2",val:""},
    {name:"预测长度", icon:"iconfont icon-shuchu2",val:"1"},
  ],
  onDialog:false,
  modelInfoOnLoading:true,
  dialogContent:1,

})
// echarts数据不要用响应式保存！
let chartOption = {
    tooltip: {
      trigger: 'axis',
      position: function (pt:any) {
        return [pt[0], '10%'];
      },
      // appendToBody:true,
      // renderMode:'richText',
      confine:true,
    },
    title: {
      left: 'center',
      text: `${modelName.toUpperCase()}模型预测结果`
    },
    toolbox: {
      // feature: {
      //   saveAsImage: {}
      // }
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: d.chartXAxis,
      axisLabel: {showMaxLabel: true}
    },
    yAxis: {
      type: 'value',
      boundaryGap: [0, '100%']
    },
    grid:{
      left:"5%",
      right:"5%",
    },
    dataZoom: [
      {
        type: 'inside',
        start: 80,
        end: 100,
      },
      {
        start: 80,
        end: 100,
      }
    ],
    series: d.chartSeries
}
let chartRef = ref()
var chart = <EChartsType>{};



onBeforeMount(()=>{
})
const getModelInfo = ()=>{
  global.httpPost(
    store.state.server.address + "/querymodel/",
    {username:store.state.status.loginUserName,type:modelName},
    (res)=>{
      if(res.status == store.state.server.successResponse){
        pd.modelInfo[0].val = res.name.length>20?res.name.slice(0,20)+'...':res.name
        pd.modelInfo[1].val = res.size
        pd.modelInfo[2].val = res.in
        pd.modelInfo[3].val = res.out
        d.hasModel = true
      }else if(res.status == store.state.server.failedResponse){
        if(res.reason == "no exist"){
          d.hasModel = false
          
        }
      }
    },
    ()=>{},
    ()=>{pd.modelInfoOnLoading = false},

  )
}
const tabOnChange = (val:any) => {
  if(val=='1'){
    pd.modelInfoOnLoading = true;
    d.hasModel = false;
    getModelInfo();
    // setTimeout(() => {
    //   // if(Object.keys(chart).length!=0){
    //     chart.resize();
    //   // }
    // }, 10);
  }
}
onMounted(()=>{
  if(d.onPredicted){
    chart = echarts.init(chartRef.value);
    chart.setOption(chartOption)
  }
  window.onresize = () => {
    if(Object.keys(chart).length!=0){
      chart.resize();
    }
  }
  getModelInfo()
})
onUnmounted(() => {
  window.onresize = () => {}
  store.state.status.menu[1].route = store.state.router.page_analyze_crnn;
})
var getHeaders = (target:string)=>{
  return{
    "Username":store.state.status.loginUserName,
    "Token":global.getToken(),
    "Model-Target":target
  }
}
const handleCheck:UploadProps['beforeUpload'] = (file) =>{
  const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1);
  const whiteList = ["h5"];
  if (whiteList.indexOf(fileSuffix) === -1) {
    ElMessage.error('只支持.h5模型。');
    return false;
  }
  if (file.size / 1024 / 1024 / 10 > 2) {
    ElMessage.error('模型大小不能超过20MB')
    return false
  }
  
  pd.modelInfoOnLoading = true
}
const handleUploadSuccess: UploadProps['onSuccess'] = (response,uploadFile) => {

  if(response.status == store.state.server.successResponse){
    ElMessage.success('模型分析成功')
    pd.modelInfo[0].val = response.name.length>20?response.name.slice(0,20)+'...':response.name
    pd.modelInfo[1].val = response.size
    pd.modelInfo[2].val = response.in
    pd.modelInfo[3].val = response.out
    pd.modelInfoOnLoading = false
    d.hasModel = true
  }else if(response.status == "out channels error"){
    pd.modelInfoOnLoading = false
    ElMessage.error(`模型输出通道：${response.out} 与期望输出通道：1 不符。请选择其他模型。`)
  }
}




const handleDatasetChange: UploadProps['onChange'] = (file) => {
  let fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx" || fileType === "xls") {
      importfile(fileContent,file.size,fileName,"dataset");
    } else {
      ElMessage.error("文件格式只支持xlsx/xls，请重新上传！")
    }
  } else {
      ElMessage.error("请上传文件！")
  }
}
const handleSampleChange: UploadProps['onChange'] = (file) => {

  if(!d.hasModel){
    ElMessage.error("当前没有模型信息，无法匹配样本。")
    return
  }

  let fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx" || fileType === "xls") {
      // d.selectXColNames=[];    // string[]
      // d.selectYColNames=[];
      importfile(fileContent,file.size,fileName,"sample");
      } else {
      ElMessage.error("文件格式只支持xlsx/xls，请重新上传！")
    }
  } else {
      ElMessage.error("请上传文件！")
  }
}
function importfile(obj:any,size:number|undefined,fileName:string,kind:string = "sample") {
  const reader = new FileReader();
  reader.readAsArrayBuffer(obj);
  reader.onload = function () {
    const buffer:any = reader.result;
    const bytes = new Uint8Array(buffer);
    const length = bytes.byteLength;
    let binary = "";
    for (let i = 0; i < length; i++) {
      binary += String.fromCharCode(bytes[i]);
    }
    const XLSX = require("xlsx");
    const wb = XLSX.read(binary, {
      type: "binary",
    });
    const data = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]],{
      header:1,
    });
    if(kind=="sample"){
      let len:number = 0,count:number = 0;
      if(Number(pd.modelInfo[2].val) == data[0].length){
        len = data[0].length
        count = data.length
      }else if(Number(pd.modelInfo[2].val) == data.length){
        len = data.length
        count = data[0].length
      }else{
        ElMessage.error({message:`样本的各个维度（${data[0].length},${data.length}）都无法与模型输入维度${pd.modelInfo[2].val}相匹配。请查看范例。`,duration:5000})
        return
      }
      
      d.sampleInfo[0].val = fileName.length>12?fileName.slice(0,12)+"...":fileName;
      if(size!=undefined)
        d.sampleInfo[1].val = size>1024 * 1024?(size/1024/1024).toFixed(2)+" MB":(size>1024)?(size/1024).toFixed(2)+" kB":(size+" Bytes")
      d.sampleInfo[2].val = len
      d.sampleInfo[3].val = count
      
      // 列名为特征，行名为样本名
      if(len == data[0].length){
        let trans:Array<any> = []
        for(let i = 0 ; i <data[0].length; i++){
          let temp:string[] = []
          for(let j = 0; j <data.length;j++){
            temp.push(data[j][i])
          }
          trans.push(temp)
        }
        d.sampleData = trans.map((val:any,index:number)=>{
          let row = <any>{};
          for(let i = 0 ; i < val.length ; i++){
            row[`sample${i+1}`] =  val[i]
          }
          row[`sort`] =  (index+1)
          return row
        })
      // 列名为样本名，行名为特征， 默认
      }else if(len == data.length)
        d.sampleData = data.map((val:any,index:number)=>{
          let row = <any>{};
          for(let i = 0 ; i < val.length ; i++){
            row[`sample${i+1}`] =  val[i]
          }
          row[`sort`] =  (index+1)
          return row
        })


      d.sampleDataColumns = Array.from({"length":count + 1}).map((_,index:any) => {
        let row = <any>{}
        row.key = `${index}`
        if(index==0){
          row.dataKey =`sort`
          row.title = `序号`
          row.width = 50
        }else{
          row.dataKey =`sample${index}`
          row.title = `样本${index}`
          row.width = 90
        }
        row.align = 'center'
        return row
      })

      d.hasSample = true
    }else if(kind=="dataset"){
      let colLen = data[0].length
      let rowLen = data.length
      if(rowLen!=1 && colLen!=1){
        ElMessage.warning({message:"维度只能为1。（请确保数据集仅为1行 或 1列）",showClose: true,duration:0})
        return
      }
      d.datasetData = data
      d.datasetInfo[0].val = colLen==1?rowLen:colLen
      d.dataSetOnloaded = true
      ElMessage.success("读取成功。")
    }
    // d.sampleData = obj.data
    // d.sampleDataColumns = obj.columns
    // d.sampleDataOnLoaded = true
  };
}
function rPush(msg:string, iftime:boolean = true) {
  if (iftime) d.trainingInfo.push('['+global.getTime_hms()+'] ' + msg);
  else d.trainingInfo.push(msg);
}
function rClear() {
  d.trainingInfo = [];
}

const ABORT = ()=>{
  rPush("正在发送中止命令...",true)
  store.state.server.socket.send(json.stringify({type:"settings",model:modelName,parameter:"training",parameter_val:false}))
  d.onTraining = false
  // rPush("训练已中止。",true)
}
const TRAIN = ()=>{
  if(!d.dataSetOnloaded){
    ElMessage.error("未选择数据集。")
    return
  }
  if(d.datasetInfo[1].val==""||d.datasetInfo[2].val==""||d.datasetInfo[3].val==""){
    ElMessage.error("请填写训练信息。")
    return
  }
  if(Number(d.datasetInfo[1].val)<=0){
    ElMessage.error("窗口大小设置异常。")
    return
  }
  if(Number(d.datasetInfo[2].val)<=0){
    ElMessage.error("预测长度设置异常。")
    return
  }
  if(Number(d.datasetInfo[2].val)>100){
    ElMessage.error("预测长度应不超过100。")
    return
  }
  if(Number(d.datasetInfo[1].val)>=Number(d.datasetInfo[0].val)){
    ElMessage.error("窗口大小应小于序列长度。")
    return
  }
  if(Number(d.datasetInfo[3].val)>100||Number(d.datasetInfo[3].val)<10){
    ElMessage.error("epoch只支持10-100之间")
    return
  }




  rClear();
  rPush("准备上传数据")
  rPush("训练样本序列长度："+d.datasetInfo[0].val+"，窗口大小："+d.datasetInfo[1].val)
  rPush("开始训练...")
  rPush("无法训练模型。原因：演示版本。已提前return。",true)

  ElMessage.info("演示版本 无法进行写操作。")
  return;



  store.state.server.socket.send(json.stringify({type:"settings",model:modelName,parameter:"training",parameter_val:true}))

  d.onTraining = true;
  d.onTrained = false;
  d.trainingInfo = [];


  global.httpPost(
    store.state.server.address + '/analyze/train/',
    {username:store.state.status.loginUserName,model:modelName,data:d.datasetData,window:d.datasetInfo[1].val,outsize:d.datasetInfo[2].val,epoch:d.datasetInfo[3].val},
    (res)=>{
      // console.log(res)
      if(res.status == "success"){
        d.onTrained = true;
        rPush(`模型${res.res.name}已经训练完成，现在可以下载模型。`,true)
        d.modelUrl = res.res.url
      }else if(res.status == "abort"){
        rPush("训练已中止，原因：用户中止训练。",true)
      }else if(res.status == "error"){
        rPush("训练已中止，原因：训练出现错误。",true)
      }
    },
    ()=>{},
    ()=>{d.onTraining = false;}
  )


}
const DOWNLOAD =  ()=> {
  ElMessage.info("下载已开始，请稍等。")
  window.location.href = store.state.server.address + d.modelUrl+"?r="+Math.random();
}
const PREDICT =  ()=> {

  ElMessage.info("演示版本 无法进行写操作。")
  return;
  d.onPredicting = true
  // function getAreaStyleColor(index:number,num:number){
    
  // }
  
  let packageData = d.sampleData.map((val:any)=>{
    let row = <any>[]
    for(let key in val){
      if(key!='sort')
        row.push(Number(val[key]))
    }
    return row
  })
  global.httpPost(
    store.state.server.address + '/analyze/predict/',
    {username:store.state.status.loginUserName,model:modelName,data:packageData},
    (res)=>{
      if(res.status == "success"){
        // console.log(res.res)
        let Series = <any>[],XLabel = <any>[]
        res.res.map((val:any,index:number)=>{
          Series.push({
            name: `样本${index+1}`,
            type: 'line',
            symbol: 'none',
            sampling: 'lttb',
            itemStyle: {
              color: 'rgb(255, 70, 131)'
            },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                {
                  offset: 0,
                  color: 'rgb(255, 158, 68)'
                },
                {
                  offset: 1,
                  color: 'rgb(255, 70, 131)'
                }
              ])
            },
            data: val
          })
        })
        for(let i = 0 ; i < Number(d.sampleInfo[2].val) ; i++)
          XLabel.push(`节点${i+1}`)
        for(let i = 0 ; i < res.res[0].length - Number(d.sampleInfo[2].val) ; i++)
          XLabel.push({value:`预测${i+1}`,textStyle: {
            color: 'darkred'
          }})
        
        d.chartSeries = Series
        d.chartXAxis = XLabel
        chartOption.series = Series
        chartOption.xAxis.data = XLabel
        d.onPredicted = true
        if (Object.keys(chart).length==0) {
          chartRef.value.style = "width:100%;height:100%"
          chart = echarts.init(chartRef.value);
        }
        chart.setOption(chartOption)  
        setTimeout(() => {
          chart.resize();
        }, 10);
        
      }else{
        ElMessage.error(`出现错误，原因：${res.status}`)
      }
    },
    (err)=>{console.log(err)},
    ()=>{d.onPredicting = false},
  )
}
const DOWNLOADPREDICT =  ()=> {
  ElMessage.info("下载已开始，请稍等。")
  let exportdata = []
  for(let i = 0 ; i < d.chartSeries.length ; i++){
    exportdata.push(d.chartSeries[i].data)
  }
  const data = XLSX.utils.json_to_sheet(global.transposition(exportdata),{skipHeader: true,})
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, data, 'Sheet1')
  XLSX.writeFile(wb,`${modelName}_predict.xlsx`)
}
const SAVEPREDICT =  ()=> {
  ElMessage.info("下载已开始，请稍等。")
  var img = new Image();
  img.src = chart.getDataURL({
    type: "png",
    pixelRatio: 1, 
    backgroundColor: "#fff",
  });
  img.onload = function () {
    var canvas = document.createElement("canvas");
    canvas.width = img.width;
    canvas.height = img.height;
    var ctx = canvas.getContext("2d");
    if(ctx==null)
      return
    ctx.drawImage(img, 0, 0);
 
    var a = document.createElement("a");
    a.download = `${modelName.toUpperCase()}预测.png` || "图片名称";
    // 将生成的URL设置为a.href属性
    a.href = canvas.toDataURL("image/png");
    // 触发a的单击事件
    a.dispatchEvent(new MouseEvent("click"));
    a.remove();
  };

}



</script>

<style scoped lang="less">
/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
}
.page{
  width: 100%;
  height: 100%;
  background: rgb(252, 252, 252);
  overflow: hidden;
}
.el-table__row {
  td:not(.is-hidden):last-child {
    border-left: 1px solid #e4e7ec;
  }
}
.dialogRow{
  height: 24px;
  line-height: 18px;
  font-size: 16px;
  color: #409EFF;
}
.dialogRow2{
  height: 24px;
  display: flex;
  line-height: 24px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.582);
}

.centerrow{
    // height: 200px;
    // width: 100px;
    // position: absolute;
    display: flex;
    align-items: start;
    // background: rebeccapurple;
    .centercolumn{
      display: flex;
      flex-wrap: wrap;
      justify-content: center;
      // background-color: red;
    }
  }
.mainCard{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  max-width: 1600px;
  max-height: 960px;
  height: calc(100% - 62px - 50px - 50px);
  display: block;

  .TrainInfoArea{

    background: rgba(109, 109, 109, 0.041);
    margin-top: 5px;
  }
  .littleBtn{
    // background: red;
    // width: 20px;
    
    height: 24px;
    padding-left: 5px;
    padding-right: 5px;
    margin-left: 5px;
    margin-right: 5px;
    // line-height: 10px;
    font-size: 16px;
  }
  .titleRow{
    height: 50px;
    font-family: "SimHei";
    border-bottom: 1px solid #dcdfe670;
    font-weight: bold;
    color: #4e6077;
    display: flex;
    align-items: center;
  }
  .modelRow{
    width: 100%;
    height: 216px;
    min-width: 840px;
    display: flex;
    position: relative;
    //  background: blue; 
    .modelColumn{
      width: 400px;
      height: 100%;
      // padding-right: 20px;
      margin-right: 20px;
      // padding-bottom: 20px;
      position: relative;
      // border-right: 1px solid #dcdfe650;
      // background: #409EFF;
      .msgRow{
        width: 100%;
        height: calc(100% - 51px);
      }
    }
  }
  .displayRow{
      height: calc(100% - 216px - 56px);
      // background: red;
      width: 100%;
    .echartRow{
      width: 100%;
      // background-color: wheat;
      height: calc(100% - 50px - 40px);
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      .chart{
        width: 100%;
        height: 100%;
        min-height: 270px;
        // background-color: antiquewhite;
      }
    }
    .btnRow{
      // background: red;
      height: 40px;
      width: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }
  }
  .tabs{
    height: calc(100 - 40px);
    width: calc(100% - 40px);
    position: absolute;
    .tabplane{
      height: calc(100vh - 62px - 100px - 60px - 39px);
      max-height: calc(960px - 60px - 39px);
      width: 100%;
      position: relative;
      // background-color: #dcdfe670;
    }

  }
}

/deep/  input::-webkit-outer-spin-button,
/deep/  input::-webkit-inner-spin-button {
  -webkit-appearance: none;
}




</style>