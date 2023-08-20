<template>
    <div class="p-3 text-center bg-gray-100 rounded-lg">
        <img src="https://i.pravatar.cc/300?img=67" class="mb-6 p-4 rounded-full">
        <template v-if="current_user_id == user.id">
            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }">
                <strong class="underline">
                    You
                </strong>
            </RouterLink>
        </template>
        <template v-else>
            <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }">
                <strong class="text-purple-600 underline">{{ user.name }}
                </strong>
            </RouterLink>
        </template>
        <br />
        <small>{{ user.email }}</small>
    </div>
</template>

<script>
export default
    {
        props: {
            user: Object,
            current_user_id: String,
        }
    }
</script>
