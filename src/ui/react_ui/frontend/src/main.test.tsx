import { describe, it, expect, vi } from "vitest";

describe("main.tsx", () => {
  it("throws when root element missing", async () => {
    const original = document.getElementById;

    vi.spyOn(document, "getElementById").mockReturnValue(null);

    await expect(import("./main")).rejects.toThrow("Root element not found");

    document.getElementById = original;
  });
});