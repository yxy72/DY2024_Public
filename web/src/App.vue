<template>
  <div class="Page">
    <!-- <div style="background: red; width: 583px; left: 200px; height: 200px; z-index: 2000; position: absolute;">1</div> -->
    <div v-if="store.state.option.style.navigateBar && store.state.status.login" ref="titleAreaRef" class="PagePanel_Title">
      <div class="menuArea">
        <el-menu
          :default-active="menuTitleActive($router.currentRoute.value.path)"
          
          mode="horizontal"
          background-color="#252525"
          text-color="#838483"
          active-text-color="#f3ffff"
          
        >
          <el-menu-item style="" v-for="(item,index) in mainMenuTable" :key="index" @click="$router.replace({path:mainMenuTable[index].route})" :index="item.id" >
            {{ item.label }}
          </el-menu-item>
        </el-menu>
      </div>
      <div class="leftArea" v-if="pd.titleLeftAreaVisibile" style="color: white">
        <div class="searchTtile">
          <el-icon><search /></el-icon>
          <el-divider direction="vertical" style="" />
          <!-- <div style="color: gray; font-size: 14px; font-style: italic">
            搜索内容
          </div> -->
          <!-- <el-input class="search_input_area" clearable v-model="serachInput" placeholder="搜索内容" /> -->
          <el-autocomplete
            v-model="searchInput"
            :fetch-suggestions="querySearch"
            :trigger-on-focus="false"
            clearable
            class="search_input_area"
            placeholder="搜索内容"
            @select="onSearchSelect"
          />
        
        </div>
      </div>
      <div class="rightArea" v-if="pd.titleRightAreaVisivle">

        <el-tooltip  style="font-size: 12px;" placement="bottom" effect="light">
          <template #content> {{store.state.status.loginUserName}}</template>
          <el-avatar
          shape="square"
          :size="24"
          :src="store.state.server.address + store.state.status.loginUserAvatarUrl"
          @click="$router.replace({ path: store.state.router.page_config_user });"
          style="cursor: pointer;"
        />
        </el-tooltip>
        
        <el-divider direction="vertical" />
        <el-button link @click="onLogout()"
          ><div style="color: white; font-size: 13px; color: lightgray">
            退出
          </div></el-button
        >
        <el-button disabled link
          ><div style="color: white; font-size: 13px; color: lightgray">
            帮助
          </div></el-button
        >
        <el-button disabled link @click="$router.replace({path:store.state.router.page_test})"
          ><div style="color: white; font-size: 13px; color: lightgray">
            关于
          </div></el-button
        >
        <el-button
          type="primary"
          style="padding: 5px; height: 30px"
          size="small"
          @click="$router.replace({ path: store.state.router.page_start });"
          ><div style="color: white; font-size: 13px; padding: 5px">
            快速开始
          </div></el-button
        >
      </div>
    </div>


  
    <div v-if="store.state.option.style.navigateBar && store.state.status.login&&!store.state.status.inStartPage" class="PagePanel_Sidebar">

      <div class="PagePanel_Sidebar_Area">

        <template v-for="(item,index) in subMenuTable" :key="index">
          <el-menu v-if="calsubMenuTableVisible(index)" :default-active="$router.currentRoute.value.path"  router>
          
            <el-sub-menu v-for="(subitem,index) in item.subItem" :key="index" :index="subitem.index">
              <template #title>
                <el-icon><component :is="subitem.icon"></component></el-icon>
                <span>{{subitem.name}}</span>
              </template>
              <el-menu-item v-for="(menuitem,index) in subitem.menuItem" :key="index" :index="menuitem.route">
                <div class="subitem">{{menuitem.name}}</div>
              </el-menu-item>
            </el-sub-menu>

            <el-menu-item v-for="(menuitem,index) in item.Item" :key="index" :index="menuitem.route">
              <el-icon><component :is="menuitem.icon"></component></el-icon>
              <span>{{menuitem.name}}</span>
            </el-menu-item>

          </el-menu>
        </template>
       
        <div class="sideline"></div>
      </div>


    </div>


    <div v-loading.fullscreen.lock="store.state.status.loginLoading"></div>
    <div class="devTest" style="display:none ;">
      <el-button type="primary" @click="devFunc">测试</el-button>  

     
    </div>              

    <div class="PageRouterViewPanel" >
      <div style="position: absolute;right:70px;font-size: 200px;z-index: 233;">
      <el-button v-if="false" @click="changeStyle()" style="color: rgba(0, 0, 0, 0.075);background-color: rgba(0, 0, 0, 0.014);border: none;">切换样式</el-button>
      </div>
    <!-- <div class="PageRouterViewPanel"> -->
      <router-view ></router-view>
    </div>



    <div class="devTest" style="display:none ;">
      <div>{{ (B()) }}</div>
      <button @click="devFunc()">测试</button>
    </div>

  </div>
