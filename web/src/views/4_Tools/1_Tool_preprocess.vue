<template>
  <div class="Page">
    <el-card class="mainArea">

      <div class="leftCol">
        <div class="leftColRow1">

          <div class="titleRow">
            <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><List /></el-icon>
            源样本
          </div>

          <div class="tableRow">
            <el-empty
              v-if="!d.onLoaded"
              :image-size="100"
              style="background: #fbfbfb; height: 100%"
              description="等待载入数据..."
            />
            <el-auto-resizer v-else>
              <template #default="{ height, width }">
                <el-table-v2
                  :width="width"
                  :height="height"
                  fixed
                  :columns="d.dataColumns_forTable"
                  :data="d.data"
                >
                </el-table-v2>
              </template>
            </el-auto-resizer>
          </div>



          <div class="bottomRow">

            <el-upload
              :on-change="handleChange"
              :show-file-list="false"
              :auto-upload="false"
              style="position: relative;height: 100%;display: flex;justify-content: center;"
            >
              <el-button plain size="small"   style="position: absolute;width: 100%;height: 100%;"
                ><div style="font-size: 15px;">载入</div></el-button>
            </el-upload>
          </div>


   
        </div>
        <div class="leftColRow2">
          <div class="titleRow">
            <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><List /></el-icon>
            预处理样本
          </div>

          <div class="tableRow">
            <el-empty
              v-if="!d.onProcessed"
              :image-size="100"
              style="background: #fbfbfb; height: 100%"
              description="等待执行预处理操作..."
            >
            </el-empty>

            <el-auto-resizer v-else v-loading="d.onProcessing">
              <template #default="{ height, width }">
                <el-table-v2
                  :width="width"
                  :height="height"
                  fixed
                  :columns="d.dataColumns_forTable"
                  :data="d.data_processed_forTable"
                >
                </el-table-v2>
              </template>
            </el-auto-resizer>
          </div>



          <div class="bottomRow">

            <el-button @click="DOWNLOAD()"
              :disabled="!d.onProcessed" plain size="small" type="primary"  style="position: absolute;width: 100%;height: 100%;"
                ><div style="font-size: 15px;">下载</div></el-button>
          </div>

        </div>
      </div>

      <div class="rightCol">

        <div class="titleRow">
          <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><List /></el-icon>
          预处理参数
        </div>

        <el-radio-group v-model="pd.preProcessVal" style="border-bottom: 1px solid #dcdfe650;" >
          <el-radio style="width:100%" size="large" v-for="(item,index) in pd.preProcess" :key="index" :label="item.val">
            <div style="font-size: 16px">{{item.name}}</div>
          </el-radio>
        </el-radio-group>


        <div style="color: gray;height: 40px;line-height: 40px;">预览</div>
        <vue-latex
          style="height:60px"
          :expression="pd.preProcess[pd.preProcess.map(function(e) { return e.val; }).indexOf(pd.preProcessVal)].expression"
          display-mode/>

        <div v-if="pd.preProcessVal!=pd.preProcess[0].val && pd.preProcessVal!=pd.preProcess[1].val&& pd.preProcessVal!=pd.preProcess[6].val">
        
          <div style="color: gray;height: 10px;border-top: 1px solid #dcdfe650;"></div>
          <div style="color: gray;height: 20px;">方式</div>

          <el-radio-group v-model="d.preprocessKind" class="ml-4">
            <el-radio label="1" size="large">基于源样本</el-radio>
            <el-radio label="2" size="large">基于其他参数</el-radio>
          </el-radio-group>
          <el-button style="margin-bottom: 10px;" v-if="d.preprocessKind==2" @click="loadParameters()">
            {{pd.parameter_onLoaded?"重新载入":"载入数据"}}
          </el-button>
        </div>


        <div style="color: gray;height: 10px;border-top: 1px solid #dcdfe650;"></div>

        <div style="color: gray;height: 30px;">小数保留位数</div>

        <div class="sliderArea">
          <div class="slider"  >
              <el-slider :max="12" :min="1" :step="1" v-model="d.tofixedNum" />
          </div>
          <div class="slidertext">{{d.tofixedNum}}</div>
        </div>

        <div style="color: gray;height: 40px;border-bottom: 1px solid #dcdfe650;">文件含表头<el-checkbox @change="d.onLoaded = false;d.onProcessed = false" style="margin-left: 10px;" v-model="d.excelHasTitle" label="" size="large" /></div>
        

        <el-button type="success" style="width: 100%;margin-Top:20px;" plain size="" @click="PREPROCESS()">执行</el-button>
        <div></div>
        <el-button :disabled="(!d.onProcessed)" plain style="width: 100%;margin-top: 10px;" @click="pd.onQueryingParams = true;">
          <div style="font-size: 12px">查看预处理参数</div>
        </el-button>
      
      </div>

    </el-card>
    <el-dialog
      v-model="pd.parameter_onLoading"
      append-to-body
      align-center
      >
      <template #header>
        <div style="margin-bottom: -20px;display: flex;">
          <div style="margin-left: 0px;font-size: 23px;margin-top: 0px;"><el-icon><Setting /></el-icon></div>
          <div style="margin-left: 4px;font-size: 20px;">自定义过程参数</div>
        </div>
      </template>
      <div class="dialogRow">预处理方式：{{ pd.preProcess[pd.preProcess.map((e:any) => { return e.val; }).indexOf(pd.preProcessVal)].name }}</div>
      <div class="dialogRow2">请以数组的形式输入下列所需参数。</div>
      <!-- <div class="dialogRow">参数:</div> -->

      
      <el-row v-for="(item, index) in pd.p" :key="index" style="height: 30px;margin-top: 10px;">
        <el-col :span="3">
          <div style="line-height: 30px;height: 30px;">{{ item.label }}</div>
        </el-col>
        <el-col :span="20">
          <el-input
            v-model="item.text"
            :placeholder="'请输入各维度对应'+item.label+'，格式：[1,2,3,...]'"
        />
        </el-col>
      </el-row>

      <div style="display: flex;justify-content: center;margin-top: 15px;">
      <el-button type="primary" @click="checkParameters(pd.p)" >
        确认
      </el-button>
      </div>
    </el-dialog>
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
      <div class="dialogRow">预处理方式：{{ d.preProcessValNow }}</div>
      <div class="dialogRow2">使用模型预测时确保输入按照同样的方式进行了初始化。</div>
      <!-- <div class="dialogRow">参数:</div> -->
      <el-table :data="d.dialogTableData" style="width: 100%"
      empty-text="-/-">
        <el-table-column fixed prop="parameters" label="参数名" />
        <el-table-column v-for="(item,index) in d.dialogTableCol" :prop="item.prop" :key="index" :label="item.label" />
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
  </div>
