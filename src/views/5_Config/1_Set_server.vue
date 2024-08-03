<template>
    <div class="page">
      <div class="page_body">
        <el-card class="main_card2">
          <div class="titleRow">
            <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><Platform /></el-icon>服务器
          </div>
          <div class="rowDivider"></div>

          <div v-if="!submiting">
            <div class="contentRow">
              <div> 服务器状态：{{"http://"+s.getIP()+":"+s.getPort()}}</div>
              <div class="colDivider"></div>
              <el-tag class="ml-2" type="success">已连接</el-tag>
            </div>
            <div class="contentRow">
              知识库状态：
              <div v-loading="s.kg_onConnecting">
                {{"bolt://"+s.getKGIP()+":"+s.getKGPort()}}
              </div>
              <div class="colDivider"></div>
              <el-tag class="ml-2" :type="s.kg_onConnecting?'warning':s.kg_onConnected?'success':'danger'">{{ s.kg_onConnecting?"获取中":s.kg_onConnected?"已连接":"连接失败" }}</el-tag>
            </div>
          </div>
          <el-form v-else style="margin-top: 20px;" ref="reset" :model="d" label-width="120px" >
            
            <el-form-item label="服务器地址">
              <el-col :span="8">
                <el-input :placeholder="s.getIP()" disabled >
                  <template #prepend>http://</template>
                </el-input>
              </el-col>
              <el-col :span="2">
                <div style="text-align:center">端口</div>
              </el-col>
              <el-col :span="3">
                <el-form-item >
                  <el-input :placeholder="s.getPort()" disabled ></el-input>
                </el-form-item>
              </el-col>
            </el-form-item>    
            <el-form-item
              label="知识库地址">
              <el-col :span="8">
                <el-form-item prop="editKGIP"
                  :rules="{required:true, validator:validateIP,trigger:'change'}">
                  <el-input v-model="d.editKGIP" >
                    <template #prepend>bolt://</template>
                  </el-input>
                </el-form-item>
              </el-col>
              <el-col :span="2">
                <div style="text-align:center">端口</div>
              </el-col>
              <el-col :span="3">
                <el-form-item prop="editKGPort"
                :rules="{required:true, validator:validatePort,trigger:'change'}">
                  <el-input v-model="d.editKGPort" >
                </el-input>
                </el-form-item>
              </el-col>

            </el-form-item>

            <div class="rowDivider"></div>

            <el-form-item>
              <div style="margin-left: -100px;">
                <el-button
                  type="primary"  plain @click="onSubmit()">{{submitingText}}
                </el-button>

              </div>

          </el-form-item>


          </el-form>

          <div class="rowDivider" v-if="submitingText=='修改'"></div>

          <div class="contentRow" v-if="submitingText=='修改'">
            <el-form-item>
              <el-button
              type="primary" :disabled="s.kg_onConnecting" plain @click="onSubmit()">{{submitingText}}
            </el-button>
            </el-form-item>
            
          </div>



            

        </el-card>
      </div>
    </div>
</template>

<script lang="ts" setup>
import { useStore } from 'vuex';
import { onBeforeMount, onMounted, onUnmounted, reactive } from 'vue';
import { ref } from 'vue';
import { ElMessage, FormInstance } from 'element-plus'
import * as global from '@/utils/global'

const store = useStore();
const reset = ref<FormInstance>()
let submiting = ref(false);
let submitingText = ref("修改");
let s = reactive(store.state.server)
let d = reactive(store.state.config)


let validateIP = (rule:any, value:any, callback:any) => {
  let reg =
    /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
  if (value == "") {
    callback(new Error("请输入IP地址"));
  } else if (value !== "" && reg.test(value) === false) {

    callback(new Error("请输入正确格式IP如(11.11.11.11)"));
  } else {
    callback();
  }

}; 
let validatePort = (rule:any, value:any, callback:any) => {
  
  let reg =/^([0-9]|[1-9]\d|[1-9]\d{2}|[1-9]\d{3}|[1-5]\d{4}|6[0-4]\d{3}|65[0-4]\d{2}|655[0-2]\d|6553[0-5])$/

  if (value == "") {
    callback(new Error("请输入端口号"));
  } else if (value !== "" && reg.test(value) === false) {

    callback(new Error("端口号应为(0-65535)"));
  } else {
    callback();
  }

}; 
function onSubmit(){
  
  if(submitingText.value=="修改"){
    submiting.value = true;
    submitingText.value = "确认"
    return;
  }
  if(reset.value==null)
    return;
  reset.value.validate((valid)=>{
    if(valid){
      let newURL = "bolt://"+d.editKGIP+":"+d.editKGPort
      if(newURL==s.kg_address){
        submiting.value = !submiting.value
        submitingText.value = submitingText.value=="修改"?"确认":"修改"
      }else{

        ElMessage.info("演示版本 无法修改服务器。")
        return;
        global.httpPost(
          store.state.server.address + '/config/setKGIP/',
          {new_url:newURL},
          (res:any)=>{
            if(res.status == s.successResponse){
              ElMessage.info("已重新修改知识图谱服务地址，正在载入。")
              s.kg_onConnecting = true
              s.onConnected = false
              global.graphInit(true)
            }
            else{
              ElMessage.error("设置失败。")
            }
          },
          ()=>{},
          ()=>{
            submiting.value = !submiting.value
            submitingText.value = submitingText.value=="修改"?"确认":"修改"
          }
          
          )
      }
        
      }
        
    }
  

  )

}

onMounted(()=>{
    //d = reactive({"editKGIP":s.getKGIP(),"editKGPort":s.getKGPort()})
    d.editKGIP = s.getKGIP()
    d.editKGPort = s.getKGPort()
})
onUnmounted(() => {
  store.state.status.menu[4].route = store.state.router.page_config_server;
})

</script>

<style>

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
}
.main_card2{
  margin-left: 50px;
  margin-top: 50px;
  width: 800px;
  min-width: 680px;
  max-width: 1600px;
  /* height: calc(100% - 100px); */
  height: 270px;
  min-height: 260px;
  
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
</style>