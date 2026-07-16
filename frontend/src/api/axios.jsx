import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true, // ¡CRUCIAL! Permite que el navegador envíe la cookie del refresh token de vuelta al backend
});

// Variable en memoria para guardar el Access Token de vida corta
let accessToken = null;

export const setAccessToken = (token) => {
  accessToken = token;
};

// 1. Interceptor de Petición: Añade el Access Token en los headers antes de enviar cualquier request
api.interceptors.request.use(
  (config) => {
    if (accessToken) {
      config.headers['Authorization'] = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 2. Interceptor de Respuesta: Si recibimos un 401, intentamos refrescar el token de forma silenciosa
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    
    // Si la API responde con 401 y no hemos reintentado ya esta petición
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        // Llamamos al backend para renovar el token (se enviará la cookie automáticamente)
        const response = await axios.post(
          'http://localhost:8000/api/auth/refresh',
          {},
          { withCredentials: true }
        );
        
        const { access_token } = response.data;
        setAccessToken(access_token);
        
        // Actualizamos la petición original con el nuevo token y volvemos a intentar
        originalRequest.headers['Authorization'] = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Si el refresh token también expiró, redirigimos al usuario al login
        setAccessToken(null);
        window.location.href = '/login'; 
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default api;