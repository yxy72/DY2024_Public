<template>
  <div class="Page">
    <el-card class="mainArea">
      <el-tabs type="card"  v-model="pd.tabPanel">
        <el-tab-pane label="灰色关联分析法" height='233px' name="first" class="tabplane">
          <div class="yxyRow">
            <div class="yxyCol" style="min-width: 570px;" >

              <div class="titleRow">
                <el-upload 
                  style="margin-left:10px"
                  class="upload-demo"
                  :auto-upload="false"
                  :on-change="handleChange"
                  :show-file-list="false">
                  <el-button size="large"
                  :style='"padding: 7px;border-radius:"+store.state.option.style.el_button_border_radius+";"'

                  type="primary" ><el-icon size="25px" style="margin-right:4px"><folder-add /></el-icon>上传</el-button>
                </el-upload>
              </div>
              <div class="tableRow">
                <el-empty v-if="!d.sampleDataOnLoaded" style="height: 100%;" description="请载入表格（支持xlsx、csv格式）" />
                <el-auto-resizer v-else>
                  <template #default="{ height, width }">
                    <el-table-v2
                      :width="width"
                      :height="height"
                      fixed
                      :columns="d.sampleDataColumns"
                      :data="d.sampleData">
                    </el-table-v2>
                  </template>
                </el-auto-resizer>
              </div>
              <div class="textRow">

                <div class="subTitleRow" style="border-top: 1px solid #dcdfe650">
                  <div class="subTitleLabel">> 选择计算列 ></div>
                </div>

                <el-descriptions
                  class="margin-top"
                  :column="2"
                  border>
                  <el-descriptions-item >
                    <template #label>
                      <div class="cell-item"><i class="iconfont"> &#xe71c; </i>特征</div>
                    </template>
                    <el-select
                      v-model="d.selectXColNames"
                      multiple
                      
                      collapse-tags
                      placeholder="对比列"
                      class="excelSecletLabel"
                      :collapse-tags-tooltip="true"
                      no-data-text="未加载数据"
                      size="small">
                      <el-option
                        v-for="item in d.sampleDataColumns"
                        :key="item.key"
                        :label="item.title"
                        :value="item.title"
                      />
                    </el-select>
                  </el-descriptions-item>

                  <el-descriptions-item >
                    <template #label><div class="cell-item"><i class="iconfont"> &#xe71c; </i>参照</div></template>
                    <el-select
                      v-model="d.selectYColNames"
                      multiple
                      collapse-tags
                      placeholder="参照列"
                      class="excelSecletLabel"
                      :collapse-tags-tooltip="true"
                      no-data-text="未加载数据"
                      size="small">
                      <el-option
                        v-for="item in d.sampleDataColumns"
                        :key="item.key"
                        :label="item.title"
                        :value="item.title"
                      />
                    </el-select>



                  </el-descriptions-item>
                </el-descriptions>

                <div class="subTitleRow">
                  <div class="subTitleLabel" style="margin-Top:20px">> 阈值计算方式 ></div>
                </div>
                <el-row style="background:;height:81px;margin-Top:-10px;"  align="middle">
                  
                  <div style="width: 180px;border-right: 1px solid #dcdfe6;display: flex;justify-content: center;">
                    <el-radio-group v-model="d.calMethod">
                      <el-radio size="small" label="方式1">
                        <div style="font-size:17px">方式1</div>
                      </el-radio><el-radio style="margin-left: -10px;" size="small" label="方式2">
                        <div style="font-size:17px">方式2</div>
                      </el-radio>
                    </el-radio-group>
                  </div>

                  
                  <div style="width: 50px;margin-left: 20px;color: gray;">预览</div>

                  <div style="display:flex;align-items: center;color: gray;"> 
                    <vue-latex v-if="d.calMethod=='方式1'" :expression="'\\frac{max_imax_j\\left(X_{ij}\\right)+min_imin_j\\left(X_{ij}\\right)}{2}'" display-mode />
                    <vue-latex v-else-if="d.calMethod=='方式2'" :expression="'\\frac{1}{N}\\sum_{i,j}^{}X_{ij}'" display-mode />
                    <el-icon style="margin-left:6px;color:lightgray"><question-filled /></el-icon>
                  </div>
                
                </el-row>
                <div class="subTitleRow">
                  <div class="subTitleLabel" style="margin-Top:-20px">> 灰色关联系数 ></div>
                </div>
                <div class="sdr">
                  <div class="slider-demo-block"  >
                      <el-slider :max="1" :step="0.01" v-model="d.coefficient" />
                  </div>
                  <div class="sdrFont">{{d.coefficient}}</div>
                </div>

              </div>

            </div>
            <el-divider direction="vertical"  style="height:calc(100% - 20px)" />
            <div class="yxyCol" style="min-width: 320px;" >

              <div class="subTitleRow" style="background: ;">
                <div class="subTitleLabel">> 计算结果 ></div>
                <div style="margin-left:20px;color:gray" class="subTitleLabel">R:{{d.threshold}}</div>
              </div>

              <div class="rightTableArea">
                <el-empty v-if="!d.sampleDataOnCalulated" style="height:100%;" description="等待计算系数" />
                <el-auto-resizer v-else v-loading="d.sampleDataOnCalulating">
                  <template #default="{ height, width }">
                    <el-table-v2
                      :width="width"
                      :height="height"
                      fixed
                      :columns="d.correlationDataColumns"
                      :data="d.correlationData">
                    </el-table-v2>
                  </template>
                </el-auto-resizer>
              </div>

              <div class="subTitleRow"  style="border-top: 1px solid #dcdfe66b;background: ;" >
                <div class="subTitleLabel">> 知识三元组 ></div>
                <div style="margin-left:20px;color:gray" class="subTitleLabel">总计:{{d.tripletData.length}}</div>
              </div>

              <div class="rightTableArea">
                <el-empty v-if="!d.sampleDataOnCalulated" style="height:100%;" description="等待计算系数" />
                <el-auto-resizer v-else v-loading="d.sampleDataOnCalulating">
                  <template #default="{ height, width }">
                    <el-table-v2
                      :width="width"
                      :height="height"
                      fixed
                      :columns="d.tripletDataColumns"
                      :data="d.tripletData">
                    </el-table-v2>
                  </template>
                </el-auto-resizer>
              </div>


        <div style="width:200px;height:200px;background:red;display:none" id="viz">35555555555555</div>







            </div>
          </div>
          <div class="bottomRow">
            <el-button 
              :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
              :disabled='d.onLoadToKG'
              :type="(d.onLoadToKG)?'info':'primary'"
              @click="CALCORRELATION(d.selectXColNames,d.selectYColNames,d.coefficient,d.calMethod)"  plain>计算系数</el-button>
            <!-- <el-button @click="KNOWLEDGEGRAPH(kgapi.nodes,null,pdd.dataTriple)" :disabled='!pdd.isValid' :type="(!pdd.isValid)?'info':'success'" plain>生成新图谱</el-button> -->
            <el-button
              :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'

              :disabled='d.onLoadToKG || !d.sampleDataOnCalulated'
              :type="(!d.sampleDataOnCalulated||d.onLoadToKG)?'info':'success'"
              @click="DOWNLOAD()"  plain>下载三元组</el-button>
           
            
              <el-select
                filterable
                allow-create
                v-model="d.loadNodeClassSelect"
                v-if="d.onLoadToKG"
                class="m-2"
                style="width: 120px;margin-left: 15px;margin-right: 15px;"
                placeholder="选择或输入"
            >
                <el-option
                v-for="item in d.graph.nodeClasses"
                :key="item"
                :label="item"
                :value="item"
                />
              </el-select>

            <el-button
              :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
              v-if="d.onLoadToKG"
              @click="LOAD()" type='primary' plain>
              确认
            </el-button>
            <el-button
              :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
              v-if="d.onLoadToKG"
              @click = "d.onLoadToKG = false;" type='primary' plain>
            取消
          </el-button>
          
            <el-button
              :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
              v-if="!d.onLoadToKG"
              @click="d.onLoadToKG = true" :disabled='!d.sampleDataOnCalulated' :type="(!d.sampleDataOnCalulated)?'info':'success'" plain>
              导入图谱
            </el-button>
          
            </div>
        </el-tab-pane>
        <el-tab-pane label="样本构造" name="second"  height='23px' class="tabplane"></el-tab-pane>
        <el-tab-pane label="其他" name="third" height='23px' class="tabplane"></el-tab-pane>

      </el-tabs>


    </el-card>
 <!--
    <el-dialog
      v-model="d.onLoadToKG"
      append-to-body
      align-center
      width="720"
      >
      <template #header>
        <div style="margin-bottom: -20px;display: flex;">
          <div style="margin-left: 4px;font-size: 20px;">确认操作</div>
        </div>
      </template>
      
      <div class="dialogRow2">1. 表格的不同行代表不同的样本，不同的列代表样本的特征或标签。</div>
      <div class="dialogRow2">2. 表格<div style="color: darkred;">应含</div>表头。</div>
      <el-divider style="margin-top: 15px;margin-bottom: 20px;"><div style="color: gray;">示例</div></el-divider>
      <div style="display: flex;justify-content: center;flex-wrap: wrap;">
        <el-image :src="store.state.server.address+'/src/images/pages/page_cnn_datasetSample.png'"></el-image>
        <div style="font-size: 16px;margin-top: 5px;">特征或标签列：8，样本数：9</div>
      </div> 
    </el-dialog>-->
  </div>
