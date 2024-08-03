<template>
  <div class="Page">
    <el-card class="mainArea">

        <div class="titleRow">
          <div class="subTitleRow">
            <div class="subTitleIcon"><el-icon size="25px" style="marginRight:4px"><histogram /></el-icon></div>
            <div class="subTitleLabel">已选数据集</div>
          </div>

          <div style="background: ;height: 80px;overflow: hidden;">
            <el-descriptions
              class="margin-top"
              :column="5"
              border>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><i class="iconfont">&#xec17;</i> 文件名</div>
                </template>
                <div style="font-family:Arial, Helvetica, sans-serif">
                  {{d.fileName==""?"未加载":d.fileName}}
                </div>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><i class="iconfont">&#xe87c;</i> 计数</div>
                </template>
                {{d.sampleRowCount}}
              </el-descriptions-item>

              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><i class="iconfont"> &#xe60e; </i>特征维度数</div>
                </template>
                {{d.selectXColNames.length==0?"未选择":d.selectXColNames.length}}
              </el-descriptions-item>

              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><i class="iconfont"> &#xe618; </i>标签维度数</div>
                </template>
                {{d.selectYColNames.length==0?"未选择":d.selectYColNames.length}}
              </el-descriptions-item>

              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><i class="iconfont"> &#xe615; </i> 预处理方式</div>
                </template>
                <!-- <el-tag size="small"><div style="fontSize:10px" >已处理</div></el-tag> -->
                {{d.preProcess[d.preProcess.map(function(e) { return e.val; }).indexOf(d.preProcessVal)].val}}

              </el-descriptions-item>

              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><i class="iconfont">&#xec17;</i> 文件大小</div>
                </template>
                <div style="font-family:Arial, Helvetica, sans-serif">
                  {{d.fileSize>1024 * 1024?(d.fileSize/1024/1024).toFixed(2)+" MB":(d.fileSize>1024)?(d.fileSize/1024).toFixed(2)+" kB":(d.fileSize+" Bytes")}}
                </div>
              </el-descriptions-item>

              <el-descriptions-item>
                <template #label>
                  <div class="cell-item"><el-icon> <office-building /> </el-icon> 处理状况</div>
                </template>
                <el-tag size="small" type="success"><div style="fontSize:10px" >已完成</div></el-tag>
              </el-descriptions-item>

            </el-descriptions>
          
          </div>
              
          <el-divider style="margin-bottom: 0;margin-top: 12px;"></el-divider>

          <div class="subTitleRow">
            <div class="subTitleIcon"><el-icon size="25px" style="marginRight:4px"><grid /></el-icon></div>
            <div class="subTitleLabel">卷积神经网络参数设定</div>
          </div>

        </div>
        
        <div class="scrollRow">

            <div class="scrollRowCol1">
              <div ref="tabRef" style="height:100%">
                <el-tabs class=""
                v-model="activeName"
                type="card"
                >
                  <el-tab-pane label="预设1" name="first" :style="'height:'+tableHeight+'px;background:red;min-height: 240px;'">
                    <el-table :data="networkData" stripe  style="width: 100%;height: 100%;" empty-text="尚未选择输入/输出特征。">
                      <el-table-column fixed prop="layer" label="层" width="90" />
                      <el-table-column prop="output" label="输出" width="120" />
                      <el-table-column prop="channels" label="通道"  />
                      <el-table-column prop="size" label="大小" />
                      <el-table-column prop="stride" label="步长"  />
                      <el-table-column prop="activation" label="激活函数"  />
                      <el-table-column fixed="right" prop="parameters" label="参数量"  />
                    
                    </el-table>
                  
                  </el-tab-pane>
                  <el-tab-pane label="预设2" name="second"></el-tab-pane>
                  <!-- <el-tab-pane label="预设3" name="third"></el-tab-pane> -->
              </el-tabs>
              </div>
            </div>

            <div class="scrollRowCol2">
              <div class="subTitleRow" style="margin-bottom:0;background: ;">
                <div class="subTitleLabel1">> 通用模型结构 ></div>
              </div>

              <div  style="overflow: scroll;height: calc(100% - 50px);background: ;width: 100%;">
                <el-image :src="require('@/assets/images/page_train/img4.png')" fit="" />
              </div>

            </div>

            <div class="scrollRowCol3">
              <div class="subTitleRow" style="marginBottom:0">
                  <div class="subTitleLabel1">> 设置模型参数 ></div>
              </div>
              <el-row style="background:;" align="middle">
                <div class="paraLabel" >LOSS</div>
                <el-select v-model="d.parameters.loss.val" class="m-2" placeholder="损失函数" size="large">
                  <el-option v-for="item in d.parameters.loss.scope"
                    :key="item"
                    :label="item"
                    :value="item"/>
                </el-select>
              </el-row>
              <el-row style="background:;marginTop:10px" align="middle">
                <div class="paraLabel" >optimizer</div>
                <el-select v-model="d.parameters.optimizer.val" class="m-2" placeholder="优化器" size="large">
                  <el-option v-for="item in d.parameters.optimizer.scope"
                    :key="item"
                    :label="item"
                    :value="item"/>
                </el-select>
              </el-row>
              <el-row style="background:;marginTop:10px" align="middle">
                <div class="paraLabel" >learning_rate</div>
                <el-select v-model="d.parameters.learning_rate.val" class="m-2" placeholder="学习率" size="large">
                  <el-option v-for="item in d.parameters.learning_rate.scope"
                    :key="item"
                    :label="item"
                    :value="item"/>
                </el-select>
              </el-row>
              <el-row style="background:;marginTop:10px" align="middle">
                <div class="paraLabel" >epoch</div>
                  <el-select v-model="d.parameters.epoch.val" class="m-2" placeholder="轮次" size="large">
                    <el-option v-for="item in d.parameters.epoch.scope"
                      :key="item"
                      :label="item"
                      :value="item" />
                  </el-select>
              </el-row>
              <el-row style="background:;marginTop:10px" align="middle">
                <div class="paraLabel" >batch</div>
                  <el-select v-model="d.parameters.batch_size.val" class="m-2" placeholder="批大小" size="large">
                    <el-option v-for="item in d.parameters.batch_size.scope"
                    :key="item"
                    :label="item"
                    :value="item"/>
                </el-select>
              </el-row>

            </div>

    
        </div>


      <div class="bottomRow">
        <el-button-group>
            <el-button size="large"  @click="$router.replace({path:store.state.router.page_predict_import_data})" type="primary" plain  ><el-icon class="el-icon--right" style=""><ArrowLeft /></el-icon>上一步</el-button>

            <el-button size="large"  @click="$router.replace({path:store.state.router.page_predict_export_data})" type="primary" plain >下一步<el-icon class="el-icon--right"><ArrowRight /></el-icon></el-button>
        </el-button-group>
        <el-divider direction="vertical" />
        <el-button style="color:gray" size="small" @click="pageReset()" link>重置本步骤</el-button>
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

