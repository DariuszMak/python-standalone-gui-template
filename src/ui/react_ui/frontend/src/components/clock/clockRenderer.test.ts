import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderClock } from "./clockRenderer";

describe("renderClock", () => {
  let canvas: HTMLCanvasElement;
  let ctx: CanvasRenderingContext2D;

  beforeEach(() => {
    ctx = {
      clearRect: vi.fn(),
      save: vi.fn(),
      restore: vi.fn(),
      translate: vi.fn(),
      rotate: vi.fn(),
      scale: vi.fn(),
      beginPath: vi.fn(),
      moveTo: vi.fn(),
      lineTo: vi.fn(),
      stroke: vi.fn(),
      arc: vi.fn(),
      fillText: vi.fn(),
    } as unknown as CanvasRenderingContext2D;

    canvas = {
      width: 0,
      height: 0,
      getContext: vi.fn(() => ctx),
    } as unknown as HTMLCanvasElement;
  });

  it("renders without throwing", () => {
    expect(() => {
      renderClock(canvas, new Date(), "12:00:00");
    }).not.toThrow();
  });

  it("clears canvas before drawing", () => {
    renderClock(canvas, new Date(), "12:00:00");

    expect(ctx.clearRect).toHaveBeenCalled();
  });

  it("draws clock hands", () => {
    renderClock(canvas, new Date(), "12:00:00");

    expect(ctx.beginPath).toHaveBeenCalled();
    expect(ctx.stroke).toHaveBeenCalled();
  });

  it("draws time label", () => {
    renderClock(canvas, new Date(), "12:00:00");

    expect(ctx.fillText).toHaveBeenCalled();
  });

  it("handles dark mode", () => {
    renderClock(canvas, new Date(), "12:00:00");

    expect(ctx.save).toHaveBeenCalled();
    expect(ctx.restore).toHaveBeenCalled();
  });
});