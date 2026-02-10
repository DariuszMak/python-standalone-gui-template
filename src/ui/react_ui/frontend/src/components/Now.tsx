import { useEffect, useState } from "react";

export function Now() {
  const [now, setNow] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/now")
      .then((r) => r.json())
      .then((d) => setNow(d.now));
  }, []);

  return (
    <div>
      <h1>Current datetime</h1>
      <p>{now ?? "Loading..."}</p>
    </div>
  );
}
