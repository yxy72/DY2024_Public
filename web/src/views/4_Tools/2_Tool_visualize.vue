<template>
  <div class="Page">
    <el-card class="mainArea">
      <div class="titleRow">
        <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><List /></el-icon>
        表格可视化
        <el-upload
          ref="uploadModelRef"
          style=""
          :show-file-list = "false"
          :auto-upload="false"
          :on-change="handleChange"
          accept=".xlsx"
          >
          <template #trigger>
            <el-button size="small" plain type="primary" style="margin-top: 0px;;margin-left: 8px;"><div style="font-size: 13px;">载入表格</div></el-button>
          </template>
      
        </el-upload>
      </div>

      <el-descriptions style="width: min-width: 800px;;max-width: 800px;margin-top: 10px;" border :column="4">
        <el-descriptions-item label="类别数">{{d.sampleCount}}</el-descriptions-item>
        <el-descriptions-item label="样本数">{{d.sampleLength}}</el-descriptions-item>
        <el-descriptions-item label="文件大小">{{d.sampleSize>1024 * 1024?(d.sampleSize/1024/1024).toFixed(2)+" MB":(d.sampleSize>1024)?(d.sampleSize/1024).toFixed(2)+" kB":(d.sampleSize+" Bytes")}}</el-descriptions-item>
      </el-descriptions>

      <div class="textRow" style="border-bottom: 1px solid #dcdfe650;">
        <div style="font-size: 14px;color: gray;">提示：读取方式为按列读取，即表格中的每一列为一类数据。</div>

        <!-- <el-radio-group style="margin-left: 15px;margin-top: 2px;" v-model="d.readType"  class="ml-4">
          <el-radio label="按列读取" size="small">按列读取</el-radio>
          <el-radio label="按行读取" disabled size="small">按行读取</el-radio>
        </el-radio-group> -->
        
        <div style="color: #e2e2e2;font-weight: 100;margin-left: 20px;margin-right: 20px; ">|</div>

        <!-- <div style="font-size: 14px;color: lightgray;">（请确保表格不含表头）</div> -->
        <div style="font-size: 14px;">含表头</div>
        <el-checkbox style="margin-left: 15px;margin-top: 2px;" v-model="d.hasTitle" label="是" size="large" />

      </div>
      
      <div class="chartArea" >
        <div class="chartRow">
          <div ref="chartRef" class="chart"></div>
        </div>
      </div>

      

    </el-card>
  
  </div>
</template>

<script setup lang="ts"> 
import { EChartsType } from "echarts";
import * as echarts from 'echarts';
import { ElMessage, UploadProps } from "element-plus";
import {onMounted, onUnmounted, reactive,ref } from "vue";
import { useStore } from "vuex";
import * as XLSX from "xlsx";

const store = useStore();
let d = reactive(store.state.tools.visualize);
let t = reactive(store.state.train);
let chartRef = ref()
let chart = <EChartsType>{};

onMounted(()=>{
  chart = echarts.init(chartRef.value);
})

onUnmounted(() => {
  store.state.status.menu[3].route = store.state.router.page_tool_visualize;
})
const LOAD = ()=>{

}
const handleChange: UploadProps['onChange'] = (file) => {
  let fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx" || fileType === "xls") {
      d.sampleSize = file.size
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
    let DATA :any;
    if(d.readType=="按列读取"){
        DATA = d.hasTitle?XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]):XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]],{header:1});
      

      d.sampleCount = d.hasTitle?Object.keys(DATA[0]).length:DATA[0].length
      d.sampleLength = DATA.length

      if(d.sampleCount>10){
        ElMessage.error("样本数量："+d.sampleCount+"大于10，无法导入。")
        return
      }
      let Series = Array.from({length:d.sampleCount}).map((_)=>(<any>[]))
        DATA.map((val:any,index:number)=>{
        if(d.hasTitle){
          let i = 0 ;
          for(let key in val){
            Series[i].push(val[key])
            i++;
          }
        }else{
          for(let i = 0 ;i<Series.length;i++){
              Series[i].push(val[i])
          }
        }
      })
      

      let label = []
      let ss = Series.map((val:any,index:number)=>({
        data:val,
        type:'line',
        name:!d.hasTitle?`默认类别${index+1}`:Object.keys(DATA[0])[index],
      }))
      for(let i = 0 ;i<ss.length;i++)
        label.push("默认类别"+(i+1))

      console.log(ss)
      d.option.series = ss
      d.option.legend = {data:d.hasTitle?Object.keys(DATA[0]):label}
      d.option.xAxis.data = Series[0].map((_,index:number)=>{return index+1})
    }
    // console.log(d.option)


    chart.setOption(d.option)
    


  };
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
  .chartArea{
    height: calc(100% - 50px - 140px);
    width:calc(100% - 40px);

    // background: rebeccapurple;
    padding-top: 20px;
    position: absolute;
    .chartRow{
      width: 100%;
      height: 90%;
      // background: wheat;
      .chart{
        width: 100%;
        height: 100%;
      }
    }
  }
  .textRow{
    height: 40px;
    display: flex;
    align-items: center;
  }


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