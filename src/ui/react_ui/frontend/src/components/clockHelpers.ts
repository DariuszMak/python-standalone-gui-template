export interface ClockHands {
  second: number;
  minute: number;
  hour: number;
}

export function calculateHandAngles(startDt: Date, elapsedSeconds: number): ClockHands {
  // Use UTC methods to match your Vitest 'utcDate' helper
  const h = startDt.getUTCHours() % 12;
  const m = startDt.getUTCMinutes();
  const s = startDt.getUTCSeconds();
  const ms = startDt.getUTCMilliseconds();

  const startTotalSeconds = h * 3600 + m * 60 + s + ms / 1000;
  const totalSeconds = startTotalSeconds + elapsedSeconds;

  return {
    second: totalSeconds,
    minute: totalSeconds / 60,
    hour: totalSeconds / 3600,
  };
}

export function clockHandsInRadians(hands: ClockHands): ClockHands {
  return {
    second: ((hands.second % 60) / 60) * 2 * Math.PI,
    minute: ((hands.minute % 60) / 60) * 2 * Math.PI,
    hour: ((hands.hour % 12) / 12) * 2 * Math.PI,
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
