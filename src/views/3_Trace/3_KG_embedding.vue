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
            <el-button size=""
              :style='"padding:7px;border-radius:"+store.state.option.style.el_button_border_radius+";"'

              type="primary" ><el-icon size="21px" style="margin-Right:4px"><folder-add /></el-icon>
              <div style="font-Size:16px">原型三元组</div>
            </el-button>
        </el-upload>
      </div>


      <div class="fixedRow">
        <el-row style="min-width: 720px;" :gutter="20" >
          <el-col :span="8" style="background:;margin-Top:0;" >
            <div class="subTitleRow" style="margin-Top:0;background:;height:40px">
              <div class="subTitleLabel" style="font-Size:14px;color:gray">> 数据统计</div>
            </div>
            <el-descriptions
              
              :column="1"
              border
            >

                
            <el-descriptions-item width="120px">
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xe613;</i>

                  <!-- <img src="../../assets/icons/1.png"/> -->
                  三元组
                </div>
              </template>
              <div v-if="!d.sampleDataOnLoaded" style="color:gray;font-Size:11px">等待加载</div>
              <div v-else>{{d.sampleTriplets.length}}</div>
            </el-descriptions-item>

            <el-descriptions-item width="120px">
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xe62f;</i>
                  实体数
                </div>
              </template>
              <div v-if="!d.sampleDataOnLoaded" style="color:gray;font-Size:11px">等待加载</div>
              <div v-else>{{d.sampleEntitis.length}}</div>
            </el-descriptions-item>

            <el-descriptions-item width="120px">
              <template #label>
                <div class="cell-item">
                  <i class="iconfont">&#xe65d;</i>
                  关系数
                </div>
              </template>
              <div v-if="!d.sampleDataOnLoaded" style="color:gray;font-Size:11px">等待加载</div>
              <div v-else>{{d.sampleEdges.length}}</div>
            </el-descriptions-item>


            </el-descriptions>



          </el-col>
          <el-divider direction="vertical" style="margin-Left:10px;height:135px;margin-Top:35px" />

          <el-col :span="14" class="excelSpanLabel">
            <el-empty v-if="!d.sampleDataOnLoaded" :image-size="100" style="height:100%;background:" description="请载入三元组表格 ( xlsx,csv )" />
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
          </el-col>
        </el-row>


        <el-row style="min-width: 720px;">
          <el-col :span="16">
            <div class="subTitleRow" style="background:">
              <div class="subTitleIcon"><el-icon size="25px" style="margin-Right:4px"><money /></el-icon></div>
              <div class="subTitleLabel">嵌入模型</div>


            </div>

            <el-row style="background:;height:50px;margin-Top:-10px;"  align="middle">
              <el-col :span="1"></el-col>
              <el-col :span="15" style="background:">
                <el-radio-group v-model="d.embedKind" >
                  <el-radio  label="TransE" style="margin:15px">
                      <div style="font-Size:15px">TransE</div>
                  </el-radio>
                  <el-radio label="TransH" style="margin:15px" >
                      <div style="font-Size:15px">TransH</div>
                  </el-radio>
                  <el-radio disabled  label="TransR" style="margin:15px">
                      <div style="font-Size:15px">TransR</div>
                  </el-radio>
                </el-radio-group>
              </el-col>
              <el-divider direction="vertical" style="margin-Right:10px" />

              <el-col :span="6" style="display:flex;align-items: center;background:"> 
                  
                <vue-latex v-if="d.embedKind=='TransE'" style="margin-Left:6px;" :expression="'\\vec h+ \\vec r=\\vec t'" display-mode />
                <vue-latex v-else-if="d.embedKind=='TransH'" style="margin-Left:6px;" :expression="'\\vec h_⊥+ \\vec r_⊥=\\vec t_⊥'" display-mode />

                <el-icon style="margin-Left:6px;color:lightgray"><question-filled /></el-icon>

              </el-col>

            </el-row>
          </el-col>

          <el-col :span="8">
            <div class="subTitleRow" style="background:">
              <div class="subTitleIcon"><el-icon size="25px" style="margin-Right:4px"><money /></el-icon></div>
              <div class="subTitleLabel">嵌入维度</div>


            </div>

            <div class="sdr">
              <div style="width:70%"  >
                <el-slider :max="50" :step="1" :min="2" v-model="d.embedDim" />
              </div>
              <div style="width:30%">
                <div style="margin-Left:16px">{{d.embedDim}}</div>
              </div>
            </div>
          </el-col>

        </el-row>
      </div>





                                              



      <div class="scrollRow">
        
        <div style="width: 100%; display: flex;
          align-items: center;
          font-family:'SimHei';
          height: 50px;
          font-weight: bold ;
          font-Size:14px;
          color:gray;
          background: ;
        ">
          <div style="width: 50%;">> 实体嵌入</div>
          <div style="width: 50%;">> 关系嵌入</div>
        </div>

        <div style="display: flex;height: calc(100% - 50px);background: ;">

          <div style=";width: calc(50% - 10px);height:100%;overflow: scroll">
            <el-empty v-if="!d.sampleDataOnCalulating" :image-size="100" style="background:;height: 100%;min-height: 360px;" description="等待嵌入结果" />
            <el-auto-resizer v-else v-loading="d.embedEntityDataOnLoading">
              <template #default="{ height, width }">
                <el-table-v2
                  :width="width"
                  :height="height"
                  fixed
                  :columns="d.embedEntityDataColumns"
                  :data="d.embedEntityData">
                </el-table-v2>
              </template>
            </el-auto-resizer>
            
          </div>


          <div style="width: calc(50% - 10px);height:100%;padding-left: 10px;margin-left: 10px;border-left: 1px solid #dcdfe690;overflow: scroll">
            <el-empty v-if="!d.sampleDataOnCalulating" :image-size="100"   style="background:;height: 100%;min-height: 360px;" description="等待嵌入结果" />
            <el-auto-resizer v-else v-loading="d.embedEdgeDataOnLoading">
              <template #default="{ height, width }">
                <el-table-v2
                  :width="width"
                  :height="height"
                  fixed
                  :columns="d.embedEdgeDataColumns"
                  :data="d.embedEdgeData">
                </el-table-v2>
              </template>
            </el-auto-resizer>
          </div>
        </div>

        
      </div>





      <div class="bottomRow">
        <el-button size='large' @click="RUN()"
          :style='"padding:7px;border-radius:"+store.state.option.style.el_button_border_radius+";"'

          type="success" plain >
          <div style="margin-Left:4px"><el-icon><video-play /></el-icon></div>
          <div style="margin-Left:4px;margin-Right:8px">Run</div>
        </el-button>

        <el-button size='large'
          :style='"heigt:223px;border-radius:"+store.state.option.style.el_button_border_radius+";"'

          :disabled='!d.sampleDataOnCalulated' :type="(!d.sampleDataOnCalulated)?'info':'primary'" plain>
          <div @click="DOWNLOAD()"  style="margin-Left:8px;margin-Right:8px">下载嵌入结果</div>
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref,reactive } from 'vue'
import { ElMessage, UploadProps } from 'element-plus'
import { useRouter } from "vue-router"
import { useStore } from 'vuex'
import { onMounted, onUnmounted } from '@vue/runtime-core'
import * as XLSX from 'xlsx'
import * as global from '@/utils/global'

