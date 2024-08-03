<template>
  <div class="page">
    <div class="page_body">
      <el-card v-on:keyup.enter="onChangingUserInfo()" class="main_card1" :style="'height:'+(userInfo.changingpwd?470:320)+'px'">
        <div class="titleRow">
          <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><Platform /></el-icon>个人信息
        </div>
        <div class="rowDivider"></div>
        <div class="avatarArea">
          <div class="avatarTile">
            <div>头像</div>
            <el-upload
              ref="upload"
              class="upload-demo"
              :action="store.state.server.address+'/postuseravatar/'"
              :show-file-list = "false"
              :limit="1"
              :on-exceed="handleExceed"
              :auto-upload="false"
              :headers="getHeaders()"
              :on-change="handleAvatarChange"
              :on-success="handleAvatarSuccess"
              >
              <template #trigger>
                <el-button type="primary" link style="margin-top: px;;margin-left: 5px;"><div style="font-size: 14px;">上传</div></el-button>
              </template>
          
            </el-upload>
          </div>
          <el-avatar shape="square" :size="110" :src="userInfo.avatarUrl" />
        </div>
        <el-form
          label-position="top"
          label-width="100px"
          :model="userInfo"
          class="formColumn"
          ref="UserRef"
          hide-required-asterisk
        >
        <el-form-item label="当前用户名" required>
          <el-input v-model="userInfo.username" />
        </el-form-item>
        <el-form-item  label="密码" v-if="!userInfo.changingpwd">
          <el-button @click="userInfo.changingpwd = true">
            更改密码
          </el-button>
        </el-form-item>
        <el-form-item prop="password_old" required label="当前密码" v-if="userInfo.changingpwd" :rules="{ required: true,message:'请输入当前密码',trigger:'change'}">
          <el-input show-password v-model="userInfo.password_old" />
        </el-form-item>
        <el-form-item prop="password_new" label="新密码" v-if="userInfo.changingpwd" :rules="{ required: true,message:'请输入新密码',trigger:'change'}">
          <el-input show-password v-model="userInfo.password_new" />
        </el-form-item>
        <el-form-item prop="password_confirm" label="确认密码" v-if="userInfo.changingpwd" :rules="{ required: true,validator:checkRegisterPassword,trigger:['change','blur']}">
          <el-input show-password v-model="userInfo.password_confirm" />
        </el-form-item>
        </el-form>
        <div class="rowDivider"></div>
        <el-form-item>
          <el-button type="primary" plain @click="onChangingUserInfo()">
            修改
          </el-button>
          <el-button type="primary" plain v-if="userInfo.changingpwd" @click="userInfo.changingpwd = false;">
            返回
          </el-button>
        </el-form-item>


          

      </el-card>
      <el-card v-if="store.state.status.loginUserAdmin" class="card_user_control">
        <div class="titleRow">
          <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><Platform /></el-icon>
          用户管理
        </div>
        <div class="rowDivider"></div>
        <el-table :data="tableData" style="width: 100%" height="445">
          <el-table-column fixed prop="id" label="UID" width="100" />
          <el-table-column fixed prop="username" label="用户名"  />
          <el-table-column
            prop="useradmin"
            label="用户类型"
            :filters="[
              { text: '管理员类型', value: '管理员' },
              { text: '普通用户', value: '用户' },
            ]"
            :filter-method="filterTag"
            filter-placement="bottom-end">
            <template #default="scope">
              <el-tag
                :type="scope.row.useradmin === '管理员' ? '' : 'info'"
                disable-transitions
                >
                <div style="font-size: 13px;">
                  {{ scope.row.useradmin }}
                </div>
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="date_create" label="创建时间" width="250" />
          <el-table-column fixed="right" label="操作" width="100">
            <template #default="scope">
              <el-button
                link
                type="primary"
                size="small"
                @click.prevent="deleteRow(scope.row)"
              >
                <div style="color:#ff5555">删除</div>
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <div v-if="registInfo.registing"  class="tableAdd">
          <el-form style="display: flex;" v-on:keyup.enter="onRegist()" hide-required-asterisk ref="RegistRef" :inline="true" :model="registInfo" class="demo-form-inline">
            <el-form-item label="用户名" prop="username" :rules="{ required: true,message:'',trigger:'change'}">
              <el-input v-model="registInfo.username" />
            </el-form-item>
            <el-form-item  label="用户类型" prop="useradmin"  :rules="{ required: true,message:'',trigger:'change'}">
              <el-select v-model="registInfo.useradmin" placeholder="请选择" >
                <el-option label="管理员" value="管理员" />
                <el-option label="普通用户" value="用户" />
              </el-select>
            </el-form-item>
            <el-form-item >
              <el-button  type="primary" @click="onRegist()">确认</el-button>
            </el-form-item>
            <el-form-item>
              <el-button style="margin-left: -20px;" type="primary" plain @click="registInfo.registing = false">取消</el-button>
            </el-form-item>
          </el-form>
        </div>
        <el-button v-if="!registInfo.registing" class="mt-4" style="width: 100% ;margin-top: 12px;" @click="registInfo.registing = true"
        >新增用户</el-button>
        <div class="rowDivider"></div>


      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted, reactive,  } from 'vue';
