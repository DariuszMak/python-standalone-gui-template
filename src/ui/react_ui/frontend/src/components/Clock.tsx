import { useEffect, useRef, useState, useCallback } from "react";

export interface ClockHands {
  second: number;
  minute: number;
  hour: number;
}

export class PID {
  private kp: number;
  private ki: number;
  private kd: number;
  /** @internal */ _prevError = 0;
  /** @internal */ _integral = 0;

  constructor(kp: number, ki: number, kd: number) {
    this.kp = kp;
    this.ki = ki;
    this.kd = kd;
  }

  update(error: number): number {
    this._integral += error;
    const derivative = error - this._prevError;
    this._prevError = error;
    return this.kp * error + this.ki * this._integral + this.kd * derivative;
  }

  reset(): void {
    this._prevError = 0;
    this._integral = 0;
  }
}

interface PIDStrategy {
  pid: PID;
  update(current: number, target: number): number;
  reset(): void;
}

function makePIDStrategy(kp: number, ki: number, kd: number): PIDStrategy {
  const pid = new PID(kp, ki, kd);
  return {
    pid,
    update(current: number, target: number): number {
      const error = target - current;
      return current + pid.update(error);
    },
    reset(): void {
      pid.reset();
    },
  };
}

export function calculateHandAngles(dt: Date): ClockHands {
  const h = dt.getHours() % 12;
  const m = dt.getMinutes();
  const s = dt.getSeconds();
  const ms = dt.getMilliseconds();

  const totalSeconds = h * 3600 + m * 60 + s + ms / 1000;

  return {
    second: totalSeconds % 60,
    minute: (totalSeconds / 60) % 60,
    hour: (totalSeconds / 3600) % 12,
  };
}

export function polarToCartesian(
  cx: number,
  cy: number,
  length: number,
  angleRad: number,
): [number, number] {
  return [cx + Math.sin(angleRad) * length, cy - Math.cos(angleRad) * length];
}

export function formatTime(dt: Date): string {
  const h = String(dt.getHours()).padStart(2, "0");
  const m = String(dt.getMinutes()).padStart(2, "0");
  const s = String(dt.getSeconds()).padStart(2, "0");
  const ms = String(Math.floor(dt.getMilliseconds())).padStart(3, "0");
  return `${h}:${m}:${s}.${ms}`;
}