const $router = useRouter()
const store = useStore();
// let pd = reactive(store.state.PageKG.embed)

let d = reactive(store.state.kg.embed)


const handleChange: UploadProps['onChange'] = (file) => {
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
    const data = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]]);
    
    if(Object.keys(data[0]).length!=3){
      ElMessage.error("样本维度："+Object.keys(data[0]).length+" 与期望维度：3不相符。")
      return
    }
    
    obj = global.getDataAndColumnsForTable(data,Object.keys(data[0]))
    d.sampleTripletCount = data.length;
    
    // console.log(data)
    // return;

    let entityGroup:string[] = []
    let relationGroup:string[] = []
    let tripletsGroup:any[] = []

    data.map((val:any,index:any)=>{
      let keys = Object.keys(val)
      tripletsGroup.push(Object.values(val))
      if(!entityGroup.includes(val[keys[0]])){
        entityGroup.push(val[keys[0]])
      }
      if(!relationGroup.includes(val[keys[1]])){
        relationGroup.push(val[keys[1]])
      }
      if(!entityGroup.includes(val[keys[2]])){
        entityGroup.push(val[keys[2]])
      }

    })

    d.sampleEntitis = entityGroup;
    d.sampleEdges = relationGroup;
    d.sampleTriplets = tripletsGroup;

    d.sampleData = data
    d.sampleDataColumns = obj.columns
    console.log(d)
    d.sampleDataOnLoaded = true
  };
}
     



