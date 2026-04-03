/**
 * clockUtils.ts — re-exports from the canonical shared modules.
 *
 * All implementations now live in:
 *   pid.ts           → PID
 *   strategies.ts    → MovementStrategy, PIDMovementStrategy, EasingMovementStrategy, TickMovementStrategy
 *   clockHelpers.ts  → ClockHands, calculateHandAngles, clockHandsInRadians, polarToCartesian, formatTime
 *   clockController.ts → ClockController
 *
 * This file exists so any external import of "clockUtils" continues to resolve.
 */

export type { ClockHands } from "./clockHelpers";
export {
  calculateHandAngles,
  clockHandsInRadians,
  polarToCartesian,
  formatTime,
} from "./clockHelpers";
export { PID } from "./pid";
export type { MovementStrategy } from "./strategies";
export { PIDMovementStrategy, EasingMovementStrategy, TickMovementStrategy } from "./strategies";
export { ClockController } from "./clockController";
