<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg">
        <h3 class="mb-6 text-xl">Trends</h3>

        <div v-if="trends.length" v-for="trend in trends" :key="trend.id">
            <div class="flex items-center justify-between space-y-4">
                <p class="text-xs">
                    <strong>#{{ trend.hashtag }}</strong><br>
                    <span class="text-gray-500">{{ trend.occurences }} posts using this #tag</span>
                </p>

                <RouterLink :to="{name: 'trends' , params:{id: trend.hashtag}}" class="py-2 px-3 bg-purple-600 text-white text-xs rounded-lg">Explore</RouterLink>
            </div>
        </div>
        <div v-else>
            <p class="text-gray-400">No Trends to show Yet :(</p>
            <small class="text-gray-500"><strong>Tip:</strong> Use # while posting to generate trends!</small>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import {useToastStore } from '@/stores/toast';
export default{
    setup()
    {
        const toast = useToastStore()
        return {
            'toast': toast
        }
    },
    data()
    {
        return{
            trends: []
        }
    }
    ,
    mounted()
    {
        this.loadTrends()
    },
    methods:{
        loadTrends()
    {
        axios
        .get('/api/posts/trends/')
        .then(response=>{
            this.trends = response.data.trends;
        })
        .catch(()=> this.toast.showToast(7000, 'Cannot load trends for U :(', 'bg-red-200'))
    }
    }

}
</script>
