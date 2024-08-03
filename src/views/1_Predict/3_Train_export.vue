<template>
  <div class="Page">
    <el-card class="mainArea">
      <div class="mainRow">
        <div class="Column1">
          <div class="subTitleRow">
            <div class="subTitleIcon">
              <el-icon size="25px" style="marginright: 4px"
                ><histogram
              /></el-icon>
            </div>
            <div class="subTitleLabel">训练参数</div>
          </div>
          <el-descriptions
            class="margin-top"
            :column="3"
            style="marginleft: 5px"
            border
          >
            <el-descriptions-item :width="160">
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xe87c;</i>

                  计数
                </div>
              </template>
              {{ d.sampleRowCount }}
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xec17;</i>
                  文件大小
                </div>
              </template>
              <div style="display: flex">
                <div>{{d.fileSize>1024 * 1024?(d.fileSize/1024/1024).toFixed(2)+" MB":(d.fileSize>1024)?(d.fileSize/1024).toFixed(2)+" kB":(d.fileSize+" Bytes")}}</div>
                <!-- <div style="color: #409eff; cursor: pointer">打开</div> -->
              </div>
            </el-descriptions-item>
            <el-descriptions-item :width="160">
              <template #label>
                <div class="cell-item">
                  <i class="iconfont"> &#xe615; </i>
                  预处理方式
                </div>
              </template>
              <!-- <el-tag size="small"><div style="fontSize:10px" >已处理</div></el-tag> -->
              {{d.preProcess[d.preProcess.map(function(e:any) { return e.val; }).indexOf(d.preProcessVal)].val}}
            </el-descriptions-item>
            <el-descriptions-item >
              <template #label>
                <div class="cell-item">
                  <i class="iconfont"> &#xe60e; </i>
                  特征维度
                </div>
              </template>
              {{ d.selectXColNames.length }}
            </el-descriptions-item>
            <el-descriptions-item :width="160">
              <template #label>
                <div class="cell-item">
                  <i class="iconfont"> &#xe618; </i>
                  标签维度
                </div>
              </template>
              {{ d.selectYColNames.length }}
            </el-descriptions-item>

           
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xe613;</i>
                  神经网络
                </div>
              </template>
              预设1
            </el-descriptions-item>
            <el-descriptions-item>
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xe62c;</i>
                  网络参数
                </div>
              </template>
              <el-tag class="ml-2" type="success"
                ><div style="fontsize: 10px">
                  loss = {{d.parameters.loss.val}}
                </div></el-tag
              >
              <el-tag class="ml-2" 
                ><div style="fontsize: 10px">
                  optimizer = {{d.parameters.optimizer.val}}
                </div></el-tag
              >
              <el-tag class="ml-2" 
                ><div style="fontsize: 10px">
                  lr = {{d.parameters.learning_rate.val}}
                </div></el-tag
              >
              <el-tag class="ml-2" type="warning"
                ><div style="fontsize: 10px">
                  epoch = {{d.parameters.epoch.val}}
                </div></el-tag
              >
              <el-tag class="ml-2" type="warning"
                ><div style="fontsize: 10px">
                  batchSize = {{d.parameters.batch_size.val}}
                </div></el-tag
              >
            </el-descriptions-item>
          </el-descriptions>
          <div class="btnRow">
            <el-button type="primary"
            :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
              @click="TRAIN()"
              :loading="d.onTraining">开始训练</el-button>
            <!-- <el-button
              :type="d.onTrained ? 'success' : 'info'"
              :disabled="!d.onTrained" @click="SAVE()">保存到平台</el-button> -->
            
            <el-button  @click="ABORT()" v-if="d.onTraining" style="padding: 7px;margin-left: 10px;" type="danger" plain>
              <div style="font-size: 16px;">中止训练</div></el-button>

            <el-button
            :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'

              :type="d.onTrained ? 'success' : 'info'"
              :disabled="!d.onTrained"
              @click="DOWNLOAD()">下载</el-button>
              
          </div>
        </div>
      </div>
      <div class="msgRow">
        <el-divider style="margin-top: 15px;margin-bottom: 15px;"><div style="color: gray;font-size: 16px;">训练状态</div></el-divider>
        <!-- <div class="stateStyRow">
          <div>训练状态</div>
        </div> -->
        <div class="TrainInfoArea">
          <el-scrollbar >
            <ul style="margin-left: 10px;margin-top: 8px;">
              <li style="height: 25px;font-size: 16px;color: rgba(100, 100, 100, 0.774);" v-for="item,index in d.trainingInfo" :key="index">
                {{ item }}
              </li>
            </ul>
          </el-scrollbar>
            
        </div>

      </div>

      <div class="bottomRow">
        <el-button-group style="marginleft: 20px">
          <el-button size="large" type="primary" :disabled="d.onTraining" @click="  $router.replace({path: store.state.router.page_predict_settings});" plain>
            <el-icon class="el-icon--right" style=""><ArrowLeft /></el-icon>上一步
          </el-button>
          <el-button size="large" disabled type="info" plain>下一步<el-icon class="el-icon--right"
              ><ArrowRight /></el-icon
          ></el-button>
        </el-button-group>
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
  </div>
