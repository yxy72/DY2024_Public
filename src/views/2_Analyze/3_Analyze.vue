<template>
  <div class="page">
    <el-card class="mainCard">
      <div class="titleArea">
        <div class="titleRow">
          <div style="color:gray">选择指标</div>
          <el-select style="margin-left: 15px;margin-right: 15px;" v-model="d.selectItem" @change="SELECTCHANGE" placeholder="正在加载...">
            <el-option
              v-for="item in pd.selectItems"
              :key="item.id"
              :label="item.value"
              :value="item.id"
            >
              <span style="float: left">{{ item.value }}</span>
              <span
                style="
                  float: right;
                  color: var(--el-text-color-secondary);
                  font-size: 13px;
                  margin-left: 10px;
                "
                >{{ ' # '+item.id}}</span>
            </el-option>
          </el-select>

          
          <div style="color:gray">单位</div>
          <div style="color:#409EFF;margin-left: 10px;font-family: 'Times New Roman', Times, serif;">{{ d.selectUnit }}</div>
        </div>
      </div>
      <div class="chartArea" >
        <div class="chartRow">
          <!--  -->
          <div  v-show="!pd.showTable" style="position: absolute;;width: 100%;height:calc(100% - 0px);z-index: 1;background: white;">
            <el-empty style="z-index: 2;" description="等待数据" />
          </div>
          <div ref="chartRef" class="chart"></div>
        </div>
      </div>
      <div class="optArea">
        <div class="titleRow" style="border-top: 1px solid #dcdfe670;border-bottom:none;background: ;">
          <el-icon size="27px" style="color: #509cfe;margin-right: 5px;"><money /></el-icon>
          结果分析
          
        </div>
        <div class
        ="textRow">
          <el-descriptions
            :column="4"
            border>
            <el-descriptions-item :width="50" :span="item.span" v-for="(item,index) in d.analyzeInfo" :key="index" >
              <template #label>
                <div class="cell-item">
                  <i :class=item.icon />
                  {{item.name}}
                </div>
              </template>
              {{ item.val }}
              <div v-if="item.name=='异常节点'">
              <el-scrollbar height="150px">
                <el-tag v-if="d.errorNodes.length!=0" type="danger" style="margin-right: 5px;" size="small" v-for="item,index in d.errorNodes"><div style="font-size: 14px;">{{item}}</div></el-tag>
                <el-tag v-else type="success"><div style="font-size: 14px;">无异常</div></el-tag>
              </el-scrollbar>
                
              </div>
              <div v-if="item.name=='关联知识节点'">
                <div v-if="d.correlatedGraphItems.length!=0">
                  <el-scrollbar height="25px">
                  <el-tag v-for="item in d.correlatedGraphItems" type="" @click="()=>{k.QM_QueryNode = item;$router.replace({path: store.state.router.page_kg_display})}" style="cursor: pointer;margin-right: 5px;" size="small" ><div style="font-size: 14px;">{{item.name}}</div></el-tag>
                </el-scrollbar>
                </div>
                <el-tag v-else type="info" ><div style="font-size: 14px;" >暂无关联</div></el-tag>
              </div>
            </el-descriptions-item>


          </el-descriptions>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import * as global from '@/utils/global'
