export function getServerStaticUrl(path: string, serverAddress: string, mockEnabled: boolean) {
  if (!path)
    return "";

  if (/^(https?:)?\/\//.test(path) || path.startsWith("data:") || path.startsWith("blob:"))
    return path;

  if (mockEnabled)
    return path.replace(/^\/src\//, "/mock/");

  return `${serverAddress}${path}`;
}
