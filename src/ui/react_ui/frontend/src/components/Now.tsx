import { useEffect, useState } from "react";

export function Now() {
  const [now, setNow] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadNow = async () => {
    setLoading(true);
    setError(null);

    try {
      const r = await fetch("http://localhost:8000/time"); // direct call

      if (!r.ok) {
        throw new Error(`HTTP ${r.status}`);
      }

      const d: { now: string } = await r.json();
      setNow(d.now);
    } catch (err) {
      console.error(err);
      setError("Failed to load time");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadNow();
  }, []);

  return (
    <div>
      <h1>Current datetime</h1>

      <button onClick={loadNow} disabled={loading}>
        {loading ? "Loading…" : "Reload time"}
      </button>

      {now && <p>{now}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
