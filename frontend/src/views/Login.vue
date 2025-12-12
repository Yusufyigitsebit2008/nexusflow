<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 relative overflow-hidden font-sans">
    
    <div class="absolute top-[-10%] left-[-10%] w-96 h-96 bg-blue-500/30 rounded-full blur-[128px]"></div>
    <div class="absolute bottom-[-10%] right-[-10%] w-96 h-96 bg-purple-500/30 rounded-full blur-[128px]"></div>

    <div class="bg-white/10 backdrop-blur-xl border border-white/20 p-8 rounded-2xl shadow-2xl w-full max-w-md relative z-10 animate-fade-in-up">
      
      <div class="text-center mb-8">
        <h1 class="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400 tracking-tight">
          NexusFlow
        </h1>
        <p class="text-slate-400 text-sm mt-2 font-medium">Proje Yönetiminin Geleceği</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        
        <div class="group">
          <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 ml-1">Kullanıcı Adı</label>
          <div class="relative">
            <input 
              v-model="username" 
              type="text" 
              class="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              placeholder="Adınız..."
              required
            >
            <span class="absolute right-4 top-3.5 text-slate-500 text-sm">👤</span>
          </div>
        </div>

        <div class="group">
          <label class="block text-xs font-bold text-slate-300 uppercase tracking-wider mb-2 ml-1">Şifre</label>
          <div class="relative">
            <input 
              v-model="password" 
              type="password" 
              class="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              placeholder="••••••••"
              required
            >
            <span class="absolute right-4 top-3.5 text-slate-500 text-sm">🔒</span>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-blue-500/30 transition-all transform active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center gap-2"
        >
          <span v-if="loading" class="animate-spin h-5 w-5 border-2 border-white border-t-transparent rounded-full"></span>
          <span v-else>Giriş Yap 🚀</span>
        </button>

      </form>

      <div class="mt-8 text-center border-t border-white/10 pt-6">
        <p class="text-slate-400 text-sm">
          Hesabın yok mu? 
          <router-link to="/register" class="text-blue-400 hover:text-blue-300 font-bold transition-colors">
            Hemen Kayıt Ol
          </router-link>
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth'; // Auth store yolunu kontrol et
import { useRouter } from 'vue-router';
import { useToast } from "vue-toastification";

const username = ref('');
const password = ref('');
const loading = ref(false);

const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const handleLogin = async () => {
  loading.value = true;
  try {
    await authStore.login({ username: username.value, password: password.value });
    toast.success(`Hoş geldin, ${username.value}! 👋`);
    router.push('/dashboard');
  } catch (error) {
    console.error(error);
    toast.error("Giriş başarısız! Bilgilerini kontrol et.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
.animate-fade-in-up {
  animation: fadeInUp 0.5s ease-out forwards;
}
</style>