</template>

<script setup lang="ts"> 
import { ElMessage, ElMessageBox } from "element-plus";
import {onMounted, onUnmounted, reactive,ref } from "vue";
import { useStore } from "vuex";
import * as XLSX from "xlsx";

const store = useStore();
let d = reactive(store.state.tools.preprocess);
let t = reactive(store.state.train);
let pd = reactive({
  preProcess:t.preProcess,
  preProcessVal:t.preProcess[0].val,
  parameter_onLoaded: false,
  parameter_onLoading: false,
  parameter_custom: <any>[],
  p: [{}],
  onQueryingParams:false,

})


function handleChange(file:any) {
  let fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx" || fileType === "xls") {
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
    let outdata:any;

    if(d.excelHasTitle){
      outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
      let data = [...outdata];
      const arr:any = [];
      let coName = Object.keys(data[0]);

      data.map((v) => {
        const obj:any = {};
        for (let i = 0; i < coName.length; i++) {
          obj[coName[i]] = v[coName[i]];
        }
        arr.push(obj);
      });      
      d.dataColumns = coName;
      d.data = arr
      d.dataColumns_forTable = d.dataColumns.map((val:any,index:any) => ({
        key: `${index}`,
        dataKey: `${val}`,
        title: val,
        width: 150,
      }))
    }else{

      outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]],{header:1});
      d.data = outdata.map((val:any)=>{
        let row = <any>{};
        for(let i = 0 ; i < val.length ; i++){
          row[`col${i+1}`] =  val[i]
        }
        return row
      })
      d.dataColumns = []
      for(let i = 0 ; i < outdata[0].length ; i++){
        d.dataColumns.push(`col${i+1}`)
      }
      d.dataColumns_forTable = d.dataColumns.map((val:any,index:any) => ({
        key: `${index}`,
        dataKey: `${val}`,
        title: `列${val.slice(3)}`,
        width: 150,
      }))
    }
    d.onLoaded = true;
    d.onProcessed = false;
  };
}

import useClipboard from 'vue-clipboard3'
const { toClipboard } = useClipboard()
const tableCopy = async(val:any) =>{
  await toClipboard(JSON.stringify(Object.values(val).slice(1).map(Number)))
}