</template>

<script lang="ts" setup>

import { ElMessage, FormInstance } from 'element-plus';
import * as global from '@/utils/global'

import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { reactive,ref } from "vue";
import { onBeforeMount, onMounted, onUnmounted } from "@vue/runtime-core";


const $router = useRouter();
const store = useStore();
const titleAreaRef = ref()
let userinfo = reactive(store.state.status)
let pd = reactive({
  titleLeftAreaVisibile:true,
  titleRightAreaVisivle:true,

})

let c = ref(1);
function B(){
  return c.value
}
let r = false;
const changeStyle = ()=>{
  if(r){
    r = false
    store.state.option.style.el_descriptions_label_background_color = 'white'
    store.state.option.style.el_button_border_radius = 0

  }else{
    r = true
    store.state.option.style.el_descriptions_label_background_color = '#f5f7fa'
    store.state.option.style.el_button_border_radius = "6px"
  }
}

global.SYS_Init() 


// 搜索框逻辑
interface serachItem{
  value:string
  path:string
}
var searchInput = ref("")
const searchTabel = ref([
  {value:"训练CNN模型",path:store.state.router.page_predict_import_data},
  {value:"训练CRNN模型",path:store.state.router.page_analyze_crnn,opt:{name:"crnn",tabPanel:'2'}},
  {value:"训练LSTM模型",path:store.state.router.page_analyze_lstm,opt:{name:"lstm",tabPanel:'2'}},
  {value:"设置神经网络参数",path:store.state.router.page_predict_settings},
  {value:"预测质量数据",path:store.state.router.page_predict_predict},
  {value:"灰色关联分析",path:store.state.router.page_kg_create},
  {value:"知识三元组",path:store.state.router.page_kg_create},
  {value:"知识图谱交互",path:store.state.router.page_kg_display},
  {value:"知识嵌入",path:store.state.router.page_kg_embed},
  {value:"服务器配置",path:store.state.router.page_config_server},
  {value:"用户设置",path:store.state.router.page_config_user},
  {value:"数据预处理",path:store.state.router.page_tool_preprocess},
  {value:"工艺优化",path:store.state.router.page_optimization},
  {value:"时序分析",path:store.state.router.page_analyze_crnn,opt:{name:"crnn",tabPanel:'1'}}, 
  {value:"CRNN时序预测",path:store.state.router.page_analyze_crnn,opt:{name:"crnn",tabPanel:'1'}},
  {value:"LSTM时序预测",path:store.state.router.page_analyze_lstm,opt:{name:"lstm",tabPanel:'1'}},
  {value:"长短期预测",path:store.state.router.page_analyze_lstm,opt:{name:"lstm",tabPanel:'1'}},
])
const querySearch = (queryString: string, cb: any) => {

  var results = queryString
    ? searchTabel.value.filter(createFilter(queryString))
    : searchTabel.value
  if(results.length==0){
    cb([{value:"没有搜索到该内容...",path:null}])
  }else
    cb(results)
}
const createFilter = (queryString: string) => {
  return (serach: serachItem) => {
    return (
      serach.value.toLowerCase().indexOf(queryString.toLowerCase()) != -1
    )
  }
}
const onSearchSelect = (item:any)=>{
  searchInput.value = ""
  if(item.opt!=undefined){
    if(item.opt.name=="crnn"){
      store.state.analyze.crnn.tabPanel = item.opt.tabPanel
    }else if(item.opt.name=="lstm"){
      store.state.analyze.lstm.tabPanel = item.opt.tabPanel
    }
  }
  $router.replace(item.path)
}



