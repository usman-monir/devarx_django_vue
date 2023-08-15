<script setup>
    import { useToastStore } from '../stores/toast'
    const toast = useToastStore()
</script>

<template>
    <div
    v-if="toast.isVisible"
    class="toast transition ease-in-out delay-500 duration-500 px-6 py-6 fixed top-full right-8 rounded-xl shadow-xl"
    :class="toast.classes"
    >
        {{ toast.message }}
    </div>
</template>
