<template>
    <div v-for="friend in friends" :key="friend.id">
        <div class="p-4 flex flex-col justify-around items-center bg-gray-100 rounded-lg">
            <img :src="friend.get_avatar" class="mb-6 w-[120px] h-[120px] rounded-full">
            <template v-if="current_user_id == friend.id">
                <RouterLink :to="{ name: 'profile', params: { 'id': friend.id } }">
                    <strong class="underline">You
                    </strong>
                </RouterLink>
            </template>
            <template v-else>
                <RouterLink :to="{ name: 'profile', params: { 'id': friend.id } }">
                    <strong class="text-purple-600 underline">{{ friend.name }}
                    </strong>
                </RouterLink>
            </template>
            <br />
            <small>{{ friend.email }}</small>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        friends: Array,
        current_user_id: String
    }
}
</script>
