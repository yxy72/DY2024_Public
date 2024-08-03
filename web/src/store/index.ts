import { createStore } from 'vuex'
import * as global from "@/utils/global"

export default createStore({
  state: {
   
    router:{
        
      page_start: '/start',
      page_login: '/login',
      page_test: '/test',

      page_predict_import_data:     '/predict/trainData',
      page_predict_settings:        '/predict/trainSettings',
      page_predict_export_data:     '/predict/trainExport',
      page_predict_predict:         '/predict/predict',

      page_analyze_lstm:      '/analyze/lstm',
      page_analyze_crnn:      '/analyze/crnn',
      page_analyze:           '/analyze/',
      page_optimization:      '/analyze/opt',

      page_kg_create:       '/grpah/create',
      page_kg_display:      '/grpah/database',
      page_kg_embed:        '/grpah/embed',

      page_tool_preprocess: '/tool/preprocess',
      page_tool_visualize:  '/tool/visualize',

      page_config_user:     '/settings/user',
      page_config_server:   '/settings/server',


    },
    server:{

      // address:'http://192.168.246.144:8888/',
      //address:'http://121.42.227.110:8888',
      // address:'http://192.168.1.111:8888',
      // address:'http://192.168.51.226:8888',
      address:'http://127.0.0.1:8888',
      // 使用lamba表达式就无效？为什么？
      // 后记：因为箭头函数没有this。
      getIP:function(){ return global.getIP(this.address)[0]},
      getPort:function(){ return global.getIP(this.address)[1]},
      ip:'',
      port:0,
      socket:<any>Object,
      kg_address:'',
      getKGIP:function(){ return global.getIP(this.kg_address)[0]},
      getKGPort:function(){ return global.getIP(this.kg_address)[1]},
      kg_onConnecting:true,
      kg_onConnected:false,
      successResponse:"success",
      failedResponse:"failed",
    },
    status:{
      login:false,
      loginUserName:"",
      loginUserAdmin:false,
      loginUserAvatarUrl:"",
      loginLoading:false,
      inStartPage:false,
      // lastPage:{
      //   predict:"",
      //   analyze:"",
      //   kg:"",
      //   tool:"",
      //   config:"",
      // },
      // getLastPage:function (target:string | number | symbol){
      //   if(global.isKey(target,this.lastPage))
      //     return this.lastPage[target]
      // },
      menu:[
        {label:"质量预测",id:"0",route:""},
        {label:"时序分析",id:"1",route:""},
        {label:"知识图谱",id:"2",route:""},
        {label:"应用工具",id:"3",route:""},
        {label:"参数配置",id:"4",route:""},
      ]
    },
    train:{

      fileName:"",
      fileSize:0,
      onTraining:false,
      onTrained:false,
      trainingInfo:["无信息"],
      modelUrl:"",
      modelName:"",
      step:0,

      onLoaded:false,
      queryValid:false,
      data:[],
      selectXColNames:[],
      selectYColNames:[],
      sampleRowCount:0,
      sampleColumnCount:0,
      sampleColumnNames:[],

      data_forTable:[],
      sampleColumnNames_forTable:[],
      
      serverDataOnLoaded:false,
      // 以下数据现在来自于服务器
      preProcessVal:"none",
      preProcess:[{"val":"none","name":"none","expression":""},],
      parameters:{
        "loss":{},
        "optimizer":{},
        "learning_rate":{},
        "epoch":{val:0},
        "batch_size":{},
      },

      // 数据预测页
      predict:{
        data:[],
        data_forTable:[],
        onLoaded: false,
        sampleColumnCount:0,
        sampleColumnNames:[],
        sampleColumnNames_forTable:[],
        sampleRowCount:0,
        onPredicted:false,
        predict_data_forTable:[],
        predictColumnNames_forTable:[],
      }
    },
    kg:{

      // 样本表
      sampleDataOnLoaded:false,
      sampleDataOnCalulating:false,
      sampleDataOnCalulated:false,
      sampleData:[],
      sampleDataColumns:[],   // {}[]
      selectXColNames:[],     // string[]
      selectYColNames:[],     // string[]
      calMethod:'方式1',      // 灰色关联系数计算方式
      coefficient:0.5,        // 灰色关联系数
      threshold:0,            // 判定为关联的界值

      // 计算系数表
      correlationData:[],
      correlationDataColumns:[],

      // 关联度表
      tripletData:[],
      tripletDataColumns:[],

      // 三元组导入知识图谱配置
      onLoadToKG:false,
      loadNodeClassSelect:"",


      graph:{
        cypher:"",
        viz:<any>Object,
        onExporting:false,
        QM_QueryNode:"",
        onConnecting:true,
        onConnected:false,
        containerLoaded:false,
        url:"加载中...",
        allNodesNum:0,
        nodes:[] as Array<string>,
        queryNode:"",
        nodeClasses:[] as Array<string>,
        queryNodeClass:"",
        relations:[] as Array<string>,
        queryRelation:"",
        maxLoad:125,
        config:<any>{
          // containerId: "viz",
          // neo4j: {
          //   serverUrl: "bolt://192.168.1.250:7687",
          //   serverUser: "neo4j",
          //   serverPassword: "Abc123()"
          // },
          // initialCypher: 'MATCH (n)-[r]->(m) RETURN n,r,m LIMIT 25 '
        },
        totalNums:0,
        new:{
          nodeClass:"",
          node:"",
          parameters:"",
      
      
          nodeClass_relation_head:"",
          node_relation_head:"",
          nodes_relation_head:"",
      
          nodeClass_relation_tail:"",
          node_relation_tail:"",
          nodes_relation_tail:"",
      
          relation:"",
        },
        del:{
          nodeClass:"",
          node:"",
          nodes:[],
        }
      },

      embed:{
        sampleDataOnLoaded:false,
        sampleData:[],
        sampleDataColumns:[],

        sampleTriplets:[],
        sampleEntitis:[],
        sampleEdges:[],

        embedKind:"TransE",
        embedDim:10,
        
        sampleDataOnCalulating:false,
        sampleDataOnCalulated:false,
        embedEntityData:[],
        embedEntityDataColumns:[],
        embedEntityDataOnLoading:false,
        embedEdgeData:[],
        embedEdgeDataColumns:[],
        embedEdgeDataOnLoading:false,


      },
      //知识库交互
      
    },
    tools:{
      preprocess:{
        onLoaded:false,
        onProcessing:false,
        onProcessed:false,
        data:[],
        dataColumns:[],

        dataColumns_forTable:[],
        data_processed_forTable:[],
        tofixedNum:4,
        preprocessKind:"1",
        excelHasTitle:true,

        dialogTableCol:[],
        dialogTableData:[],
        preProcessVal:"",
      },
      visualize:{
        sampleCount:0,
        sampleLength:0,
        sampleSize:0,
        readType:"按列读取",
        hasTitle:true,
        option:{
          grid:{
            left:"5%",
            right:"5%",
          },
          tooltip: {
            trigger: 'axis'
          },
          xAxis: {
            type: 'category',
            data: []
          },
          yAxis: {
            type: 'value'
          },
          series: [
            {
              data: [150, 230, 224, 218, 135, 147, 260],
              type: 'line'
            }
          ],
          dataZoom: [
            {
              type: 'inside',
              start: 0,
              end: 100,
            },
            {
              start: 0,
              end: 100,
            }
          ],
        }
      }
    },
    analyze:{
      crnn:{
        tabPanel:"1",
        hasModel:false,
        hasSample:false,
        sampleData:[],
        sampleDataColumns:[],
        sampleInfo:[
          {name:"文件名",   icon:"iconfont icon-24gl-tags2",val:""},
          {name:"文件大小", icon:"iconfont icon-shiti1",val:""},
          {name:"序列长度", icon:"iconfont icon-shuchu2",val:""},
          {name:"样本个数", icon:"iconfont icon-shuzi2",val:""},],

        onTraining:false,
        onTrained:false,
        modelUrl:"",
        trainingInfo:["无信息"],
        // traininfInfoColumns:[{key:"msg1",dataKey: "msg1",title: "msg1"}],
        dataSetOnloaded:false,
        datasetData:[],
        datasetInfo:[
          {name:"序列长度", icon:"iconfont icon-24gl-tags2",val:"等待加载 . . ."},
          {name:"窗口大小", icon:"iconfont icon-24gl-minimize2",val:""},
          {name:"预测长度", icon:"iconfont icon-dangjian_dangyuanguanxizhuanjie",val:""},
          {name:"训练轮次", icon:"iconfont icon-shiti1",val:""},
        ],
        onPredicting:false,
        onPredicted:false,

        chartSeries:<any>[],
        chartXAxis:<any>[],
        
      },
      lstm:{
        tabPanel:"1",
        hasModel:false,
        hasSample:false,
        sampleData:[],
        sampleDataColumns:[],
        sampleInfo:[
          {name:"文件名",   icon:"iconfont icon-24gl-tags2",val:""},
          {name:"文件大小", icon:"iconfont icon-shiti1",val:""},
          {name:"序列长度", icon:"iconfont icon-shuchu2",val:""},
          {name:"样本个数", icon:"iconfont icon-shuzi2",val:""},],

        onTraining:false,
        onTrained:false,
        modelUrl:"",
        trainingInfo:["无信息"],
        // traininfInfoColumns:[{key:"msg1",dataKey: "msg1",title: "msg1"}],
        dataSetOnloaded:false,
        datasetData:[],
        datasetInfo:[
          {name:"序列长度", icon:"iconfont icon-24gl-tags2",val:"等待加载 . . ."},
          {name:"窗口大小", icon:"iconfont icon-24gl-minimize2",val:""},
          {name:"预测长度", icon:"iconfont icon-dangjian_dangyuanguanxizhuanjie",val:""},
          {name:"训练轮次", icon:"iconfont icon-shiti1",val:""},],
        onPredicting:false,
        onPredicted:false,

        chartSeries:<any>[],
        chartXAxis:<any>[],
      },
      analyze:{
        chartXAxis:<any>{},
        chartSeries:<any>{},
        onLoading:true,
        selectItem:"",
        selectUnit:"",
        analyzeInfo:[
          {name:"样本长度", icon:"iconfont icon-24gl-tags2",val:"",span:1},
          {name:"预测长度", icon:"iconfont icon-dangjian_dangyuanguanxizhuanjie",val:"",span:1},
          {name:"最大阈值", icon:"iconfont icon-24gl-minimize2",val:"",span:1},
          {name:"最小阈值", icon:"iconfont icon-shiti1",val:"",span:1},
          {name:"异常节点", icon:"iconfont icon-jinggaozhuangtai",val:"",span:4},
          {name:"关联知识节点", icon:"iconfont icon-guanxitu1",val:"",span:4},
        ],
        errorNodes:[],
        correlatedGraphItems:[],

        chartZoomCustom:{},
        chartOption:{
          tooltip: {
            trigger: 'axis',
            position: function (pt:any) {
              return [pt[0], '10%'];
            },
            // appendToBody:true,
            // renderMode:'richText',
            confine:true,
          },
          title: {
            left: 'center',
            text: `模型预测结果`,
            top:20,
          },
          toolbox: {
            // feature: {
            //   saveAsImage: {}
            // }
          },
          xAxis: {
            type: 'category',
            boundaryGap: false,
            // data: d.chartXAxis,
            axisLabel: {showMaxLabel: true}
          },
          yAxis: {
            type: 'value',
            boundaryGap: [0, '100%'],
            max:0,
          },
          grid:{
            left:"5%",
            right:"5%",
          },
          dataZoom: [
            {
              type: 'inside',
              start: 90,
              end: 100,
            },
            {
              start: 90,
              end: 100,
            }
          ],
          // series: d.chartSeries,
         
        }
      }
    },
    config:{
        editKGIP:"",
        editKGPort:"",
    },
    option:{
      NEEDLOGIN:true,
      style:{
        
        // el_descriptions_label_background_color:'',
        // el_button_border_radius:0,//6
        // navigateBar:false,
        // barOffsetLeft:"-220px",
        // barOffsetTop:"-60px",


        el_descriptions_label_background_color:'#f5f7fa',
        el_button_border_radius:6,
        navigateBar:true,
        barOffsetLeft:"0",
        barOffsetTop:"0",

      }
    }
    ,optimization:{
      modelInfo:[
        {name:"模型名",   icon:"iconfont icon-24gl-tags2",val:""},
        {name:"大小",     icon:"iconfont icon-shiti1",val:"0"},
        {name:"输入维度", icon:"iconfont icon-shuchu2",val:"0"},
        {name:"输出维度", icon:"iconfont icon-shuchu2",val:"0"},
      ],
      parametersLoaded:false,
      parameters:{
        size:0,
        count:0,
        rowCount:0,

        //参数的表
        columnNames:[],
        data_Table:[],

        //所有列名
        columnNames_really:[],
        data:[],
        data_opt:[],
        // 结果视图的表
        data_Table_res:[],
        columnNames_res:[],
        check:false,
        tips:"无",
        tipsColor:"",
        min:[],
        max:[],
      },
      onOptimizing:false,
      onOptimized:false,
      iterations:5,
      info:["无信息"],
      option: {
        legend: {
          data: [],
          top:15,
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: []
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Placeholder',
            type: 'bar',
            stack: 'Total',
            silent: true,
            itemStyle: {
              borderColor: 'transparent',
              color: 'transparent'
            },
            emphasis: {
              itemStyle: {
                borderColor: 'transparent',
                color: 'transparent'
              }
            },
            data:[]
          },
        ]
      },
      tabsName:"1",
      cmpTips:"请载入模型训练集（原始文件，Min-max预处理之前），且不包含表头，不包含标签列。",
      cmpTipsColor:"gray",
      onComparing:false,
      onCompared:false,
      cmpDataChecked:false,
      send_train:[],
      send_opt:[],
      cmp:{
        data_table:[],
        data_column_table:[],
        scroll:0,
      }

    },
  },
  mutations: {

  },
  actions: {
   
  },
  modules: {
  }
})
