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
 * Compute display-unit hand positions from a Date using local time fields.
 *
 * Returns values that naturally wrap within their display cycle:
 *   second ∈ [0, 60)   — seconds elapsed in the current minute (+ms fraction)
 *   minute ∈ [0, 60)   — minutes elapsed in the current hour   (+seconds fraction)
 *   hour   ∈ [0, 12)   — hours elapsed in the current 12-h period (+minutes fraction)
 *
 * Mirrors the visual intent of calculate_clock_hands_angles in helpers.py when
 * called with duration = 0 (i.e. displaying the current moment, not an elapsed span).
 */
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

/**
 * Convert clock hand display-units to radians.
 * Mirrors clock_hands_in_radians() in src/ui/shared/model/helpers.py
 */
export function clockHandsInRadians(hands: ClockHands): ClockHands {
  return {
    second: (hands.second / 60) * 2 * Math.PI,
    minute: (hands.minute / 60) * 2 * Math.PI,
    hour: (hands.hour / 12) * 2 * Math.PI,
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
