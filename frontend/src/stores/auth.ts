// stores/auth.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { API_URL } from '@/config'

interface LoginCredentials {
  username: string // email
  password: string
}

interface LoginResponse {
  access_token: string
  token_type: string
  user_id: string
  role: string
}

interface RegisterCredentials {
  email: string
  password: string
}

interface RegisterResponse {
  email: string
  role: string
}

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref<string | null>(localStorage.getItem('token') || null)
  const userEmail = ref<string | null>(localStorage.getItem('userEmail') || null) // Добавяме взимане от localStorage
  const userId = ref<string | null>(localStorage.getItem('userId') || null) // Добавяме взимане от localStorage
  const userRole = ref<string | null>(localStorage.getItem('userRole') || null)
  const isAuthenticated = ref(!!token.value)


  const clearUserData = () => {
    token.value = null
    userEmail.value = null
    userId.value = null
    userRole.value = null
    isAuthenticated.value = false
    localStorage.removeItem('token')
    localStorage.removeItem('userEmail')
    localStorage.removeItem('userId')
    localStorage.removeItem('userRole')
  }


  const setToken = (newToken: string | null) => {
    token.value = newToken
    isAuthenticated.value = !!newToken

    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const setUserEmail = (email: string | null) => {
    userEmail.value = email
    if (email) {
      localStorage.setItem('userEmail', email)
    } else {
      localStorage.removeItem('userEmail')
    }
  }

      const setUserId = (id: string | null) => {
    userId.value = id
    if (id) {
      localStorage.setItem('userId', id)
    } else {
      localStorage.removeItem('userId')
    }
  }

  const setUserRole = (role: string | null) => {
    userRole.value = role
    if (role) {
      localStorage.setItem('userRole', role)
    } else {
      localStorage.removeItem('userRole')
    }
  }

  const initializeFromToken = async () => {
    const savedToken = localStorage.getItem('token')
    if (savedToken) {
      try {
        const response = await fetch(`${API_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${savedToken}`
          }
        })
        if (response.ok) {
          const userData = await response.json()
          setUserId(userData.id)
          setUserRole(userData.role)
          setUserEmail(userData.email)
          setToken(savedToken)
          isAuthenticated.value = true
        } else {
          clearUserData()
        }
      } catch (error) {
        console.error('Failed to initialize user data:', error)
        clearUserData()
      }
    }
  }


  const login = async (credentials: LoginCredentials): Promise<boolean> => {
  try {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    const response = await fetch(`${API_URL}/users/login`, {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('Login failed')
    }

    const data: LoginResponse = await response.json()

      // Store the token, email, and role
      setToken(data.access_token)
      userEmail.value = credentials.username
      setUserRole(data.role)
      userEmail.value = credentials.username
      userId.value = data.user_id
      userRole.value = data.role

    await router.push('/')

    return true
  } catch (error) {
    console.error('Login error:', error)
    setToken(null)
    userEmail.value = null
    setUserRole(null)
    return false
  }
}

  const register = async (credentials: RegisterCredentials): Promise<boolean> => {
    try {
      const response = await fetch(`${API_URL}/users/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password
        })
      })

      if (!response.ok) {
        throw new Error('Registration failed')
      }

      const data: RegisterResponse = await response.json()

      setUserRole(data.role)

      const loginSuccess = await login({
        username: credentials.email,
        password: credentials.password
      })

      if (!loginSuccess) {
        throw new Error('Auto-login after registration failed')
      }

      return true
    } catch (error) {
      console.error('Registration error:', error)
      return false
    }
  }

  const logout = async (): Promise<boolean> => {
    try {
      setToken(null)
      setUserEmail(null)
      setUserId(null)
      setUserRole(null)
      // userEmail.value = null
      // userRole.value = null

      await router.push('/login')
      return true
    } catch (error) {
      console.error('Logout failed:', error)
      return false
    }
  }

  const fetchUserRole = async (): Promise<string | null> => {
    try {
      if (!token.value) {
        throw new Error('User is not authenticated')
      }

      const response = await fetch(`${API_URL}/users/me`, {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })

      if (!response.ok) {
        throw new Error('Failed to fetch user role')
      }

      const data = await response.json()
      const role = data.role
      setUserRole(role)
      setUserId(data.id)
      setUserEmail(data.email)
      return role
    } catch (error) {
      console.error('Error fetching user role:', error)
      setUserRole(null)
      return null
    }
  }

  return {
    token,
    userEmail,
    userId,
    userRole,
    isAuthenticated,
    initializeFromToken,
    login,
    register,
    logout,
    fetchUserRole
  }
})
