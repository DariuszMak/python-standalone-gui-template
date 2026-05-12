import { describe, it, expect, vi, beforeEach } from "vitest";
import { drawClock } from "./clockRenderer";

function createMockContext(): CanvasRenderingContext2D {
  return {
    canvas: document.createElement("canvas"),

    // basic state (mocked no-ops)
    save: vi.fn(),
    restore: vi.fn(),
    clearRect: vi.fn(),
    translate: vi.fn(),
    rotate: vi.fn(),
    beginPath: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    stroke: vi.fn(),
    arc: vi.fn(),
    fill: vi.fn(),

    // styling
    strokeStyle: "",
    fillStyle: "",
    lineWidth: 1,
    globalAlpha: 1,
    globalCompositeOperation: "source-over",

    // text (if used)
    font: "",
    textAlign: "left" as CanvasTextAlign,
    textBaseline: "top" as CanvasTextBaseline,
    fillText: vi.fn(),
    measureText: vi.fn(() => ({
      width: 0,
      actualBoundingBoxAscent: 0,
      actualBoundingBoxDescent: 0,
      fontBoundingBoxAscent: 0,
      fontBoundingBoxDescent: 0,
      emHeightAscent: 0,
      emHeightDescent: 0,
      alphabeticBaseline: 0,
    })),

    // transform (optional safety)
    setTransform: vi.fn(),
    getTransform: vi.fn(),

  } as unknown as CanvasRenderingContext2D;
}

describe("clockRenderer", () => {
  let ctx: CanvasRenderingContext2D;

  beforeEach(() => {
    ctx = createMockContext();
    vi.clearAllMocks();
  });

  it("renders clock without crashing", () => {
    const date = new Date(2025, 0, 1, 10, 15, 30);

    drawClock(ctx, date);
    expect(ctx.save).toHaveBeenCalled();
  });

  it("handles midnight time", () => {
    const date = new Date(2025, 0, 1, 0, 0, 0);

    drawClock(ctx, date);
    expect(ctx.beginPath).toHaveBeenCalled();
  });

  it("handles noon time", () => {
    const date = new Date(2025, 0, 1, 12, 0, 0);

    drawClock(ctx, date);
    expect(ctx.restore).toHaveBeenCalled();
  });

  it("renders seconds hand correctly", () => {
    const date = new Date(2025, 0, 1, 10, 10, 45);

    drawClock(ctx, date);
    expect(ctx.rotate).toHaveBeenCalled();
  });
});