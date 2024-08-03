<template>
  <div class="Page">
    <el-card class="mainArea">
      <div class="scrollRow">
        <div class="leftColumn">
          
          <div class="vizArea" v-loading="!d.containerLoaded">

            <div id="viz"></div>
          </div>
          <div class="bottomRow">
            <el-row class="row1" align="middle">
              <el-icon><edit /></el-icon>
              <div style="margin: 2px">自定义查询</div>
              <!-- <el-button @click="setEdge(1)" link type="primary"> <div style="font-size:15px;margin:px">所有节点</div> </el-button> -->
            </el-row>
            <el-row
              style="height: 30px; font-size: 18px; color: gray"
              align="middle">
              <el-input
                class="inputState"
                v-model="d.cypher"
                placeholder="$ 输入Cypher语句"
                clearable
                @keydown.enter="SUBMIT()"
              />
              <!-- 
                :formatter="
                  (value:any) => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
                "
                :parser="(value:any) => value.replace(/\$\s?|(,*)/g, '')" -->
              <el-button
                class="inputBtn"
                :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'

                type="primary"
                @click="SUBMIT()"
                plain
                >执行</el-button
              >
            </el-row>
          </div>
        </div>
        <div class="rightColumn">
          <div class="subTitleRow" style="display: flex">
            <div class="subTitleIcon">
              <el-icon size="23px" style="margin-right: 4px"
                ><position
              /></el-icon>
            </div>
            <div class="subTitleLabel">工艺质量知识图谱</div>
          </div>
          <el-descriptions
              style="width: 95%; margin-left: 10px"
              direction="vertical"
              :column="4"
              border
            >
              <el-descriptions-item  label="实例地址">
                {{d.url}}<el-button @click="linkToChangeIP()" style="margin-top: -3px;margin-left: 5px;" link> <el-icon :size="16" color="#409EFF"><Edit /></el-icon> </el-button> 

                </el-descriptions-item>
              <el-descriptions-item label="节点数">{{
                d.allNodesNum
              }}</el-descriptions-item>
              <el-descriptions-item label="类别数">{{
                d.nodeClasses.length
              }}</el-descriptions-item>
              <el-descriptions-item label="路径数">{{
                d.relations.length
              }}</el-descriptions-item>
              <el-descriptions-item label="连接状态">
                <el-tag :type="d.onConnecting?'warning':d.onConnected?'success':'danger'" size="small"
                  ><div style="font-size: 10px">{{d.onConnecting?"连接中":d.onConnected?"已连接":"连接失败"}}</div></el-tag
                >
              </el-descriptions-item> 
              <el-descriptions-item label="知识总数">{{
                d.totalNums
              }}</el-descriptions-item>
              <el-descriptions-item label="操作">
                <el-button   size="small" type="primary" plain
                :loading = "d.onExporting"
                :disabled = "!d.onConnected"
                @click="kgExport()"
                >
                  
                  <div style="font-size: 12px;">
                    <div v-if="d.onExporting">导出</div>
                    <div v-else>导出</div>
                  </div>
                  </el-button>
                <el-icon :size="20">
                  <!-- <edit /> -->
                </el-icon>
              </el-descriptions-item>
          </el-descriptions>

          <el-divider style="margin-top: 15px;margin-bottom: 15px;"><div style="color:gray">操作面板</div></el-divider>

          <div class="scrollRow_option">
            <div  style="height: 100%;">
                <div class="optionRow" >
                <div class="subTitleIcon">
                    <el-icon size="21px" style="margin-right: 4px"
                    ><search
                    /></el-icon>
                </div>
                <div class="subTitleLabel">节点查询</div>
                </div>
                <!-- <el-divider style="marginTop:0px;marginBottom:10px" /> -->
                
                <div class="optionRow" >
                <div style="font-size: 15px;color: gray;
                    margin-left: 10px;margin-right: 20px;">
                    > 通过节点类别 
                </div>
                <el-select
                    filterable
                    allow-create
                    v-model="d.queryNodeClass"
                    @change="queryNodeFromClasses"
                    class="m-2"
                    placeholder="查询某一类的全部特征 "
                    size="large"
                >
                    <el-option
                    v-for="item in d.nodeClasses"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>

                <el-button @click="QUERYNODECLASSES()" link type="primary">
                    <div style="font-size: 15px; margin-left: 15px">查询</div>
                </el-button>
                </div>

                <div class="optionRow">
                <div style="font-size: 15px;color: gray;
                    margin-left: 10px;margin-right: 20px;">
                    > 通过节点名称 
                </div>
                <el-select
                    filterable
                    allow-create
                    v-model="d.queryNode"
                    class="m-2"
                    placeholder="查询特定类别下的实体节点 "
                    size="large"
                    no-data-text="请先选择节点类别"
                >
                    <el-option
                    v-for="item in d.nodes"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>

                <el-button @click="QUERYNODES()" link type="primary">
                    <div style="font-size: 15px; margin-left: 15px">查询</div>
                </el-button>
                </div>

                <div class="optionRow" >
                <div
                    style="font-size: 15px;color: gray;
                    margin-left: 10px;margin-right: 20px;">
                    > 通过节点路径
                </div>
                <el-select
                    filterable
                    allow-create
                    v-model="d.queryRelation"
                    class="m-2"
                    placeholder="选择关系节点"
                    size="large"
                >
                    <el-option
                    v-for="item in d.relations"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>
                <el-button @click="QUERYRELATIONS()" link type="primary">
                    <div style="font-size: 15px; margin-left: 15px">查询</div>
                </el-button>
                </div>


                <div class="optionRow" >
                <div class="subTitleIcon">
                    <el-icon size="21px" style="margin-right: 4px"
                    ><circle-plus
                    /></el-icon>
                </div>
                <div class="subTitleLabel">新增自定义节点</div>
                </div>
                
                <div class="optionRow">
                <div class="optionLabel">所属类别</div>
                <el-select
                    filterable
                    allow-create
                    v-model="d.new.nodeClass"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择或输入"
                >
                    <el-option
                    v-for="item in d.nodeClasses"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>
                <!-- <el-button @click="setNode(1)" link type="primary">
                    <div style="font-size: 15px; margin-left: 15px">载入</div>
                </el-button> -->
                <div class="optionLabel">节点名称</div>
                <el-input
                    v-model="d.new.node"
                    placeholder="输入"
                    style="width: 80px"
                />
                <el-button
                    :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
                    @click="NEWNODE()" type="primary" style="margin-left: 20px;" plain>新增</el-button>
                </div>
                <div class="optionRow">
                <div class="optionLabel">附加属性</div><el-input
                    v-model="d.new.parameters"
                    placeholder="（可选）节点的附加属性的JSON字符串"
                    style="width: 280px"
                />

                </div>



                <div class="optionRow" >
                <div class="subTitleIcon">
                    <el-icon size="21px" style="margin-right: 4px"
                    ><circle-plus
                    /></el-icon>
                </div>
                <div class="subTitleLabel">新增自定义路径</div>
                </div>
                <div class="optionRow">
                <div class="optionLabel">头部类别</div>
                <el-select
                    filterable
                    v-model="d.new.nodeClass_relation_head"
                    @change="newRelation_HeadClassOnchange"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择"
                >
                    <el-option
                    v-for="item in d.nodeClasses"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>
                <div class="optionLabel">头部名称</div>
                <el-select
                    filterable
                    v-model="d.new.node_relation_head"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择"
                    no-data-text="请先选择类别"
                >
                    <el-option
                    v-for="item in d.new.nodes_relation_head"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>

                </div>
                <div class="optionRow">
                <div class="optionLabel">尾部类别</div>
                <el-select
                    filterable
                    v-model="d.new.nodeClass_relation_tail"
                    @change="newRelation_TailClassOnchange"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择"
                >
                    <el-option
                    v-for="item in d.nodeClasses"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>
                <div class="optionLabel">尾部名称</div>
                <el-select
                    filterable
                    v-model="d.new.node_relation_tail"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择"
                    no-data-text="请先选择类别"
                >
                    <el-option
                    v-for="item in d.new.nodes_relation_tail"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>

                </div>

                <div class="optionRow">
                <div class="optionLabel">关系名称</div>
                <el-input
                    v-model="d.new.relation"
                    placeholder="输入已选节点间的关系名称"
                    style="width: 235px"
                />
                <el-button
                    :style='"border-radius:"+store.state.option.style.el_button_border_radius+";"'
                    @click="NEWRELATION()" type="primary" style="margin-left: 20px;" plain>新增</el-button>

                </div>


                <div class="optionRow" >
                <div class="subTitleIcon">
                    <el-icon size="21px" style="margin-right: 4px"
                    ><CircleClose  /></el-icon>
                </div>
                <div class="subTitleLabel">删除节点</div>
                </div>
                <div class="optionRow">
                <div class="optionLabel">所属类别</div>
                <el-select
                    filterable
                    v-model="d.del.nodeClass"
                    @change="delClassOnchange"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择"
                >
                    <el-option
                    v-for="item in d.nodeClasses"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>
                <!-- <el-button @click="setNode(1)" link type="primary">
                    <div style="font-size: 15px; margin-left: 15px">载入</div>
                </el-button> -->
                <div class="optionLabel">节点名称</div>
                <el-select
                    filterable
                    v-model="d.del.node"
                    class="m-2"
                    style="width: 120px"
                    placeholder="选择"
                    no-data-text="请先选择节点类"
                >
                    <el-option
                    v-for="item in d.del.nodes"
                    :key="item"
                    :label="item"
                    :value="item"
                    />
                </el-select>
                <el-button @click="DELETE()" link type="primary">
                    <div style="font-size: 15px; margin-left: 10px">删除</div>
                </el-button>
                <el-button @click="DELETEALL()" link type="primary">
                    <div style="font-size: 15px; margin-left: 1px">删除类</div>
                </el-button>
                </div>






        

                <div class="optionRow">
                <div class="subTitleIcon">
                    <el-icon size="21px" style="margin-right: 4px"
                    ><tools
                    /></el-icon>
                </div>
                <div class="subTitleLabel">其他设置</div>
                </div>
                <div class="optionRow" >
                <div style="font-size: 15px;color: gray;
                    margin-left: 10px;margin-right: 20px;">
                    > 最大载入数
                </div>
                <div style="width:200px;display:inline-block ;" >
                    <el-slider :max="200" :min="1" :step="1" v-model="d.maxLoad" />
                </div>
                <div  style="display:inline-block;width: 30px;margin-left: 20px;">{{d.maxLoad}}</div>
                <el-button @click="MAXLOAD()" link type="primary">
                    <div style="font-size: 15px; margin-left: 15px">刷新</div>
                </el-button>
                </div>
            </div>

          </div>
        </div>
      </div>

    </el-card>
  </div>
