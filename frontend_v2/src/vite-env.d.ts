/// <reference types="vite/client" />

interface ImportMetaEnv {
	readonly VITE_QDRANT_DEMO_URL?: string;
}

interface ImportMeta {
	readonly env: ImportMetaEnv;
}