import { onBeforeMount, onMounted, onUnmounted, reactive, ref } from 'vue';
import { useStore } from 'vuex';
import { ElMessage} from "element-plus";
import * as echarts from 'echarts';
import { el } from 'element-plus/es/locale';
type EChartsType = echarts.EChartsType;
const store = useStore()
let d = reactive(store.state.analyze.analyze);
let k = reactive(store.state.kg.graph);
let chartRef = ref()
let chart = <EChartsType>{};
let pd = reactive({
  selectItems:[{value:'均衡等级',id:'# 0001'}],
  showTable:true,
})
let interval:any;
const getAnalyzeData = () => {
  global.httpPost(
    store.state.server.address + "/analyze/get/",{},
    (res)=>{
      if(res.status == store.state.server.failedResponse){
        ElMessage.error("状态异常。")
        return
      }
      if(res.status == "onPredicting"){
        ElMessage.warning("后台数据正在计算中，请稍后重新访问。")
        return
      }
      let data = res.data.table
      let label = res.data.label
      let predictLen = res.data.predictLen
      let maxThreshold = res.data.maxThreshold
      let minThreshold = res.data.minThreshold


      let Series = <any>[],XLabel = <any>[]

      data.map((val:any,index:number)=>{
        Series.push({
          name: `${label[index]}`,
          type: 'line',
          symbolSize:8,
          symbol: "none",
          // (params:any)=>{
          //   if(params < maxThreshold && params >minThreshold){
          //     return "none"
          //   }else
          //     return "circle"
          // },
          sampling: 'lttb',
          itemStyle: {
            // color:'rgb(255, 70, 131)',
            // (params:any)=>{
            //   if(params.value > maxThreshold){
            //     return 'red'
            //   }else if(params.value <maxThreshold && params.value >minThreshold){
            //     return 'rgb(255, 70, 131)'
            //   }else if(params.value <minThreshold){
            //     return 'blue'
            //   }
            // },

          },
          markLine: {
            symbol:'none',
            label:{
              show:true,
              // position:'middle'
              formatter: '最大阈值',
              // color:"red"
            },
            data: [
              { type: 'average', name: 'Avg' },
              {
                name: 'Y 轴值为 100 的水平线',
                yAxis: 1.02
              },
            ]
          },
          // markArea: {
          //   itemStyle: {
          //     // color: 'rgba(255, 173, 177, 0.4)'
          //   },
          // },
          // lineStyle:{ 
          //   color:'rgb(255, 70, 131)'
          // },
          // areaStyle: {
            // color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            //   {
            //     offset: 0,
            //     color: 'rgb(255, 158, 68)'
            //   },
            //   {
            //     offset: 1,
            //     color: 'rgb(255, 70, 131)'
            //   }
            // ])
          // },
          data: val
        })
      })
      
      


      /*Series.push({
        type: 'line',
        itemStyle: {
          color: 'rgb(255, 70, 131)'
        },
        markLine: {
          data: [{
            name:'标记线',
            yAxis:maxThreshold
          }],
          silent: true,
          symbol:'none',
          label:{
            show:true,
            // position:'middle'
            formatter: '最大阈值',
            color:"red"
          }
        },
      })
      Series.push({
        type: 'line',
        itemStyle: {
          color: 'blue'
        },
        markLine: {
          data: [{
            name:'标记线',
            yAxis:minThreshold
          }],
          silent: true,
          symbol:'none',
          label:{
            show:true,
            // position:'middle'
            formatter: '最小阈值',
            color:"blue"
          }
        },
      })*/
      
      for(let i = 0 ; i < Number(data[0].length) - Number(predictLen) ; i++)
        XLabel.push(`节点${i+1}`)
      for(let i = 0 ; i < Number(predictLen) ; i++)
        XLabel.push({value:`预测${i+1}`,textStyle: {
          color: 'darkred'
        }})
      
      d.chartSeries = Series
      d.chartXAxis = XLabel
      d.chartOption.series = Series
      d.chartOption.xAxis.data = XLabel
     
      chart.setOption(d.chartOption)




    }
  )
}



