<template>
    <div class="page">
      <el-card class="mainCard">
        <div class="areaLoad">
          <div class="subTitleRow">
            <el-icon class="elicon" size="25px"><histogram/></el-icon>
            载入分类模型
            <div style="display: flex;margin-left:calc(20px);margin-top: 2px;">
              <el-upload
                :disabled="pd.onModelLoading" 
                ref="uploadModelRef"
                class="upload-demo"
                :action="store.state.server.address+'/postmodel/'"
                :show-file-list = "false"
                :auto-upload="true"
                accept=".h5"
                :headers="getHeaders()"
                :beforeUpload="handleCheck"
                :on-success="handleUploadSuccess"
                >
                <template #trigger>
                  <el-button disabled size="small" type="primary" plain><div style="font-size: 16px;">{{pd.onModelLoaded?'更改':'上传'}}</div></el-button>
                </template>
              
              </el-upload>
              <el-button @click="$router.replace({path:store.state.router.page_predict_import_data})" type="info" link style="margin-top: 0px;margin-left: 10px;">
              <div style="font-size: 14px;">在线训练</div></el-button>
            </div>

            
          </div>
          <div 
            style="border-top: 1px solid #dcdfe6;"
            v-loading="pd.onModelLoading" element-loading-text="获取数据中...">

            <el-descriptions
              :column="1"
              style="margin-left: 0px;margin-top: 0px;"
              border
              v-if="pd.onModelLoaded">
              <el-descriptions-item :width="10" v-for="(item,index) in d.modelInfo" :key="index">
                <template #label>
                  <div class="cell-item">
                    <i :class=item.icon />
                    {{item.name}}
                  </div>
                </template>
                <div style="width: 80px;">{{ item.val }}</div>
              </el-descriptions-item>
            </el-descriptions>
            <el-empty
              v-else
              :image-size="64"
              style="height: calc(100%); background: #f7f7f7"
              description="当前没有可用模型。"
            />
          <div v-if="pd.onModelLoaded" style="margin-top: 5px;width: ;background: ;display: flex;justify-content: right;align-items: center;font-size: 12px;color: gray;">优化迭代次数：
            <el-input-number style="width: 100px;" v-model="d.iterations" type="number" size="small" :min="1" :max="100"/>
          </div>

          </div>
        

        </div>



        <div class="areaSctP">

          <div class="subTitleRow" style="min-width: 400px;">
            <el-icon size="25px" class="elicon" ><histogram/></el-icon>
            载入优化参数范围
            <div style="margin-left:calc(20px);margin-top: 2px;">
              <el-upload
                :on-change="handleChange"
                :show-file-list="false"
                :auto-upload="false">
                <el-button size="small" type="primary" plain><div style="font-size: 16px;">{{d.parametersLoaded?'重新载入':'载入'}}</div></el-button>
              </el-upload>
            </div>
            <el-button @click="pd.onDialog = true;" type="info" link style="margin-top: 2px;margin-left: 10px;">
              <div style="font-size: 14px;">示例</div></el-button>
          </div>

          <el-empty
            v-if="!d.parametersLoaded"
            :image-size="100"
            style="border-top: 1px solid #dcdfe6;height: 188px;position: relative; background: #f7f7f7;margin-left: 0px;margin-top: 0px;"
            description="请载入Excel表格（.xlsx）">
          </el-empty>
          <el-auto-resizer v-else
            style="border-top: 1px solid #dcdfe6;height: 150px;position: relative; background: #f7f7f7;margin-left: 0px;margin-top: 0px;margin-bottom: 10px;"

          >
            <template #default="{ height, width }">
              <el-table-v2
                :width="width"
                :height="height"
                fixed
                :columns="d.parameters.columnNames"
                :data="d.parameters.data_Table"

                      
              >
              </el-table-v2>
            </template>
          </el-auto-resizer>
          <!-- {{ d.parameters.check?'green':'darkred' }} -->
          <div class="paraTips" v-if="d.parametersLoaded">
            大小 {{d.parameters.size>1024 * 1024?(d.parameters.size/1024/1024).toFixed(2)+" MB":(d.parameters.size>1024)?(d.parameters.size/1024).toFixed(2)+" kB":(d.parameters.size+" Bytes")}} &nbsp;
            参数 {{d.parameters.columnNames.length }}个 &nbsp;
            异常检查  &nbsp;[
            <div :style="'color:'+ (d.parameters.check?'green':'darkred') ">{{ d.parameters.tips }}</div>]
          </div>
        </div>

        <div class="areaRun">
          <el-button
              @click="OPTIMIZATION()"
              style="height: 32px;;width: 100%;"
              type="success"
              plain
              :disabled="!d.parametersLoaded || !pd.onModelLoaded ||!d.parameters.check"
              :loading="d.onOptimizing"
            >
            {{d.onOptimizing?"优化中":"开始优化"}}
          </el-button>
        </div>

        <div class="areaResult">
          <div class="subTitleRow">
            <el-icon size="25px" class="elicon" ><histogram/></el-icon>
            优化结果
          </div>
          

          <!-- <div class="infoWindow" style="right: 258px;width: 7px;border-left: 1px solid #dcdfe67c;">

          </div> -->
          <div class="infoWindow">
            <div class="TrainInfoArea">
              <el-scrollbar >
                <ul style="line-height: 1.5;margin-left: 10px;margin-top: 8px;">
                  <li style="font-size: 16px;color: rgba(100, 100, 100, 0.774);" v-for="item,index in d.info" :key="index">
                    {{ item }}
                  </li>
                </ul>
              </el-scrollbar>
            </div>
          </div>



          <el-tabs class="areaTabs" @tab-change="Table_change" v-model="d.tabsName"  id="tabsCNM" type="border-card">
            <el-tab-pane v-loading="d.onOptimizing" element-loading-text="等待优化结果..." class="Tab" :style="'height:'+pd.tabsHeight+'px'" name="1" label="结果视图">
              <div v-if="!d.onOptimized">  <el-empty description="暂无结果数据" /></div>
              
        
              <div class="areaChart">
                <div ref="chartRef" style="width: 100%;height: 100%;"></div>
              </div>
              
              <div class="areaTable">
                <div class="zhezhao"></div>
                <!-- <div style="font-weight:bolder;color: gray;display: flex;align-items: center;justify-content: center;height: 30px;"> 最优值</div> -->
                <el-auto-resizer
                  style="border-top: 1px solid #dcdfe6;height: 70px;position: relative; background: #f7f7f7;margin-left: 0px;margin-top: 0px;margin-bottom: 10px;"
                  >
                  <template #default="{ height, width }">
                    <el-table-v2
                      :width="width"
                      :height="height"
                      :header-height="40"
                      :row-height="30"
                      fixed
                      :columns="d.parameters.columnNames_res"
                      :data="d.parameters.data_Table_res"
                    >
                      
                    </el-table-v2>
                  </template>
                </el-auto-resizer>
              </div>

            </el-tab-pane>
            <el-tab-pane v-loading="d.onOptimizing||d.onComparing" element-loading-text="等待优化结果..." class="Tab" :style="'height:'+pd.tabsHeight+'px'" name="2" label="对比">
              <div v-if="!d.onOptimized">  <el-empty description="请先运行优化" /></div>
              <div v-else>
                <el-upload
                  style="position: absolute;left: 20px;top: 20px;"
                  action=""
                  :on-change="handleChange_cmp"
                  :show-file-list="false"
                  :auto-upload="false">
                  <el-button 
                  :disabled="!d.onOptimized" :style='"padding: 7px;border-radius:"+store.state.option.style.el_button_border_radius+";"' type="primary"
                    ><el-icon size="20px" style="margin-right: 4px"
                      ><folder-add /></el-icon
                    ><div style="font-size: 16px;">载入对照文件</div></el-button
                  >
              </el-upload>
                <div style="position: absolute;left: 170px;top: 26px;font-size: 14px;display: flex;"><div style="min-width:30px ;">提示</div> &nbsp;[ &nbsp;
                  <div :style="'color: '+((!d.onOptimized)?'red':d.cmpTipsColor)">{{ !d.onOptimized?"还未进行优化操作。":d.cmpTips }}</div>]
                </div>
                <div v-if="d.onCompared">
                  <div class="zhezhao2"></div>
                  <el-auto-resizer 
                    style="position: absolute; top: 150px;
                    background: #f7f7f7;
                    height: calc(100% - 160px);width: 100%;"
                    
                    v-loading="d.onComparing"

                  >
                    <template #default="{ height, width }">
          
                      <el-table-v2
                        ref="tableRef_body"
                        :width="width"
                        :height="height+45"
                        fixed
                        :header-height="45"
                        :row-height="35"
                        :row-class="rowClass_B"
                        :columns="d.cmp.data_column_table"
                        :data="d.cmp.data_table.slice(1)"
                        style="margin-top: -45px;"
                        @scroll="SCROLL_BODY"

                      > </el-table-v2>

                    </template>
                  </el-auto-resizer>
                  <el-auto-resizer 
                    style="border-top: 1px solid #dcdfe6;position: absolute; 
                    background: #f7f7f7;top: 70px;
                    height: 80px;width: 100%;"
                    
                    v-loading="d.onComparing"

                  >
                    <template #default="{ height, width }">
          
                      <el-table-v2
                        ref="tableRef_header"
                        :width="width"
                        :height="height"
                        :row-class="rowClass_H"
                        fixed
                        :header-height="45"
                        :row-height="35"
                        :columns="d.cmp.data_column_table"
                        :data="d.cmp.data_table.slice(0,1)"
                        @scroll="SCROLL_HEADER"
                      
                      > </el-table-v2>

                    </template>
                  </el-auto-resizer>
              
                </div>
                <div v-else style="background: rgba(0, 0, 0, 0.037);position: absolute;width: 100%;top: 72px;height: calc(100% - 82px)" ><el-empty description="等待数据"></el-empty></div>
              </div>
              


            </el-tab-pane>
          </el-tabs>



          <div class="areaOut">


            <el-button
              v-if="d.tabsName=='1'"
              @click="DOWNLOAD()"
              style="height: 32px;"
              type="primary"
              plain
              :disabled="!d.onOptimized"
            >下载结果
            </el-button>
            <el-button
              v-if="d.tabsName=='1'"
              style="height: 32px;"
              type="primary"
              plain
              @click="SAVEIMG()"
              :disabled="!d.onOptimized"
            >保存图片
            </el-button>

            <el-button
              v-if="d.tabsName=='2'"
              style="height: 32px;"
              type="success"
              plain
              :loading="d.onComparing"
              @click="COMPARE()"
              :disabled="!d.cmpDataChecked||d.onOptimizing"
            >运行对比
            </el-button>



          </div>





        </div>
      </el-card>
      <el-dialog
        v-model="pd.onDialog"
        append-to-body
        align-center
        width="770"
        >
        <template #header>
          <div style="margin-bottom: -20px;display: flex;">
            <div style="margin-left: 0px;font-size: 23px;margin-top: 0px;"><el-icon><Setting /></el-icon></div>
            <div style="margin-left: 4px;font-size: 20px;">参数范围文件接收说明</div>
          </div>
        </template>
        <div class="dialogRow">1. 表格的第一行：各参数的<div style="color: darkred;">参数名</div>。</div>
        <div class="dialogRow">2. 表格的第二行：各参数的<div style="color: darkred;">最小值</div>。</div>
        <div class="dialogRow">3. 表格的第三行：各参数的<div style="color: darkred;">最大值</div>。</div>
        <div class="dialogRow">请确保参数顺序与训练分类模型时的参数顺序一致。</div>
        <el-divider style="margin-top: 15px;margin-bottom: 20px;"><div style="color: gray;">示例</div></el-divider>
        <div style="display: flex;justify-content: center;flex-wrap: wrap;">
          <el-image :src="store.state.server.address+'/src/images/pages/page_optimization_samp.png'"></el-image>
        </div>
      </el-dialog>
    </div>
