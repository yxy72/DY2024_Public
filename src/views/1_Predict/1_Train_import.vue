<template>
  <div class="Page">
      <el-card class="mainArea">
        <div class="titleRow">
          <el-upload
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :show-file-list="false"
              :auto-upload="false">
              <el-button size="large" :style='"padding: 7px;border-radius:"+store.state.option.style.el_button_border_radius+";"' type="primary"
                ><el-icon size="25px" style="margin-right: 4px"
                  ><folder-add /></el-icon
                >读取Excel文件</el-button
              >
            </el-upload>
            
            <div style="margin-left: 20px;font-size: 13px;color: gray;font-family: Arial, Helvetica, sans-serif;display: flex;align-items: end;margin-bottom: 10px; ">
              从本地文件上传用于训练模型的数据集<el-button @click="pd.onDialog = true;" type="primary" link style="margin-left: 10px;padding: 0;">
              <div style="font-size: 14px;">查看说明</div></el-button>
            </div>
        </div>
        <div class="scollRow">
          <div class="tableRow">
            <el-empty
            v-if="!d.onLoaded"
            style="height: 100%; background: #f7f7f7"
            description="请载入表格（支持xlsx、csv格式）"
            />
            <el-auto-resizer v-else>
              <template #default="{ height, width }">
                <el-table-v2
                  :width="width"
                  :height="height"
                  fixed
                  :columns="d.sampleColumnNames_forTable"
                  :data="d.data_forTable"
                >
                  <!-- <el-table-column
                    v-for="(item, index) in d.sampleColumnNames"
                    :key="index"
                    :prop="item"
                    :label="item"
                  ></el-table-column> -->
                </el-table-v2>
              </template>
              </el-auto-resizer>
          


          </div>

              
              
          <div class="optionRow">
            <div class="subTitleRow">
              <div class="subTitleIcon">
                <el-icon size="25px" style="marginright: 4px"
                  ><histogram
                /></el-icon>
              </div>
              <div class="subTitleLabel">数据集属性</div>
            </div>
            <div style="min-width: 1080px;">
              <el-descriptions class="margin-top" :column="4" border >
                <el-descriptions-item width="120px" >
                  <template #label >
                    <div class="cell-item" >
                      <i class="iconfont" >&#xe87c;</i>
                      样本总计1
                    </div>
                  </template>
                  <div
                    v-if="!d.onLoaded"
                    style="color: gray; font-size: 11px"
                  >
                    等待加载
                  </div>
                  <div v-else>{{ d.sampleRowCount }}</div>
                </el-descriptions-item>
                <el-descriptions-item width="120px">
                  <template #label>
                    <div class="cell-item">
                      <i class="iconfont">&#xe618;</i>

                      样本列数
                    </div>
                  </template>
                  <div
                    v-if="!d.onLoaded"
                    style="color: gray; font-size: 11px"
                  >
                    等待加载
                  </div>
                  <div v-else>{{ d.sampleColumnCount }}</div>
                </el-descriptions-item>
                <el-descriptions-item width="120px">
                  <template #label>
                    <div class="cell-item">
                      <i class="iconfont"> &#xe60e; </i>
                      特征维度数
                    </div>
                  </template>
                  <div
                    v-if="!d.onLoaded"
                    style="color: gray; font-size: 11px"
                  >
                    等待加载
                  </div>
                  <div v-else>{{ d.selectXColNames.length }}</div>
                </el-descriptions-item>
                <el-descriptions-item width="120px">
                  <template #label>
                    <div class="cell-item">
                      <i class="iconfont"> &#xe618; </i>
                      标签维度数
                    </div>
                  </template>
                  <div
                    v-if="!d.onLoaded"
                    style="color: gray; font-size: 11px"
                  >
                    等待加载
                  </div>
                  <div v-else>{{ d.selectYColNames.length }}</div>
                </el-descriptions-item>
                <el-descriptions-item>
                  <template #label>
                    <div class="cell-item">
                      <i class="iconfont"> &#xe60a; </i>
                      数据状态
                    </div>
                  </template>
                  <el-tag
                    v-if="
                      d.selectXColNames.length == 0 || d.selectYColNames.length == 0
                    "
                    class="ml-2"
                    type="warning"
                    ><div style="font-size: 12px;">未处理</div></el-tag>
                  <el-tag v-else class="ml-2" type="success"
                    ><div style="font-size: 12px;">已处理</div></el-tag>
                  
                </el-descriptions-item>
                <el-descriptions-item>
                  <template #label>
                    <div class="cell-item">
                      <i class="iconfont"> &#xe71c; </i>
                      选择特征列
                    </div>
                  </template>
                  <el-select
                    v-model="d.selectXColNames"
                    multiple
                    collapse-tags
                    @change="selectOnchange"
                    placeholder="特征列"
                    class="excelSecletLabel"
                    style="width: 240px"
                  >
                    <el-option
                      v-for="item in d.sampleColumnNames"
                      :key="item"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-descriptions-item>
                <el-descriptions-item>
                  <template #label>
                    <div class="cell-item">
                      <i class="iconfont"> &#xe71c; </i>
                      选择标签列
                    </div>
                  </template>
                  <el-select
                    v-model="d.selectYColNames"
                    multiple
                    collapse-tags
                    placeholder="标签列"
                    class="excelSecletLabel"
                    style="width: 240px"
                  >
                    <el-option
                      v-for="item in d.sampleColumnNames"
                      :key="item"
                      :label="item"
                      :value="item"
                    />
                  </el-select>
                </el-descriptions-item>
              </el-descriptions>
            </div>

            <el-divider style="margin-bottom: 5px;min-width: 1080px;" />
            <div style="min-width: 1080px;">
              <div class="subTitleRow">
                <div class="subTitleIcon">
                  <el-icon size="25px" style="marginright: 4px"
                    ><data-line
                  /></el-icon>
                </div>
                <div class="subTitleLabel">预处理</div>
                <el-button :disabled="(d.onloaded)" style="margin-left: 10px" size="small" @click="queryPreParameters()">
                  <div style="font-size: 12px">查看参数</div>
                </el-button>
              </div>
              <el-row v-if="d.serverDataOnLoaded"
                style="background: ; height: 80px; margin-top: -20px"
                align="middle"
              >
                <el-col :span="1"></el-col>
                <el-col :span="16">
                  <el-radio-group v-model="d.preProcessVal" >
                    <el-radio size="small" v-for="(item,index) in d.preProcess" :key="index" :label="item.val"
                    ><div style="font-size: 17px">{{item.name}}</div>
                    </el-radio>
                  
                  </el-radio-group>
                </el-col>
                <el-divider direction="vertical" />
                <el-col :span="1">
                  <div style="">预览</div>
                </el-col>
                <el-col :span="5" style="display: flex; align-items: center;">
                  <vue-latex
                    :expression="d.preProcess[d.preProcess.map(function(e) { return e.val; }).indexOf(d.preProcessVal)].expression"
                    display-mode/>
                  <el-icon style="marginleft: 6px; color: lightgray"
                    ><question-filled
                  /></el-icon>
                </el-col>
              </el-row>
            </div>
          </div>


        </div>




        <div class="bottomRow">
          <el-button-group>
            <el-button hidden="hidden" size="large" type="info" plain disabled><el-icon class="el-icon--right" style=""><ArrowLeft /></el-icon>上一步</el-button>
            <el-button @click="$router.replace({path: store.state.router.page_predict_settings});"
              size="large" type="primary" plain>下一步<el-icon class="el-icon--right"><ArrowRight /></el-icon>
            </el-button>
          </el-button-group>
          <el-divider direction="vertical" />
          <el-button style="color: gray" size="small" @click="pageReset()" link>重置本步骤</el-button>
        </div>
      </el-card>
      <div class="bottomArea">
      <div class="step">
        <el-steps
          :active="d.step"
          finish-status="success"
          simple>
          <el-step title="导入数据" />
          <el-step title="预处理" />
          <el-step title="选择网络" />
          <el-step title="训练模型" />
          <el-step title="完成" />
        </el-steps>
      </div>
    </div>

    <el-dialog
      v-model="pd.onQueryingParams"
      append-to-body
      align-center
      >
      <template #header>
        <div style="margin-bottom: -20px;display: flex;">
          <div style="margin-left: 0px;font-size: 23px;margin-top: 0px;"><el-icon><Setting /></el-icon></div>
          <div style="margin-left: 4px;font-size: 20px;">过程参数</div>
        </div>
      </template>
      <div class="dialogRow">预处理方式：{{d.preProcess[d.preProcess.map((e:any) => { return e.val; }).indexOf(d.preProcessVal)].name  }}</div>
      <div class="dialogRow2">使用模型预测时确保输入按照同样的方式进行了初始化。</div>
      <!-- <div class="dialogRow">参数:</div> -->
      <el-table :data="pd.dialogTableData" style="width: 100%"
      empty-text="-/-">
        <el-table-column fixed prop="parameters" label="参数名" />
        <el-table-column v-for="(item,index) in pd.dialogTableCol" :prop="item.prop" :key="index" :label="item.label" />
        <el-table-column fixed="right" label="操作" >
          <template #default="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click.prevent="tableCopy(scope.row)"
              >
                <div style="color:#409EFF"><div style="font-size: 14px;">复制</div></div>
              </el-button>
            </template> 
        </el-table-column>

      </el-table>
    </el-dialog>

    <el-dialog
      v-model="pd.onDialog"
      append-to-body
      align-center
      width="720"
      >
      <template #header>
        <div style="margin-bottom: -20px;display: flex;">
          <div style="margin-left: 0px;font-size: 23px;margin-top: 0px;"><el-icon><Setting /></el-icon></div>
          <div style="margin-left: 4px;font-size: 20px;">数据集说明</div>
        </div>
      </template>
      <div class="dialogRow2">1. 表格的不同行代表不同的样本，不同的列代表样本的特征或标签。</div>
      <div class="dialogRow2">2. 表格<div style="color: darkred;">应含</div>表头。</div>
      <el-divider style="margin-top: 15px;margin-bottom: 20px;"><div style="color: gray;">示例</div></el-divider>
      <div style="display: flex;justify-content: center;flex-wrap: wrap;">
        <el-image :src="store.state.server.address+'/src/images/pages/page_cnn_datasetSample.png'"></el-image>
        <div style="font-size: 16px;margin-top: 5px;">特征或标签列：8，样本数：9</div>
      </div>
    </el-dialog>
  </div>

