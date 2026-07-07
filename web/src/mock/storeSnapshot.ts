const skipKeys = new Set(["socket", "viz"]);

function isDomLike(value: any){
  if(typeof window == "undefined" || value == null)
    return false;

  return value instanceof Element || value instanceof Event || value === window;
}

function toSerializable(value: any, key: string = "", seen: WeakSet<object> = new WeakSet()): any{
  if(typeof value == "function")
    return undefined;

  if(skipKeys.has(key))
    return null;

  if(value == null || typeof value != "object")
    return value;

  if(value instanceof Date)
    return value.toISOString();

  if(isDomLike(value))
    return undefined;

  if(seen.has(value))
    return "[Circular]";

  seen.add(value);

  let result: any;
  if(Array.isArray(value)){
    result = value
      .map((item) => toSerializable(item, "", seen))
      .filter((item) => item !== undefined);
  }else{
    result = {};
    Object.keys(value).forEach((itemKey) => {
      const item = toSerializable(value[itemKey], itemKey, seen);
      if(item !== undefined)
        result[itemKey] = item;
    });
  }

  seen.delete(value);
  return result;
}

export function createStoreSnapshot(state: any){
  return toSerializable(state);
}

export function createStoreSnapshotJson(state: any){
  return JSON.stringify(createStoreSnapshot(state), null, 2);
}

export async function copyStoreSnapshot(state: any){
  const json = createStoreSnapshotJson(state);
  await navigator.clipboard.writeText(json);
  return json;
}

export function downloadStoreSnapshot(state: any, filename: string = "dy-store-snapshot.json"){
  const json = createStoreSnapshotJson(state);
  const blob = new Blob([json], { type: "application/json;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
  return json;
}

export function saveStoreSnapshotToLocalStorage(state: any, key: string = "DY2024_STORE_SNAPSHOT"){
  const json = createStoreSnapshotJson(state);
  localStorage.setItem(key, json);
  return json;
}

function isPlainObject(value: any){
  return Object.prototype.toString.call(value) == "[object Object]";
}

export function hydrateStoreFromSnapshot(target: any, snapshot: any){
  Object.keys(snapshot).forEach((key) => {
    const snapshotValue = snapshot[key];

    if(snapshotValue === undefined)
      return;

    if(isPlainObject(snapshotValue) && isPlainObject(target[key])){
      hydrateStoreFromSnapshot(target[key], snapshotValue);
    }else{
      target[key] = snapshotValue;
    }
  });
}

export async function loadMockSnapshot(path: string = "/mock/dy-store-snapshot.json"){
  const response = await fetch(path, { cache: "no-store" });
  if(!response.ok)
    throw new Error(`Failed to load mock snapshot: ${response.status}`);

  const snapshot = await response.json();
  repairSnapshot(snapshot);
  return snapshot;
}

function hasCircularRows(rows: any){
  return Array.isArray(rows) && rows.some((row) => row == "[Circular]");
}

function rebuildRowsForTable(rows: any[]){
  return rows.map((row, index) => ({
    ...row,
    id: row.id ?? index,
    parentId: row.parentId ?? null,
  }));
}

function stripTableMeta(rows: any[]){
  return rows.map((row) => {
    const { id, parentId, ...data } = row;
    return data;
  });
}

function getColumnKeys(columns: any){
  if(!Array.isArray(columns))
    return [];

  return columns
    .map((column) => typeof column == "string" ? column : column?.dataKey)
    .filter(Boolean);
}

function getOptimizationAxisLabels(optimization: any){
  const legendData = optimization?.option?.legend?.data;
  if(Array.isArray(legendData))
    return legendData;

  const columnNames = optimization?.parameters?.columnNames_really;
  if(Array.isArray(columnNames))
    return columnNames;

  return getColumnKeys(optimization?.parameters?.columnNames);
}

function repairSnapshot(snapshot: any){
  if(hasCircularRows(snapshot?.train?.data_forTable) && Array.isArray(snapshot.train.data))
    snapshot.train.data_forTable = rebuildRowsForTable(snapshot.train.data);

  if(hasCircularRows(snapshot?.train?.predict?.data_forTable) && Array.isArray(snapshot.train.predict.data))
    snapshot.train.predict.data_forTable = rebuildRowsForTable(snapshot.train.predict.data);

  const optimization = snapshot?.optimization;
  if(optimization?.option?.xAxis && !Array.isArray(optimization.option.xAxis.data)){
    const labels = getOptimizationAxisLabels(optimization);
    if(labels.length > 0)
      optimization.option.xAxis.data = labels;
  }

  if(hasCircularRows(optimization?.parameters?.data) && Array.isArray(optimization.parameters.data_Table))
    optimization.parameters.data = stripTableMeta(optimization.parameters.data_Table);
}

export async function hydrateStoreFromMockSnapshot(store: any, path?: string){
  const snapshot = await loadMockSnapshot(path);
  hydrateStoreFromSnapshot(store.state, snapshot);
  store.state.mock.enabled = true;
  return snapshot;
}

export function installStoreSnapshotTools(store: any){
  (window as any).DYStoreTools = {
    snapshot: () => createStoreSnapshot(store.state),
    json: () => createStoreSnapshotJson(store.state),
    copy: () => copyStoreSnapshot(store.state),
    download: (filename?: string) => downloadStoreSnapshot(store.state, filename),
    save: (key?: string) => saveStoreSnapshotToLocalStorage(store.state, key),
    loadMock: (path?: string) => hydrateStoreFromMockSnapshot(store, path),
  };
}
