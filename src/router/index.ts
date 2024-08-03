import { createRouter, createWebHashHistory, RouteRecordRaw } from 'vue-router'

import { ElMessage } from 'element-plus'
import store from '@/store'
import * as global from "@/utils/global"


const routes: Array<RouteRecordRaw> = [
  {
    path: "/",
    // component: () => import( '../views/Login.vue'),
    component: () => import( '../views/Start.vue'),
  },{
    path: "/test",
    // component: () => import( '../views/Login.vue'),
    component: () => import( '../views/Test.vue'),
  },
  {
    path: store.state.router.page_start,
    component: () => import( '../views/Start.vue'),
  },{path: store.state.router.page_login,
    component: () => import( '../views/Login.vue')
  },{
    path: store.state.router.page_predict_import_data,
    component: () => import( '../views/1_Predict/1_Train_import.vue'),
  },{
    path: store.state.router.page_predict_settings,
    component: () => import( '../views/1_Predict/2_Train_network.vue'),
  },{
    path: store.state.router.page_predict_export_data,
    component: () => import( '../views/1_Predict/3_Train_export.vue'),
  }, {
    path: store.state.router.page_predict_predict,
    component: () => import( '../views/1_Predict/4_Predict_predict.vue'),
  },{
    path: store.state.router.page_tool_preprocess,
    component: () => import( '../views/4_Tools/1_Tool_preprocess.vue'),
  },{
    path: store.state.router.page_tool_visualize,
    component: () => import( '../views/4_Tools/2_Tool_visualize.vue'),
  },{
    path: store.state.router.page_kg_create,
    component: () => import( '../views/3_Trace/1_KG_create.vue'),
  },{
    path: store.state.router.page_kg_display,
    component: () => import( '../views/3_Trace/2_KG_database.vue'),
  },{
    path: store.state.router.page_kg_embed,
    component: () => import( '../views/3_Trace/3_KG_embedding.vue'),
  },{
    path: store.state.router.page_analyze_crnn,
    component: () => import( '../views/2_Analyze/1_CRNN.vue'),
  },{
    path: store.state.router.page_analyze_lstm,
    component: () => import( '../views/2_Analyze/2_LSTM.vue'),
  },{
    path: store.state.router.page_analyze,
    component: () => import( '../views/2_Analyze/3_Analyze.vue'),
  },{
    path: store.state.router.page_optimization,
    component: () => import( '../views/2_Analyze/4_Optimization.vue'),
  },{
    path: store.state.router.page_config_server,
    component: () => import( '../views/5_Config/1_Set_server.vue'),
  },{
    path: store.state.router.page_config_user,
    component: () => import( '../views/5_Config/2_Set_user.vue'),
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})
router.beforeEach((to, from, next) => {


  
  if(!store.state.option.NEEDLOGIN || to.path == "/login" || store.state.status.login) {
    next();
  }else{
        // httpPost(
        //     store.state.server.address + "/checkauth/",
        //     {},
        //     (res)=>{
        //       if(res == store.state.server.successResponse){
        //         store.state.status.login = true;
        //         next();
        //       }else{
        //         next(`/login`);
        //         store.state.status.login = false;
        //         ElMessage.info("请登录")
        //       }
        //     },
        //     ()=>{
        //       next(`/login`);
        //     }
        //   )
        global.httpPost(
          store.state.server.address + "/getuser/",
          {},
          (res)=>{
            if(res.status == store.state.server.successResponse){
              next();
              store.state.status.login = true
              store.state.status.loginUserName = res.data.username;
              store.state.status.loginUserAvatarUrl = res.data.avatar+"?r="+Math.random();
              store.state.status.loginUserAdmin = res.data.admin
              store.state.train.preProcess = res.data.preData.preProcess;
              store.state.train.preProcessVal = res.data.preData.preProcessVal;
              store.state.train.parameters = res.data.preData.parameters;
              store.state.train.serverDataOnLoaded = true;

              if(res.subsystem){
                store.state.option.style.navigateBar=false;
                store.state.option.style.barOffsetLeft="-220px";
                store.state.option.style.barOffsetTop="-60px";
              }else{
                store.state.option.style.navigateBar=true;
                store.state.option.style.barOffsetLeft="0";
                store.state.option.style.barOffsetTop="0"
              }
              

              // 耗时操作
              global.graphInit()
              global.webSocketInit()
              
              if(!res.subsystem && res.login)
                ElMessage({"type":"info","duration":500,"message":"用户"+res.data.username+"：多地登录可能导致异常。"})

              // console.log(global.getToken())

            }else{
              next(`/login`);
              ElMessage.info("请重新登录")
            }
          }
        )
  }



})
export default router