</template>
<script setup lang="ts">



import { ElMessage } from "element-plus";
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { Store, useStore } from "vuex";
import { onMounted, onUnmounted, ref } from "@vue/runtime-core";
import useClipboard from 'vue-clipboard3'
import type { UploadProps, UploadUserFile } from 'element-plus'

const $router = useRouter();
const store = useStore();
const { toClipboard } = useClipboard()

let d = reactive(store.state.train);

let pd = reactive({
  onDialog:false,
  onQueryingParams:false,
  queryValid:false,
  dialogTableData:[{}],
  dialogTableCol:[{}],
})
onMounted(() => {
  d.step = d.onLoaded?2:0;
});
onUnmounted(() => {
  store.state.status.menu[0].route = store.state.router.page_predict_import_data;
})
const selectOnchange = (val:any)=>{
  if(val.length==0){
    pd.queryValid = false
    d.queryValid = false
    return
  }else{
    pd.queryValid = true
    d.queryValid = true
  }
}
const tableCopy = async(val:any) =>{
  await toClipboard(JSON.stringify(Object.values(val).slice(1).map(Number)))

}
const queryPreParameters = () => {
  if(!d.queryValid){
    ElMessage.error("还没有选择特征列。")
    return
  }
  pd.onQueryingParams = true;
  
  
  // 预处理列名
  pd.dialogTableCol = Array.from({"length":d.selectXColNames.length})
  .map((_,index)=>({
    prop:d.selectXColNames[index],
    label:d.selectXColNames[index]
  }))
  let rowNames :any[] = []

  // 特征列数据
  let colData = Array.from({"length":d.selectXColNames.length}).map((_,index)=>({
    colName:d.selectXColNames[index],
    val: <any>[],
  }))
  for(let i = 0 ; i<d.data.length ; i++){
    for(let j = 0 ; j<colData.length ; j++){
      colData[j].val.push(d.data[i][colData[j].colName])
    }
  }
  
  function calRes(type:string,data:number[]){
    switch(type){
      case "0":
        return data[0].toFixed(2)
      case "min":
        return Math.min(...data).toFixed(2)
      case "max":
        return Math.max(...data).toFixed(2)
      case "mean":
        return (data.reduce((a,b)=>a+b,0)/data.length).toFixed(2)
      case "std":
        let mean = data.reduce((a,b)=>a+b,0)/data.length
        return (Math.sqrt(data.reduce((a,b)=>a+(b-mean)**2,0)/data.length)).toFixed(2)
    }
  }
  switch(d.preProcessVal){
    case d.preProcess[0].val:
      rowNames = ["映射"];
      break;
    case d.preProcess[1].val:
      rowNames = ["映射"]; break;
    case d.preProcess[2].val:
      rowNames = ["均值"]; break;
    case d.preProcess[3].val:
      rowNames = ["初值"]; break;
    case d.preProcess[4].val:
      rowNames = ["均值","标准差"]; break;
    case d.preProcess[5].val:
      rowNames = ["最小值","最大值"]; break;
    case d.preProcess[6].val:
      rowNames = []; break;
  }
  
  pd.dialogTableData = rowNames
  .map((rowName,index)=>{
    let row:any = {parameters:rowName};
    switch(rowName){
      case "映射":
        for(let r = 0; r<d.selectXColNames.length;r++){
          row[d.selectXColNames[r]] = d.preProcessVal==d.preProcess[0].val?"log10":"ln"
        }
        break;
      case "均值":
        for(let r = 0; r<d.selectXColNames.length;r++){
          let data = colData[colData.findIndex((item)=>item.colName==d.selectXColNames[r])].val
          row[d.selectXColNames[r]] = calRes("mean",data)
        }
        break;
      case "初值":
        for(let r = 0; r<d.selectXColNames.length;r++){
          // let data = colData[colData.findIndex((item)=>item.colName==d.selectXColNames[r])].val
          // row[d.selectXColNames[r]] = calRes("0",data)
          row[d.selectXColNames[r]] = d.data[0][d.selectXColNames[r]]
        }
        break;
      case "标准差":
        for(let r = 0; r<d.selectXColNames.length;r++){
          let data = colData[colData.findIndex((item)=>item.colName==d.selectXColNames[r])].val
          row[d.selectXColNames[r]] = calRes("std",data)
        }
        break;
      case "最小值":
        for(let r = 0; r<d.selectXColNames.length;r++){
          let data = colData[colData.findIndex((item)=>item.colName==d.selectXColNames[r])].val
          row[d.selectXColNames[r]] = calRes("min",data)
        }
        break;
      case "最大值":
        for(let r = 0; r<d.selectXColNames.length;r++){
          let data = colData[colData.findIndex((item)=>item.colName==d.selectXColNames[r])].val
          row[d.selectXColNames[r]] = calRes("max",data)
        }
        break;
    }
    return row
  }
  )


}


