<template>
    <div class="p-3 flex flex-col justify-around items-center bg-white border border-gray-300 rounded-lg">
        <img :src="user.get_avatar" class="mb-6 w-[100px] h-[100px] rounded-full">
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
