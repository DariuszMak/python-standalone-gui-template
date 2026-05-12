import { beforeEach, afterEach, describe, expect, it, vi } from "vitest";
import { renderClock } from "./clockRenderer";

interface MockContext {
  clearRect: ReturnType<typeof vi.fn>;
  beginPath: ReturnType<typeof vi.fn>;
  arc: ReturnType<typeof vi.fn>;
  fill: ReturnType<typeof vi.fn>;
  stroke: ReturnType<typeof vi.fn>;
  moveTo: ReturnType<typeof vi.fn>;
  lineTo: ReturnType<typeof vi.fn>;
  fillText: ReturnType<typeof vi.fn>;
  save: ReturnType<typeof vi.fn>;
  restore: ReturnType<typeof vi.fn>;
  translate: ReturnType<typeof vi.fn>;
  rotate: ReturnType<typeof vi.fn>;
}

const createMockContext = (): CanvasRenderingContext2D =>
  ({
    clearRect: vi.fn(),
    beginPath: vi.fn(),
    arc: vi.fn(),
    fill: vi.fn(),
    stroke: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    fillText: vi.fn(),
    save: vi.fn(),
    restore: vi.fn(),
    translate: vi.fn(),
    rotate: vi.fn(),
  }) as unknown as CanvasRenderingContext2D;

const createMediaQueryList = (matches: boolean): MediaQueryList => ({
  matches,
  media: "",
  onchange: null,
  addListener: vi.fn(),
  removeListener: vi.fn(),
  addEventListener: vi.fn(),
  removeEventListener: vi.fn(),
  dispatchEvent: vi.fn(),
});

describe("renderClock", () => {
  let context: MockContext;
  let canvas: HTMLCanvasElement;

  beforeEach(() => {
    Object.defineProperty(window, "matchMedia", {
      writable: true,
      value: vi.fn().mockImplementation(() => createMediaQueryList(false)),
    });

    context = createMockContext() as unknown as MockContext;

    canvas = {
      width: 300,
      height: 300,
      getContext: vi.fn(() => context),
    } as unknown as HTMLCanvasElement;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders without throwing", () => {
    expect(() => {
      renderClock(canvas, mockContext, new Date(), "12:00:00");
    }).not.toThrow();
  });

  it("clears canvas before drawing", () => {
    renderClock(canvas, mockContext, new Date(), "12:00:00");

    expect(context.clearRect).toHaveBeenCalled();
  });

  it("draws clock hands", () => {
    renderClock(canvas, mockContext, new Date(), "12:00:00");

    expect(context.lineTo).toHaveBeenCalled();
  });

  it("draws time label", () => {
    renderClock(canvas, mockContext, new Date(), "12:00:00");

    expect(context.fillText).toHaveBeenCalledWith(
      "12:00:00",
      expect.any(Number),
      expect.any(Number),
    );
  });

  it("handles dark mode", () => {
    window.matchMedia = vi.fn().mockImplementation(() => createMediaQueryList(true));

    renderClock(canvas, mockContext, new Date(), "12:00:00");

    expect(window.matchMedia).toHaveBeenCalled();
  });
});