function pageReset() {
  d.sampleColumnNames = [];
  d.data = [];
  d.sampleRowCount = "-";
  d.sampleColumnCount = "-";
  d.onLoaded = false;
  d.selectXColNames = [];
  d.selectYColNames = [];
  d.preProcessIndex = 4;
  d.step = 0;
}
function reloadDefaultSettings() {
  d.selectXColNames = [];
  d.selectYColNames = [];
}
const handleChange: UploadProps['onChange'] = (file) => {
  // ElMessage('success')
  let fileContent;
  reloadDefaultSettings();
  fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx" || fileType === "xls") {
      d.fileSize = file.size
      d.fileName = fileName;
      importfile(fileContent);
    } else {
      ElMessage.error("附件格式错误，请重新上传！")
    }
  } else {
      ElMessage.error("请上传附件！")
  }
}
function importfile(obj:any) {
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
    const outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
    let data = [...outdata];
    const arr:any = [];
    let coName = Object.keys(data[0]);
    d.sampleColumnCount = coName.length;
    let rowSum = 0;
    data.map((v) => {
      const obj:any = {};
      for (let i = 0; i < coName.length; i++) {
        obj[coName[i]] = v[coName[i]];
      }
      rowSum++;
      d.sampleColumnNames = coName;
      arr.push(obj);
    });
    d.sampleRowCount = rowSum;
    d.data = arr;
    d.onLoaded = true;
    d.step = 1;


    d.data_forTable = d.data.map((val:any,rowIndex:any) => {
      val.id = rowIndex
      val.parentId = null
      return val
    })
    d.sampleColumnNames_forTable = d.sampleColumnNames.map((val:any,index:any) => ({
      key: `${index}`,
      dataKey: `${val}`,
      title: val,
      width: 150,
    }))


    // console.log(d.sampleColumnNames)
    // console.log(d.data)
    // console.log(d.sampleColumnNames)
  };
}