</template>
<script setup lang="ts">
import { reactive,watch } from "vue";
import { ElMessage, ElMessageBox } from 'element-plus'
import { useStore } from "vuex";
import { onMounted, onUnmounted } from "@vue/runtime-core";
import NeoVis from "neovis.js/dist/neovis.js";
import { useRouter,useRoute } from "vue-router";
import { httpPost } from "@/utils/global";
import * as XLSX from "xlsx";
import router from "@/router";
var base64js = require('base64-js')
const store = useStore();

let d = reactive(store.state.kg.graph);
const $router = useRouter();
const route = useRoute();

let viz = <any>{};
const graphInit = ()=>{
  viz = new NeoVis(d.config);
  //viz.render();
  if(route.query.name!=null && route.query.label!=null ){
    d.queryNodeClass = route.query.label
    d.queryNode = route.query.name
    setTimeout(() => {
      QUERYNODES()
      d.containerLoaded = true
    }, 200);
  }else if(d.QM_QueryNode.length!=""){
    d.queryNode = d.QM_QueryNode.name
    d.queryNodeClass = d.QM_QueryNode.label
    d.onConnecting = true
    d.containerLoaded = true
    setTimeout(() => {
      QUERYNODES()
      d.QM_QueryNode = ""
      d.onConnecting = false
    }, 200);
  }else{
    viz.updateWithCypher('MATCH (n)-[r]->(m) RETURN n,r,m LIMIT '+d.maxLoad);
    d.containerLoaded = true
  }
}
onMounted(() => {
  watch(()=>d.onConnected,(newV,oldV)=>{
    if(newV)
      graphInit();
  })
  if(d.onConnected){
    graphInit();
  }
  
});
onUnmounted(() => {
  store.state.status.menu[2].route = store.state.router.page_kg_display;
})
const queryNodeFromClasses = (val:any)=>{
  
  d.queryNode = ""
  httpPost(
    store.state.server.address + '/kg/query/',
    {"label":val},
    (res)=>{
      d.nodes = res.list  
    }
  )
}
const newRelation_HeadClassOnchange = (val:any)=>{
  d.new.node_relation_head = ""
  httpPost(
    store.state.server.address + '/kg/query/',
    {"label":val},
    (res)=>{
      d.new.nodes_relation_head = res.list  
    }
  )
}
const newRelation_TailClassOnchange = (val:any)=>{
  d.new.node_relation_tail = ""
  httpPost(
    store.state.server.address + '/kg/query/',
    {"label":val},
    (res)=>{
      d.new.nodes_relation_tail = res.list  
    }
  )
}
const delClassOnchange = (val:any)=>{
  d.del.node = ""
  httpPost(
    store.state.server.address + '/kg/query/',
    {"label":val},
    (res)=>{
      d.del.nodes = res.list  
    }
  )
}

