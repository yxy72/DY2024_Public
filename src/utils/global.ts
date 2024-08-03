import axios from "axios";
import Cookies from 'js-cookie'
import { ElMessage } from 'element-plus';
import { useStore } from "vuex";
import NeoVis from "neovis.js/dist/neovis.js";
import store from '../store'

export const setToken = (token:any,days:number=7)=>{
  Cookies.set('token',token,{ expires: Number(days) })
}
export const getToken = ()=>{
  return Cookies.get('token')
}



export const removeToken = ()=>{
  Cookies.remove('token');
}

export function httpPost(url:string,data:object,option:(res:any)=>void=()=>{},err_option:(err:any)=>void=()=>{},final:()=>void=()=>{}){
  axios.post(url,data,{
      headers:{
        token : getToken() ,
        "Content-Type": "application/json",
        // "Content-Type": "application/x-www-form-urlencoded",
    }})
    .then(function (res) {
      option(res.data)
    })
    .catch((error)=>{
      err_option(error)
      if(error.request)
        ElMessage.error("数据返回异常。")
      if(error.response){
        ElMessage.error("服务器访问失败。")
        
    }
    })
    .finally(()=>{
      final();
    });
}

export function getTime() {
	var time = new Date();
	var year = time.getFullYear();
	var month = time.getMonth() + 1;
	var date = time.getDate();
	var h = time.getHours();
	var hh = h < 10 ? '0' + h : h;
	var m = time.getMinutes();
	var mm = m < 10 ? '0' + m : m;
	var s = time.getSeconds();
	var ss = s < 10 ? '0' + s : s;
	return (year + "年" + month + "月" + date + "日 " + hh + ":" + mm + ":" + ss) ;
}
export function getTime_number() {
	var time = new Date();
	var year = time.getFullYear();
	var month = time.getMonth() + 1;
	var date = time.getDate();
	var h = time.getHours();
	var hh = h < 10 ? '0' + h : h;
	var m = time.getMinutes();
	var mm = m < 10 ? '0' + m : m;
	var s = time.getSeconds();
	var ss = s < 10 ? '0' + s : s;
	return (year + "/" + month + "/" + date + "/ " + hh + ":" + mm + ":" + ss) ;
}
export function getTime_hms() {
  let d = new Date();
  let s = d.getSeconds() < 10 ? "0" + String(d.getSeconds()) : d.getSeconds();
  let m = d.getMinutes() < 10 ? "0" + String(d.getMinutes()) : d.getMinutes();
  let h = d.getHours() < 10 ? "0" + String(d.getHours()) : d.getHours();
  return h + ":" + m + ":" + s ;
}
export function calTimelag(date1:Date,date2:Date){
  let ms = (date2.getTime() - date1.getTime());
  let h = Math.floor(ms/1000/3600) ;
  let m = Math.floor(ms/1000%3600/60);
  let s = (ms/1000%3600%60);
  let ss = "";
  if(s.toFixed(2)[0] != '0')
    ss = s.toFixed(2)
  else if(s.toFixed(2) != "0.00")
    ss = s.toFixed(2)
  else
    if(s.toFixed(3) != "0.000")
      ss = s.toFixed(3)
    else
      if(s.toFixed(4) != "0.0000")
        ss = s.toFixed(4)
    else 
      ss = s.toFixed(5)
  let hh = h==0?"":String(h)+"时";
  let mm = m==0?"":String(m)+"分";
  ss = ss+"秒";
  return hh + mm +ss ;
}
//该函数给原始的对象数组加上id和parentId标识，生成适用于el-table-v2组件的数据对象数组
//并生成适用于el-table-v2组件的列名对象数组
export function getDataAndColumnsForTable(data:{}[],columns:string[],widths?:number[]){
  // {X_Minimum: 42, X_Maximum: 50, 
  // {X_Minimum: 645, X_Maximum: 6
  let obj = {
    data:<any>[],
    columns:<any>[],
  }
  obj.data = data
  // obj.data = data.map((val:any,rowIndex:any) => {
  //   val.id = rowIndex
  //   val.parentId = null
  //   return val
  // })
  obj.columns = columns.map((val:any,index:any) => ({
    key: `${index}`,
    dataKey: `${val}`,
    title: val,
    width: widths == undefined?120:widths[index],
  }))
  return obj
}
export function transposition(arr:[][]){
  let trans:Array<any> = []
  for(let i = 0 ; i <arr[0].length; i++){
    let temp:string[] = []
    for(let j = 0; j <arr.length;j++){
      temp.push(arr[j][i])
    }
    trans.push(temp)
  }
  return trans
}
export const getIP = (address:string)=>{
    const reg_ip = /(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/g
    const reg_port = /.+:(\d{1,5})/;
    let ip_list = address.match(reg_ip)
    let port_list = address.match(reg_port)
    if(ip_list!=null && port_list != null)
        return [ip_list[0],port_list[1]]
    else
        return ["null","null"]
}
// 因为登录界面和APP.mouted界面都要用到
export const graphInit = async(tips:boolean = false) => {
  httpPost(
    store.state.server.address + '/kg/init/',
    {},
    (res)=>{
      let g = store.state.kg.graph
      let s = store.state.server
      let c = store.state.config
      var base64js = require('base64-js')
      if(res.status == store.state.server.successResponse){
        g.url = res.obj.url;
        g.nodeClasses = res.obj.nodes;
        g.allNodesNum = res.obj.allNodesNum;
        g.relations = res.obj.relations;
        g.totalNums = res.obj.totalNums;
        let obj = <any>{}
        res.obj.nodes.map((val:any)=>{
          obj[val]={
            label: "name",
            color:'color',
          }
        })
        let edgeObj = <any>{}
        res.obj.relations.map((val:any)=>{
          edgeObj[val]={
            label: "name",
          }
        })
        g.config = {
          containerId: "viz",
          neo4j: {
            serverUrl: res.obj.url,
            serverUser: res.obj.neo4j_username,
            serverPassword: String.fromCharCode.apply(String, base64js.toByteArray(res.obj.neo4j_password))
          },
          visConfig: {
            nodes: {
              color:'austo',
            },
            edges: {
              arrows: {
                to: {enabled: false}
              }
            },
          },
          labels: obj,
          relationships: edgeObj,
          initialCypher: 'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT '+g.maxLoad+' '
        };
        g.onConnected = true;
        g.onConnecting = false
        s.kg_address = res.obj.url
        c.editKGIP = getIP(s.kg_address)[0]
        c.editKGPort = getIP(s.kg_address)[1]
        store.state.server.kg_onConnected = true
        if(tips)
            ElMessage.success("图形数据库连接成功。")
      }else{
        // ElMessage.error("图形数据库连接失败")
        g.url = res.obj.url
        s.kg_address = res.obj.url
        c.editKGIP = getIP(s.kg_address)[0]
        c.editKGPort = getIP(s.kg_address)[1]
        g.onConnected = false;
        g.onConnecting = false
        store.state.server.kg_onConnected = false
        if(tips)
            ElMessage.error("图形数据库连接失败。")
      }
    },
    ()=>{},
    ()=>{
      store.state.server.kg_onConnecting = false
    },
  )
  console.log("GRAPH DONE")
}
export const webSocketInit = () => {
  store.state.server.socket = new WebSocket("ws"+store.state.server.address.slice(4)+"/connect/"+store.state.status.loginUserName+"/")
  store.state.server.socket.onmessage = function(event:any){
    let res = JSON.parse(event.data)
    if(res.type=="cnn"){
      if(res.kind=="loss"){
        store.state.train.trainingInfo.push(
          "Epoch "+(res.info.epoch+1)+"/"+store.state.train.parameters.epoch.val+"\r\n" 
          + " - loss: " +String(res.info.loss) 
          + " - accuracy: " +String(res.info.accuracy) 
        )
      }else if(res.kind=="text"){
        store.state.train.trainingInfo.push(('['+getTime_hms()+'] ' + res.info))
      }
    }else if(res.type=="crnn"){
      if(res.kind=="loss"){
        store.state.analyze.crnn.trainingInfo.push(
          "Epoch "+(res.info.epoch+1)+"/"+res.info.EPOCH+"\r\n" 
          + " - loss: " +String(res.info.loss)
          + " - val_loss: " +String(res.info.val_loss) 
        )
      }else if(res.kind=="text"){
        store.state.analyze.crnn.trainingInfo.push(('['+getTime_hms()+'] ' + res.info))
      }
    }else if(res.type=="lstm"){
      if(res.kind=="loss"){
        store.state.analyze.lstm.trainingInfo.push(
          "Epoch "+(res.info.epoch+1)+"/"+res.info.EPOCH+"\r\n" 
          + " - loss: " +String(res.info.loss)
          + " - val_loss: " +String(res.info.val_loss) 
        )
      }else if(res.kind=="text"){
        store.state.analyze.lstm.trainingInfo.push(('['+getTime_hms()+'] ' + res.info))
      }
    }else if(res.type=="pso"){
        store.state.optimization.info.push(('['+getTime_hms()+'] ' + res.info))
    }
  }
  console.log("WEBSOCKET DONE")
}
export const SYS_Init = () => {
  // let lp =  store.state.status.lastPage
  let r = store.state.router
  // lp.predict = r.page_predict_import_data
  // lp.analyze = r.page_analyze_crnn
  // lp.kg = r.page_kg_create
  // lp.tool = r.page_tool_preprocess
  // lp.config = r.page_config_user


  let sm = store.state.status.menu
  sm[0].route = r.page_predict_import_data
  sm[1].route = r.page_analyze_crnn
  sm[2].route = r.page_kg_create
  sm[3].route = r.page_tool_preprocess
  sm[4].route = r.page_config_user





}

//判断key
export function isKey(key: string | number | symbol,object: object): key is keyof typeof object{
  return key in object;
}