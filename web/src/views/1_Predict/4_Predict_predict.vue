<template>
  <div class="Page">
    <el-card class="PagePanel_BoxCard">
        
      <div class="rowArea1">
        <div class="rowArea1Col1">
          
          <div class="subTitleRow">
            <div class="subTitleIcon">
              <el-icon size="25px" style="margin-right: 4px"
                ><money
              /></el-icon>
            </div>
            <div class="subTitleLabel">目标模型</div>
            
            <el-upload
              :disabled="pd.modelInfoOnLoading" 
                v-if="(hasModel)"
                ref="uploadModelRef"
                class="upload-demo"
                :action="store.state.server.address+'/postmodel/'"
                :show-file-list = "false"
                :auto-upload="true"
                :headers="getHeaders()"
                :on-change="handleUploadChange"
                :beforeUpload="handleCheck"
                :on-success="handleUploadSuccess"
                accept=".h5"
                >

                <!-- :disabled="pd.modelInfoOnLoading"  -->
                <template #trigger>
                  <el-button :disabled="true"  text type="primary" style="margin-top: 0px;;margin-left: 8px;"><div style="font-size: 15px;">更改</div></el-button>
                </template>
            
              </el-upload>
          </div>
          <div style="height: clac(100% - 50px);"
            v-loading="pd.modelInfoOnLoading"
            element-loading-text="获取数据中...">
            <el-empty
              v-if="!(hasModel)"
              :image-size="64"
              style="height: calc(100%); background: #f7f7f7"
              description="当前没有可用模型。"
            >
              <div style="display: flex;margin-top: -15px;">
                <el-upload
                  ref="uploadModelRef"
                  class="upload-demo"
                  :action="store.state.server.address+'/postmodel/'"
                  :show-file-list = "false"
                  :auto-upload="true"
                  :headers="getHeaders()"
                  :on-change="handleUploadChange"
                  :beforeUpload="handleCheck"
                  :on-success="handleUploadSuccess"
                  accept=".h5"
                  >
                  <template #trigger>
                    <el-button disabled  class="littleBtn" text type="primary" style="margin-top: -15px;;">上传</el-button>
                  </template>
              
                </el-upload>




                或
                <el-button class="littleBtn" size="small" text type="primary" @click="$router.replace({path:store.state.router.page_predict_import_data})">
                  在线训练
                </el-button>
              
              </div>

            </el-empty>


            <el-descriptions
              v-else
              class="margin-top"
              :column="1"
              style="margin-left: 5px"
              border
            >
              <el-descriptions-item :width="180" v-for="(item,index) in modelInfo" :key="index">
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


          <div v-if="hasModel" style="  width: 100%;
              height: 70px;
              display: flex;
              align-items: center;
            "
          >
            <div style="
                background: #fbfbfb;
                width: 100%;
                display: flex;
                align-items: center;
                justify-content: center;
              "
            >
              <el-button
              :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'

                size="large"
                @click="RUN()"
                type="success"
                :disabled="pd.modelInfoOnLoading || d.onPredicting"
                plain
              >
                <div style="margin-left: 4px;margin-top: 3px;;">
                  <el-icon><video-play /></el-icon>
                </div>
                <div style="margin-left: 4px; margin-right: 8px">Run</div>
              </el-button>
            </div>
          </div>
        </div>
        <div class="rowArea1Col2">
          <div class="subTitleRow">
            <div class="subTitleIcon">
              <el-icon size="25px" style="margin-right: 4px"><List /></el-icon>
            </div>
            <div class="subTitleLabel">特征数据</div>

            <el-upload
              v-if="d.onLoaded"
              style=" margin-top: 0px; margin-left: 0px"
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :show-file-list="false"
              :auto-upload="false"
            >
              <el-button plain size="small" text type="primary"
                ><div style="font-size: 15px">重载</div></el-button
              >
            </el-upload>

          </div>
          <el-divider style="margin-bottom: 12px; margin-top: 0" />
          
          <div class="tableRow">
            <el-empty
            v-if="!d.onLoaded"
            :image-size="100"
            style="background: #fbfbfb; height: 205px"
            description="无数据"
          >
            <el-upload
              style="margin-left: 10px; margin-top: -40px; margin-left: 80px"
              class="upload-demo"
              action=""
              :on-change="handleChange"
              :show-file-list="false"
              :auto-upload="false"
            >
              <el-button class="littleBtn" style="margin-left: 10px;" plain size="small" text type="primary"
                >载入</el-button
              >
            </el-upload>
            </el-empty>
            
            <el-auto-resizer v-else>
                <template #default="{ height, width }">
                  <el-table-v2
                    :width="width"
                    :height="height"
                    fixed
                    :columns="d.sampleColumnNames_forTable"
                    :data="d.data_forTable"
                  >

                  </el-table-v2>
                </template>

            </el-auto-resizer>

          </div>
        </div>
      </div>
      
      <el-divider style="width: calc(100vw - 220px - 100px - 40px);max-width: 1560px;margin-bottom: 3px; margin-top: 0" />

      <div class="rowArea2">
        <div class="subTitleRow">
          <div class="subTitleIcon">
            <el-icon size="25px" style="margin-right: 4px"
              ><histogram
            /></el-icon>
          </div>
          <div class="subTitleLabel">预测结果</div>
        </div>
      <div class="predictResArea"
        v-loading="d.onPredicting"
        element-loading-text="获取数据中..."
      >
        <el-empty v-if="!d.onPredicted"
          :image-size="100"
          style="background:#fbfbfb;width: 100%; height:100% "
          description="等待加载...">
        </el-empty>

        
        <div class="predictResAreaRow" v-else>

          <div class="predictResAreaRow1">
            <el-auto-resizer >
              <template #default="{ height, width }">
                <el-table-v2
                  class="headerClass"
                  :width="width"
                  :height="height"
                  fixed
                  :columns="d.predictColumnNames_forTable"
                  :data="d.predict_data_forTable"
                ></el-table-v2>
              </template>
            </el-auto-resizer>
          </div>

          <div class="predictResAreaRow2">
            <el-button plain @click="reflect()" type="success">
              <div style="margin-left: 4px; margin-right: 8px">映射列名</div>
            </el-button>
            <el-button @click="DOWNLOAD()" type="success">
              <div style="margin-left: 4px; margin-right: 8px">下载</div>
            </el-button>
          </div>
        </div>

      </div>
      </div>


    </el-card>
    <el-dialog
      v-model="pd.onReflecting"
      append-to-body
      align-center
      >
      <template #header>
        <div style="margin-bottom: -20px;display: flex;">
          <div style="margin-left: 0px;font-size: 23px;margin-top: 0px;"><el-icon><Setting /></el-icon></div>
          <div style="margin-left: 4px;font-size: 20px;">列名映射</div>
        </div>
      </template>
      <div class="dialogRow2">将各所属类别和指定标签进行对应。</div>


      <el-row style="height: 30px;margin-top: 10px;">
        <el-col :span="3">
          <div style="line-height: 30px;height: 30px;">映射值</div>
        </el-col>
        <el-col :span="20">
          <el-input
            v-model="pd.Reflection_custom"
            :placeholder="getPlaceholder()"
        />
        </el-col>
      </el-row>

      <div style="display: flex;justify-content: center;margin-top: 15px;">
      <el-button type="primary" @click="checkReflection()" >
        确认
      </el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive,watch  } from "vue";