const kgExport = ()=>{
  d.onExporting = true
  httpPost(
    store.state.server.address + '/kg/export/',
    {},
    (res)=>{
      if(res.status){
        ElMessage.success("数据读取成功，已开始下载。")
        const data = XLSX.utils.json_to_sheet(res.obj)
        const wb = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(wb, data, 'Sheet1')
        XLSX.writeFile(wb,`知识图谱数据.xlsx`)
      }else
        ElMessage.error("后台返回了错误代码。")
    },
    ()=>{},
    ()=>{d.onExporting = false}
  )
}


function DELETE(){
  if(d.del.node==""){
    ElMessage.error("未选择要删除的节点。")
    return
  }
  ElMessageBox.confirm('确定要删除节点'+d.del.node+"?",
    '删除',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
    .then(() => {
      ElMessage.info("演示版本，无法修改知识图谱。");
      return;


      viz.updateWithCypher('MATCH (n:'+d.del.nodeClass+'{name:"'+d.del.node+'"}) DETACH DELETE n');
      d.nodes.splice(d.nodes.indexOf(d.del.node),1)
      if(d.queryNode==d.del.node){
        d.queryNode = ""
      }
      freshGraphInfo()
      ElMessage.success("删除成功。")
    })
    .catch(() => {
      return
  })
}
function DELETEALL(){
  if(d.del.nodeClass==""){
    ElMessage.error("未选择要删除的节点类。")
    return
  }
  ElMessageBox.confirm('确定要删除类 [ '+d.del.nodeClass+" ] 中的所有节点?",
    '警告',
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning',
    })
    .then(() => {
      ElMessage.info("演示版本，无法修改知识图谱。");
      return;
      viz.updateWithCypher('MATCH (n:'+d.del.nodeClass+') DETACH DELETE n');
      d.nodeClasses.splice(d.nodeClasses.indexOf(d.del.nodeClass),1)
      if(d.queryNodeClass==d.del.nodeClass){
        d.queryNodeClass = ""
        d.queryNode = ""
      }
      freshGraphInfo()
      ElMessage.success("删除成功。")
    })
    .catch(() => {
      return
  })
}
function NEWNODE(){
  if(d.new.nodeClass=="" || d.new.node == ""){
    ElMessage.error("未设置节点类别或节点名称")
    return
  }

  



  let obj = <any>{}
    
  if(d.new.parameters==""){
    ElMessage.info("演示版本，无法修改知识图谱。");
    return;

    obj.name = d.new.node
    obj.color = "#D3D3D3"
    let str_ = "{"
    for(let key in obj){
      str_ += key
      str_ += ':"'
      str_ += obj[key]
      str_ += '",'
    }
    str_ = str_.slice(0,-1)
    str_ += "}"
    if(d.nodeClasses.indexOf(d.new.nodeClass)==-1){
      d.nodeClasses.push(d.new.nodeClass)
      d.config.labels[d.new.nodeClass] = {
        label:"name",
        color:"color",
      }
    }
    viz.updateWithCypher('MERGE(n:'+d.new.nodeClass+str_+')');
    d.nodes.push(d.new.node)
    ElMessage.success("成功。")
  }
  else{
    try{
      console.log(JSON.stringify(({"SD":2})))
      obj = JSON.parse(d.new.parameters)
      obj.name = d.new.node
      let str_ = "{"
      for(let key in obj){
        if(key[0].charCodeAt(0)>=48 && key[0].charCodeAt(0)<=57){
          ElMessage.error('键名的第一个字符不能为数字。')
          return
        }
        if(typeof(obj[key])!="string"){
          ElMessage.error('值只能为字符串。')
          return
        }
        str_ += key
        str_ += ':"'
        str_ += obj[key]
        str_ += '",'
      }
      ElMessage.info("演示版本，无法修改知识图谱。");
      return;

      str_ = str_.slice(0,-1)
      str_ += "}"
      // console.log(str_)
      if(d.nodeClasses.indexOf(d.new.nodeClass)==-1){
        d.nodeClasses.push(d.new.nodeClass)
        d.config.labels[d.new.nodeClass] = {
          label:"name",
          color:"color",
        }
      }
      viz.updateWithCypher('MERGE(n:'+d.new.nodeClass+str_+')');
      d.nodes.push(d.new.node)
      ElMessage.success("成功。")
    }catch(e){
      console.log(e)
      ElMessage.error("JSON字串错误，新增失败")
      return
    }
  }
  freshGraphInfo()
}
function NEWRELATION(){
  if(d.new.nodeClass_relation_head=="" ||d.new.nodeClass_relation_tail=="" ||d.new.node_relation_head=="" ||d.new.nodeClass_relation_tail=="" ){
    ElMessage.error("节点选择不完整。")
    return
  }
  if(d.new.relation==""){
    ElMessage.error("未填写关系名称。")
    return
  }

  ElMessage.info("演示版本，无法修改知识图谱。");
  return;


  let str = 'MATCH(a:'+d.new.nodeClass_relation_head+'),(b:'+d.new.nodeClass_relation_tail+')WHERE a.name="'+d.new.node_relation_head+'"AND b.name="'+d.new.node_relation_tail+'"MERGE(a)-[r:'+d.new.relation+'{name:"'+d.new.relation+'"}]->(b)RETURN r'
  d.relations.push(d.new.relation)
  d.config.relationships[d.new.relation] = {
    label:"name"
  }
  viz.updateWithCypher(str);
  freshGraphInfo()
  ElMessage.success("创建成功。")
}