onUnmounted(() => {
  clearInterval(interval)
})
const SELECTCHANGE = (val:string) => {
  global.httpPost(
    store.state.server.address + '/quality/getChart/',
    {uid:val},
    (res)=>{
      if(res.status != store.state.server.successResponse){
        ElMessage.info(res.status)
        d.selectItem = d.lastSelectItem
        return
      }
      let data = JSON.parse(res.data)
      if(data==null)
        pd.showTable=false
      else
        pd.showTable=true
      let maxThreshold = Number(res.threshold.maxThreshold)
      let minThreshold = Number(res.threshold.minThreshold)
      let predictLen = Number(res.outputDim)
      let inputDim = Number(res.inputDim)
      let graphLeft = Number(res.graphLeft)
      let graphRight = Number(res.graphRight)
      let label = res.label
      let maxOverflows = []
      let minOverflows = []
      d.errorNodes= []

      if(data!=null)
        for(let i = 0;i<data.length;i++){

          if(Number(data[i])>maxThreshold){
            if(i>Number(data.length) - Number(predictLen)){
              maxOverflows.push([
                {
                  xAxis: i==Number(data.length) - Number(predictLen)+1?`节点${i-1}`:`预测${i-Number(data.length)+Number(predictLen)}`
                },
                {
                  xAxis: `预测${i-Number(data.length)+Number(predictLen)+1}`
                }
              ])
              d.errorNodes.push(i==Number(data.length) - Number(predictLen)+1?`预测1`:`预测${i-Number(data.length)+Number(predictLen)+1}`)
            }else{
              maxOverflows.push([
                {
                  xAxis: `节点${i}`
                },
                {
                  xAxis: `节点${i+1}`
                }
              ])
              d.errorNodes.push(`节点${i+1}`)
            }
          }

          if(Number(data[i])<minThreshold){
            if(i>Number(data.length) - Number(predictLen)){
              minOverflows.push([
                {
                  xAxis: i==Number(data.length) - Number(predictLen)+1?`节点${i-1}`:`预测${i-Number(data.length)+Number(predictLen)}`
                },
                {
                  xAxis: `预测${i-Number(data.length)+Number(predictLen)+1}`
                }
              ])
              d.errorNodes.push(i==Number(data.length) - Number(predictLen)+1?`预测1`:`预测${i-Number(data.length)+Number(predictLen)+1}`)
            }else{
              minOverflows.push([
                {
                  xAxis: `节点${i}`
                },
                {
                  xAxis: `节点${i+1}`
                }
              ])
              d.errorNodes.push(`节点${i+1}`)
            }
          }



        }
      
      d.correlatedGraphItems = (res.neighbors)
      
    //   switch(val){
    //     case("0001"):
    //       d.correlatedGraphItems = [
    //         {label:"装配后筒、尾圈",class:"工艺参数属性"},
    //         {label:"配置环氧胶",class:"工艺参数属性"},
    //         {label:"整流罩装配",class:"工艺参数属性"},
    //         {label:"拧入深度",class:"质量因素"},
    //         {label:"产品长度",class:"质量因素"},
    //       ]
    //       break;
    //     case("0002"):
    //       d.correlatedGraphItems = [
    //         {label:"固化湿度",class:"质量因素"},
    //         {label:"点胶量",class:"质量因素"},
    //         {label:"破甲火箭弹对接-预配摆差",class:"工艺参数属性"},
    //         {label:"破甲火箭弹检验-摆差",class:"工艺参数属性"},
    //         {label:"破甲火箭弹对接-夹具夹紧",class:"工艺参数属性"},
    //       ]
    //       break;
    //     default:
    //       d.correlatedGraphItems =[
    //       ]

    //   }


   



      let Series = <any>[],XLabel = <any>[]

      Series.push({
        type: 'line',
        symbolSize:8,
        symbol: "none",
        
        sampling: 'lttb',
        markLine: {
          symbol:'none',
          label:{
            show:true,
            // position:'middle'
            // formatter: '最大阈值',
            // color:"red"
          },
          data: [
            {
              name: '最大阈值',
              yAxis: maxThreshold,
              label: {
                formatter: '最大阈值'
              },
            },
            {
              name: '最小阈值',
              yAxis: minThreshold,
              label: {
                formatter: '最小阈值'
              },
            },
          ]
        },
        data: data,
        markArea:{
          itemStyle: {
            color: 'rgba(255, 173, 177, 0.4)'
          },
          data:maxOverflows
        }
      })
      
      
      d.chartOption.yAxis.max = function(val:any){
        let max = val.max > Number(maxThreshold)?val.max:Number(maxThreshold)
        let xs = max<10?1:0
        let abs = Math.abs(Number(maxThreshold)-val.max)
        return ((max+abs)).toFixed(2)
      }
      d.chartOption.yAxis.min = function(val:any){
        let min = val.min < Number(minThreshold)?val.min:Number(minThreshold)
        let xs = min<10?1:0
        let abs = Math.abs(Number(minThreshold)-val.min)
        return (min-abs<0?0:min-abs).toFixed(2)
      }

      if(data!=null){
        for(let i = 0 ; i < Number(data.length) - Number(predictLen) ; i++)
          XLabel.push(`节点${i+1}`)
        for(let i = 0 ; i < Number(predictLen) ; i++)
          XLabel.push({value:`预测${i+1}`,textStyle: {
            color: 'darkred'
          }})
      }
      d.chartOption.series = Series
      d.chartOption.xAxis.data = XLabel
      d.selectUnit = res.unit
      d.analyzeInfo[0].val = inputDim
      d.analyzeInfo[1].val = predictLen
      d.analyzeInfo[2].val = maxThreshold
      d.analyzeInfo[3].val = minThreshold
      // chartOption.series = Series
      // chartOption.xAxis.data = XLabel

      chart.off();
      chart.on('datazoom', function (params:any) {
          d.chartZoomCustom[label] = {}
          d.chartZoomCustom[label].start = params.start
          d.chartZoomCustom[label].end = params.end
      });
      let s = d.chartZoomCustom[label]==undefined?graphLeft:d.chartZoomCustom[label].start;
      let e = d.chartZoomCustom[label]==undefined?graphRight:d.chartZoomCustom[label].end;

      d.chartOption.dataZoom =  [{
        type: 'inside',
        start: s,
        end: e,
      },{
        start: s,
        end: e,
      }]

      d.lastSelectItem = d.selectItem
      chart.setOption(d.chartOption)
      chart.resize()
    }
  )

}
onBeforeMount(()=>{
  // ElMessage.info("演示版本，图表不再间隔刷新");
  /*global.httpPost(
    store.state.server.address + '/option/GraphTime/',
    {type:"get"},
    (res)=>{
    if(res.time!=undefined)
      interval = setInterval(() => {
        SELECTCHANGE(d.selectItem)
      }, Number(res.time)*1000);
    else
      interval = setInterval(() => {
        SELECTCHANGE(d.selectItem)
      }, 5000);
      
    },
    ()=>{
      interval = setInterval(() => {
        SELECTCHANGE(d.selectItem)
      }, 5000);
    
    }
  )*/
})
onMounted(()=>{


  ElMessage.info("演示版本，图表不再间隔刷新"); //取消onBeforeMount的内容。

  chart = echarts.init(chartRef.value);
  // getAnalyzeData();
  window.addEventListener("resize", () => {
    chart.resize();
  });



  global.httpPost(
    store.state.server.address + '/quality/getItems/',
    {},
    (res)=>{
      pd.selectItems = <any>[]
      for(let i = 0 ;i<res.items.length;i++){
        pd.selectItems.push({value:res.items[i].label,id:res.items[i].uid})
      }
      d.selectItem = d.selectItem == ""?pd.selectItems[0].id:d.selectItem
      SELECTCHANGE(d.selectItem)
    }
  )

})
onUnmounted(() => {
  store.state.status.menu[1].route = store.state.router.page_analyze;
})
</script>