<script lang="ts" setup>
import { ElMessage, FormInstance } from 'element-plus'
import { reactive,ref} from 'vue'
import { useRouter,useRoute } from "vue-router";
import { useStore } from 'vuex'
import { onMounted, onUnmounted } from '@vue/runtime-core';
import { httpPost } from '@/utils/global';


const $router = useRouter()
const store = useStore();


let d = reactive(store.state.train)

let networkData = ref([])
var tableHeight = ref(0)
const tabRef = ref()

let activeName = "first"


function pageReset(){
  d.parameters.loss.val = "";
  d.parameters.optimizer.val = "";
  d.parameters.learning_rate.val = "";
  d.parameters.epoch.val = "";
  d.parameters.batch_size.val = "";
}




// let networkData={isValid:false,data:''};

// let formServer =[
//         {
//             layer: 'Conv1D',
//             output: '(N,27,4)',
//             channel: '4',
//             size: '1',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },
//         {   
//             layer: 'Conv1D',
//             output: '(N,27,4)',
//             channel: '4',
//             size: '1',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },
//         {   
//             layer: 'MaxPooling1D',
//             output: '(N,13,4)',
//             channel: '-',
//             size: '-',
//             stride: '2',
//             activation: '-',
//             other: '-',
//         },{   
//             layer: 'Conv1D',
//             output: '(N,13,64)',
//             channel: '64',
//             size: '4',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },{   
//             layer: 'Conv1D',
//             output: '(N,13,64)',
//             channel: '64',
//             size: '4',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },{   
//             layer: 'MaxPooling1D',
//             output: '(N,6,64)',
//             channel: '-',
//             size: '-',
//             stride: '2',
//             activation: '-',
//             other: '-',
//         },{   
//             layer: 'Conv1D',
//             output: '(N,6,256)',
//             channel: '256',
//             size: '4',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },{   
//             layer: 'Conv1D',
//             output: '(N,6,256)',
//             channel: '256',
//             size: '4',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },{   
//             layer: 'MaxPooling1D',
//             output: '(N,3,256)',
//             channel: '-',
//             size: '-',
//             stride: '2',
//             activation: '-',
//             other: '-',
//         },{   
//             layer: 'Conv1D',
//             output: '(N,3,512)',
//             channel: '512',
//             size: '4',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },{   
//             layer: 'Conv1D',
//             output: '(N,3,512)',
//             channel: '512',
//             size: '4',
//             stride: '1',
//             activation: 'relu',
//             other: '-',
//         },{   
//             layer: 'MaxPooling1D',
//             output: '(N,1,512)',
//             channel: '-',
//             size: '-',
//             stride: '2',
//             activation: '-',
//             other: '-',
//         },{   
//             layer: 'GlobalAveragePooling1D',
//             output: '(N,512)',
//             channel: '-',
//             size: '-',
//             stride: '-',
//             activation: '-',
//             other: '-',
//         },{   
//             layer: 'Dropout',
//             output: '(N,512)',
//             channel: '-',
//             size: '-',
//             stride: '-',
//             activation: '-',
//             other: '0.3',
//         },{   
//             layer: 'Dense',
//             output: '(N,5)',
//             channel: '5',
//             size: '-',
//             stride: '-',
//             activation: 'softmax',
//             other: '-',
//         }
// ]
            
            



