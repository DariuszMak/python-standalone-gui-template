/**
 * Clock utility helpers — mirrors:
 *   src/ui/shared/helpers.py          (calculateHandAngles, polarToCartesian, formatTime)
 *   src/ui/shared/model/helpers.py    (clockHandsInRadians)
 */

export interface ClockHands {
  second: number;
  minute: number;
  hour: number;
}

/**
 * Compute UNBOUNDED cumulative hand positions from a start anchor and an
 * elapsed duration in seconds.
 *
 * Values grow without bound — they are NOT wrapped to [0, 60) / [0, 12).
 * This is intentional: the PID controller tracks a monotonically increasing
 * target so it never sees a discontinuous wrap (e.g. second 59 → 0) that
 * would drive a hand backwards.
 *
 *   second = totalSeconds          (e.g. 3723.0  after 1 h 2 m 3 s)
 *   minute = totalSeconds / 60     (e.g.   62.05)
 *   hour   = totalSeconds / 3600   (e.g.    1.034…)
 *
 * Mirrors calculate_clock_hands_angles(start_dt, duration) in helpers.py.
 *
 * For rendering, pass the result through clockHandsInRadians() which applies
 * modulo before the trig conversion.
 */
export function calculateHandAngles(startDt: Date, elapsedSeconds: number): ClockHands {
  // Express the start instant as local seconds within the current 12-hour
  // period so the display reflects local time (matches Python display_tz).
  const h = startDt.getHours() % 12;
  const m = startDt.getMinutes();
  const s = startDt.getSeconds();
  const ms = startDt.getMilliseconds();
  const startTotalSeconds = h * 3600 + m * 60 + s + ms / 1000;

  const totalSeconds = startTotalSeconds + elapsedSeconds;

  return {
    second: totalSeconds,
    minute: totalSeconds / 60,
    hour: totalSeconds / 3600,
  };
}

/**
 * Convert unbounded hand totals to radians, applying modulo so the canvas
 * angle stays within one revolution.
 *
 * Mirrors clock_hands_in_radians() in src/ui/shared/model/helpers.py.
 */
export function clockHandsInRadians(hands: ClockHands): ClockHands {
  return {
    second: ((hands.second % 60) / 60) * 2 * Math.PI,
    minute: ((hands.minute % 60) / 60) * 2 * Math.PI,
    hour: ((hands.hour % 12) / 12) * 2 * Math.PI,
  };
}

/**
 * Polar → Cartesian conversion with clock convention (0 rad = 12 o'clock, CW positive).
 * Mirrors polar_to_cartesian() in src/ui/shared/helpers.py
 */
export function polarToCartesian(
  cx: number,
  cy: number,
  length: number,
  angleRad: number,
): [number, number] {
  return [cx + Math.sin(angleRad) * length, cy - Math.cos(angleRad) * length];
}

/**
 * Format a Date as HH:MM:SS.mmm using local time fields.
 * Mirrors format_datetime() in src/ui/shared/helpers.py
 */
export function formatTime(dt: Date): string {
  const h = String(dt.getHours()).padStart(2, "0");
  const m = String(dt.getMinutes()).padStart(2, "0");
  const s = String(dt.getSeconds()).padStart(2, "0");
  const ms = String(Math.floor(dt.getMilliseconds())).padStart(3, "0");
  return `${h}:${m}:${s}.${ms}`;
}
