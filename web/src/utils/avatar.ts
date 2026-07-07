import defaultAvatarUrl from "@/assets/images/default.jpeg";

function isAbsoluteUrl(url: string) {
  return /^(https?:)?\/\//.test(url) || url.startsWith("data:") || url.startsWith("blob:");
}

export function getAvatarUrl(avatarUrl: string, serverAddress: string, mockEnabled: boolean) {
  if (!avatarUrl)
    return defaultAvatarUrl;

  if (isAbsoluteUrl(avatarUrl))
    return avatarUrl;

  if (mockEnabled)
    return defaultAvatarUrl;

  return `${serverAddress}${avatarUrl}`;
}
