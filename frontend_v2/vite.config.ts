import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import path from "path";
// https://vitejs.dev/config/

const defaultConfig = {
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
};

export default defineConfig(({ command, mode }) => {
  if (command === "serve") {
    const isDev = mode === "development";

    return {
      ...defaultConfig,
      server: {
        proxy: {
          "/api": {
            target: isDev
              ? "https://demo.qdrant.tech"
              : "https://demo.qdrant.tech",
            changeOrigin: true,
          },
        },
      },
    };
  } else {
    return defaultConfig;
  }
});
