import js from "@eslint/js";
import globals from "globals";

export default [
  {
    ignores: [
      "dist",
      "node_modules",
    ],
  },

  {
    files: [
      "src/**/*.{js,jsx}",
    ],

    ...js.configs.recommended,

    languageOptions: {
      ecmaVersion: "latest",
      sourceType: "module",

      globals: {
        ...globals.browser,
        ...globals.es2021,
      },

      parserOptions: {
        ecmaFeatures: {
          jsx: true,
        },
      },
    },

    rules: {
      ...js.configs.recommended.rules,

      "no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
        },
      ],
    },
  },
];