export function Clock() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animRef = useRef<number>(0);
  const serverAnchorRef = useRef<Date>(new Date(0));
  const wallAnchorRef = useRef<number>(performance.now());
  const handsRef = useRef<ClockHands>({ second: 0, minute: 0, hour: 0 });
  const strategiesRef = useRef([
    makePIDStrategy(0.15, 0.005, 0.005),
    makePIDStrategy(0.08, 0.004, 0.004),
    makePIDStrategy(0.08, 0.002, 0.002),
  ]);

  const [datetime, setDatetime] = useState<string | null>(null);
  const [status, setStatus] = useState<"loading" | "ok" | "error">("loading");

  const fetchTime = useCallback(async () => {
    setStatus("loading");
    try {
      const res = await fetch("http://localhost:8000/time");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data: { datetime: string } = await res.json();
      setDatetime(data.datetime);
      serverAnchorRef.current = new Date(data.datetime);
      wallAnchorRef.current = performance.now();
      handsRef.current = { second: 0, minute: 0, hour: 0 };
      strategiesRef.current.forEach((s) => s.reset());
      setStatus("ok");
    } catch {
      setStatus("error");
    }
  }, []);

  useEffect(() => {
    fetchTime();
  }, [fetchTime]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const draw = () => {
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      const elapsed = (performance.now() - wallAnchorRef.current) / 1000;
      const now = new Date(serverAnchorRef.current.getTime() + elapsed * 1000);

      const target = calculateHandAngles(now);
      const [ss, sm, sh] = strategiesRef.current;
      handsRef.current = {
        second: ss.update(handsRef.current.second, target.second),
        minute: sm.update(handsRef.current.minute, target.minute),
        hour: sh.update(handsRef.current.hour, target.hour),
      };

      const dpr = window.devicePixelRatio || 1;
      const size = canvas.clientWidth;
      if (canvas.width !== size * dpr || canvas.height !== size * dpr) {
        canvas.width = size * dpr;
        canvas.height = size * dpr;
        ctx.scale(dpr, dpr);
      }

      const cx = size / 2;
      const cy = size / 2;
      const radius = size * 0.42;

      ctx.clearRect(0, 0, size, size);

      const isDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

      ctx.fillStyle = isDark ? "#1a1a1a" : "#ffffff";
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = isDark ? "#555" : "#ccc";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.arc(cx, cy, radius, 0, Math.PI * 2);
      ctx.stroke();

      for (let i = 0; i < 60; i++) {
        const angle = (i / 60) * Math.PI * 2;
        const isHour = i % 5 === 0;
        const outer = polarToCartesian(cx, cy, radius, angle);
        const inner = polarToCartesian(cx, cy, radius - (isHour ? 10 : 5), angle);
        ctx.strokeStyle = isDark ? "#888" : "#aaa";
        ctx.lineWidth = isHour ? 2.5 : 1;
        ctx.beginPath();
        ctx.moveTo(inner[0], inner[1]);
        ctx.lineTo(outer[0], outer[1]);
        ctx.stroke();
      }

      const fontSize = Math.max(8, Math.floor(radius * 0.13));
      ctx.font = `${fontSize}px system-ui, Arial, sans-serif`;
      ctx.fillStyle = isDark ? "#ddd" : "#333";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      for (let i = 0; i < 12; i++) {
        const angle = (i / 12) * Math.PI * 2;
        const [tx, ty] = polarToCartesian(cx, cy, radius - fontSize * 1.8, angle);
        const label = ((i + 11) % 12) + 1;
        ctx.fillText(String(label), tx, ty);
      }

      const h = handsRef.current;

      const hourAngle = (h.hour / 12) * Math.PI * 2;
      const minuteAngle = (h.minute / 60) * Math.PI * 2;
      const secondAngle = (h.second / 60) * Math.PI * 2;

      const [hx, hy] = polarToCartesian(cx, cy, radius * 0.5, hourAngle);
      ctx.strokeStyle = isDark ? "#ffffff" : "#222";
      ctx.lineWidth = 6;
      ctx.lineCap = "round";
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(hx, hy);
      ctx.stroke();

      const [mx, my] = polarToCartesian(cx, cy, radius * 0.7, minuteAngle);
      ctx.strokeStyle = isDark ? "#cccccc" : "#444";
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(mx, my);
      ctx.stroke();

      const [sx, sy] = polarToCartesian(cx, cy, radius * 0.88, secondAngle);
      ctx.strokeStyle = "#ff3333";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(sx, sy);
      ctx.stroke();

      ctx.fillStyle = isDark ? "#ff3333" : "#cc0000";
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();

      const timeStr = formatTime(now);
      const tfSize = Math.max(10, Math.floor(radius * 0.12));
      ctx.font = `${tfSize}px "Consolas", monospace`;
      ctx.fillStyle = isDark ? "#96ffbe" : "#1a7a40";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(timeStr, cx, cy + radius * 0.62);

      animRef.current = requestAnimationFrame(draw);
    };

    animRef.current = requestAnimationFrame(draw);
    return () => cancelAnimationFrame(animRef.current);
  }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1rem" }}>
      <h1 style={{ margin: 0 }}>Current datetime</h1>
      {datetime && <p style={{ margin: 0 }}>{datetime}</p>}
      <canvas
        ref={canvasRef}
        style={{
          width: "300px",
          height: "300px",
          borderRadius: "50%",
          display: "block",
        }}
      />
      <button onClick={fetchTime} disabled={status === "loading"}>
        {status === "loading" ? "Loading…" : "Reload time"}
      </button>
      {status === "error" && <p style={{ color: "red", margin: 0 }}>Failed to load time</p>}
    </div>
  );
}