onMounted(()=>{
    // tableSty.value = "width:"+document.querySelectorAll('.PagePanel_BoxCard')[0].offsetWidth+"px"
});
onUnmounted(() => {
  store.state.status.menu[2].route = store.state.router.page_kg_embed;
})
function RUN(){



  
  ElMessage.info("演示版本，无法执行计算");
  return;

  d.embedEntityDataOnLoading = true;
  d.embedEdgeDataOnLoading = true;
  d.sampleDataOnCalulating = true
  

  global.httpPost(
    store.state.server.address + "/embed/",
    {username:store.state.status.loginUserName,entities:d.sampleEntitis,edges:d.sampleEdges,triplets:d.sampleTriplets,dim:d.embedDim,kind:d.embedKind},
    (res)=>{
      if(res.status==store.state.server.successResponse){
        d.embedEntityData = res.result.EmbedE.map((val:any,index:any)=>{
          let row = <any>{}
          for(let i = 0 ; i < d.embedDim ; i++){
            row["dim"+(i+1)] = val[i]
          }
          row["实体名"] = res.result.E_label[index]
          return row
        })
        d.embedEntityDataColumns = Array.from({"length":d.embedDim + 1}).map((val:any,index:any)=>{
          let row = <any>{}
          row.key =  `${index}`;
          if(index == 0){
            row.dataKey =  "实体名";
            row.title = "实体名";
            row.width =  120;
            row.fixed = true
          }else{
            row.dataKey =  `dim${index}`;
            row.title = `dim${index}`;
            row.width =  120;
          }
          return row
        })
        d.embedEntityDataOnLoading = false;

        d.embedEdgeData = res.result.EmbedR.map((val:any,index:any)=>{
          let row = <any>{}
          for(let i = 0 ; i < d.embedDim ; i++){
            row["dim"+(i+1)] = val[i]
          }
          row["关系名"] = res.result.R_label[index]
          return row
        })
        d.embedEdgeDataColumns = Array.from({"length":d.embedDim + 1}).map((val:any,index:any)=>{
          let row = <any>{}
          row.key =  `${index}`;
          if(index == 0){
            row.dataKey =  "关系名";
            row.title = "关系名";
            row.width =  120;
            row.fixed = true
          }else{
            row.dataKey =  `dim${index}`;
            row.title = `dim${index}`;
            row.width =  120;
          }
          return row
        })
        d.embedEdgeDataOnLoading = false;
        d.sampleDataOnCalulated = true;
      }else{
        ElMessage.error("服务错误")
      }
    },
  )

}

function DOWNLOAD(){

  let ws = XLSX.utils.json_to_sheet(d.embedEntityData)
  // 设置每列的列宽，10代表10个字符，注意中文占2个字符
  ws['!cols'] = [
  ]
  // 新建book
  let wb = XLSX.utils.book_new()


  
  // 生成xlsx文件(book,sheet数据,sheet命名)
  XLSX.utils.book_append_sheet(wb, ws, '实体嵌入')
  // 写文件(book,xlsx文件名称)
  XLSX.writeFile(wb, 'embeding_entities.xlsx')


  ws = XLSX.utils.json_to_sheet(d.embedEdgeData)
  // 设置每列的列宽，10代表10个字符，注意中文占2个字符
  ws['!cols'] = [
  ]
  // 新建book
  wb = XLSX.utils.book_new()


  
  // 生成xlsx文件(book,sheet数据,sheet命名)
  XLSX.utils.book_append_sheet(wb, ws, '关系嵌入')
  // 写文件(book,xlsx文件名称)
  XLSX.writeFile(wb, 'embeding_Relations.xlsx')







}

</script>

<style scoped lang="less">
/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
}
html,body,#app{
 height: 100%;/* precious */
}*{
    margin: 0;
    padding: 0;
}
.sdr{
    /* background: red; */
    /* margin-top: -10px; */
    width: 100%;
    display: flex;
    align-items: center;

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
  height: calc(100% - 62px - 100px);
   display: block;
  max-width: 1600px;
  //  min-height: 500px;
  overflow: hidden;
  /* background-color: wheat; */
  .titleRow{
    display: block;
    // background-color: red; 
    height: 40px;
    border-bottom: 1px solid #dcdfe6;
    width: calc(100% - 40px);
    // position: absolute;
    overflow: hidden;
    // display: flex;
  }
  .bottomRow{
    //  background-color: red; 
    background: white;
    border-top: 1px solid #dcdfe6;
    display: flex;
    align-items: center;
    justify-content: center;
    width: calc(100% - 40px);
    height: 92px;
    position: absolute;
    bottom:0;
  }
  .fixedRow{
    // background: red;
    // position: absolute;
    // top: 40px;
    height: 280px;
    border-bottom: 1px solid #dcdfe6;
  }
  .scrollRow{
    position: absolute;
    width: calc(100% - 40px);
    top: calc(280px + 40px + 20px);
    height: calc(100% - 280px - 40px - 92px - 20px + 6px);
    // background-color: red; 
    // display: flex;
    overflow: scroll;
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