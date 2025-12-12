import axios from 'axios';

// Axios örneği oluştur
const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/',
    headers: {
        'Content-Type': 'application/json',
    }
});

// 🕵️‍♂️ İSTEK (REQUEST) INTERCEPTOR
// Her istek gönderilmeden hemen önce burası çalışır
api.interceptors.request.use(
    (config) => {
        // LocalStorage'dan token'ı al
        const token = localStorage.getItem('access_token');
        
        // Eğer token varsa, header'a "Bearer <token>" olarak ekle
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 🛡️ YANIT (RESPONSE) INTERCEPTOR (Opsiyonel ama iyi olur)
// Eğer 401 (Yetkisiz) hatası alırsak kullanıcıyı login'e atabiliriz
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            console.warn("Oturum süresi doldu veya yetkisiz erişim.");
            // İstersen burada otomatik logout yapabilirsin:
            // localStorage.clear();
            // window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api;