import { ElMessage, genFileId, UploadInstance, UploadProps, UploadRawFile,TableV2FixedDir } from "element-plus";
import { useRouter,useRoute } from "vue-router";
import { useStore } from "vuex";
import { onMounted, onUnmounted } from "@vue/runtime-core";
import * as global from "@/utils/global"
import * as XLSX from "xlsx";
import { tr } from "element-plus/es/locale";

let calReady = ref(false);
const $router = useRouter();
const store = useStore();
const route = useRoute();

const uploadModelRef = ref<UploadInstance>()

var getHeaders = ()=>{return{ username:store.state.status.loginUserName,token:global.getToken(),"Model-Target":"cnn"}}

let pd = reactive({
  onReflecting:false,
  Reflection_columnName:[],
  Reflection_custom: "",
  modelInfoOnLoading:true,
})
let d = reactive(store.state.train.predict)

let hasModel = ref(false);
let hasAutoData = ref(false);
let modelInfo = reactive([
  {name:"模型名",   icon:"iconfont icon-24gl-tags2",val:""},
  {name:"大小",     icon:"iconfont icon-shiti1",val:""},
  {name:"输入维度", icon:"iconfont icon-shuchu2",val:""},
  {name:"输出维度", icon:"iconfont icon-shuchu2",val:""},
])



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
const handleExceed: UploadProps['onExceed'] = (files) => {
  uploadModelRef.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  uploadModelRef.value!.handleStart(file)
}
const handleUploadChange: UploadProps['onChange'] = (uploadFile,uploadFiles) => {
  let file = uploadFile.raw
  if(file== null)
    return
  // const fileSuffix = file.name.substring(file.name.lastIndexOf(".") + 1);
  // const whiteList = ["h5"];
  // if (whiteList.indexOf(fileSuffix) === -1) {
  //   ElMessage.error('只支持.h5模型。');
  //   return false;
  // }

}
const handleUploadSuccess: UploadProps['onSuccess'] = (response,uploadFile) => {
  if(response.status == store.state.server.successResponse){
    ElMessage.success('模型分析成功')
    modelInfo[0].val = response.name.length>20?response.name.slice(0,20)+'...':response.name
    modelInfo[1].val = response.size
    modelInfo[2].val = response.in
    modelInfo[3].val = response.out
    hasModel.value = true
  }
    pd.modelInfoOnLoading = false
}




