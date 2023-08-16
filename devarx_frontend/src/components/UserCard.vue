<template>
     <div  class="p-3 text-center bg-gray-100 rounded-lg" >
        <img src="https://i.pravatar.cc/300?img=67" class="mb-6 p-4 rounded-full">
            <template v-if="current_user_id == user.id">
                    <p><strong>{{  user.name }}</strong></p>
            </template>
            <template v-else>
                <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }">
                    <strong
                        class="text-purple-600 underline">{{ user.name }}
                    </strong>
                </RouterLink>
            <br />
            </template>
            <small>{{ user.email }}</small>

            <div class="mt-6 flex space-x-8 justify-around">
                <p class="text-xs text-gray-500">182 friends</p>
                <p class="text-xs text-gray-500">120 posts</p>
            </div>
    </div>
</template>

<script>
export default
{
    props:{
        user: Object,
        current_user_id: String,
    }
}
</script>
