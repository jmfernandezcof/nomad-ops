import { StrictMode, useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { api, type User } from "./api";
import "./styles.css";

type View = "overview" | "knowledge" | "alerts";
type Result = { outcome: string; data: Array<Record<string, unknown>> | Record<string, unknown>; error?: string };

function Login({ onLogin }: { onLogin: (user: User, csrf: string) => void }) {
  const [email, setEmail] = useState("user006@asteria.example");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  async function submit(event: React.FormEvent) {
    event.preventDefault(); setError("");
    try {
      const result = await api<{ user: User; csrf_token: string }>("/api/v1/auth/login", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });
      onLogin(result.user, result.csrf_token);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Unable to sign in");
    }
  }
  return <main className="login-page"><form className="login-card" onSubmit={submit}>
    <div className="brand"><div className="brand-mark">N</div><div><div className="brand-name">NOMAD Ops</div><div className="brand-sub">AI FOR REAL OPERATIONS</div></div></div>
    <h1>Welcome to Asteria</h1><p>Fictional enterprise demonstration environment</p>
    <label>Email<input value={email} onChange={e => setEmail(e.target.value)} autoComplete="username" /></label>
    <label>Password<input type="password" value={password} onChange={e => setPassword(e.target.value)} autoComplete="current-password" /></label>
    {error && <div className="login-error" role="alert">{error}</div>}
    <button className="primary-btn" type="submit">Sign in</button>
  </form></main>;
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [csrf, setCsrf] = useState("");
  const [view, setView] = useState<View>("overview");
  const [result, setResult] = useState<Result | null>(null);
  const [query, setQuery] = useState("supplier onboarding");
  const [alertId, setAlertId] = useState("ALT-003");
  useEffect(() => {
    api<{ user: User; csrf_token: string }>("/api/v1/auth/me")
      .then(x => { setUser(x.user); setCsrf(x.csrf_token); })
      .catch(() => undefined);
  }, []);
  if (!user) return <Login onLogin={(u, token) => { setUser(u); setCsrf(token); }} />;

  async function logout() {
    await api("/api/v1/auth/logout", { method: "POST", headers: { "X-CSRF-Token": csrf } });
    setUser(null); setCsrf(""); setResult(null);
  }
  async function searchDocuments() {
    setResult(await api<Result>(`/api/v1/documents/search?q=${encodeURIComponent(query)}`));
  }
  async function getAlert() {
    try { setResult(await api<Result>(`/api/v1/alerts/${encodeURIComponent(alertId)}`)); }
    catch (error) { setResult({ outcome: "DENIED", data: {}, error: error instanceof Error ? error.message : "Denied" }); }
  }

  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-mark">N</div><div><div className="brand-name">NOMAD Ops</div><div className="brand-sub">AI FOR REAL OPERATIONS</div></div></div>
      <div className="tenant-card"><div className="tenant-icon">A</div><div><div className="tenant-title">Asteria Manufacturing Group</div><div className="tenant-sub">Synthetic enterprise laboratory</div></div></div>
      <nav className="nav">{(["overview", "knowledge", "alerts"] as View[]).map(item =>
        <button key={item} className={`nav-item ${view === item ? "active" : ""}`} onClick={() => { setView(item); setResult(null); }}>
          <span>{item === "overview" ? "⌂" : item === "knowledge" ? "▤" : "△"}</span>{item[0].toUpperCase() + item.slice(1)}
        </button>)}</nav>
      <div className="user-card"><div className="avatar">{user.display_name.split(" ").map(x => x[0]).slice(0, 2).join("")}</div><div><div className="user-name">{user.display_name}</div><div className="user-role">{user.role.replaceAll("_", " ")}</div></div></div>
    </aside>
    <main className="main">
      <header className="topbar"><strong>{user.primary_site_id}</strong><button className="link-btn" onClick={logout}>Sign out</button></header>
      <section className="content">
        {view === "overview" && <><section className="hero"><div className="hero-kicker">ASTERIA MANUFACTURING GROUP</div><h1>Keep operations moving.</h1><p>Authorized context. Controlled actions. Human accountability.</p></section>
          <section className="metrics"><article className="metric green"><div className="metric-title">Session</div><div className="metric-value">2h</div><div className="metric-sub">30 min inactivity limit</div></article>
            <article className="metric blue"><div className="metric-title">Your sites</div><div className="metric-value">{user.site_scope.length}</div><div className="metric-sub">Explicitly authorized</div></article>
            <article className="metric amber"><div className="metric-title">Environment</div><div className="metric-value">Sandbox</div><div className="metric-sub">Synthetic data only</div></article></section></>}
        {view === "knowledge" && <section><h1 className="view-title">Knowledge</h1><p className="view-sub">Only current documents within your authorized department and sites are returned.</p><div className="command-wrap"><input value={query} onChange={e => setQuery(e.target.value)} /><button className="primary-btn" onClick={searchDocuments}>Search</button></div></section>}
        {view === "alerts" && <section><h1 className="view-title">Alerts</h1><p className="view-sub">Try ALT-003 and ALT-004 to verify the Ciudad Real boundary.</p><div className="command-wrap"><input value={alertId} onChange={e => setAlertId(e.target.value)} /><button className="primary-btn" onClick={getAlert}>Open</button></div></section>}
        {result && <article className="card result-card"><h3>{result.outcome}</h3>{result.error && <p>{result.error}</p>}<pre>{JSON.stringify(result.data, null, 2)}</pre></article>}
      </section>
    </main>
  </div>;
}

createRoot(document.getElementById("root")!).render(<StrictMode><App /></StrictMode>);