</template>


<script lang="ts" setup>
import * as global from '@/utils/global'
import { onBeforeMount, onMounted, onUnmounted, reactive, ref,computed } from 'vue';
import { useStore } from 'vuex';
import { ElMessage,TableV2FixedDir} from "element-plus";
import * as echarts from 'echarts';
type EChartsType = echarts.EChartsType;
const store = useStore()
import type { UploadProps,UploadInstance,TableV2Instance,RowClassNameGetter} from 'element-plus'
import * as XLSX from 'xlsx'
const uploadModelRef = ref<UploadInstance>()
const tableRef_body = ref<TableV2Instance>()
const tableRef_header = ref<TableV2Instance>()

let chartRef = ref()
let chart = <EChartsType>{};

let d = reactive(store.state.optimization);
let pd = reactive({
  onDialog:false,
  onModelLoading:false,
  onModelLoaded:false,
  tabsHeight:1,
})

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
    d.parameters.count = coName.length;
    let rowSum = 0;
    data.map((v) => {
      const obj:any = {};
      for (let i = 0; i < coName.length; i++) {
        obj[coName[i]] = v[coName[i]];
      }
      rowSum++;
      arr.push(obj);
    });
    d.parameters.rowCount = rowSum;
    d.parameters.columnNames = coName;
    d.parameters.data = arr;
    d.parametersLoaded = true;


    d.parameters.data_Table = d.parameters.data.map((val:any,rowIndex:any) => {
      val.id = rowIndex
      val.parentId = null
      return val
    })
    d.parameters.columnNames_really = d.parameters.columnNames
    d.parameters.columnNames = d.parameters.columnNames.map((val:any,index:any) => ({
      key: `${index}`,
      dataKey: `${val}`,
      title: val,
      width: 120,
    }))
    parametersCheck();
    // console.log(d.parameters.columnNames)
    // console.log(d.parameters.data)
    // console.log(d.sampleColumnNames)
  };
}
const parametersCheck = ()=>{
  if(!pd.onModelLoaded){
    d.parameters.tips = "还没有载入模型。";
    d.parameters.check = false;
    return
  }
  if(d.modelInfo[3].val!=2){
    d.parameters.tips = "单分类模型输出维度只支持为2，请载入其他模型";
    d.parameters.check = false;
    return
  }
  if(d.parameters.columnNames.length != d.modelInfo[2].val){
    d.parameters.tips = "参数个数("+d.parameters.columnNames.length+")与模型输入维度("+d.modelInfo[2].val+")不一致。";
    d.parameters.check = false;
    return
  }
  if(d.parameters.data.length!=2){
    d.parameters.tips = "行数过多或过少。";
    d.parameters.check = false;
    return
  }
  let negCol=[];
  for(let i = 0 ; i<d.parameters.columnNames.length;i++){
    if(d.parameters.data[0][d.parameters.columnNames[i]['dataKey']]<0||d.parameters.data[1][d.parameters.columnNames[i]['dataKey']]<0){
      negCol.push(d.parameters.columnNames[i]['dataKey']);
    }
  }
  if(negCol.length!=0){
    d.parameters.tips = "以下参数的最值出现了负数：["+negCol+"]";
    d.parameters.check = false;
    return
  }
  for(let i = 0 ; i<d.parameters.columnNames.length;i++){
    if(d.parameters.data[0][d.parameters.columnNames[i]['dataKey']]>d.parameters.data[1][d.parameters.columnNames[i]['dataKey']]){
      negCol.push(d.parameters.columnNames[i]['dataKey']);
    }
  }
  if(negCol.length!=0){
    d.parameters.tips = "以下参数的最小值大于最大值：["+negCol+"]";
    d.parameters.check = false;
    return
  }
  d.parameters.check = true;
  d.parameters.tips = "无异常";
}
const handleChange: UploadProps['onChange'] = (file) => {
  let fileContent;
  fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx") {
      importfile(fileContent);
      d.parameters.size = file.size
    } else {
      ElMessage.error("附件格式只支持xlsx，请重新上传！")
    }
  } else {
      ElMessage.error("请上传附件！")
  }
}
const handleChange_cmp: UploadProps['onChange'] = (file) => {
  let fileContent;
  fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx") {
      importfile_cmp(fileContent);
    } else {
      ElMessage.error("附件格式只支持xlsx，请重新上传！")
    }
  } else {
      ElMessage.error("请上传附件！")
  }
}
function importfile_cmp(obj:any) {
  d.cmpDataChecked = false
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
    const outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]],{header:1})
    let data = [...outdata];

    if(data[0].length!=d.modelInfo[2].val){
      d.cmpTips = `异常：载入数据的输入特征${data[0].length}与模型输入特征${d.modelInfo[2].val}不符。`
      d.cmpTipsColor = "darkred"
      return
      
    }
    let wrong_Flag = false
    let data_process = data.map((val:any,_)=>{
      let temp = []
      for(let i = 0;i<val.length;i++){
        let t = Number(val[i])
        if(Number.isNaN(t)||t==undefined){
          d.cmpTips = "异常：表格中存在字符串，是否包含了表头？"
          d.cmpTipsColor = "darkred"
          wrong_Flag = true;
        }
        temp.push(t)
      }
      
      return temp
    })
    if(wrong_Flag)
      return
    else
      d.cmpDataChecked = true
    // console.log(data_process)
    d.cmpTips = "载入成功，请点击下方运行按钮。"
    d.cmpTipsColor = "green"
    d.send_train = data_process
  };
}
//上传模型
var getHeaders = ()=>{return{ username:store.state.status.loginUserName,token:global.getToken(),"Model-Target":"cnn"}}
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
  pd.onModelLoading = true;
}
const handleUploadSuccess: UploadProps['onSuccess'] = (res,uploadFile) => {
  if(res.status == store.state.server.successResponse){
    ElMessage.success('模型分析成功')
    d.modelInfo[0].val = res.name.length>30?res.name.slice(0,30)+'...':res.name
    d.modelInfo[1].val = res.size
    d.modelInfo[2].val = res.in
    d.modelInfo[3].val = res.out
    pd.onModelLoaded = true
    parametersCheck();
  }else
    pd.onModelLoaded = false
  pd.onModelLoading = false;
}
const stickyIndex = ref(0)
const fixedData = computed(() =>
d.cmp.data_table.slice(0, 1)
)

