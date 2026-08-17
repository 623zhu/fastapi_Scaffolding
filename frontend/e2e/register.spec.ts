import { expect, test } from '@playwright/test'

test('registers a user', async ({ page }) => {
  await page.route('**/api/v1/users', async (route) => {
    await route.fulfill({
      status: 201,
      contentType: 'application/json',
      body: JSON.stringify({
        id: 1,
        username: 'new_user',
        email: 'new@example.com',
        is_active: true,
        created_at: '2026-08-16T12:00:00Z',
        updated_at: '2026-08-16T12:00:00Z',
      }),
    })
  })

  await page.goto('/register')
  await page.getByLabel('用户名').fill('new_user')
  await page.getByLabel('邮箱').fill('new@example.com')
  await page.getByLabel('密码', { exact: true }).fill('password123')
  await page.getByRole('button', { name: '创建账户' }).click()

  await expect(page.getByRole('status')).toContainText('账户创建成功')
  await expect(page.getByRole('status')).toContainText('new@example.com')
})

test('registration page has no horizontal overflow', async ({ page }) => {
  await page.goto('/register')
  const dimensions = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }))

  expect(dimensions.scrollWidth).toBe(dimensions.clientWidth)
})
