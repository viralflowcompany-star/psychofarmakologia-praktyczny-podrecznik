import { defineConfig } from "vite";
import { sites } from "@openai/sites-vite-plugin";
import { fileURLToPath } from "node:url";

const projectFile = (path) => fileURLToPath(new URL(path, import.meta.url));

export default defineConfig({
  plugins: [sites()],
  build: {
    outDir: "dist/client",
    rollupOptions: {
      input: {
        main: projectFile("./index.html"),
        dziekujemy: projectFile("./dziekujemy/index.html"),
      },
    },
  },
});
