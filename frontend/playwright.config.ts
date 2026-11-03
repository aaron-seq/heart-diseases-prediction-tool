import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './tests',
  fullyParallel: false,
  workers: 1,
  retries: 0,
  use: { browserName: 'chromium', trace: 'off' },
  projects: [
    { name: 'same-origin', use: { baseURL: 'http://127.0.0.1:4173' } },
    { name: 'configured-api', use: { baseURL: 'http://127.0.0.1:4174' } },
  ],
  webServer: [
    { command: 'node tests/server.mjs 4173', url: 'http://127.0.0.1:4173', reuseExistingServer: false },
    { command: 'node tests/server.mjs 4174 http://127.0.0.1:4180/', url: 'http://127.0.0.1:4174', reuseExistingServer: false },
  ],
})