function checkParameters(p:any){
  pd.parameter_onLoaded = false
  let obj = []
  try{
    for(let i = 0; i<p.length;i++){
      obj.push(JSON.parse(p[i].text))
    }
  }catch(error){
    ElMessage.error("输入格式有误。")
    return
  }
  if(obj[0].length != d.dataColumns.length){
    ElMessage.error("参数数量："+obj[0].length+"与样本维度数："+d.dataColumns.length+"不匹配。")
    return
  }
  pd.parameter_custom = obj;
  pd.parameter_onLoaded = true
  pd.parameter_onLoading = false
  ElMessage.success("载入成功。")
}
function loadParameters(){
  if(d.dataColumns.length==0){
    ElMessage.error("请先在左侧载入源样本。")
    return

  }
  switch(pd.preProcessVal){
    case pd.preProcess[2].val:
      pd.p = [{label:"均值",text:""}];break;
    case pd.preProcess[3].val:
      pd.p = [{label:"初值",text:""}];break;
    case pd.preProcess[4].val:
      pd.p = [{label:"均值",text:""},{label:"标准差",text:""}];break;
    case pd.preProcess[5].val:
      pd.p = [{label:"最小值",text:""},{label:"最大值",text:""}];break;
  }
  pd.parameter_onLoading = true
}