</template>

<script setup lang="ts">
import { ref,reactive, onUnmounted, onMounted} from 'vue'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex'
import NeoVis from 'neovis.js/dist/neovis.js';
import * as global from '@/utils/global'
import * as XLSX from 'xlsx'
import type { UploadProps} from 'element-plus'



const store = useStore();
onUnmounted(() => {
  store.state.status.menu[2].route = store.state.router.page_kg_create;
})
onMounted(()=>{
  console.log(d.onLoadToKG)
})
let pd = reactive({
  tabPanel :"first",
})
let d = reactive(store.state.kg)

let tempData = store.state.PageKG
// if(tempData.importData.isValid){
// let   pageDatas = tempData.importData
// }
// let pdd = reactive(pageDatas)
// let kgapi =  reactive(tempData.graphAPI)

const handleChange: UploadProps['onChange'] = (file) => {
  let fileContent = file.raw;
  const fileName = file.name;
  const fileType = fileName.substring(fileName.lastIndexOf(".") + 1);
  if (fileContent) {
    if (fileType === "xlsx" || fileType === "xls") {
      d.selectXColNames=[];    // string[]
      d.selectYColNames=[];
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
    const data = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
    obj = global.getDataAndColumnsForTable(data,Object.keys(data[0]))
    
    d.sampleData = obj.data
    d.sampleDataColumns = obj.columns
    d.sampleDataOnLoaded = true
  };
}




function CALCORRELATION(xCol1:string[],yCol1:string[],rho:number,kind:string){
  if(xCol1.length==0||yCol1.length==0){
    ElMessage('请选择比较列和参照列')
    return;
  }
  d.sampleDataOnCalulating = true
  let coName = d.sampleDataColumns.map((val:any)=>{
    return val.title
  })

  let xCol = [];
  for(let i = 0;i<xCol1.length;i++){
    xCol.push(coName.indexOf(xCol1[i]))
  }
  let yCol = [];
  for(let i = 0;i<yCol1.length;i++){
    yCol.push(coName.indexOf(yCol1[i]))
  }
  let data:any[] = JSON.parse(JSON.stringify(d.sampleData)).map((val:any,index:any)=>{
    let row:any[] = []
    for(let key in val){
      if(key=="id"||key=="parientId")
        continue
      else
      row.push(Number(val[key]))
    }
    return row
  })
  let nt = data
  
  // console.log(coName)
  let cha_average = [] //计算列特征均值
  let colSum = 0;
  for(let j = 0;j<coName.length;j++){
  colSum = 0;
  for(let i = 0;i<data.length;i++){
      colSum += nt[i][j]
  }
  cha_average.push(colSum/data.length)

  for(let i = 0;i<data.length;i++){
      nt[i][j] /= cha_average[j]
  }
  }
  let label_Col = <any>[];//提取y：参照列
  for(let k = 0;k<yCol.length;k++){
    label_Col.push([])
    label_Col[k] = [];
    for(let i = 0;i<data.length;i++){
      label_Col[k].push(nt[i][yCol[k]])
    }
  }
  let Character_Col = <any>[];//提取x：比较列
  for(let k = 0;k<xCol.length;k++){
    Character_Col.push([])
    Character_Col[k] = [];
    for(let i = 0;i<data.length;i++){
      Character_Col[k].push(nt[i][xCol[k]])
    }
  }
  



  let mmin=[],mmax=[];
  for(let k = 0;k<yCol.length;k++){
  mmin.push(1)
  mmax.push(0)
  }
  let hyperCol = <any>[];
  for(let k = 0;k<yCol.length;k++){
    hyperCol.push([])
    hyperCol[k]=[];
    for(let i = 0;i<data.length;i++){
      hyperCol[k].push([])
      hyperCol[k][i]=[];
      for(let j = 0;j<xCol.length;j++){
          hyperCol[k][i].push(Math.abs(Character_Col[j][i] - label_Col[k][i]))
          if(hyperCol[k][i][j]>mmax[k])
            mmax[k] = hyperCol[k][i][j]
          if(hyperCol[k][i][j]<mmin[k])
            mmin[k] = hyperCol[k][i][j]
      }
    }
  }
  let ksi = <any>[];
  for(let k = 0;k<yCol.length;k++){
    ksi.push([])
    ksi[k] = []
    for(let i = 0;i<data.length;i++){
      ksi[k].push([])
      ksi[k][i] = []
      for(let j = 0;j<xCol.length;j++){
        ksi[k][i].push((mmin[k]+rho*mmax[k])/(  hyperCol[k][i][j]+rho*mmax[k]))
      }
    }
  }
  
  let sum = [];
  for(let k = 0;k<yCol.length;k++){
    sum.push(0)
  }
  let corr = <any>[]
  for(let k = 0;k<yCol.length;k++){
    corr.push([])
    corr[k] = []
    for(let j = 0;j<xCol.length;j++){
      sum[k] = 0
      for(let i = 0;i<data.length;i++){
        sum[k] += ksi[k][i][j]
      }
      corr[k].push(sum[k]/data.length)
    }                     
  }
  
  let SUM = 0;
  let max = 0;
  let min = 1;
  for(let i = 0;i<yCol.length;i++){           
  for(let j = 0;j<xCol.length;j++){
    SUM+=corr[i][j]
    if(corr[i][j]>max)
      max = corr[i][j]
    if(corr[i][j]<min)
      min = corr[i][j]
  }
  }
  let average = SUM/(yCol.length*xCol.length)
  d.threshold = (kind=="方式1"?(max+min)/2:average)
  tempData = []
  for(let j = 0 ;j<corr[0].length;j++){//特征
    let obj = <any>{}
    obj['对象'] = coName[xCol[j]]
    for(let i = 0;i<corr.length;i++){//标签
      obj[coName[yCol[i]]]=String(corr[i][j]).slice(0, 7)
    } 
    tempData.push(obj)
  }

  d.correlationData = tempData
  d.correlationDataColumns = Object.keys(tempData[0]).map((val:any,index:any) => ({
    key: `${index}`,
    dataKey: `${val}`,
    title: val,
    width: 120,
  }))

  let tempData1 = [], edges = [];
  console.log(max)
  console.log(0.9*max)
  for(let j = 0 ;j<corr[0].length;j++){//特征
  for(let i = 0;i<corr.length;i++){//标签
    let obj = <any>{}
    let edge = (corr[i][j])>0.9*(max-d.threshold)+d.threshold?'strong_correlation':(corr[i][j])<0.9*(max-d.threshold)+d.threshold&& (corr[i][j])>d.threshold?'correlate':'non_corr'
    obj['head']=coName[xCol[j]]
    obj['relation'] = edge
    obj['tail']=coName[yCol[i]]
    edges.push(edge)
    tempData1.push(obj)
  }
  }
  d.tripletData = tempData1
  d.tripletDataColumns = Object.keys(tempData1[0]).map((val:any,index:any) => ({
    key: `${index}`,
    dataKey: `${val}`,
    title: val,
    width: 120,
  }))
  setTimeout(() => {
  d.sampleDataOnCalulated = true
  d.sampleDataOnCalulating = false
    
  }, 100);
  return


  let HEAD_ENITY = [],TAIL_ENITY = []
  for(let j = 0 ;j<xCol.length;j++)
  HEAD_ENITY.push(coName[xCol[j]])
  for(let j = 0 ;j<yCol.length;j++)
  TAIL_ENITY.push(coName[yCol[j]])
  let ALL_ENITY = []
  for (let i = 0; i < HEAD_ENITY.length; i++) 
  if (ALL_ENITY.indexOf(HEAD_ENITY[i]) == -1) 
      ALL_ENITY.push(HEAD_ENITY[i])
  for (let i = 0; i < TAIL_ENITY.length; i++) 
  if (ALL_ENITY.indexOf(TAIL_ENITY[i]) == -1) 
      ALL_ENITY.push(TAIL_ENITY[i])            
  let ALL_EDGES = []
  for (let i = 0; i < edges.length; i++)
  if (ALL_EDGES.indexOf(edges[i]) == -1) 
      ALL_EDGES.push(edges[i])          
  kgapi.nodes = ALL_ENITY,
  kgapi.edges = ALL_EDGES,
  kgapi.headE =  HEAD_ENITY,
  kgapi.tailE = TAIL_ENITY,
  store.dispatch('setData_KG_api',kgapi)
  pdd.isValid = true;
  loading = false;
}
function DOWNLOAD(){
  const ws = XLSX.utils.json_to_sheet(d.tripletData)
  ws['!cols'] = [
    { wch: 20 },
    { wch: 20 },
    { wch: 20 },
  ]
  const wb = XLSX.utils.book_new()
  var wsrows = [{ hidden: true }];
  ws['!rows'] = wsrows;
  XLSX.utils.book_append_sheet(wb, ws, 'Sheet1')
  XLSX.writeFile(wb, 'triplet.xlsx')
}

function LOAD(){
  if(d.loadNodeClassSelect==""){
    ElMessage.info("未选择目标类别。")
    return
  }
  let g = ['1','2','3','4','5','6','7','8','9','0']
  // console.log(d.loadNodeClassSelect[0])
  // console.log(typeof(d.loadNodeClassSelect[0]))
  if(g.indexOf(d.loadNodeClassSelect[0])!=-1){
    ElMessage.info("类别名首字符不能为数字。")
    return

  }

  ElMessage.info("演示版本，无法写入知识图谱");
  return;



  global.httpPost(
    store.state.server.address + "/kg/send/",
    {target:d.loadNodeClassSelect,tripletList:d.tripletData},
    (res)=>{
      if(res.status==store.state.server.successResponse){
        ElMessage.success("导入成功。")
        
        global.graphInit()
      }
      else{
        ElMessage.error("导入失败。")}
    },
    ()=>{},
    ()=>{
      d.onLoadToKG = false;
    }
  )

}



</script>

<style scoped lang="less">
/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
}
html,body,#app{
height: 100%;/* precious */
}

