import { useEffect, useState } from "react";

export function Now() {
  const [now, setNow] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadNow = async () => {
    setLoading(true);
    setError(null);

    try {
      const r = await fetch("http://localhost:8000/time");

      if (!r.ok) {
        throw new Error(`HTTP ${String(r.status)}`);
      }

      const d = (await r.json()) as { datetime: string };
      setNow(d.datetime);
    } catch (err) {
      setError(`Failed to load time: ${String(err)}`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void loadNow();
  }, []);

  const handleReload = () => {
    void loadNow();
  };

  return (
    <div>
      <h1>Current datetime</h1>

      <button onClick={handleReload} disabled={loading}>
        {loading ? "Loading…" : "Reload time"}
      </button>

      {now && <p>{now}</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}
