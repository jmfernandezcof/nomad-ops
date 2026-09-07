export type User = {
  id: string; display_name: string; email: string; role: string;
  department_id: string; primary_site_id: string; site_scope: string[];
};

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  if (!path.startsWith("/api/")) throw new Error("Refusing a non-API request target");
  const response = await fetch(path, { credentials: "include", ...init });
  const body = await response.json();
  if (!response.ok) throw new Error(body.detail ?? "Request failed");
  return body as T;
}
