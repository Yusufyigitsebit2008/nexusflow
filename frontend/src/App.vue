<template>
  <CommandPalette v-if="isAuthenticated" />
  
  <router-view></router-view>
</template>

<script setup>
import { computed } from 'vue';
import { useAuthStore } from './stores/auth';
import CommandPalette from './components/CommandPalette.vue';

const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
</script>

<style>
</style>