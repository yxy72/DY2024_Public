import * as XLSX from 'xlsx'

export type ExcelTableRow = Record<string, any>

export interface TableV2Column {
  key: string
  dataKey: string
  title: string
  width: number
  [key: string]: any
}

export interface ExcelTableResult<T extends ExcelTableRow = ExcelTableRow> {
  rows: T[]
  columnNames: string[]
  rowCount: number
  columnCount: number
}

export interface TableV2Result<T extends ExcelTableRow = ExcelTableRow> {
  data: T[]
  columns: TableV2Column[]
}

const readBlobAsArrayBuffer = (file: Blob) => new Promise<ArrayBuffer>((resolve, reject) => {
  const reader = new FileReader()
  reader.onload = () => resolve(reader.result as ArrayBuffer)
  reader.onerror = () => reject(reader.error)
  reader.readAsArrayBuffer(file)
})

const arrayBufferToBinary = (buffer: ArrayBuffer) => {
  const bytes = new Uint8Array(buffer)
  let binary = ''
  for (let i = 0; i < bytes.byteLength; i++) {
    binary += String.fromCharCode(bytes[i])
  }
  return binary
}

export const readExcelAsJson = async <T extends ExcelTableRow = ExcelTableRow>(file: Blob) => {
  const buffer = await readBlobAsArrayBuffer(file)
  const workbook = XLSX.read(arrayBufferToBinary(buffer), {
    type: 'binary',
  })
  return XLSX.utils.sheet_to_json<T>(workbook.Sheets[workbook.SheetNames[0]])
}

export const normalizeExcelRows = <T extends ExcelTableRow = ExcelTableRow>(rows: T[]): ExcelTableResult<T> => {
  const data = [...rows]
  const columnNames = Object.keys(data[0])
  const normalizedRows = data.map((row) => {
    const normalizedRow: ExcelTableRow = {}
    for (let i = 0; i < columnNames.length; i++) {
      normalizedRow[columnNames[i]] = row[columnNames[i]]
    }
    return normalizedRow as T
  })

  return {
    rows: normalizedRows,
    columnNames,
    rowCount: normalizedRows.length,
    columnCount: columnNames.length,
  }
}

export const createTableV2Data = <T extends ExcelTableRow = ExcelTableRow>(rows: T[]) => {
  return rows.map((row, rowIndex) => {
    row.id = rowIndex
    row.parentId = null
    return row
  })
}

export const createTableV2Columns = (columnNames: string[], width = 150) => {
  return columnNames.map<TableV2Column>((columnName, index) => ({
    key: `${index}`,
    dataKey: `${columnName}`,
    title: columnName,
    width,
  }))
}

export const createTableV2 = <T extends ExcelTableRow = ExcelTableRow>(
  rows: T[],
  columnNames: string[],
  width = 150,
): TableV2Result<T> => ({
  data: createTableV2Data(rows),
  columns: createTableV2Columns(columnNames, width),
})

export const useExcelTable = () => ({
  readExcelAsJson,
  normalizeExcelRows,
  createTableV2Data,
  createTableV2Columns,
  createTableV2,
})
