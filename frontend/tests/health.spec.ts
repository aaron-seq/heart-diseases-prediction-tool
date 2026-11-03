import { test, expect } from '@playwright/test'

const health = {
  status: 'healthy',
  timestamp: '2026-11-03T00:00:00Z',
  version: 'test-fixture',
  model_status: {
    is_model_healthy: true, model_version: 'synthetic', last_training_date: 'unknown',
    model_accuracy: 0, total_predictions_made: 0, average_response_time_ms: 0,
  },
}

test('health request uses API configuration and prevents overlapping requests', async ({ page, baseURL }, testInfo) => {
  const apiURL = testInfo.project.name === 'configured-api'
    ? 'http://127.0.0.1:4180/api/v1/health'
    : `${baseURL}/api/v1/health`
  let calls = 0
  let release: () => void = () => {}
  const pending = new Promise<void>((resolve) => { release = resolve })
  const unexpected: string[] = []
  await page.route('**/*', async (route) => {
    const url = route.request().url()
    if (url === apiURL) {
      calls += 1
      await pending
      await route.fulfill({ json: health })
    } else if (url.startsWith(`${baseURL}/`) && !url.includes('/api/')) {
      await route.continue()
    } else {
      unexpected.push(url)
      await route.abort()
    }
  })
  await page.goto('/')
  const button = page.getByRole('button', { name: 'Ping API' })
  await button.click()
  try {
    await expect(button).toBeDisabled()
    await expect(page.getByRole('status')).toContainText('loading')
    await expect.poll(() => calls).toBe(1)
    await button.dispatchEvent('click')
    expect(calls).toBe(1)
  } finally {
    release()
  }
  await expect(page.getByRole('status')).toContainText('ok')
  await expect(page.locator('pre')).toContainText('synthetic')
  await expect(button).toBeEnabled()
  expect(calls).toBe(1)
  expect(unexpected).toEqual([])
})

for (const failure of ['HTTP 503', 'network'] as const) {
  test(`${failure} error is shown and a later request recovers`, async ({ page, baseURL }, testInfo) => {
    const apiURL = testInfo.project.name === 'configured-api'
      ? 'http://127.0.0.1:4180/api/v1/health'
      : `${baseURL}/api/v1/health`
    let calls = 0
    await page.route('**/*', async (route) => {
      const url = route.request().url()
      if (url === apiURL) {
        calls += 1
        if (calls === 1 && failure === 'network') {
          await route.abort('failed')
        } else {
          await route.fulfill(calls === 1
            ? { status: 503, json: { detail: 'fixture not ready' } }
            : { json: health })
        }
      } else if (url.startsWith(`${baseURL}/`) && !url.includes('/api/')) {
        await route.continue()
      } else {
        await route.abort()
      }
    })
    await page.goto('/')
    const button = page.getByRole('button', { name: 'Ping API' })
    await button.click()
    await expect(page.getByRole('status')).toContainText('error')
    await expect(page.locator('pre')).toContainText(failure === 'network'
      ? 'Unable to connect to the server'
      : 'Service temporarily unavailable')
    await button.click()
    await expect(page.getByRole('status')).toContainText('ok')
    await expect(page.locator('pre')).toContainText('synthetic')
    expect(calls).toBe(2)
  })
}