var mainMenuTable= reactive(store.state.status.menu)
let subMenuTable = ([
  {
    name:"质量预测",
    subItem:[
      {name:"训练新模型",icon:"mostly-cloudy",index:"1",menuItem:[
        {name:"导入数据",route:store.state.router.page_predict_import_data},
        {name:"神经网络",route:store.state.router.page_predict_settings},
        {name:"生成模型",route:store.state.router.page_predict_export_data},]},
      {name:"质量预测",icon:"compass",index:"2",menuItem:[
        {name:"数据预测",route:store.state.router.page_predict_predict}]},
      
    ]
    // ,Item:[
    //   {name:"通用管理",icon:"setting",route:""},]
  },{
    name:"知识图谱",
    subItem:[
      {name:"知识图谱",icon:"reading",index:"1",menuItem:[
        {name:"创建三元组",route:store.state.router.page_kg_create},
        {name:"知识检索",route:store.state.router.page_kg_display},]},
      {name:"质量追溯",icon:"compass",index:"2",menuItem:[
        {name:"知识嵌入",route:store.state.router.page_kg_embed},]},],
    // Item:[
    //   {name:"知识库管理",icon:"coin",route:""},]
  },{
    name:"时序分析",
    subItem:[
    {name:"时序模型",icon:"reading",index:"1",menuItem:[
        {name:"CRNN 模型",route:store.state.router.page_analyze_crnn},
        {name:"LSTM 模型",route:store.state.router.page_analyze_lstm},]
      },{name:"工艺优化",icon:"SetUp",index:"2",menuItem:[
        {name:"单目标优化",route:store.state.router.page_optimization},]
      }],
    Item:[
      {name:"质量分析",icon:"PieChart",route:store.state.router.page_analyze},
    ]
  },{
    name:"应用工具",
    subItem:[
      {name:"表格工具",icon:"Connection",index:"1",menuItem:[
        {name:"数据预处理",route:store.state.router.page_tool_preprocess},
        {name:"表格可视化",route:store.state.router.page_tool_visualize}]},],
    Item:[
      
      // {name:"用户设置",icon:"user",route:store.state.router.page_config_user},
    ]
  },{
    name:"参数配置",
    subItem:[],
    Item:[
    {name:"用户设置",icon:"user",route:store.state.router.page_config_user},
    {name:"服务器配置",icon:"monitor",route:store.state.router.page_config_server},
      ]
  },{
  }

])
onBeforeMount(()=>{     
  
  // global.httpPost(
  //     store.state.server.address + "/option/isSubsystem/",
  //     {},
  //     (res)=>{
  //       if(res.res){
  //         global.setToken("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIn0.qQSekbR5BFKQPc3_7gUiDY6Q9y7RojKzvBTLJ9jGtec",180)
          
  //         store.state.status.loginUserName = "admin";
  //         store.state.option.NEEDLOGIN = false;
  //         store.state.option.style.navigateBar=false;
  //         store.state.option.style.barOffsetLeft="-220px";
  //         store.state.option.style.barOffsetTop="-60px";
  //         if(!store.state.status.login){
  //           global.httpPost(
  //             store.state.server.address + "/getuser/",
  //             {},
  //             (res)=>{
  //               if(res.status == store.state.server.successResponse || res.status == "login error"){
  //                 store.state.status.login = true
  //                 store.state.status.loginUserName = res.data.username;
  //                 store.state.status.loginUserAvatarUrl = res.data.avatar+"?r="+Math.random();
  //                 store.state.status.loginUserAdmin = res.data.admin
  //                 store.state.train.preProcess = res.data.preData.preProcess;
  //                 store.state.train.preProcessVal = res.data.preData.preProcessVal;
  //                 store.state.train.parameters = res.data.preData.parameters;
  //                 store.state.train.serverDataOnLoaded = true;
                  
              

  //                 // 耗时操作
  //                 global.graphInit()
  //                 global.webSocketInit()
                  

  //               }else{
  //                 onLogout();
  //               }
  //             }
  //           )

  //         }
  //       }else{
  //         store.state.option.NEEDLOGIN = true;
  //         store.state.option.style.el_descriptions_label_background_color = '#f5f7fa';
  //         store.state.option.style.el_button_border_radius=6;
  //         store.state.option.style.navigateBar=true;
  //         store.state.option.style.barOffsetLeft="0";
  //         store.state.option.style.barOffsetTop="0"
  //         if(!store.state.status.login){
  //           global.httpPost(
  //             store.state.server.address + "/getuser/",
  //             {},
  //             (res)=>{
  //               if(res.status == store.state.server.successResponse){
  //                 store.state.status.login = true
  //                 store.state.status.loginUserName = res.data.username;
  //                 store.state.status.loginUserAvatarUrl = res.data.avatar+"?r="+Math.random();
  //                 store.state.status.loginUserAdmin = res.data.admin
  //                 store.state.train.preProcess = res.data.preData.preProcess;
  //                 store.state.train.preProcessVal = res.data.preData.preProcessVal;
  //                 store.state.train.parameters = res.data.preData.parameters;
  //                 store.state.train.serverDataOnLoaded = true;
                  
              

  //                 // 耗时操作
  //                 global.graphInit()
  //                 global.webSocketInit()
                  

  //               }else if(res.status == "login error"){
  //                 ElMessage.warning("用户"+res.username+"已在其他地方登录，请退出该用户后再尝试。")
  //                 onLogout();
  //               }else{
  //                 onLogout();
  //               }
  //             }
  //           )

  //         }    
  //       }



  //     }
  //   )



})
onMounted(() => {
  // console.log(mainMenuTable)
  // console.log(store.state.status.getLastPage("config"))
  window.onresize = () => {
    return (() => {
      if(titleAreaRef.value.clientWidth<960)
        pd.titleRightAreaVisivle = false
      else
        pd.titleRightAreaVisivle = true

      if(titleAreaRef.value.clientWidth<720)
        pd.titleLeftAreaVisibile = false
      else
        pd.titleLeftAreaVisibile = true

    })()
  }
});

