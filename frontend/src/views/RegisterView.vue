<script setup lang="ts">
import {
  AlertCircle,
  CheckCircle2,
  Eye,
  EyeOff,
  LockKeyhole,
  Mail,
  UserRound,
  UserRoundPlus,
} from '@lucide/vue'
import { computed, reactive, ref } from 'vue'

import { ApiError } from '@/api/client'
import { registerUser } from '@/api/users'
import type { User } from '@/types/user'

const appName = import.meta.env.VITE_APP_TITLE || 'FastAPI Vue Starter'
const form = reactive({ username: '', email: '', password: '' })
const showPassword = ref(false)
const submitting = ref(false)
const errorMessage = ref('')
const createdUser = ref<User | null>(null)

const canSubmit = computed(
  () =>
    form.username.trim().length >= 3 &&
    form.email.trim().length > 0 &&
    form.password.length >= 8 &&
    !submitting.value,
)

async function submitRegistration() {
  if (!canSubmit.value) return

  submitting.value = true
  errorMessage.value = ''

  try {
    createdUser.value = await registerUser({
      username: form.username.trim(),
      email: form.email.trim(),
      password: form.password,
    })
  } catch (error) {
    if (error instanceof ApiError && error.status === 409) {
      errorMessage.value = '用户名或邮箱已存在'
    } else {
      errorMessage.value = error instanceof ApiError ? error.message : '无法连接到服务，请稍后重试'
    }
  } finally {
    submitting.value = false
  }
}

function resetForm() {
  form.username = ''
  form.email = ''
  form.password = ''
  errorMessage.value = ''
  createdUser.value = null
}
</script>

<template>
  <div class="auth-shell">
    <header class="app-header">
      <div class="brand-mark" aria-hidden="true">
        <UserRoundPlus :size="19" :stroke-width="2" />
      </div>
      <span class="brand-name">{{ appName }}</span>
      <span class="header-section">账户注册</span>
    </header>

    <main class="auth-main">
      <section class="registration-intro" aria-labelledby="registration-title">
        <p class="section-label">新用户</p>
        <h1 id="registration-title">创建账户</h1>
        <p>填写账户信息以完成注册。</p>
      </section>

      <section class="registration-panel" aria-label="用户注册表单">
        <div v-if="createdUser" class="success-state" role="status">
          <CheckCircle2 :size="32" :stroke-width="1.8" aria-hidden="true" />
          <div>
            <h2>账户创建成功</h2>
            <p>
              <strong>{{ createdUser.username }}</strong>
              <span>{{ createdUser.email }}</span>
            </p>
          </div>
          <button class="secondary-button" type="button" @click="resetForm">
            <UserRoundPlus :size="17" aria-hidden="true" />
            注册另一个账户
          </button>
        </div>

        <form v-else class="registration-form" @submit.prevent="submitRegistration">
          <div class="field-group">
            <label for="username">
              <UserRound :size="16" aria-hidden="true" />
              用户名
            </label>
            <input
              id="username"
              v-model="form.username"
              name="username"
              type="text"
              autocomplete="username"
              minlength="3"
              maxlength="50"
              placeholder="至少 3 个字符"
              required
            />
          </div>

          <div class="field-group">
            <label for="email">
              <Mail :size="16" aria-hidden="true" />
              邮箱
            </label>
            <input
              id="email"
              v-model="form.email"
              name="email"
              type="email"
              autocomplete="email"
              maxlength="320"
              placeholder="name@example.com"
              required
            />
          </div>

          <div class="field-group">
            <label for="password">
              <LockKeyhole :size="16" aria-hidden="true" />
              密码
            </label>
            <div class="password-control">
              <input
                id="password"
                v-model="form.password"
                name="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
                minlength="8"
                maxlength="128"
                placeholder="至少 8 个字符"
                required
              />
              <button
                class="visibility-button"
                type="button"
                :aria-label="showPassword ? '隐藏密码' : '显示密码'"
                :title="showPassword ? '隐藏密码' : '显示密码'"
                @click="showPassword = !showPassword"
              >
                <EyeOff v-if="showPassword" :size="18" aria-hidden="true" />
                <Eye v-else :size="18" aria-hidden="true" />
              </button>
            </div>
          </div>

          <div v-if="errorMessage" class="error-message" role="alert">
            <AlertCircle :size="18" aria-hidden="true" />
            <span>{{ errorMessage }}</span>
          </div>

          <button class="submit-button" type="submit" :disabled="!canSubmit">
            <UserRoundPlus :size="18" aria-hidden="true" />
            {{ submitting ? '正在创建...' : '创建账户' }}
          </button>
        </form>
      </section>
    </main>
  </div>
</template>

<style scoped>
.auth-shell {
  min-height: 100vh;
}

