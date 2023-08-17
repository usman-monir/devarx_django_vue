<template>
    <div v-for="friend in friends" :key="friend.id">
                <div  class="p-3 text-center bg-gray-100 rounded-lg" >
                        <img src="https://i.pravatar.cc/300?img=67" class="mb-6 p-4 rounded-full">
                        <RouterLink :to="{ name: 'profile', params: { 'id': friend.id } }">
                            <strong
                                class="text-purple-600 underline">{{ friend.name }}
                            </strong>
                        </RouterLink>
                        <br />
                        <small>{{ friend.email }}</small>
                    </div>
                </div>
</template>

<script>
    export default {
        props:{
            friends: Array
        }
    }
</script>