.slider-demo-block {
display: flex;
align-items: center;
width: 70%;
height: 40px;
}
.slider-demo-block .el-slider {
margin-top: 0;
margin-left: 12px;
}
.sdr{
  /* background: red; */
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: -10px;
}
.sdrFont{
  /* background: rebeccapurple; */
  color: rgba(0, 0, 0, 0.712);
  height: 100%;
  font-size: 18px;
  margin-left: 10px;
  width: 30px;
}


.el-tab-pane {
height: calc(100vh - 250px);
overflow-y: auto;
}
.tabplane{
  // background: wheat; 
  width: 100%;
}
.ROW{
  /* background: red; */
  width: 100%;
  height:100%;
}
.Page {
  width: 100vw;
  height: 100vh;
  background: rgb(252, 252, 252);
  position: relative;
}
.excelSecletLabel{
  width: 100%;
  height: 30px;
}
.mainArea{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  height: calc(100% - 62px - 100px);
  display: block;
  max-width: 1600px;
  //  min-height: 500px;
  overflow: hidden;
  .titleRow{
    display: block;
    // background-color: red; 
    height: 50px;
    border-bottom: 1px solid #dcdfe66b;
    width: calc(100% - 10px);
    // position: absolute;
    overflow: hidden;
    // display: flex;
  }
  .tableRow{
    height: calc(100% - 50px - 320px);
    width: 100%;
  }
  .textRow{
    // background: red;
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 320px;
    background: white;
  }
  .bottomRow{
    //  background-color: red; 
    border-top: 1px solid #dcdfe6;
    display: flex;
    align-items: center;
    justify-content: center;
    width: calc(100% );
    height: 80px;
    position: absolute;
    bottom:0;
  }
  .yxyRow{
    width: 100%;
    height:calc(100% - 80px);
    // background: wheat; 
    display: flex;
    overflow: scroll;
  }
  .yxyCol{
    overflow: hidden;
    height: 100%;
    width:50%;
    // background: blue;
    position: relative;
  }
  .rightTableArea{
    // background: yellow;
    height: calc(50% - 50px);
    width: 100%;
  }
}
.iconfont{
  font-family:"iconfont" !important;
  font-size:14px;
  font-style:normal;
  font-weight:100;
  -webkit-font-smoothing: antialiased;
  -webkit-text-stroke-width: 0.2px;
  -moz-osx-font-smoothing: grayscale;
  
}
::-webkit-scrollbar { /* 滚动条整体样式 */
width: 5px; /* 高宽分别对应横竖滚动条的尺寸 */
height: 8px;

}
::-webkit-scrollbar-thumb { /* 滚动条内滑块的样式 */
border-radius: 5px;
-webkit-box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.11);
background: #8d8d8d34;
}
.subTitleRow{
  width: 100%;
  /* background: rgba(102, 51, 153, 0.151); */
  height: 50px;
  display: flex;
  align-items: center;
}
.subTitleIcon{
  margin-left: 5px;
  color: #509cfe;
}
.subTitleLabel{
  margin-left: 2px;
  font-size: 16px;
  font-family:'SimHei';
  font-weight: bold ;
  color: #4e6077;
}
</style>