onMounted(() => {
  global.httpPost(
    store.state.server.address + "/querymodel/",
    {username:store.state.status.loginUserName, type:"cnn"},
    (res)=>{
      if(res.status == store.state.server.successResponse){
        modelInfo[0].val = res.name.length>20?res.name.slice(0,20)+'...':res.name
        modelInfo[1].val = res.size
        modelInfo[2].val = res.in
        modelInfo[3].val = res.out
        hasModel.value = true
      }else if(res.status == store.state.server.failedResponse){
        if(res.reason == "no exist"){
          hasModel.value = false
        }
      }
      
      pd.modelInfoOnLoading = false
    },
  )
  const stop = watch([()=>hasModel.value,()=>hasAutoData.value],([newV,oldV],[newV1,oldV1])=>{
    if(hasModel.value && hasAutoData.value){
      RUN()
      stop()
    }
  })
  if(route.query.load!=null ){
    if(route.query.load!="true")
      return;




      global.httpPost(
        store.state.server.address + "/predict/data/",
        {type:"get"},
        (res)=>{
          if(res.status == store.state.server.successResponse){
            console.log(res.data)
            if(res.data.length==0){
              ElMessage.warning("自动拉取的数据为空。")
              return
            }

            try{
              data = res.data;

              const arr:any = [];
              let coName = Object.keys(data[0]);
              d.sampleColumnCount = coName.length;
              let rowSum = 0;
              data.map((v:any) => {
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

              d.onPredicted = false

              d.data_forTable = d.data.map((val:any,rowIndex:any) => {
                val.id = rowIndex
                val.parentId = null
                return val
              })

              let props:any;
              d.sampleColumnNames_forTable = d.sampleColumnNames.map((val:any,index:any) => ({
                ...props,
                key: `${index}`,
                dataKey: `${val}`,
                title: val,
                width: 150,
              }))
            }catch(e){
              ElMessage.warning("自动拉取的数据存在错误。")
            }
            hasAutoData.value = true;
          }
        },
      )






      
  }
});
onUnmounted(() => {
  store.state.status.menu[0].route = store.state.router.page_predict_predict;
})
function test() {
  pd;
  ElMessage("load");
  $router.replace({
    // path:'/Predict/Train/network'
  });
}
let fileContent;
let data;
function handleChange(file:any) {
  fileContent = file.raw;
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
    const outdata = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
    data = [...outdata];


    // console.log(data)

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

    d.onPredicted = false

    d.data_forTable = d.data.map((val:any,rowIndex:any) => {
      val.id = rowIndex
      val.parentId = null
      return val
    })
    
    let props:any;
    d.sampleColumnNames_forTable = d.sampleColumnNames.map((val:any,index:any) => ({
      ...props,
      key: `${index}`,
      dataKey: `${val}`,
      title: val,
      width: 150,
    }))


    // console.log(d.sampleColumnNames)
    // console.log(d)
    // console.log(d.sampleColumnNames)
  };
}
function RUN() {
  if(!d.onLoaded){
    ElMessage.error("未载入样本。")
    return
  }
  if(d.sampleColumnNames.length != modelInfo[2].val){
    ElMessage.error("样本的输入维度："+d.sampleColumnNames.length+"，与模型的输入维度："+modelInfo[2].val+" 不匹配。")
    return
  }


  ElMessage.info("演示版本 无法进行写操作。")
  return;


  let sendData = (()=>{
    let Data = [];
    for(let i = 0 ; i<d.data.length ; i++){
      let row = []
      for(let j = 0 ; j<d.sampleColumnNames.length; j++){
        row.push(Number(d.data[i][d.sampleColumnNames[j]]))
      }
      Data.push(row)
    }
    return Data
  })()
  d.onPredicting = true
  global.httpPost(
    store.state.server.address + "/predict/",
    {username:store.state.status.loginUserName,data:sendData},
    (res)=>{
      if(res.status == store.state.server.successResponse){
        // console.log(res.result)
        d.predict_data_forTable = 
          res.result.map((val:any,index:any) => {
            let row = <any>{}
              row.id = index
              row.parentId = null
              row["0"] = index+1
              row[String(val.length+1)] = Math.max(...val).toFixed(4)
              row[String(val.length+2)] = "类别"+(val.indexOf(Math.max(...val))+1)
              for(let i = 0 ; i < val.length ; i++){
                row[String(i+1)] = val[i].toFixed(4)
              }
            return row
          })
        
        d.predictColumnNames_forTable = 
          Array.from({"length":Number(modelInfo[3].val) + 1 + 2}).map((_,index:any) =>
          {
            let row = <any>{};
            row.key = `${index}`;
            row.dataKey = String(index);
            if(index==0){
              row.title = "样本序号"
              row.fixed = TableV2FixedDir.LEFT
              row.width = 100;
            }
            else if(index==Number(modelInfo[3].val)+1){
              row.fixed = TableV2FixedDir.RIGHT
              row.width = 150
              row.title = "最大值"
            } else if(index==Number(modelInfo[3].val)+2){
              row.fixed = TableV2FixedDir.RIGHT
              row.width = 150
              row.title = "预测标签"
            } else{
              row.title = "类别"+index
              row.width = 150
            }
            
            row.align = 'center'

            return row;
          })

        d.onPredicted = true

      }else{
        ElMessage.error("服务异常。")
      }
    },
    ()=>{},
    ()=>{
      d.onPredicting = false
    },
  )



    // console.log(sendData)

  // let obj = {};
  // obj.modelUrl = "model20220428220455.h5";
  // obj.inputDim = 27;
  // obj.inputData = [];

  // let coName = Object.keys(pd.data[0]);
  // for (let i = 0; i < pd.data.length; i++) {
  //   obj.inputData.push([]);
  //   obj.inputData[i] = [];
  //   for (let j = 0; j < obj.inputDim; j++) {
  //     obj.inputData[i].push(pd.data[i][coName[j]]);
  //   }
  // }
  // axios
  //   .get("http://127.0.0.1:8001/predict?obj=" + JSON.stringify(obj))
  //   .then(function (res) {
  //     console.log(res.data);
  //     let obj = JSON.parse(JSON.stringify(res.data));
  //     let finalData = [];
  //     let row = {};
  //     let max = 0;
  //     for (let i = 0; i < obj.resPred.length; i++) {
  //       row = {};
  //       row["sort"] = i + 1;
  //       max = 0;
  //       for (let j = 0; j < obj.resPred[0].length; j++) {
  //         row[pd.predictColumnName[j]] = obj.resPred[i][j].toFixed(6);
  //         max = obj.resPred[i][j] > max ? obj.resPred[i][j] : max;
  //       }
  //       row["max"] = max.toFixed(6);
  //       row["res"] = pd.predictColumnName[obj.resClass[i]];
  //       finalData.push(row);
  //     }
  //     pd.dataPredict = JSON.parse(JSON.stringify(finalData));
  //     pd.excelHasPredict = true;
  //     calReady.value = true;
  //   });
}
function DOWNLOAD(){
  let temp = JSON.parse(JSON.stringify(d.predict_data_forTable))
  temp = temp.map((val:any,index:any)=>{
    delete val.id
    delete val.parentId
    return val
  })

  temp = temp.map((val:any,index:any)=>{

    val["样本序号"] = val[0]
    for(let i = 0; i < pd.Reflection_columnName.length; i++){
      let temp:string = val[i+1] 
      delete val[i+1]
      val[String(pd.Reflection_columnName[i])] = temp
    }
    val["最大值"] = val[Number(modelInfo[3].val)+1]
    val["预测标签"] = val[Number(modelInfo[3].val)+2]
    delete val[0]
    delete val[Number(modelInfo[3].val)+1]
    delete val[Number(modelInfo[3].val)+2]
    

    return val
  })



  const data = XLSX.utils.json_to_sheet(temp)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, data, 'Sheet1')
  XLSX.writeFile(wb,'data_predict.xlsx')
  ElMessage.success("导出成功。")
}
function reflect(){
  pd.onReflecting = true
}
function checkReflection(){
  try{
    pd.Reflection_columnName = JSON.parse(pd.Reflection_custom)
  }catch(error){
    ElMessage.error("输入格式有误。")
    return
  }
  
  if(pd.Reflection_columnName.length != Number(modelInfo[3].val)){
    ElMessage.error("映射类别数："+pd.Reflection_columnName.length+" 与输出维度数："+Number(modelInfo[3].val)+"不匹配。")
    return
  }


  d.predict_data_forTable = 
    d.predict_data_forTable.map((val:any,index:any) => {
      // console.log(val)
      // console.log(Number(modelInfo[3].val)+2)
      // console.log(val[Number(modelInfo[3].val)+2])
      let max = Number(val[(Number(modelInfo[3].val)+1)])
      let group = []
      for(let key in val){
        if(key=="0"||key==String(Number(modelInfo[3].val)+1)||key == String(Number(modelInfo[3].val)+1))
          continue
        group.push(Number(val[key]))
      }
      let id = group.indexOf(max)
      val[(Number(modelInfo[3].val)+2)] = pd.Reflection_columnName[id]
      return val
    })

  d.predictColumnNames_forTable = 
    d.predictColumnNames_forTable.map((val:any,index:any) =>
    {
      if(index==0||index==Number(modelInfo[3].val)+1||index==Number(modelInfo[3].val)+2)
        return val
      else
        val.title = pd.Reflection_columnName[index-1]
      return val;
    })
  pd.onReflecting = false
  ElMessage.success("映射成功。")
}
function getPlaceholder(){
  return '请输入'+modelInfo[3].val+'个维度对应的列名，格式：["name1","name2","name3",...]'
}
</script>
<style scoped lang="less">
/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
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
}
.rowArea1{
  /* background: yellow; */
  height: 282px;
  width: 100%;
  display: flex;
}
.rowArea1Col1{
  min-width: 360px;
  /* background: yellow; */
}
.rowArea1Col2{
  margin-left: 27px;
  /* width: 100%; */
  width:  calc(100% - 27px);
  // background: pink; 
  height: 100%;
  .tableRow{
    background-color: yellow;
    height: calc(100% - 50px - 30px);
    display: block;
    min-height: 120px;
  }
  
}
.rowArea2{
  /* background: blue; */
  height: calc(100% - 282px);
  
}
.predictResArea{
  width: 100%;
  height:calc(100% - 50px);
  /* min-height: 400px; */
  overflow: scroll;
  .headerClass{
    font-size: 15px;
  }
  .predictResAreaRow{
    height: 100%;
    .predictResAreaRow1{
      height: calc(100% - 60px);
      background: #509bfe18;
    }
    .predictResAreaRow2{
      width: calc(100%);
      height: 60px;
      background: #1ffa020e;
      border-radius: 5px;
      display: flex;
      align-items: center;
      justify-content: center;
    }

  }
}
.PagePanel_BoxCard {

  
  position: absolute;
  top: calc(62px + 50px);
  left: calc(220px + 50px);

  height: calc(100% - 100px - 62px);
  width: calc(100% - 100px - 220px);
  
  //  background: gray; 
  display:flex;
  max-width: 1600px;
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
</style>