onUnmounted(()=>{
  store.state.server.socket.close()
}
)

function calsubMenuTableVisible(index:any){
  let path = $router.currentRoute.value.path
  switch(index){
    case 0: return path==store.state.router.page_predict_import_data||
      path==store.state.router.page_predict_settings||
      path==store.state.router.page_predict_export_data||
      path==store.state.router.page_predict_predict
    case 1: return path==store.state.router.page_kg_create||
      path==store.state.router.page_kg_display||
      path==store.state.router.page_kg_embed
    case 2: return path==store.state.router.page_analyze_crnn||
      path==store.state.router.page_analyze_lstm||
      path==store.state.router.page_analyze||
      path==store.state.router.page_optimization
    case 3: return path==store.state.router.page_tool_preprocess||
      path==store.state.router.page_tool_visualize
    case 4: return path==store.state.router.page_config_server||
      path==store.state.router.page_config_user
  }
}
function menuTitleActive(route:any){
  switch(route){
    case store.state.router.page_predict_import_data:
    case store.state.router.page_predict_settings:
    case store.state.router.page_predict_export_data:
    case store.state.router.page_predict_predict:
      return "0";

    case store.state.router.page_analyze_crnn:
    case store.state.router.page_analyze_lstm:
    case store.state.router.page_analyze:
    case store.state.router.page_optimization:
      return "1";


    case store.state.router.page_kg_create:
    case store.state.router.page_kg_display:
    case store.state.router.page_kg_embed:
      return "2";

    case store.state.router.page_tool_preprocess:
    case store.state.router.page_tool_visualize:
      return "3";

    case store.state.router.page_config_server:
    case store.state.router.page_config_user:
      return "4";
      
    default:
      return "/"
  }
}

