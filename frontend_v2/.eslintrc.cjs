const path = require('path');

const tsconfigPath = path.join(__dirname, 'tsconfig.json');

module.exports = {
	env: { browser: true, es2020: true },
	parser: '@typescript-eslint/parser',
	parserOptions: { ecmaVersion: 'latest', sourceType: 'module', project: [tsconfigPath] },
	plugins: ['react-refresh'],
	extends: [
		'eslint:recommended',
		'plugin:@typescript-eslint/recommended',
		'plugin:react-hooks/recommended',
		'plugin:react/recommended',
		'plugin:import/typescript',
		'plugin:prettier/recommended',
	],
	rules: {
		'react-refresh/only-export-components': 'warn',
		'react/react-in-jsx-scope': 0,
		'react-refresh/only-export-components': 0,
		'react-hooks/exhaustive-deps': 0,
	},
	settings: {
		react: {
			version: 'detect',
		},
	},
};