function Table_change(name:string){
  if(name=="1")
    setTimeout(() => {
      chart.resize();
    }, 10);
}
function rPush(msg:string,iftime = true) {
  if (iftime) d.info.push('['+global.getTime_hms()+'] ' + msg);
}
function rClear() {
  d.info = []
}

const OPTIMIZATION = () =>{
  if(!d.parameters.check){
    ElMessage.warning("参数文件异常或与模型不匹配。")
  }
  
  ElMessage.info("演示版本 无法进行写操作。")
  return;
  d.onOptimizing = true;
  d.onOptimized = false

  d.info = [];


  
  global.httpPost(
    store.state.server.address + "/optimize/",
    {username:store.state.status.loginUserName,iterations:d.iterations, parameters:d.parameters.data},
    (res)=>{
      if(res.status == store.state.server.successResponse){



        let legend = []
        for(let i = 0 ;i<d.parameters.columnNames.length;i++){
          legend.push(d.parameters.columnNames[i]["dataKey"]);
        } 
        let min = res.maxmin[0];
        let max = res.maxmin[1];
        d.parameters.min = min;
        d.parameters.max = max;


        let data_opt = res.data;
        d.parameters.data_opt = data_opt;

        let obj_res:any = {}
        obj_res.parentId = null;
        obj_res.id = 0;
        for(let i  = 0;i<data_opt.length;i++)
          obj_res[legend[i]] = data_opt[i].toFixed(2)
        d.parameters.data_Table_res = []
        d.parameters.data_Table_res.push(obj_res)
        d.parameters.columnNames_res = d.parameters.columnNames


        d.option.legend.data = legend
        d.option.xAxis.data = legend
        d.option.series = [{
          name: 'Placeholder',
          type: 'bar',
          stack: 'Total',
          silent: true,
          itemStyle: {
            borderColor: 'transparent',
            color: 'transparent'
          },
          emphasis: {
            itemStyle: {
              borderColor: 'transparent',
              color: 'transparent'
            }
          },
          data:min
        }]
        d.option.yAxis.max = 'dataMax'
        let columnHeight = []
        for(let i =  0; i<min.length;i++){
          columnHeight.push(max[i]-min[i])
        }

        for(let i =  0; i<min.length;i++){
          let columnHeighti = []
          for(let j =  0; j<min.length;j++){
            if(j==i)
              columnHeighti.push(columnHeight[j])
            else
              columnHeighti.push('-')
          }
          let o:any = {
            name: legend[i],
            type: 'bar',
            stack: 'Total',
            label: {
              show: true,
              formatter:data_opt[i].toFixed(2),
            },
            data: columnHeighti,
            markLine: {
              symbol:'none',
              data: [[
                {
                    coord: i==0?[0, data_opt[i]]:[i-1, data_opt[i]]
                },
                {
                    coord: i==data_opt.length-1?[i, data_opt[i]]:[i+1, data_opt[i]]
                }
              ]],
            },
          }
          d.option.series.push(o)
        }

        d.onOptimized = true
        chart.setOption(d.option)
        chart.resize()
      }
      
    },
    ()=>{},
    ()=>{
      d.onOptimizing = false
    }
  )
}
function DOWNLOAD(){
  let data = d.parameters.data_Table_res
  delete data[0]['parentId']
  delete data[0]['id']
  const ws = XLSX.utils.json_to_sheet(d.parameters.data_Table_res)

  ws['!cols'] = [
    { wch: 20 },
    { wch: 20 },
    { wch: 20 },
  ]
  const wb = XLSX.utils.book_new()
  // var wsrows = [{ hidden: true }];
  // ws['!rows'] = wsrows;
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')
  XLSX.writeFile(wb, 'optimization_'+global.getTime_number()+'.xlsx')
}
const SAVEIMG =  ()=> {
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
    a.download = `参数优化结果图示.png` || "图片名称";
    // 将生成的URL设置为a.href属性
    a.href = canvas.toDataURL("image/png");
    // 触发a的单击事件
    a.dispatchEvent(new MouseEvent("click"));
    a.remove();
  };

}
const rowClass_H = ({ rowIndex }: Parameters<RowClassNameGetter<any>>[0]) => {

  return 'bg-blue-200'
}
const rowClass_B = ({ rowIndex }: Parameters<RowClassNameGetter<any>>[0]) => {
  if (rowIndex % 2 === 1) {
    return 'bg-gray-100'
  } else {
    return ''
  }
}
function SCROLL_BODY(p:any){
  tableRef_header.value?.scrollToLeft(p.scrollLeft)
}
function SCROLL_HEADER(p:any){
  tableRef_body.value?.scrollToLeft(p.scrollLeft)
}
const COMPARE = ()=>{

  rClear();
  rPush("预处理对照文件...")
  let sendData = d.send_train.map((val:any,id:Number)=>{
    let row = []
    for(let i = 0;i<val.length;i++){
      row.push(Number(val[i]-d.parameters.min[i])/(d.parameters.max[i] - d.parameters.min[i]))
    }
    return row
  })
  rPush("预处理完成。")
  d.onComparing = true;
  d.onCompared = false;
  rPush("预测对照文件中...")
  global.httpPost(
    store.state.server.address + "/predict/",
    {username:store.state.status.loginUserName,data:sendData},
    (res)=>{
      if(res.status == store.state.server.successResponse){



        rPush("预测对照文件完成。")
        rPush("预处理最优值...")
        let sendData = [d.parameters.data_opt.map((val:any,i:any)=>{
          val = (val - d.parameters.min[i])/(d.parameters.max[i] - d.parameters.min[i])
          return val
        })]
        let CMP_RES = res.result




        rPush("预测最优值中...")
        global.httpPost(
          store.state.server.address + "/predict/",
          {username:store.state.status.loginUserName,data:sendData},
          (res)=>{
            if(res.status == store.state.server.successResponse){
              let OPT_RES = res.result


              rPush("最优值预测完成。")
              rPush("整理对比...")
              let fuckAarry = OPT_RES.concat(CMP_RES)
              



              d.cmp.data_table = fuckAarry.map((val:any,id:any)=>{
                let obj:any = {}
                if(id == 0){
                  for(let i = 0;i<d.parameters.columnNames_really.length;i++){
                    obj[d.parameters.columnNames_really[i]] = Number(d.parameters.data_opt[i].toFixed(3))
                  }
                }else{
                  for(let i = 0;i<d.parameters.columnNames_really.length;i++){
                    obj[d.parameters.columnNames_really[i]] = Number(d.send_train[id-1][i].toFixed(3))
                  }
                }
                obj["概率1"] = Number(val[0].toFixed(4))
                obj["概率2"] = Number(val[1].toFixed(4))
                obj["id"] = id
                obj["parentId"] = null
                return obj
              })

              // console.log("fuck:")
              // console.log(d.parameters.data_Table)
              // console.log(d.cmp.data_table)

              d.cmp.data_column_table = Array.from({"length":Number(d.modelInfo[2].val) + 2}).map((_,index:any) => {
                let row:any = {}
                row.key = `${index}`
                row.width = 120

                if(index<d.parameters.columnNames_really.length){
                  row.dataKey = `${d.parameters.columnNames_really[index]}`
                  row.title = `${d.parameters.columnNames_really[index]}`
                }else{
                  row.dataKey = index == d.parameters.columnNames_really.length?`概率1`:`概率2`
                  row.title = index == d.parameters.columnNames_really.length?`概率1`:`概率2`
                  row.fixed = TableV2FixedDir.RIGHT

                }

                row.align = 'center'

                return row
              })
              d.onCompared = true
              rPush("整理完成。")

            }else{
              ElMessage.error("服务异常。")
              rPush("预测失败。")
            }
          },
          ()=>{},
          ()=>{
          },
        )






      }else{
        ElMessage.error("服务异常。")
        rPush("预测失败。")
      }
    },
    ()=>{},
    ()=>{
      d.onComparing = false;
    },
  )



}
onMounted(() => {
  pd.onModelLoading = true
  global.httpPost(
    store.state.server.address + "/querymodel/",
    {username:store.state.status.loginUserName, type:"cnn"},
    (res)=>{
      if(res.status == store.state.server.successResponse){
        // d.modelInfo[0].val = res.name.length>20?res.name.slice(0,20)+'...':res.name
        d.modelInfo[0].val = res.name.length>30?res.name.slice(0,30)+'...':res.name
        d.modelInfo[1].val = res.size
        d.modelInfo[2].val = res.in
        d.modelInfo[3].val = res.out
        pd.onModelLoaded = true
      }else if(res.status == store.state.server.failedResponse){
        if(res.reason == "no exist"){
          pd.onModelLoaded = false
        }
      }
      
    },
    ()=>{},
    ()=>{
      pd.onModelLoading = false
    }
  )
  chart = echarts.init(chartRef.value);
  chart.setOption(d.option)
  setTimeout(() => {
    chart.resize();
  }, 10);
  let obj = document.getElementById("tabsCNM")
  if(obj!=null)
    pd.tabsHeight = obj.offsetHeight - 46;
  window.addEventListener("resize", () => {
    if(obj!=null){
      pd.tabsHeight = obj.offsetHeight - 46;
      setTimeout(() => {
        chart.resize();
      }, 50);
    }
  });


  chart.on('legendselectchanged', function (params:any) {
    // console.log(params.selected)
    let scaleMax = 0;
    
    // key: `${index}`,
    //   dataKey: `${val}`,
    //   title: val,
    //   width: 120,

    // columnNames_res data_Table_res
    let colres = []
    let datares:any = [{}]
    datares[0].id = null;
    datares[0].parentId = null;
    // console.log("]]")
    for(let i = 0 ;i<d.parameters.columnNames_really.length;i++){
      if(params.selected[d.parameters.columnNames_really[i]]){
        if(d.parameters.max[i]>scaleMax)
          scaleMax = d.parameters.max[i]
        colres.push({key:`${i}`,dataKey:`${d.parameters.columnNames_really[i]}`,title:d.parameters.columnNames_really[i],width:120})
        datares[0][d.parameters.columnNames_really[i]] = d.parameters.data_opt[i].toFixed(2)

      }
    }

    // console.log("colres")
    // console.log(colres)
    // console.log(datares)
    d.parameters.columnNames_res = colres
    d.parameters.data_Table_res = datares
    d.option.yAxis.max = Math.ceil( scaleMax)
    chart.setOption(d.option)
    chart.resize()
  });


});
onUnmounted(() => {
  store.state.status.menu[1].route = store.state.router.page_optimization;
})
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
.subTitleRow {
  width: 100%;
  // background: rgba(102, 51, 153, 0.151); 
  height: 50px;
  display: flex;
  align-items: center;
  .elicon{
    margin-right: 4px;margin-left: 5px;color: #509cfe;
  }
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -khtml-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  // border-bottom: 1px solid #dcdfe6;
  font-size: 16px;
  font-family: "sans-serif";
  font-weight: bold;
  color: #4e6077;
}