</script>
<style scoped lang="less">

/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
}
.iconfont {
  font-family: "iconfont" !important;
  font-size: 14px;
  font-style: normal;
  font-weight: 100;
  -webkit-font-smoothing: antialiased;
  -webkit-text-stroke-width: 0.2px;
  -moz-osx-font-smoothing: grayscale;
}
html,
body,
#app {
  height: 100%; /* precious */
}
/* *{
    margin: 0;
    padding: 0;
} */
.Page {
  width: 100vw;
  height: 100vh;
  background: transparent;
  position: relative;
}
.mainArea{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  max-width: 1600px;
  height: calc(100% - 62px - 50px - 46px - 20px - 50px);
  // display: block;
  /* overflow: hidden; */
  /* background-color: wheat; */
}
.titleRow{
  display: block;
  // background-color: red; 
  height: 50px;
  border-bottom: 1px solid #dcdfe6;
  width: calc(100% - 40px);
  position: absolute;
  display: flex;
}
.bottomRow{
  //  background-color: red; 
  border-top: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  justify-content: center;
  width: calc(100% - 40px);
  height: 90px;
  position: absolute;
  bottom:0px;
}
.scollRow{
  position: absolute;
  width: calc(100% - 40px);
  top: 73px;
  height: calc(100% - 70px - 90px - -2px);
  // background-color: red; 
  display: block;
  overflow: scroll;
  .optionRow{
    margin-top: 3px;
    border-top: 1px solid #dcdfe6;
    min-width: 1080px;
    // background-color: red;
    // position: absolute;
    // width: 100%;
    height: 285px;
    // bottom: 0;
    display: block;
  }
  .tableRow{
    // background-color: yellow;
    height: calc(100% - 289px);
    display: block;
    min-height: 120px;
    min-width: 1080px;
    // position: relative;
    // .tableD{
    //   background-color: red;
    //   height: 100%;
    // }
  }
}
.bottomArea{
  width:calc(100% - 220px - 100px - 0px);
  overflow: hidden;
  height: 46px;

  padding-top: 8px;
  padding-bottom: 8px;
  padding-left: 8px;
  padding-right: 8px;

  position: absolute;
  bottom: 42px;
  left: calc(220px + 50px - 8px);
  max-width: 1600px;
  align-items: center;
  // background: #509bfe2d;

  .step{
    height: 46px;
    min-width: 810px;
    // background: red;
    box-shadow: 0px 0px 8px 0px rgba(109, 109, 109, 0.205);
  }
}
::-webkit-scrollbar {
  /* 滚动条整体样式 */
  width: 5px; /* 高宽分别对应横竖滚动条的尺寸 */
  height: 8px;
}
::-webkit-scrollbar-thumb {
  /* 滚动条内滑块的样式 */
  border-radius: 5px;
  -webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.11);
  background: #8d8d8d34;
}


.excel {
  width: 100%;
  height: 100%;
  /* background: red; */
}

.formula {
  background: red;
  width: 200px;
  height: 100%;
}
.subTitleRow {
  width: 100%;
  /* background: rgba(102, 51, 153, 0.151); */
  height: 50px;
  display: flex;
  align-items: center;
}
.subTitleIcon {
  margin-left: 5px;
  color: #509cfe;
}
.subTitleLabel {
  margin-left: 2px;
  font-size: 16px;
  font-family: "SimHei";
  font-weight: bold;
  color: #4e6077;
}

.dialogRow{
  height: 24px;
  line-height: 24px;
  font-size: 16px;
  color: #409EFF;
}
.dialogRow2{
  height: 24px;
  line-height: 24px;
  font-size: 14px;
  display: flex;
  color: rgba(0, 0, 0, 0.582);
}
</style>