import { ref } from 'vue';
import { ElMessage,ElMessageBox } from 'element-plus';
import * as global from "@/utils/global"
import type { FormInstance} from 'element-plus'
import { ElNotification } from 'element-plus'
import { genFileId } from 'element-plus'
import type { UploadInstance, UploadProps, UploadRawFile } from 'element-plus'


const $router = useRouter();
const store = useStore();
const UserRef = ref<FormInstance>()
const RegistRef = ref<FormInstance>()
//上传
const upload = ref<UploadInstance>()
let userInfo = reactive({
  username:"",
  changingpwd:false,
  changingavatar:false,
  password_old:"",
  password_new:"",
  password_confirm:"",
  avatarUrl:(store.state.server.address + store.state.status.loginUserAvatarUrl),
})
let registInfo = reactive({
  username:"",
  useradmin:"",
  registing:false,
}) 
interface User {
  id: string
  username: string
  useradmin: string
  date_create: string
}
var tableData= ref([{
  id:"0",
  username:"1",
  useradmin:"0",
  date_create:"2",
}])
function deleteRow(row:any){

  ElMessageBox.confirm(
    row.username!=store.state.status.loginUserName?('确定要从数据库中删除用户'+row.username):"确定要删除自己的账户？（将会退出系统）",
    '删除',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
    .then(() => {
      ElMessage.info("演示版本，无法修改用户信息");
      return;
      global.httpPost(
        store.state.server.address + "/deleteuser/",
        {username:row.username},
        (res)=>{
          if(res.status==store.state.server.successResponse){
            tableData.value.splice(tableData.value.indexOf(row),1)
            ElMessage.info('用户'+row.username+'删除成功。')
            if(row.username==store.state.status.loginUserName)
              onLogout()
          }
        }
      )
    }).catch(() => {})
}
function onRegist(){
  if(RegistRef.value==null)
      return;
  RegistRef.value.validate((valid:any)=>{
    if(valid){

      
  

      ElMessage.info("演示版本，无法修改用户信息");
      return;
      global.httpPost(
        store.state.server.address + "/regist/config/",
        {username:registInfo.username,useradmin:registInfo.useradmin=="管理员"?true:false},
        (res)=>{
          if(res.status==store.state.server.successResponse){
            ElNotification.success({
              title: '新增',
              message: '已增加用户'+registInfo.username+', 默认密码123456',
              showClose: true,
            })
            tableData.value = res.userList
          }else if(res.status=="username error"){
            ElMessage.error("用户名已存在。")
          }
        }
      )
    }
  })
}
function checkRegisterPassword(rule:any,value:any,callback:any){
    if (value === '') {
        callback(new Error('请再次输入密码'));
      } else if (value !== userInfo.password_new) {
        callback(new Error('两次输入密码不一致!'));
      } else {
        callback();
      }
}
function onChangingUserInfo(){

  
  ElMessage.info("演示版本，无法修改用户信息");
  return;

  if(!userInfo.changingpwd){
    if(userInfo.username == store.state.status.loginUserName && !userInfo.changingavatar)
      return;
    let changeUsername = !(userInfo.username == store.state.status.loginUserName)
    global.httpPost(
      store.state.server.address + "/changeuser/",
      {type:"username",username:userInfo.username,changeusername:changeUsername},
      (res)=>{
        if(res.status==store.state.server.successResponse){
          ElMessage.success("修改成功。")
          store.state.status.loginUserName = userInfo.username
          global.setToken(res.token)
          //必须token改变之后再改变头像。
          if(userInfo.changingavatar){
            upload.value!.submit();
          }
        }else if(res.status==store.state.server.failedResponse){
          ElMessage.error("操作失败，原因："+res.reason)
        }
      }
    )
  }else{
    if(UserRef.value==null)
      return;
    UserRef.value.validate((valid:any)=>{
      if(valid){
        let changeUsername = !(userInfo.username == store.state.status.loginUserName)
        global.httpPost(
          store.state.server.address + "/changeuser/",
          {type:"password",changeusername:changeUsername,username:userInfo.username,password:userInfo.password_old,password_new:userInfo.password_new},
          (res)=>{
            if(res.status==store.state.server.successResponse){
              ElMessage.success("修改成功。")
              store.state.status.loginUserName = userInfo.username
              global.setToken(res.token)
              //必须token改变之后再改变头像。
              if(userInfo.changingavatar){
                upload.value!.submit();
              }
            }else if(res.status==store.state.server.failedResponse){
              ElMessage.error("操作失败，原因："+res.reason)
            }
          }
        )
      }
      
    })
  }
}
function onLogout(){
  global.removeToken()
  store.state.status.login = false
  store.state.status.loginUserName = ""
  $router.replace({ path: store.state.router.page_login});
}
const filterTag = (value: string, row: User) => {
  return row.useradmin === value
}
//上传文件
const handleExceed: UploadProps['onExceed'] = (files) => {
  upload.value!.clearFiles()
  const file = files[0] as UploadRawFile
  file.uid = genFileId()
  upload.value!.handleStart(file)
}
var imageUrl = ref('')
const handleAvatarChange: UploadProps['onChange'] = (uploadFile,uploadFiles) => {
  if(uploadFile.raw == null)
    return
  if (uploadFile.raw.type !== 'image/jpeg' && uploadFile.raw.type !== 'image/png') {
    ElMessage.error('图片格式只支持jpg/png')
    return false
  } else if (uploadFile.raw.size / 1024 / 1024 > 2) {
    ElMessage.error('图片大小不能超过2MB')
    return false
  }
  userInfo.avatarUrl = URL.createObjectURL(uploadFile.raw!)
  userInfo.changingavatar = !userInfo.changingavatar
}
const handleAvatarSuccess: UploadProps['onSuccess'] = (response,uploadFile) => {
  if(response.status == store.state.server.successResponse){
    store.state.status.loginUserAvatarUrl = response.avatar+"?r="+Math.random()
  }
}
var getHeaders = ()=>{return{ token:global.getToken()}}
onMounted(()=>{
  userInfo.username = store.state.status.loginUserName
  // 显示用户列表
  global.httpPost(
    store.state.server.address + "/getalluser/",
    {},
    (res)=>{
      if(res.status==store.state.server.successResponse){
        tableData.value = res.userList
      }
    }
  )
})
onUnmounted(() => {
  store.state.status.menu[4].route = store.state.router.page_config_user;
})
function devFunc(){}
</script>
<style scoped lang="less">
.page{
  /* background: wheat; */
  width: 100vw;
  height: 100vh;
  position: relative;
}
.page_body{
  background: rgb(252, 252, 252);
  width: 100%;
  position: absolute;
  top: 62px;
  left: 220px;
  width: calc(100% - 220px);
  height: calc(100% - 62px);
  display: flex;
  /* align-items: center; */
  overflow: scroll;
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
.devTest{
  position: absolute;
  width: 200px;
  height: 200px;
  background: wheat;
  left: 520px;
  top: 450px;
  box-shadow: 3px 0px 10px 0px rgba(109, 109, 109, 0.205);
  display: flex;
  align-items: center;
  justify-content: center;
}

.main_card1{
  margin-left: 50px;
  margin-top: 50px;
  min-width: 480px;
  /* height: calc(100% - 120px); */
  /* height: 470px; */
  min-height: 260px;
  position: relative;
  .formColumn{
    width: calc(100% - 150px - 20px);
  }
  .avatarArea{
    width: 150px;
    height: 150px;
    /* background: red; */
    position: absolute;
    right: 20px;
  }
}
.card_user_control{
  margin-top: 50px;
  margin-left: 50px;
  width: calc(100% - 150px - 580px);
  /* height: calc(100% - 50px - 50px); */
  height: 600px;
  min-width: 680px;
  max-width: 910px;
}

.avatarTile{
  font-size: 14px;
  color: #606266;
  height: 25px;
  /* line-height: 25px; */
  display: flex;
  align-items: center;
  /* background: red; */
}
.titleRow{
/* background: blue; */
height: 40px;
font-family: "SimHei";
font-weight: bold;
color: #4e6077;
display: flex;
align-items: center;
}
.contentRow{
  margin-left: 20px;
  height: 50px;
  line-height: 40px;
  display: flex;
  align-items: center;
}
.rowDivider{
  width: 100%;
  height: 1px;
  margin-top: 10px;
  margin-bottom: 10px;
  background:#dcdfe6;

}
.colDivider{
  width: 1px;
  height: 60%;
  margin-left: 10px;
  margin-right: 10px;
  background:#efeff1;

}


.tableAdd{
  margin-top: 12px;
  height: 32px;
  display: flex;
  justify-content: center;
}
</style>