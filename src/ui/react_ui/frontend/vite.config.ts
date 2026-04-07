import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: path.resolve(__dirname, "../src/static"),
    emptyOutDir: true,
  },
  test: {
    environment: "jsdom",
  },
});