.mainCard{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  max-width: 1600px;
  max-height: calc(1440px - 220px - 100px);
  height: calc(100% - 62px - 50px - 50px);

  .areaLoad{
    width: calc(450px - 40px);
    height: 250px;
    // background: rgba(255, 0, 0, 0.281);
    position: absolute;
    top: 20px;
    color:#4e6077
  }

  //area select parameters
  .areaSctP{
    
    width: calc((100% - 40px - 450px) - 0px);
    height: 250px;
    // background: rgba(128, 128, 128, 0.247);
    position: absolute;
    // top: calc((100% - 40px)/3 + 20px);;
    left: calc(450px + 20px);
    top: 20px;
  
    .paraTips{
      font-size: 15px;
      color: gray;
      display:flex;min-width: 600px;
    }
  }
  .areaRun{
    // background: rgba(47, 46, 46, 0.281);
    position: absolute;
    top: calc(20px + 240px);
    width: calc(100% - 40px);
    display: flex;
    justify-content:center ;
    align-items: center;
    height: 45px;
      // border-top: 1px solid #dcdfe6;
      border-bottom: 1px solid #dcdfe6;
  }
  .areaResult{
    width: calc(100% - 40px);
    // height: calc((100% - 40px)/3);
    height: calc((100% - 305px - 10px));
    // background: rgba(172, 255, 47, 0.409);
    position: absolute;
    // top: calc((100% - 40px)/3*2 + 20px);;
    top:305px;
    .subTitleRow{
      border-bottom: none;

    }
    .areaTable{
      width: calc(100%);
      // height: 70px;
      position: absolute;
      bottom: 0px;
      // background: red;
      .zhezhao{
        width: 100%;
        height: 40px;
        background: rgba(0, 0, 0, 0.04);
        position: absolute;
        bottom: 40px;
        z-index: 1000;
      }
      .eltable2H{
        background: red;
        height: 20000px;
      }
    }
    .areaTabs{
      // background: red;
      height: calc(100% - 55px - 38px);
      width: calc(100% - 268px);
      position: relative;
        // overflow: hidden;
      .Tab{
        width: calc(100% + 30px);
        // background: red;
        margin-left: -15px;
        margin-top: -15px;
        overflow: hidden;
      }
      .zhezhao2{
        width: 100%;
        height: 35px;
        background: rgba(5, 255, 1, 0.15);
        position: absolute;
        top: 115px;
        z-index: 100;
      }
    }
    .areaChart{
      width: calc(100% );
      // height: calc(100% - 55px - 40px - 100px);
      height: calc(100% - 87px);
      // background: #dcdfe629;
      position: absolute;

    }
    .areaOut{
      height: 38px;
      width: calc(100% - 267px);
      position: absolute;
      display: flex;
      align-items: center;
      justify-content: center;
      bottom: -2px;
      // background: #4e6077;
    }

    .infoWindow{
      width: 260px;
      position: absolute;
      right: 0;
      top: 50px;
      height: calc(100% - 50px);
      // background: #4e60771b;
      .TrainInfoArea{
        background: rgba(109, 109, 109, 0.041);
        // margin-top: 9px;
        height: calc(100% - 5px);
        width: calc(100%);
        }
    }
  }


}
.dialogRow{
  height: 24px;
  line-height: 24px;
  font-size: 14px;
  display: flex;
  color: rgba(0, 0, 0, 0.582);
}
.rowClassTest{
  --el-table-tr-bg-color: var(--el-color-warning-light-9);
}
</style>