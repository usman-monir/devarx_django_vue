<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">People you may know</h3>

        <div class="space-y-4">
            <template v-for="user in suggestedPeople" :key="user.id">
                <div class="flex items-center justify-between" v-if="current_profile_opened != user.id">
                    <div class="flex items-center space-x-2">
                        <img :src="user.get_avatar" class="w-[40px] rounded-full">

                        <p class="text-xs"><strong>{{user.name}}</strong></p>
                    </div>

                    <RouterLink :to="{name: 'profile', params:{id: user.id} }" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Show</RouterLink>
                </div>
            </template>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'

export default {
    setup()
    {
        const toast = useToastStore()
        return {
            'toast': toast,
        }
    },
    props:{
        current_profile_opened: String,
    },
    data()
    {
        return {
            suggestedPeople: []
        }
    }
    ,mounted()
    {
        this.loadSuggestedPeople()
    },
    methods:{
        loadSuggestedPeople()
        {
            axios
            .get(`/api/user/suggestedPeople/`)
            .then(response=>{
                this.suggestedPeople= response.data.suggestedPeople
            })
            .catch(()=> this.toast.showToast(5000,'Cannot load suggested people for u!', 'bg-red-300'))
        }
    }
}


</script>
