import store from "@/store";

function getMockQueryModelResponse(data:any){
  const type = data?.type;

  if(type == "cnn"){
    const modelInfo = store.state.optimization.modelInfo;
    const modelName = modelInfo?.[0]?.val || store.state.train.modelName || "mock_cnn_model.h5";
    return {
      status: store.state.server.successResponse,
      name: modelName,
      size: modelInfo?.[1]?.val || "0",
      in: modelInfo?.[2]?.val || store.state.train.selectXColNames.length || 0,
      out: modelInfo?.[3]?.val || store.state.train.selectYColNames.length || 0,
    };
  }

  if(type == "crnn" || type == "lstm"){
    const analyzeState = type == "crnn" ? store.state.analyze.crnn : store.state.analyze.lstm;
    if(!analyzeState.hasModel)
      return {
        status: store.state.server.failedResponse,
        reason: "no exist",
      };

    return {
      status: store.state.server.successResponse,
      name: `${type.toUpperCase()}_mock_model.h5`,
      size: analyzeState.sampleInfo?.[1]?.val || "0",
      in: analyzeState.datasetInfo?.[1]?.val || analyzeState.sampleInfo?.[2]?.val || 0,
      out: analyzeState.datasetInfo?.[2]?.val || 1,
    };
  }
}

let mockQualityDataPromise:any = null;
let mockUsersPromise:any = null;
let mockLayersPromise:any = null;
let mockKgInitPromise:any = null;

function loadMockQualityData(){
  if(mockQualityDataPromise != null)
    return mockQualityDataPromise;

  mockQualityDataPromise = fetch("/mock/quality-analysis.json", { cache: "no-store" })
    .then((res) => {
      if(!res.ok)
        throw new Error("Failed to load mock quality data");
      return res.json();
    });

  return mockQualityDataPromise;
}

function loadMockUsers(){
  if(mockUsersPromise != null)
    return mockUsersPromise;

  mockUsersPromise = fetch("/mock/users.json", { cache: "no-store" })
    .then((res) => {
      if(!res.ok)
        throw new Error("Failed to load mock users");
      return res.json();
    });

  return mockUsersPromise;
}

function loadMockLayers(){
  if(mockLayersPromise != null)
    return mockLayersPromise;

  mockLayersPromise = fetch("/mock/layers.json", { cache: "no-store" })
    .then((res) => {
      if(!res.ok)
        throw new Error("Failed to load mock layers");
      return res.json();
    });

  return mockLayersPromise;
}

function loadMockKgInit(){
  if(mockKgInitPromise != null)
    return mockKgInitPromise;

  mockKgInitPromise = fetch("/mock/kg-init.json", { cache: "no-store" })
    .then((res) => {
      if(!res.ok)
        throw new Error("Failed to load mock kg init");
      return res.json();
    });

  return mockKgInitPromise;
}

function getMockQualityResponse(url:string){
  if(url.indexOf("/option/GraphTime/") != -1)
    return loadMockQualityData().then((data:any) => data.graphTime);

  if(url.indexOf("/quality/getItems/") != -1)
    return loadMockQualityData().then((data:any) => data.items);

  if(url.indexOf("/quality/getChart/") != -1)
    return loadMockQualityData().then((data:any) => data.chart);
}

export function getMockPostResponse(url:string,data:any){
  if(url.indexOf("/querymodel/") != -1)
    return getMockQueryModelResponse(data);

  if(url.indexOf("/getalluser/") != -1)
    return loadMockUsers();

  if(url.indexOf("/layers/") != -1)
    return loadMockLayers();

  if(url.indexOf("/kg/init/") != -1)
    return loadMockKgInit();

  const qualityResponse = getMockQualityResponse(url);
  if(qualityResponse != undefined)
    return qualityResponse;
}