.app-header {
  display: flex;
  align-items: center;
  min-height: 60px;
  padding: 0 28px;
  border-bottom: 1px solid var(--border-default);
  background: var(--surface-panel);
}

.brand-mark {
  display: grid;
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  place-items: center;
  border-radius: 6px;
  color: #ffffff;
  background: var(--accent);
}

.brand-name {
  min-width: 0;
  margin-left: 10px;
  overflow: hidden;
  color: var(--text-primary);
  font-size: 15px;
  font-weight: 700;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.header-section {
  margin-left: auto;
  padding-left: 20px;
  color: var(--text-secondary);
  font-size: 13px;
}

.auth-main {
  width: min(100% - 32px, 560px);
  margin: 0 auto;
  padding: 64px 0 72px;
}

.registration-intro {
  margin-bottom: 22px;
}

.section-label {
  margin: 0 0 8px;
  color: var(--accent);
  font-size: 13px;
  font-weight: 700;
}

.registration-intro h1 {
  margin: 0;
  color: var(--text-primary);
  font-size: 30px;
  font-weight: 750;
  line-height: 1.25;
}

.registration-intro > p:last-child {
  margin: 10px 0 0;
  color: var(--text-secondary);
  font-size: 15px;
}

.registration-panel {
  min-height: 430px;
  padding: 28px;
  border: 1px solid var(--border-default);
  border-radius: 8px;
  background: var(--surface-panel);
  box-shadow: 0 8px 24px rgba(24, 32, 40, 0.07);
}

.registration-form {
  display: grid;
  gap: 22px;
}

.field-group {
  display: grid;
  gap: 8px;
}

.field-group label {
  display: flex;
  align-items: center;
  gap: 7px;
  color: var(--text-primary);
  font-size: 14px;
  font-weight: 650;
}

.field-group input {
  width: 100%;
  height: 44px;
  padding: 0 12px;
  border: 1px solid var(--border-default);
  border-radius: 6px;
  color: var(--text-primary);
  background: #ffffff;
  transition:
    border-color 140ms ease,
    box-shadow 140ms ease;
}

.field-group input:hover {
  border-color: var(--border-strong);
}

.field-group input:focus {
  border-color: var(--accent);
  outline: none;
  box-shadow: 0 0 0 3px var(--focus-ring);
}

.field-group input::placeholder {
  color: #8b969f;
}

.password-control {
  position: relative;
}

.password-control input {
  padding-right: 48px;
}

.visibility-button {
  position: absolute;
  top: 2px;
  right: 2px;
  display: grid;
  width: 40px;
  height: 40px;
  place-items: center;
  border: 0;
  border-radius: 5px;
  color: var(--text-secondary);
  background: transparent;
}

.visibility-button:hover {
  color: var(--text-primary);
  background: var(--surface-muted);
}

.submit-button,
.secondary-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 44px;
  border-radius: 6px;
  font-weight: 700;
}

.submit-button {
  width: 100%;
  margin-top: 2px;
  border: 1px solid var(--accent);
  color: #ffffff;
  background: var(--accent);
}

.submit-button:hover:not(:disabled) {
  border-color: var(--accent-hover);
  background: var(--accent-hover);
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.52;
}

.error-message {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 11px 12px;
  border-left: 3px solid var(--danger);
  color: var(--danger);
  background: var(--danger-surface);
  font-size: 14px;
}

.error-message svg {
  flex: 0 0 auto;
  margin-top: 1px;
}

.success-state {
  display: grid;
  min-height: 372px;
  align-content: center;
  justify-items: center;
  color: var(--success);
  text-align: center;
}

.success-state h2 {
  margin: 14px 0 8px;
  color: var(--text-primary);
  font-size: 22px;
  font-weight: 750;
}

.success-state p {
  display: grid;
  gap: 4px;
  margin: 0;
  color: var(--text-secondary);
  font-size: 14px;
}

.success-state strong {
  color: var(--text-primary);
  font-size: 16px;
}

.secondary-button {
  margin-top: 28px;
  padding: 0 16px;
  border: 1px solid var(--border-strong);
  color: var(--text-primary);
  background: #ffffff;
}

.secondary-button:hover {
  border-color: var(--accent);
  color: var(--accent);
}

@media (max-width: 600px) {
  .app-header {
    min-height: 56px;
    padding: 0 16px;
  }

  .brand-name {
    max-width: 180px;
  }

  .header-section {
    display: none;
  }

  .auth-main {
    width: min(100% - 24px, 560px);
    padding: 36px 0 48px;
  }

  .registration-intro h1 {
    font-size: 26px;
  }

  .registration-panel {
    min-height: 420px;
    padding: 22px 18px;
  }
}
</style>