function QUERYNODES(){
  if(d.queryNodeClass==""||d.queryNode==""){
    ElMessage.error("请输入节点名称。")
    return
  }
  viz.renderWithCypher('MATCH(n:' + d.queryNodeClass + ')-[r]->(nn) WHERE n.name="'+d.queryNode+'" RETURN n,r,nn  LIMIT '+d.maxLoad);
  viz.updateWithCypher('MATCH(n)-[r]->(nn:' + d.queryNodeClass + ') WHERE nn.name="'+d.queryNode+'" RETURN n,r,nn  LIMIT '+d.maxLoad);

  viz.updateWithCypher('MATCH(n:' + d.queryNodeClass + ') WHERE n.name="'+d.queryNode+'" RETURN n  LIMIT '+d.maxLoad);

}
function QUERYNODECLASSES(){
  if(d.queryNodeClass==""){
    ElMessage.error("请输入节点类别。")
    return
  }
  viz.renderWithCypher("MATCH(n:" + d.queryNodeClass + ")-[r]->(nn)  RETURN n,r,nn  LIMIT "+d.maxLoad);
  viz.updateWithCypher("MATCH(n)-[r]->(nn:" + d.queryNodeClass + ")  RETURN n,r,nn  LIMIT "+d.maxLoad);

  viz.updateWithCypher("MATCH(n:" + d.queryNodeClass + ")  RETURN n  LIMIT "+d.maxLoad);
}
function QUERYRELATIONS(){
  if(d.queryRelation==""){
    ElMessage.error("请输入节点路径。")
    return
  }
  viz.renderWithCypher("MATCH(n)-[r:" + d.queryRelation + "]->(nn)  RETURN n,r,nn  LIMIT "+d.maxLoad);
}  
function MAXLOAD(){
  d.config.initialCypher =  'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT '+d.maxLoad
  viz = new NeoVis(d.config);
  viz.render();
}
function linkToChangeIP(){
    $router.replace({path: store.state.router.page_config_server})
}
function freshGraphInfo(){
  httpPost(
    store.state.server.address + '/kg/init/',
    {},
    (res)=>{
      let s = store.state.server
      if(res.status == store.state.server.successResponse){
        d.url = res.obj.url;
        d.nodeClasses = res.obj.nodes;
        d.allNodesNum = res.obj.allNodesNum;
        d.relations = res.obj.relations;
        d.totalNums = res.obj.totalNums;


        d.onConnected = true;
        s.kg_address = res.obj.url
        store.state.server.kg_onConnected = true
      }else{
        d.url = res.obj.url
        s.kg_address = res.obj.url
        d.onConnected = false;
        store.state.server.kg_onConnected = false
      }
    },
    ()=>{},
    ()=>{},
  )
}
let value_nodeSelect = reactive({
  head: "",
  tail: "",
  edge: "",
  newHead: "",
  newTail: "",
  newEdge: "",
  newE: "",
});
function SUBMIT() {
  var cypher = d.cypher;
  
  
  ElMessage.info("无法判断查询语句是否有写入操作，故无法执行。");
  return;

  if (cypher.length > 3) {
    viz.renderWithCypher(cypher);
    // console.log(viz.nodes._data);
    // console.log(d.cypher)
  freshGraphInfo()

  } else {
    // console.log("reload");
    viz.reload();
  }
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
  height: calc(100% - 62px - 100px);
  display: block;
  max-width: 1600px;
  max-height: 1080px;
  overflow: hidden;


  
  .scrollRow{
    position: absolute;
    width: calc( 100% - 40px);
    
    top:20px;
    height: calc(100%  - 20px);
    // background-color: rgba(245, 222, 179, 0.41); 
    display: block;
    // overflow: scroll;
    .leftColumn {
      width: calc(100% - 496px - 20px - 20px);
      height: calc(100%);
      overflow: hidden;
      position: absolute;
    //   background-color: red;
    //   display: flex;
    //   min-height: 860px;
      .vizArea{
        height:calc(100% - 95px - 32px);
        width: 100%;
        background-color: rgba(211, 211, 211, 0.144);
        border-radius: 5px;
        // background-color: red;
      }
      .bottomRow{
        //  background-color: red; 
        // border-top: 1px solid #dcdfe6;
        // display: flex;
        align-items: center;
        justify-content: center;
        width: calc(100% );
        overflow: hidden;
        height: 95px;
        position: absolute;
        bottom:32px;
        .inputState {
          height: 50px;
          width: calc(100% - 100px - 10px);
          font-size: 20px;
        }
        .inputBtn{
          height: 49px;
          margin-left: 10px;
          width: 100px
        }
      }
    }
    .rightColumn {
    //   min-height: 860px;
      width: 496px;
      height: calc(100% - 20px);
      position: absolute;
      right: 0px;
      padding-left: 20px;
      top: 0;
      display: block;
    //   background: #509cfe;
      border-left: 1px solid #dcdfe656;
        .scrollRow_option{
            // background: red;
            overflow: scroll;
            width: 100%;

            height: calc(100% - 250px);
        }

    }
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

.yxyRow {
  width: 100%;
  height: 87%;
  display: flex;
  /* background: rebeccapurple; */
}
.subTitleRow {
  /* background: rgba(102, 51, 153, 0.151); */
  height: 45px;
  display: block;
  align-items: center;
}
.optionRow{
  height: 44px;
  display: flex;
  align-items: center;
  .optionLabel{
    font-size: 15px;
    width: 72px;
    margin-left: 10px;
    color: gray;  
  }
}
.subTitleIcon {
  margin-left: 5px;
  color: #509cfe;
}

.subTitleLabel {
  margin-left: 2px;
  font-size: 16px;
  font-family: "SimHei";
  color: #1d1f20a8;
}


textarea {
  /* border: 1px solid lightgray; */
  margin: 5px;
  border-radius: 5px;
}
#viz {
  width: 100%;
  height: 100%;
  /* border: 1px solid #2291c9; */
  font: 22pt arial;
}
input {
  border: 1px solid #ccc;
}
.row1 {
  height: 35px;
  font-size: 18px;
  margin-top: 10px;
  color: rgba(72, 182, 255, 0.856);
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
</style>