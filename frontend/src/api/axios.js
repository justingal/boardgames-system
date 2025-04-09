import axios from 'axios'

const instance = axios.create({
  baseURL: 'http://localhost:8000/api/',
})

instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('access')

  // Apsauga: naudoti tik jei tokenas yra string
  if (token && typeof token === 'string') {
    config.headers.Authorization = `Bearer ${token}`
  } else {
    console.warn('JWT tokenas neegzistuoja arba blogo formato:', token)
  }

  return config
})

export default instance
