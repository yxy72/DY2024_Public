<template>
  <div class="page">
    <div class="page_title_placeholder"></div>
    <div class="main_container">
      
      <el-card class="main_card">
        <div class="card_row1">
          <div class="vertical_bar"/>
          欢迎使用
        </div>
        <div class="card_row2">
          <div>
            <el-icon size="22"><WarningFilled /></el-icon>
            <span>演示版本</span>
            由于性能限制，服务器仅提供读操作。（已去密）

            </div>
        </div>
        <div class="card_row3">


          <div v-for="(item, index) in Navigation" :key="index" class="row3_col">
            <div>
              <el-image style="width: 100px; height: 100px" :src="item.src" :fit="item.fit" />
            </div>
            <div class="colTitle" :style="item.style">{{ item.name }}</div>
            <div class="colOptionArea">
              <el-button style="margin-left:0; margin-top:5px" v-for="(item, index) in (item.btn)" :key="index" @click="item.Click" link type="primary">{{item.Name}}</el-button>
            </div>
          </div>



        </div>
        <div class="card_row4">时间：{{nowtime}} </div>

      </el-card>

    </div>
  </div>
</template>

<script lang="ts" setup>
import { useStore } from 'vuex';
import { useRouter } from 'vue-router';
import { onMounted, onUnmounted } from 'vue';
import { ref } from 'vue';
import { getTime } from "@/utils/global"

const $router = useRouter();
const store = useStore();
let nowtime = ref("")
const Navigation = [
  {
    name:"质量预测",
    style:"color:rgb(89,126,247)",
    src:require("@/assets/images/page_start/predict.png"),
    btn:[
      { Name:"训练一个模型...", Click: ()=>{ $router.push({ path: store.state.router.page_predict_import_data }); }},
      { Name:"预测数据...", Click: ()=>{ $router.push({ path: store.state.router.page_predict_predict }); }},
    ]
  },{
    name:"知识图谱",
    style:"color:#0fae57",
    src:require("@/assets/images/page_start/predict2.png"),
    btn:[
      { Name:"灰色关联分析...", Click: ()=>{ $router.push({ path: store.state.router.page_kg_create }); }},
      { Name:"知识图谱交互...", Click: ()=>{ $router.push({ path: store.state.router.page_kg_display }); }},
      { Name:"知识嵌入...", Click: ()=>{ $router.push({ path: store.state.router.page_kg_embed }); }},
    ]
  },{
    name:"数据分析",
    style:"color:#ff7226",
    src:require("@/assets/images/page_start/predict3.png"),
    btn:[
      { Name:"CRNN分析...", Click: ()=>{ $router.push({ path: store.state.router.page_analyze_crnn }) }},
      { Name:"LSTM分析...", Click: ()=>{ $router.push({ path: store.state.router.page_analyze_lstm }) }},
      { Name:"产品质量分析...", Click: ()=>{ $router.push({ path: store.state.router.page_analyze }) }},
      { Name:"工艺优化...", Click: ()=>{ $router.push({ path: store.state.router.page_optimization }) }},
    ]
  },{
    name:"实用工具",
    style:"color:#409EFF",
    src:require("@/assets/images/page_start/tool.png"),
    btn:[
      { Name:"数据预处理...", Click: ()=>{ $router.push({ path: store.state.router.page_tool_preprocess });  }},
      { Name:"表格可视化...", Click: ()=>{ $router.push({ path: store.state.router.page_tool_visualize });  }},
    ]
  },
]
onMounted(()=>{
  store.state.status.inStartPage = true
  setInterval(() => {
    nowtime.value = getTime()
  }, 1000);
  store.state.status.loginLoading = false
})
onUnmounted(()=>{
  store.state.status.inStartPage = false
})


</script>

<style>

.page{
  /* background: wheat; */
  width: 100vw;
  height: 100vh;
}
.page_title_placeholder{
  height: 62px;
}
.main_container{
  background: rgb(252, 252, 252);
  height: calc(100% - 62px);
  position: relative;
}
.main_card{
  width: 90%;
  max-width: 1600px;
  height: 75%;
  min-height: 600px;
  display: flex;
  position:absolute;
  left:50%;
  top:50%;
  transform:translate(-50%,-50%);
  
}
.card_row1{
  height: 100px;
  margin-left: 20px;
  color: #409EFF;
  font-size: 36px;
  font-style: italic;
  display: flex;
  align-items:center;
  border-bottom:1px rgb(161, 161, 161) solid;
}
.vertical_bar{
  width: 5px;
  height: 40%;
  margin-right: 10px;
  border-radius: 5px;
  background:rgb(64, 158, 255);
}

.card_row2{
  flex-shrink:0 ;
  width:calc(90vw - 80px);
  height: 50px;
  max-width: calc(1600px - 80px);
  margin-left: 20px;
  user-select: none;
  border-width: 1px 0 0 0;
  div{
    display: flex;
    align-items: center;
    position: absolute;
    /* width: 299px; */
    height: 30px;
    margin: 10px 0;
    background-color: #8b8b8b11;
    color: rgb(172, 146, 0);
    span{
      font-size: 18px;
      margin: 0 8px 0 5px;
      font-weight: bold;

    }
  }
}
.card_row3{
  height: calc(100% - 100px - 50px - 80px);
  margin-left: 20px;
  /* background: wheat; */
  display: flex;
  align-items: center;
}
.row3_col{
  /* background: blanchedalmond; */
  width: 33.333%;
  height: 80%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  
}
.row3_col_divider{
  border: rgb(228, 228, 228) solid;
  border-width:0 1px 0 0;
  height: 100%;
  position: absolute;
  right: 0;
  top: 0;
}
.colTitle{
  height: 60px;
  line-height: 50px;
  font-size: 21px;
}
.colOptionArea{
  width: 120px;
  height: 100px;
  background: rgba(250, 250, 255, 0.685);
  border: rgba(204, 204, 204, 0.274) solid 1px;
  border-width: 1px 0 0 0;
  display: flex;
  flex-direction: column;
  align-items: start;
  padding: 20px;
}


.card_row4{
  height: 50px;
  line-height: 50px;
  border: rgb(161, 161, 161) solid;
  border-width: 1px 0 0 0;
  color: rgb(184, 184, 184);
  margin-left: 20px;
}

</style>