<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-slate-900 to-blue-900 font-sans text-slate-100">
    
    <header class="bg-black/20 backdrop-blur-md border-b border-white/10 p-4 px-8 flex justify-between items-center">
      <div class="flex items-center gap-3 cursor-pointer" @click="$router.push('/dashboard')">
        <span class="text-2xl">⬅</span>
        <h1 class="text-xl font-bold">Profilim</h1>
      </div>
    </header>

    <div class="flex-1 flex items-center justify-center p-6">
        <div class="bg-white/10 backdrop-blur-xl border border-white/20 p-8 rounded-3xl shadow-2xl w-full max-w-2xl relative overflow-hidden">
            
            <div class="absolute top-0 right-0 w-64 h-64 bg-blue-500/20 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2"></div>

            <div class="flex items-center gap-6 mb-8 relative z-10">
                <div class="w-24 h-24 bg-gradient-to-tr from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-4xl font-bold text-white shadow-lg border-4 border-white/10">
                    {{ user?.username.charAt(0).toUpperCase() }}
                </div>
                <div>
                    <h2 class="text-3xl font-bold text-white">{{ user?.username }}</h2>
                    <p class="text-blue-300">Full Stack Developer</p>
                </div>
            </div>

            <div class="space-y-6 relative z-10">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div class="group">
                        <label class="block text-xs font-bold text-slate-400 uppercase mb-2">Kullanıcı Adı</label>
                        <input :value="user?.username" disabled class="w-full bg-slate-900/50 border border-slate-700 rounded-xl p-4 text-slate-300 cursor-not-allowed">
                    </div>
                    <div class="group">
                        <label class="block text-xs font-bold text-slate-400 uppercase mb-2">E-Posta</label>
                        <input :value="user?.email || 'email@yok.com'" disabled class="w-full bg-slate-900/50 border border-slate-700 rounded-xl p-4 text-slate-300 cursor-not-allowed">
                    </div>
                </div>

                <hr class="border-white/10 my-6">

                <div>
                    <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        🚀 Geliştirici Araçları
                    </h3>
                    
                    <div class="bg-blue-600/20 border border-blue-500/30 rounded-xl p-6 flex flex-col md:flex-row items-center justify-between gap-4">
                        <div>
                            <h4 class="font-bold text-blue-200">Demo Verisi Oluştur</h4>
                            <p class="text-xs text-blue-300/70 mt-1">Dashboard boş mu? Tek tıkla örnek projeler ve görevler ekle.</p>
                        </div>
                        <button 
                            @click="generateDemoData" 
                            :disabled="loading"
                            class="bg-blue-600 hover:bg-blue-500 text-white px-6 py-3 rounded-lg font-bold shadow-lg shadow-blue-500/20 transition transform active:scale-95 flex items-center gap-2"
                        >
                            <span v-if="loading" class="animate-spin">⚙️</span>
                            <span v-else>✨ Veri Üret</span>
                        </button>
                    </div>
                </div>
            </div>

        </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useToast } from "vue-toastification";
import api from '../utils/axios';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const toast = useToast();
const router = useRouter();
const user = computed(() => authStore.user);
const loading = ref(false);

const generateDemoData = async () => {
    loading.value = true;
    try {
        await api.post('generate-demo/');
        toast.success("Sihir tamamlandı! 🪄 Dashboard'a yönlendiriliyorsun...");
        
        setTimeout(() => {
            router.push('/dashboard');
        }, 1500);
        
    } catch (error) {
        console.error(error);
        toast.error("Demo veri oluşturulamadı.");
    } finally {
        loading.value = false;
    }
};
</script>