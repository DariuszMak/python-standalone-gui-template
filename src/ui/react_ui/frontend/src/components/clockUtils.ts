// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

export interface ClockHands {
  second: number;
  minute: number;
  hour: number;
}

// ---------------------------------------------------------------------------
// PID controller
// ---------------------------------------------------------------------------

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

// ---------------------------------------------------------------------------
// PID movement strategy
// ---------------------------------------------------------------------------

export interface PIDStrategy {
  pid: PID;
  update(current: number, target: number): number;
  reset(): void;
}

export function makePIDStrategy(kp: number, ki: number, kd: number): PIDStrategy {
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

// ---------------------------------------------------------------------------
// Clock maths
// ---------------------------------------------------------------------------

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