<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 relative overflow-hidden font-sans">
    
    <div class="absolute bottom-[-10%] left-[-10%] w-96 h-96 bg-emerald-500/20 rounded-full blur-[128px]"></div>
    <div class="absolute top-[-10%] right-[-10%] w-96 h-96 bg-blue-500/30 rounded-full blur-[128px]"></div>

    <div class="bg-white/10 backdrop-blur-xl border border-white/20 p-8 rounded-2xl shadow-2xl w-full max-w-md relative z-10 animate-fade-in-up">
      
      <div class="text-center mb-8">
        <h1 class="text-3xl font-extrabold text-white tracking-tight">Aramıza Katıl</h1>
        <p class="text-slate-400 text-sm mt-2">NexusFlow ile projelerini uçurmaya başla.</p>
      </div>

      <form @submit.prevent="handleRegister" class="space-y-5">
        
        <div>
          <label class="block text-xs font-bold text-slate-300 uppercase mb-1 ml-1">Kullanıcı Adı</label>
          <input v-model="form.username" type="text" required class="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all" placeholder="kullanici_adi">
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-300 uppercase mb-1 ml-1">E-Posta</label>
          <input v-model="form.email" type="email" required class="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all" placeholder="ornek@email.com">
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-bold text-slate-300 uppercase mb-1 ml-1">Şifre</label>
              <input v-model="form.password" type="password" required class="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all" placeholder="••••••">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-300 uppercase mb-1 ml-1">Tekrar</label>
              <input v-model="form.passwordConfirm" type="password" required class="w-full bg-slate-900/50 border border-slate-700 rounded-xl px-4 py-3 text-white placeholder-slate-500 focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all" placeholder="••••••">
            </div>
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full bg-gradient-to-r from-emerald-500 to-teal-600 hover:from-emerald-400 hover:to-teal-500 text-white font-bold py-3.5 rounded-xl shadow-lg shadow-emerald-500/20 transition-all transform active:scale-95 disabled:opacity-50 mt-4"
        >
          <span v-if="loading">İşleniyor...</span>
          <span v-else>Hesap Oluştur ✨</span>
        </button>

      </form>

      <div class="mt-6 text-center border-t border-white/10 pt-4">
        <p class="text-slate-400 text-sm">
          Zaten hesabın var mı? 
          <router-link to="/login" class="text-emerald-400 hover:text-emerald-300 font-bold transition-colors">
            Giriş Yap
          </router-link>
        </p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';
import { useToast } from "vue-toastification";

const form = reactive({
    username: '',
    email: '',
    password: '',
    passwordConfirm: ''
});

const loading = ref(false);
const authStore = useAuthStore();
const router = useRouter();
const toast = useToast();

const handleRegister = async () => {
    if (form.password !== form.passwordConfirm) {
        toast.warning("Şifreler eşleşmiyor! ⚠️");
        return;
    }

    loading.value = true;
    try {
        await authStore.register({
            username: form.username,
            email: form.email,
            password: form.password
        });
        toast.success("Kayıt başarılı! Giriş yapılıyor... 🎉");
        router.push('/dashboard');
    } catch (error) {
        console.error(error);
        toast.error("Kayıt olunamadı. Kullanıcı adı alınmış olabilir.");
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