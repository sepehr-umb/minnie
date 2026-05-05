# React + TypeScript + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default defineConfig([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
Project Minnie 

Members
Ahmet A.
Ezequiel Cordero
Junior Diaz
Ramsa Ombati
Dora M. 
Sepehr Rashighi

Goal
The goal of this project is to expand the scope of the Minnie test server in its goal to teach basic backend development to UMB CS students. Through building an all in one tool for teaching students about backend programming, as well as giving them a platform to apply that newly gained knowledge. Finally, we hope to migrate this learning tool to the CS servers so that any student can access it remotely, as opposed to relying on a dedicated router.


Requirements
Set up Minnie as is and review the current setup and test it’s functionality 

Review Professor. DeBlois’s current setup on Minnie and how the education environment is set up 

Read documentation of Apache to better understand how to properly utilize it and apply it to the CS server in the future

Read documentation of Django 

Create a text file containing dialogue options for Minnie based on the progress of the user in the education module - Like a “did you mean…” prompt
Possibly a man/help page on django as a template, for the step by step

Contact Tom Mullay via email on applying Minnie’s utility onto the CS servers 

Migrate Minnie’s education module onto CS server - request a VM for testing
Decide how to handle users/accounts when using Minnie’s module through CS server

Develop lesson plan 

Test lesson plan