function onLogout(){
  global.removeToken()
  store.state.server.socket.close()
  userinfo.login = false
  let temp = userinfo.loginUserName
  userinfo.loginUserName = ""
  $router.replace({ path: store.state.router.page_login});
  global.httpPost(
      store.state.server.address + "/logout/",
      {username: temp},
      (res)=>{
        
      },
      ()=>{},
      ()=>{
       
        ElMessage.info("已退出。")
      }
    )

}
function devFunc(){
  // store.state.kg.onLoadToKG = ! store.state.kg.onLoadToKG;
  console.log(store.state.optimization.cmp.scroll)
}


</script>


<style lang="less" >


.el-menu{
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
  height: 100%;
}
.el-menu-item {
  line-height: 60px;
  font-size: 16px !important;
}
html,body,#app {
  height: 100%;
} /* precious */
.input-with-select .el-input-group__prepend {
  background-color: red;
}

.decoreateArea {
  width: 100%;
  height: 100%;
  /* background: rgba(255, 0, 0, 0.11); */
  /* bottom: 1px; */
  position: absolute;
  display: flex;
  align-items: center;
  /* margin: 5px; */
  float: right;
  z-index: 2;
}
.rightArea {
  width: 255px;
  /* background: rebeccapurple; */
  height: 100%;
  display: flex;
  align-items: center;
  position: absolute;
  right: 0;
  z-index: 4;
}
.leftArea {
  width: 200px;
  height: 100%;
  left: 0;
  display: flex;
  position: absolute;
  z-index: 4;
}
.searchTtile{
  display: flex;
  align-items: center;
  margin-left: 29px;
}
.searchArea{
  position: absolute;
  background: rgba(243, 243, 243, 0.753);
  top: 62px;
  left: 50px;
  box-shadow: 3px 0px 10px 0px rgba(109, 109, 109, 0.205);
  width: 270px;
  height: a
}
.fontTitle {
  color: rgba(255, 255, 255, 0.712);
  font-size: 22px;
  font-family: "方正粗黑宋简体";
  /* font-style: italic; */
  margin-left: 13px;
}
.menuArea {
  width: 100%;
  height: 100%;
  position: absolute;
  z-index: 3;
}
* {
  margin: 0;
  padding: 0;
}

.Page {
  width: 100vw;
  height: 100vh;
  position: absolute;
  
  
}


.devTest{
  position: absolute;
  width: 200px;
  height: 200px;
  z-index: 10;
  background: wheat;
  left: 0px;
  top: 450px;
  box-shadow: 3px 0px 10px 0px rgba(109, 109, 109, 0.205);
  display: flex;
  align-items: center;
  justify-content: center;
}






span {
  font-size: 17px;
}
.subitem {
  margin-left: 15px;
}







.PageRouterViewPanel{
  position: absolute;
  width: 100vw;
  height: 100vh;
  z-index: 1;
  left: v-bind('store.state.option.style.barOffsetLeft');
  top: v-bind('store.state.option.style.barOffsetTop');
}


.PagePanel_Title {
  /* grid-area: pt; */
  background: #252525;
  display: flex;
  height: 62px;
  width: 100vw;
  justify-content: center;
  position: absolute;
}

.PagePanel_Sidebar {
  position: absolute;
  width: 220px;
  height: 100vh;
  background: white;
  overflow: hidden;
  z-index: 2;
  box-shadow: 3px 0px 10px 0px rgba(109, 109, 109, 0.205);
}
.PagePanel_Sidebar_Area{
  margin-top: 62px;
  position: absolute;
  overflow: hidden;
  height:100%;
  width: 100%;
  position: relative;
}
.sideline{
  width: 1px;
  height: 100%;
  background: #dcdfe6;
  position: absolute;
  right: 0;
}



.search_input_area{
  .el-input__inner{
    color: rgb(197, 197, 197);
    border: none;
    width: auto;
  }
  .el-input__wrapper{
    background: transparent !important;
    box-shadow: 0 0 0 0px var(--el-input-border-color, var(--el-border-color)) inset;
    border: none;
    // border-bottom: rgb(87, 87, 87) 1px solid;
  }
}
</style>
