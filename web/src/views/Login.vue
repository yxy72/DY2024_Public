<template>
  <div class="page">
    <div  class="loginContainer"  >
      <div class="loginWindow"  >
        <div class="lW1">
          <div >
            <el-image style="width:36px;margin-right: 20px;" :src="require('@/assets/images/titleImg.png')"></el-image>
          </div>
          <div class="loginTitle">
            XX产品质量知识分析与管理系统
          </div>
        </div>
        <el-divider style="margin:15px 40px 40px 40px;width: 520px;"  />

        <div class="lW2">
          <div class="lW2main">
            <el-form  
              label-position="left"
              label-width="80px"
              :model="loginData"
              v-on:keyup.enter="onSubmit()"
            >
              <el-form-item label="用户名">
                <el-input v-model="loginData.username"></el-input>
              </el-form-item>
              <el-form-item label="密码">
                <el-input type="password" v-model="loginData.password"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button
                v-loading.fullscreen.lock="onloading"
                type="primary" @click="onSubmit">登录</el-button>
                <el-button type="text" @click="registerWindowVisible=true">注册</el-button>
                <el-button type="text" @click="about=true">关于</el-button>

              </el-form-item>
            </el-form>

            <el-dialog v-model="about" @closed="about=false" align-center title="关于" width="30%" center>
              <div>版本：1.5（已去密） &nbsp; | &nbsp; 服务器版本：1.5</div>
              <div>发布时间：2024年8月1日19:00</div>
            </el-dialog>


            <el-dialog v-model="registerWindowVisible" @closed="registed=false"
             align-center title="注册账号" width="30%" center
             v-on:keyup.enter="onRegisterSubmit()">
              <el-result v-if="registed"  icon="success" title="注册成功" sub-title="点击任意处返回" >
              </el-result>
              <el-form v-if="!registed" 
                label-position="left"
                label-width="80px"
                :model="registerData"
                ref="registerValidation"
              >
                <el-form-item
                  label="注册码" 
                  prop="serial"
                  :rules="{ required: true, message: '请输入注册码'}"
                  hint:
                >
                  <el-input v-model="registerData.serial"></el-input>
                </el-form-item>

                <el-form-item 
                  prop="username"
                  label="用户名"
                  :rules="{ required: true, message: '请输入用户名'}"
                  >
                  <el-input v-model="registerData.username"></el-input>
                </el-form-item>

                <el-form-item
                  label="密码"
                  prop="password"
                  :rules="{ required: true, message: '请输入密码'}"
                > 
                  <el-input show-password v-model="registerData.password"></el-input>
                </el-form-item>

                <el-form-item
                    label="确认密码"
                    prop="repassword"
                    :rules="{ required: true,validator:checkRegisterPassword,trigger:'change'}"
                    >
                  <el-input show-password v-model="registerData.repassword" ></el-input>
                </el-form-item>

                <el-form-item>
                  <el-button
                  v-loading.fullscreen.lock="onloading"
                  type="primary" @click="onRegisterSubmit()">确认</el-button>
                </el-form-item>

              </el-form>
            </el-dialog>




          </div>
         
        </div>
      
  



      </div>
    </div>
    <div  class="titleBKG"></div>

 </div>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { ref } from "vue";
import { useStore } from "vuex";
import * as global from "@/utils/global"
import { reactive } from "vue";
import { ElMessage } from 'element-plus';
import type { FormInstance} from 'element-plus'

const $router = useRouter();
const store = useStore();
const registerValidation = ref<FormInstance>()

let registed = ref(false);
let registerWindowVisible = ref(false)
let about = ref(false)
let userinfo = reactive(store.state.status)
let onloading = store.state.status.loginLoading

