<template>
  <div class="home-wrapper">
    <div class="header-image"></div>
    <div class="header-overlay"></div>

    <div class="content-wrapper">
      <v-container class="register-container">
        <v-card class="register-card">
          <div class="register-background"></div>
          <div class="register-content">
            <h2 class="text-center mb-6">Register</h2>

            <!-- Error Alert -->
            <v-alert
              v-if="error"
              type="error"
              variant="tonal"
              closable
              class="mb-4"
            >
              {{ error }}
            </v-alert>

            <v-form @submit.prevent="handleRegister" ref="form">
              <!-- Email Field -->
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                variant="outlined"
                prepend-icon="mdi-email"
                class="mb-4"
                required
                error-messages-class="custom-error-message"
              ></v-text-field>

              <!-- Password Field -->
              <v-text-field
                v-model="password"
                label="Password"
                :type="showPassword ? 'text' : 'password'"
                :rules="[rules.required, rules.min]"
                variant="outlined"
                prepend-icon="mdi-lock"
                :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                @click:append="showPassword = !showPassword"
                class="mb-6"
                required
                error-messages-class="custom-error-message"
              ></v-text-field>

              <!-- Login Button -->
              <v-btn
                type="submit"
                :loading="loading"
                block
                class="register-btn mb-4"
                height="44"
              >
                Register
              </v-btn>

              <!-- Register Link -->
              <div class="text-center">
                <span class="text-medium-emphasis">Already have an account?</span>
                <v-btn
                  variant="text"
                  to="/login"
                  class="login-link ms-2"
                >
                  Login now
                </v-btn>
              </div>
            </v-form>
          </div>
        </v-card>
      </v-container>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const form = ref(null)
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)

const rules = {
  required: (v: string) => !!v || 'This field is required',
  email: (v: string) => /.+@.+\..+/.test(v) || 'Invalid email address',
  min: (v: string) => v.length >= 6 || 'Password must be at least 6 characters'
}

const handleRegister = async () => {
  if (!form.value) return

  const { valid } = await form.value.validate()

  if (!valid) return

  try {
    loading.value = true
    error.value = ''

    // Call the login method from the auth store
    const success = await authStore.register({
      email: email.value, // Backend expects username field for email
      password: password.value
    })

    if (success) {
      router.push('/')
    } else {
      error.value = 'This email is already taken.' // Redirect to home page after successfully registering the user
    }
  } catch (err) {
    error.value = 'This email is already taken.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  max-width: 500px;
  margin-top: -100px;

}

.register-card {
  background: rgba(45, 55, 75, 0.8);
  border-radius: 20px;
  border: 2px solid #42ddf2;
  box-shadow: 0 0 15px rgba(8, 87, 144, 0.3);
  backdrop-filter: blur(10px);
  position: relative;
  overflow: hidden;
  padding: 40px;
}

.register-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-position: center;
  background-size: cover;
  opacity: 0.1;
  z-index: 1;
}

.register-content {
  position: relative;
  z-index: 2;
}

.register-btn {
  background: #42ddf2 !important;
  color: #171c26 !important;
  font-weight: bold;
  letter-spacing: 1px;
  text-transform: uppercase;
  transition: all 0.3s;
}

.register-btn:hover {
  background: #fed854 !important;
  box-shadow: 0 0 15px rgba(254, 216, 84, 0.3);
}

:deep(.v-messages__message) {
  color: #fed854 !important;
  font-size: 14px;
}

:deep(.v-field--error) {
  --v-field-border-color: #fed854 !important;
}

:deep(.v-field--variant-outlined.v-field--error) {
  border-color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline) {
  color: #fed854 !important;
}

:deep(.v-field--error .v-field__outline__start),
:deep(.v-field--error .v-field__outline__end),
:deep(.v-field--error .v-field__outline__notch) {
  border-color: #fed854 !important;
}

:deep(.v-alert) {
  background-color: rgba(254, 216, 84, 0.1) !important;
  color: #fed854 !important;
  border-color: #fed854 !important;
}

:deep(.v-alert__close-button) {
  color: #fed854 !important;
}

:deep(.v-alert__prepend) {
  color: #fed854 !important;
}

:deep(.v-alert__content) {
  color: #fed854 !important;
}

input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
  -webkit-box-shadow: 0 0 0 30px rgba(45, 55, 75, 0.8) inset !important;
  -webkit-text-fill-color: white !important;
  transition: background-color 5000s ease-in-out 0s;
  caret-color: white !important;
}

input:autofill {
  background: rgba(45, 55, 75, 0.8) !important;
  color: white !important;
}

:deep(.v-field__input:-webkit-autofill) {
  -webkit-box-shadow: 0 0 0 30px rgba(45, 55, 75, 0.8) inset !important;
  -webkit-text-fill-color: white !important;
}

.text-medium-emphasis {
  color: rgba(86, 91, 91, 0.99) !important;
  font-weight: bold;
}

.login-link {
  color: #42ddf2 !important;
}

.login-link:hover {
  color: #fed854 !important;
}

/* Match your existing header styling */
.header-image {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px;
  background-image: url('@/assets/top-image.png');
  background-size: cover;
  background-position: center;
  z-index: 1;
  opacity: 0.6;
}

.header-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 600px;
  background: linear-gradient(
    to bottom,
    rgba(23, 28, 38, 0) 0%,
    rgba(23, 28, 38, 0.8) 80%,
    rgba(23, 28, 38, 1) 100%
  );
  z-index: 2;
}

.content-wrapper {
  position: relative;
  z-index: 3;
  padding-top: 200px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100vw !important;
  margin-bottom: 100px;
}

:deep(.v-field) {
  border-color: rgba(66, 221, 242, 0.3) !important;
}

:deep(.v-field:hover) {
  border-color: #42ddf2 !important;
}

:deep(.v-field.v-field--focused) {
  border-color: #42ddf2 !important;
}

:deep(.v-label) {
  color: rgba(255, 255, 255, 0.7) !important;
}

:deep(.v-field__input) {
  color: white !important;
}

:deep(.v-icon) {
  color: rgba(255, 255, 255, 0.7) !important;
}

h2 {
  color: #42ddf2;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(66, 221, 242, 0.3);
}
</style>
