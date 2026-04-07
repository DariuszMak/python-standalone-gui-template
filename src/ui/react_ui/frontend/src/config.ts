export function getApiBaseUrl(): string {
  return window.__APP_CONFIG__?.apiBaseUrl ?? (import.meta.env.VITE_BACKEND_URL as string | undefined) ?? "http://localhost:8000";
}