const QueryPreParameters = () => {
  pd.onQueryingParams = true;
}
function PREPROCESS(){
  if(!d.onLoaded){
    ElMessage.error('还没有载入样本数据。')
    return
  }
  if(d.preprocessKind==1){
    let wrongFlag = false
    if(pd.preProcessVal == pd.preProcess[0].val || pd.preProcessVal == pd.preProcess[1].val)
      for(let i=0;i<d.data.length;i++){
        for(let key in d.data[i]){
          if(d.data[i][key]==0){
            wrongFlag = true;
            break;
          }
        }
      }
    if(wrongFlag)
      ElMessageBox.confirm(
        '所选数据集含有0值，采用log初始化会导致数据异常，是否继续？',
        'Warning',
        {
          confirmButtonText: '继续',
          cancelButtonText: '取消',
          type: 'warning',
        }
      ).then(() => {
        func()
      }).catch(() => {
        return
      })
    else
      func()

    function func(){
      d.onProcessing = true
      let rowNames :any[] = []
      // 特征列数据
      let colData = Array.from({"length":d.dataColumns.length}).map((_,index)=>({
        colName:d.dataColumns[index],
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
            return data[0]
          case "min":
            return Math.min(...data)
          case "max":
            return Math.max(...data)
          case "mean":
            return (data.reduce((a,b)=>a+b,0)/data.length)
          case "std":
            let mean = data.reduce((a,b)=>a+b,0)/data.length
            return (Math.sqrt(data.reduce((a,b)=>a+(b-mean)**2,0)/data.length))
          default:
            return 0;
        }
      }
      switch(pd.preProcessVal){
        case pd.preProcess[0].val:
          rowNames = ["映射"];
          break;
        case pd.preProcess[1].val:
          rowNames = ["映射"]; break;
        case pd.preProcess[2].val:
          rowNames = ["均值"]; break;
        case pd.preProcess[3].val:
          rowNames = ["初值"]; break;
        case pd.preProcess[4].val:
          rowNames = ["均值","标准差"]; break;
        case pd.preProcess[5].val:
          rowNames = ["最小值","最大值"]; break;
        case pd.preProcess[6].val:
          rowNames = []; break;
      }
      d.preprocessParameters = JSON.parse(JSON.stringify(rowNames)) 
      .map((rowName:string,index:number)=>{
        let row:any = {parameters:rowName,obj:{}};
        switch(rowName){
          case "映射":
            for(let r = 0; r<d.dataColumns.length;r++){
              row.obj[d.dataColumns[r]] = pd.preProcessVal==pd.preProcess[0].val?"log10":"ln"
            }
            break;
          case "均值":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row.obj[d.dataColumns[r]] = calRes("mean",data)
            }
            break;
          case "初值":
            for(let r = 0; r<d.dataColumns.length;r++){
              // let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              // row[d.dataColumns[r]] = calRes("0",data)
              row.obj[d.dataColumns[r]] = d.data[0][d.dataColumns[r]]
            }
            break;
          case "标准差":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row.obj[d.dataColumns[r]] = calRes("std",data)
            }
            break;
          case "最小值":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row.obj[d.dataColumns[r]] = calRes("min",data)
            }
            break;
          case "最大值":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row.obj[d.dataColumns[r]] = calRes("max",data)
            }
            break;
        }
        return row
      })
      d.data_processed_forTable = JSON.parse(JSON.stringify(d.data)) 
      .map((val:any,index:any)=>{
        let raw = val;
        switch(pd.preProcessVal){
          //log10
          case pd.preProcess[0].val:
            for(let key in raw){
              raw[key] = Math.log10(raw[key]).toFixed(d.tofixedNum)
            }
            break;
          //loge
          case pd.preProcess[1].val:
            for(let key in raw){
              raw[key] = Math.log(raw[key]).toFixed(d.tofixedNum)
            }
            break;
          //均值和初值
          case pd.preProcess[2].val:
          case pd.preProcess[3].val:
            for(let key in raw){
              raw[key] = (raw[key]/d.preprocessParameters[0].obj[key]).toFixed(d.tofixedNum)
            }
            break;
          //Z-Score
          case pd.preProcess[4].val:
            for(let key in raw){
              raw[key] =((raw[key] - d.preprocessParameters[0].obj[key]) / d.preprocessParameters[1].obj[key]).toFixed(d.tofixedNum)
            }
            break;
          //Min-max
          case pd.preProcess[5].val:
            for(let key in raw){
              raw[key] = ((raw[key] - d.preprocessParameters[0].obj[key]) / (d.preprocessParameters[1].obj[key] - d.preprocessParameters[0].obj[key])).toFixed(d.tofixedNum)
            }
            
          break;
          //none
          case pd.preProcess[6].val:
            for(let key in raw){
              raw[key] = raw[key]
            }
          break;
        }
        return raw
      })
      
      d.dialogTableCol = Array.from({"length":d.dataColumns.length})
      .map((_,index)=>({
        prop:d.dataColumns[index],
        label:d.dataColumns[index]
      }))
      d.dialogTableData = JSON.parse(JSON.stringify(rowNames)) 
      .map((rowName:string)=>{
        let row:any = {parameters:rowName};
        switch(rowName){
          case "映射":
            for(let r = 0; r<d.dataColumns.length;r++){
              row[d.dataColumns[r]] = pd.preProcessVal==pd.preProcess[0].val?"log10":"ln"
            }
            break;
          case "均值":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row[d.dataColumns[r]] = calRes("mean",data).toFixed(4)
            }
            break;
          case "初值":
            for(let r = 0; r<d.dataColumns.length;r++){
              row[d.dataColumns[r]] = d.data[0][d.dataColumns[r]]
            }
            break;
          case "标准差":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row[d.dataColumns[r]] = calRes("std",data).toFixed(4)
            }
            break;
          case "最小值":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row[d.dataColumns[r]] = calRes("min",data).toFixed(4)
            }
            break;
          case "最大值":
            for(let r = 0; r<d.dataColumns.length;r++){
              let data = colData[colData.findIndex((item)=>item.colName==d.dataColumns[r])].val
              row[d.dataColumns[r]] = calRes("max",data).toFixed(4)
            }
            break;
        }
        return row
      }
      )

      console.log(d.dialogTableData)
      d.preProcessValNow = pd.preProcess[pd.preProcess.map((e:any) => { return e.val; }).indexOf(pd.preProcessVal)].name
      d.onProcessed = true
      d.onProcessing = false
    }
  }else if(d.preprocessKind==2){

    if(!pd.parameter_onLoaded){
      ElMessage.error('还没有载入预处理参数。')
      return
    }
    d.onProcessing = true
    let valRaw:any[] = Array.from({"length":pd.parameter_custom.length})
    for(let i = 0 ;i< pd.parameter_custom.length;i++){

      valRaw[i] = <any>{}
      for(let j = 0 ; j<d.dataColumns.length; j++){
        valRaw[i][d.dataColumns[j]] = pd.parameter_custom[i][j]
      }

    }

    console.log(valRaw)
    let temp = JSON.parse(JSON.stringify(d.data)) 
    d.data_processed_forTable = temp
    .map((val:any,index:any)=>{
      let raw = val;
      switch(pd.preProcessVal){
        //均值和初值
        case pd.preProcess[2].val:
        case pd.preProcess[3].val:
          for(let key in raw){
            raw[key] = (raw[key]/valRaw[0][key]).toFixed(d.tofixedNum)
          }
          break;
        //Z-Score
        case pd.preProcess[4].val:
          for(let key in raw){
            raw[key] =((raw[key] - valRaw[0][key]) / valRaw[1][key]).toFixed(d.tofixedNum)
          }
          break;
        //Min-max
        case pd.preProcess[5].val:
          for(let key in raw){
            raw[key] = ((raw[key] - valRaw[0][key]) / (valRaw[1][key] - valRaw[0][key])).toFixed(d.tofixedNum)
          }
          
        break;
        //none
        case pd.preProcess[6].val:
          for(let key in raw){
            raw[key] = raw[key]
          }
        break;
      }
      return raw
    })

    d.dialogTableCol = Array.from({"length":d.dataColumns.length})
    .map((_,index)=>({
      prop:d.dataColumns[index],
      label:d.dataColumns[index]
    }))
    
    let rowNames :string[] = []
    switch(pd.preProcessVal){
        case pd.preProcess[0].val:
          rowNames = ["映射"];
          break;
        case pd.preProcess[1].val:
          rowNames = ["映射"]; break;
        case pd.preProcess[2].val:
          rowNames = ["均值"]; break;
        case pd.preProcess[3].val:
          rowNames = ["初值"]; break;
        case pd.preProcess[4].val:
          rowNames = ["均值","标准差"]; break;
        case pd.preProcess[5].val:
          rowNames = ["最小值","最大值"]; break;
        case pd.preProcess[6].val:
          rowNames = []; break;
      }
    d.dialogTableData = JSON.parse(JSON.stringify(valRaw)) 
    .map((row:any,index:number)=>{
      row.parameters = rowNames[index]
      return row
    }
    )

    
    d.preProcessValNow = pd.preProcess[pd.preProcess.map((e:any) => { return e.val; }).indexOf(pd.preProcessVal)].name
    d.onProcessed = true
    d.onProcessing = false
  }





}
function DOWNLOAD(){


  let data;
  if(d.excelHasTitle)
    data = XLSX.utils.json_to_sheet(d.data_processed_forTable)//此处tableData.value为表格的数据
  else
    data = XLSX.utils.json_to_sheet(d.data_processed_forTable,{skipHeader: true,})//此处tableData.value为表格的数据
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, data, 'Sheet1')//test-data为自定义的sheet表名
  XLSX.writeFile(wb,'data_'+pd.preProcessVal+'.xlsx')

  // var wb = XLSX.utils.table_to_book(d.data_processed_forTable);
  // XLSX.writeFile(1, "123.xlsx");
}