let loginData = reactive({
    username:"admin",
    password:"123456"
})
let registerData = reactive({
    serial:"",
    username:"",
    password:"",
    repassword:"",
  
})
function onSubmit(){
  if(loginData.username=="")
    ElMessage.error("请输入用户名")
  if(loginData.password=="")
    ElMessage.error("请输入密码")
  if(loginData.username==""||loginData.password=="")
    return;
  userinfo.loginLoading = true







  global.httpPost(
    store.state.server.address + "/login/",
    {username:loginData.username,password:loginData.password},
    (res)=>{
      // console.log(res)
      if((res.status=="username error")||(res.status=="password error"))
        ElMessage.error("用户名或密码错误")
      else if(res.status=="login error" ){
        
        // ElMessage.info("用户"+loginData.username+"已在其他地方登录，请退出该用户后再尝试。")
        $router.replace({ path: store.state.router.page_start });
        userinfo.login = true
        userinfo.loginUserName =  res.data.username
        userinfo.loginUserAvatarUrl = res.data.avatar+"?r="+Math.random();
        userinfo.loginUserAdmin = res.data.admin
      }else if(res.status=="success"){
        $router.replace({ path: store.state.router.page_start });
        ElMessage.success("登陆成功")
        userinfo.login = true
        userinfo.loginUserName =  res.data.username
        userinfo.loginUserAvatarUrl = res.data.avatar+"?r="+Math.random();
        userinfo.loginUserAdmin = res.data.admin
        
        store.state.train.preProcess = res.data.preData.preProcess;
        store.state.train.preProcessVal = res.data.preData.preProcessVal;
        store.state.train.parameters = res.data.preData.parameters;
        store.state.train.serverDataOnLoaded = true;

        global.setToken(res.data.token,res.data.tokenExpires)

        // 耗时操作
        global.graphInit()
        global.webSocketInit()
          
      }else{
        ElMessage.error("未知的返回码，无法登陆")
        console.log(res.status)
      }},
    (error)=>{
      // ElMessage.success("登陆成损失功")
      // ElMessage({
      //   showClose: true,
      //   message:  ("登陆成损失功"),
      //   type: 'error',
      //   duration:1000
      // })
    
    },
    ()=>{ store.state.status.loginLoading = false }
  )
}
function checkRegisterPassword(rule:any,value:any,callback:any){
  if (value === '') {
      callback(new Error('请再次输入密码'));
    } else if (value !== registerData.password) {
      callback(new Error('两次输入密码不一致!'));
    } else {
      callback();
    }
}
function onRegisterSubmit(){
  if(registerValidation.value==null)
    return;
  registerValidation.value.validate((valid:any)=>{
    if(valid){
      store.state.status.loginLoading = true
      global.httpPost(
        store.state.server.address + "/register/",
        {serial:registerData.serial,username:registerData.username,password:registerData.password},
        (res)=>{
          if(res==("serial error"))
            ElMessage.error("注册码无效")
          else if(res=="username error")
            ElMessage.warning("该用户名已存在")
          else if(res=="success"){
            registed.value = true
          }else{
            ElMessage.error("未知错误，无法登陆")
          }},
        ()=>{},
        ()=>{ store.state.status.loginLoading = false }
      )
    }

  })





}
</script>

<style>
#app {
  height: 100%;
}
.Page {
  width: 100vw;
  height: 100vh;
}
.titleBKG{
  background-image:url("../assets/images/cnm.jpg");
  background-size: cover ;
  width: 100vw;
  height: 100vh;
  position: absolute;
  top: 0;
  z-index: 0;
}

.loginContainer{
  width: 100%;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.13);
}
.loginWindow{
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.993);
  width: 600px;
  height: 300px;
  box-shadow: 12px 12px 12px 0 rgba(0,0,0,0.1);
  z-index: 1;


}
.lW1{
  background: none;
  height: 60px;
  margin: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.lW2{
  height: 1fr;
  margin: 15px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.lW2main{
  width: 70%;
  background: none;
}
.loginTitle{
  font-size: 25px;
  font-family: 'Times New Roman', Times, serif;
  font-weight: 1000;
  color: rgb(0, 127, 212);
}
</style>