</template>
<script setup lang="ts">
import { ref, reactive } from "vue";
import { ElMessage } from "element-plus";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { onBeforeMount, onMounted, onUnmounted } from "@vue/runtime-core";
import * as global from "@/utils/global"

const $router = useRouter();
const store = useStore();
let modelName = "";

let d = reactive(store.state.train);

// onBeforeMount(()=>{
//   console.log(d.preProcess);
// })
onMounted(() => {
  d.step = d.onLoaded?3:0;
});
onUnmounted(() => {
  store.state.status.menu[0].route = store.state.router.page_predict_export_data;
})
function test() {
  ElMessage("test");
}

function rPush(msg:string, iftime = true) {
  if (iftime) d.trainingInfo.push('['+global.getTime_hms()+'] ' + msg);
  else d.trainingInfo.push(msg);
}
function rClear() {
  d.trainingInfo = [];
}
const ABORT = ()=>{
  rPush("正在发送中止命令...",true)
  store.state.server.socket.send(JSON.stringify({type:"settings",model:"cnn",parameter:"training",parameter_val:false}))
  d.onTraining = false
  // rPush("训练已中止。",true)
}
function TRAIN() {

  if(d.data == null){
    ElMessage.error("未选择训练样本。")
    return
  }
  if(d.selectXColNames.length == 0 || d.selectYColNames.length ==0){
    ElMessage.error("未选择特征列或标签列。")
    return
  }
  if(d.parameters.loss.val == ""||d.parameters.optimizer.val == ""||d.parameters.learning_rate.val == ""||d.parameters.epoch.val == ""||d.parameters.batch_size.val == ""){
    ElMessage.error("未选择模型参数。")
    return
  }
  if(d.selectXColNames.length > 32 ){
    ElMessage.error("最多只支持32个特征维度选择。")
    return
  }
  if(d.selectYColNames.length > 16 ){
    ElMessage.error("最多只支持16个标签维度选择。")
    return
  }
  // d.onTraining = true;
  // d.onTrained = false;
  let startTime:Date;
  let finishTime:Date;

  rClear();
  rPush("准备建立连接");
  // rPush("连接成功。");
  rPush("数据预处理方式："+d.preProcessVal)
  rPush(
    "用户自定义参数:" + d.parameters.loss.val +
      "," + d.parameters.optimizer.val +
      "," + d.parameters.learning_rate.val +
      "," + d.parameters.epoch.val +
      "," + d.parameters.batch_size.val
  );
  rPush("开始训练，等待中...");
  startTime = new Date()

  


  d.onTraining = true;
  d.onTrained = false;

  rPush("无法训练模型。原因：演示版本。已提前return。",true)
  ElMessage.info("演示版本 无法进行写操作。")
  d.onTraining = false;
  return;

  store.state.server.socket.send(JSON.stringify({type:"settings",model:"cnn",parameter:"training",parameter_val:true}))
  let sendData = (()=>{
    let xData = [], yData = [];
    for(let i = 0 ; i<d.data.length ; i++){
      let row = []
      for(let j = 0 ; j<d.selectXColNames.length; j++){
        row.push(Number(d.data[i][d.selectXColNames[j]]))
      }
      xData.push(row)
      row = []
      for(let j = 0 ; j<d.selectYColNames.length; j++){
        row.push(Number(d.data[i][d.selectYColNames[j]]))
      }
      yData.push(row)
    }
    return {
      xData,
      yData,
      xColNames : d.selectXColNames,
      yColNames : d.selectYColNames,
    }
  })()


  global.httpPost(
    store.state.server.address + "/train/",
    {
      parameters:{
        loss:d.parameters.loss.val,
        optimizer:d.parameters.optimizer.val,
        learning_rate:d.parameters.learning_rate.val,
        epoch:d.parameters.epoch.val,
        batch_size:d.parameters.batch_size.val
      },preProcess:d.preProcessVal
      ,sendData,
      username:store.state.status.loginUserName,
    },
    (res)=>{
      if(res.status == "success"){
        finishTime = new Date()
        rPush('模型训练完成，用时：'+global.calTimelag(startTime,finishTime)+'。点击下载按钮存储到本地。');
        d.step = 5;
        d.modelUrl = res.url
        d.modelName = res.name
        d.onTrained = true;
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

function SAVE(){
  global.httpPost(
    store.state.server.address + "/train/save/",
    {username:store.state.status.loginUserName,filename:d.modelName},
    (res)=>{
      if(res.status==store.state.server.successResponse){
        ElMessage.success('保存成功。')
      }
      else
        ElMessage.success('保存失败。')

    }
  )
}

function DOWNLOAD() {
  ElMessage.info("下载已开始，请稍等。")
  window.location.href = store.state.server.address + d.modelUrl+"?r="+Math.random();
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

.Page {
  width: 100vw;
  height: 100vh;
  background: rgb(252, 252, 252);
  position: relative;
}
.mainArea{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  height: calc(100% - 62px - 100px - 96px + 30px);
  max-width: 1600px;
  //  min-height: 500px;
  overflow: hidden;
  display: flex;
  .bottomRow{
    //  background-color: red; 
    border-top: 1px solid #dcdfe6;
    display: flex;
    align-items: center;
    justify-content: center;
    width: calc(100% - 40px);
    height: 90px;
    position: absolute;
    bottom:0;
    background: white;
  }
  .mainRow{
    // background: wheat;
    height: 230px;
    width: calc(100% - 40px);
    display: flex;
    // overflow: scroll;
    position: absolute;
    // border-bottom: 1px solid #dcdfe6;
    .Column1{
    // background: red;
      width: 100%;
      height: 100%;
      min-width: 1100px;
      .btnRow{
        // background: green;
        height: 54px;
        display: flex;
        align-items: center;
        // justify-content: center;
      }
    }
  }
  .msgRow{
    // background: #509cfe;
    top: 234px;
    width: calc(100% - 40px);
    height: calc(100% - 254px - 90px - 20px);
    position: absolute;
    .stateStyRow {
      height: 40px;
      line-height: 40px;
      margin-left: 10px;
      color: gray;
      font-size: 16px;
    }
    // ul {
    //   padding-top: 10px;
    //   width: calc(100% - 40px);
    //   height: calc(100% - 40px - 10px);
    //   background: rgba(109, 109, 109, 0.041);
    //   overflow: auto;
    // }
    // ul li {
    //   //关闭小圆点
    //   list-style-type: none; 
    //   font-size: 16px;
    //   height:27px; 
    //   font-weight: normal;
    //   font-family: Arial, Helvetica, sans-serif ;
    //   margin-left: 12px;
    //   color: rgba(100, 100, 100, 0.774);
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
.el-tag {
  margin-right: 10px;
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
.TrainInfoArea{

  background: rgba(109, 109, 109, 0.041);
  // margin-top: 9px;
  height: calc(100% - 5px);
  width: calc(100%);
}
</style>