onUnmounted(() => {
  store.state.status.menu[3].route = store.state.router.page_tool_preprocess;
})

function onBeforeMount(arg0: () => void) {
throw new Error("Function not implemented.");
}
</script>

<style lang="less" scoped>
.Page {
  width: 100%;
  height: 100%;
  background: rgb(252, 252, 252);
  position: relative;
}
.mainArea{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  max-width: 1600px;
  height: calc(100% - 62px - 50px - 50px);
  .leftCol{
    position:absolute;
    // background: rgba(0, 0, 255, 0.041);
    height: calc(100% - 40px);
    width: calc(100% - 270px - 40px - 40px);
    .leftColRow1{
      height: 50%;
      // background: rgba(187, 255, 0, 0.089);
    }
    .leftColRow2{
      height: 50%;

    }
  
  }
  .rightCol{
    position:absolute;
    right: 20px;
    // background: rgba(255, 0, 0, 0.068);
    border-left: 1px solid #dcdfe6;
    padding-left: 20px;
    height: calc(100% - 40px);
    width: 270px;
    .sliderArea{
      // background: wheat;
      position: relative;
      width: 100%;
      height: 40px;
      border-bottom: 1px solid #dcdfe650;
      .slider{
        // background: red;
        height: 100%;
        padding-left: 20px;
        width: calc(100% - 60px - 20px);
        position: absolute;
      }
      .slidertext{
        width: 40px;
        padding-left: 20px;
        position: absolute;
        height: 100%;
        right: 0;
        // background: blue;
      }
    }
  }
  .titleRow{
    /* background: blue; */
    border-bottom: 1px solid #dcdfe650;
    height: 36px;
    font-family: "SimHei";
    font-weight: bold;
    color: #4e6077;
    display: flex;
    align-items: center;
  }
  .tableRow{
    // background: blue;
    height: calc(100% - 32px - 36px - 5px);
  }
  .bottomRow{
    position: relative;
    // background: red;
    height: 32px;
  }
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
  color: rgba(0, 0, 0, 0.582);
}
</style>