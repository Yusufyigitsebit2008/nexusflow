import { defineStore } from 'pinia';
import api from '../utils/axios';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        token: localStorage.getItem('access_token') || null,
    }),
    
    getters: {
        isAuthenticated: (state) => !!state.token,
    },

    actions: {
        // GİRİŞ YAPMA
        async login(credentials) {
            try {
                const response = await api.post('token/', credentials);
                
                this.token = response.data.access;
                localStorage.setItem('access_token', response.data.access);
                localStorage.setItem('refresh_token', response.data.refresh);
                
                // Token'ı aldıktan sonra kullanıcı detayını çekebilirsin (Opsiyonel)
                this.user = { username: credentials.username }; 
                localStorage.setItem('user', JSON.stringify(this.user));
                
                return true;
            } catch (error) {
                console.error("Giriş hatası:", error);
                throw error;
            }
        },

        // KAYIT OLMA (YENİ EKLENDİ)
        async register(userData) {
            try {
                // 1. Backend'e kayıt isteği at
                await api.post('auth/register/', userData);
                
                // 2. Kayıt başarılıysa, hemen ardından GİRİŞ YAP (Auto-Login)
                await this.login({
                    username: userData.username,
                    password: userData.password
                });
                
                return true;
            } catch (error) {
                console.error("Kayıt hatası:", error);
                throw error;
            }
        },

        // ÇIKIŞ YAPMA
        logout() {
            this.user = null;
            this.token = null;
            localStorage.removeItem('user');
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            window.location.reload();
        }
    }
});