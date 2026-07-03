<script setup lang="ts">
import { useThemeStore } from '../../stores/theme';
import { SunIcon, MoonIcon, LogOutIcon } from 'lucide-vue-next';
import Button from '../../components/ui/Button.vue';
import { useRouter } from 'vue-router';

const themeStore = useThemeStore();
const router = useRouter();

const handleExit = () => {
  router.push('/');
};
</script>

<template>
  <div class="w-64 border-r border-border bg-surface flex flex-col justify-between hidden md:flex">
    <div class="p-6">
      <h2 class="text-xl font-bold tracking-tight text-text">DataDash</h2>
      <p class="text-xs text-muted-foreground mt-1">Enterprise Analytics</p>
    </div>
    <div class="p-4 border-t border-border space-y-2">
      <Button variant="ghost" class="w-full justify-start" @click="themeStore.toggleDark()">
        <SunIcon v-if="themeStore.isDark" class="h-4 w-4 mr-2" />
        <MoonIcon v-else class="h-4 w-4 mr-2" />
        Toggle Theme
      </Button>
      <Button variant="ghost" class="w-full justify-start text-destructive hover:text-destructive hover:bg-destructive/10" @click="handleExit">
        <LogOutIcon class="h-4 w-4 mr-2" />
        Exit Dataset
      </Button>
    </div>
  </div>
</template>
