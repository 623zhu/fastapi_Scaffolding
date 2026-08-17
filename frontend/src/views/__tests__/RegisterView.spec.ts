import { flushPromises, mount } from '@vue/test-utils'
import { afterEach, describe, expect, it, vi } from 'vitest'

import RegisterView from '../RegisterView.vue'

describe('RegisterView', () => {
  afterEach(() => {
    vi.unstubAllGlobals()
  })

  it('submits the registration form and displays the created user', async () => {
    const fetchMock = vi.fn<typeof fetch>().mockResolvedValue(
      new Response(
        JSON.stringify({
          id: 1,
          username: 'new_user',
          email: 'new@example.com',
          is_active: true,
          created_at: '2026-08-16T12:00:00Z',
          updated_at: '2026-08-16T12:00:00Z',
        }),
        { status: 201, headers: { 'Content-Type': 'application/json' } },
      ),
    )
    vi.stubGlobal('fetch', fetchMock)

    const wrapper = mount(RegisterView)
    await wrapper.get('#username').setValue('new_user')
    await wrapper.get('#email').setValue('new@example.com')
    await wrapper.get('#password').setValue('password123')
    await wrapper.get('form').trigger('submit')
    await flushPromises()

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/users',
      expect.objectContaining({ method: 'POST' }),
    )
    expect(wrapper.text()).toContain('账户创建成功')
    expect(wrapper.text()).toContain('new@example.com')
  })
})