<style scoped lang="less">
/deep/ .el-descriptions__label.el-descriptions__cell.is-bordered-label{
  background:v-bind('store.state.option.style.el_descriptions_label_background_color');
}
.page{
  width: 100%;
  height: 100%;
  background: rgb(252, 252, 252);
  overflow: hidden;
}

.mainCard{
  position:absolute;
  left:calc(220px + 50px);
  top:calc(62px + 50px);
  width:calc(100% - 220px - 100px);
  max-width: 1600px;
  max-height: calc(1440px - 220px - 100px);
  height: calc(100% - 62px - 50px - 50px);

  .titleArea{
    
    // background: red;
    height: 50px;
    border-bottom: 1px solid #dcdfe6ce;
    border-top: 1px solid #dcdfe6ce;
    .titleRow{
      height: 100%;
      display: flex;
      align-items: center;
    }
  }
  .chartArea{
    height: calc(100% - 50px - 300px);
    width:calc(100% - 40px);

    // background: rebeccapurple;
    position: absolute;
    .chartRow{
      width: 100%;
      height: 90%;
      position: relative;
      // background: wheat;
      .chart{
        width: 100%;
        height: 100%;
      }
    }
  }
  .optArea{
    height: 300px;
    width:calc(100% - 40px);
    bottom : 20px;
    // background: red;
    position: absolute;
    .titleRow{
      height: 50px;
      font-family: "SimHei";
      border-bottom: 1px solid #dcdfe6b4;
      font-weight: bold;
      color: #4e6077;
      display: flex;
      align-items: center;
    }
    .textRow{
      height: 250px;
      max-height: 250px;
      min-height: 250px;
    }
  }

}



</style>