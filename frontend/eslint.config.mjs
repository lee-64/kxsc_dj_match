import { dirname } from "path";
import { fileURLToPath } from "url";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const compat = new FlatCompat({
  baseDirectory: __dirname,
});

const eslintConfig = [
  ...compat.extends("next/core-web-vitals"),
  {
    languageOptions: {
      ecmaVersion: 2020,
      sourceType: 'module',
      parser: (await import('@babel/eslint-parser')).default,
      parserOptions: {
        requireConfigFile: false,
        ecmaFeatures: {
          jsx: true
        }
      }
    }
  }
];

export default eslintConfig;