onMounted(()=>{
  d.step = d.onLoaded?2:0;
  if(d.selectXColNames.length!=0 && d.selectYColNames.length!=0){
    httpPost(
      store.state.server.address + "/train/layers/",
      {dimX:d.selectXColNames.length,dimY:d.selectYColNames.length},
      (res)=>{
        networkData.value = (res.layers)
      }
    )
  }

  


  tableHeight.value = tabRef.value.clientHeight - 60
  window.onresize = () => {
    return (() => {
      tableHeight.value = tabRef.value.clientHeight - 60
    })()
  }

});
onUnmounted(() => {
  window.onresize = () => {}
  store.state.status.menu[0].route = store.state.router.page_predict_settings;

  // store.state.status.menu[0].route = store.state.router.page_predict_settings
})



// let 

</script>

<style scoped lang="less">
/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
}
html,body,#app{
height: 100%;/* precious */


}
/* *{
  margin: 0;
  padding: 0;
} */
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
  height: calc(100% - 62px - 50px - 46px - 20px - 50px);
   display: block;
  max-width: 1600px;
  //  min-height: 500px;
  overflow: hidden;
  /* background-color: wheat; */
  .titleRow{
    display: block;
    // background-color: red; 
    height: 190px;
    min-width:970px;
    // border-bottom: 1px solid #dcdfe6;
    width: calc(100%);
    // position: absolute;
    overflow: hidden;
    // display: flex;
  }
  .bottomRow{
    background: white;
    border-top: 1px solid #dcdfe6;
    display: flex;
    align-items: center;
    min-width:360px;
    justify-content: center;
    width: calc(100% - 40px);
    height: 90px;
    position: absolute;
    bottom:0;
  }
  .scrollRow{
    width: calc(100% - 40px);
    position: absolute;
    height: calc(100% - 190px - 90px - 20px);
    // background-color: rgba(255, 0, 0, 0.055); 
    display: flex;
    // overflow: scroll;
    .tabs1{
      display: flex;
      height: 100%;
      background: #509cfe;
    }
    .scrollRowCol1{
      // position: absolute;
      width: calc(45% - 18px);
      min-width: 220px;
      height: 100%;
      margin-right: 25px;
      // background: red;
    }
    .scrollRowCol2{
    //   display: flex;
    //   width: 100px;
      height: 100%;
      width: calc(30% - 53px);
      padding-left: 20px;
      overflow: scroll;
      margin-right: 20PX;
    //   background: #509cfe;
      min-width: 220px;
      border-left: 1px solid #dcdfe67e;
    }
    .scrollRowCol3{
      min-width: 220px;
      width: calc(25% - 20px);
      padding-left: 20px;
      height: 100%;
      border-left: 1px solid #dcdfe67e;
      .paraLabel{
        font-size:14px;
        color:gray;
        width: 100px
      }
      .m-2{
        width: calc(100% - 100px);
      }
    }
    .table1{
        // style="background-color: red;width:100% ;height: 120%;"
        z-index: 200;
        background: red;
        width: 1000px;
        height: 100%;
        // display: flex;
        // position: absolute;
        margin-top: 50px;
        margin-left: -10px;
        left: 0;
      }
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




.excel{
  width: 100%;
  height: 100%;
  /* background: red; */
  
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
/* .el-tag{
  font-size: 11px;
} */
.excelSpanLabel{
  font-size: 13px;
}
.formula{
  background: red;
  width: 200px;
  height: 100%;
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
}.subTitleLabel1{
  margin-left: 2px;
  font-size: 15px;
  font-family:'SimHei';
  /* font-weight: bold ; */
  color: #4e6077;
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
</style>