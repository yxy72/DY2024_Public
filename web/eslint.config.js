import globals from 'globals';
import pluginVue from 'eslint-plugin-vue';
import stylistic from '@stylistic/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import vueParser from 'vue-eslint-parser';

const commonRules = {
  '@stylistic/indent': ['error', 2, { SwitchCase: 1 }],
  '@stylistic/no-mixed-spaces-and-tabs': 'error',
  '@stylistic/space-infix-ops': 'error',
  '@stylistic/space-before-function-paren': ['error', 'never'],
  '@stylistic/space-before-blocks': 'error',
  '@stylistic/comma-spacing': ['error', { before: false, after: true }],
  '@stylistic/keyword-spacing': 'error',
  '@stylistic/arrow-parens': ['error', 'as-needed'],
};

export default [
  {
    ignores: ['dist/**', 'node_modules/**'],
  },
  {
    files: ['**/*.{js,mjs,cjs}'],
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      '@stylistic': stylistic,
    },
    rules: commonRules,
  },
  {
    files: ['**/*.{ts,tsx,d.ts,mts,cts}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      '@stylistic': stylistic,
    },
    rules: commonRules,
  },
  {
    files: ['**/*.vue'],
    languageOptions: {
      parser: vueParser,
      parserOptions: {
        parser: tsParser,
        ecmaVersion: 'latest',
        sourceType: 'module',
      },
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
    plugins: {
      '@stylistic': stylistic,
      vue: pluginVue,
    },
    rules: {
      ...commonRules,
      'vue/html-indent': ['error', 2],
    },
  },
];
