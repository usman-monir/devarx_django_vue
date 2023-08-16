<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg">
                <form @submit.prevent="submitSearchForm">
                    <div class="p-4 flex space-x-4">
                        <input v-model="query" type="search" class="p-4 w-full bg-gray-100 rounded-lg"
                            placeholder="What are you looking for?">

                        <button href="#" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Search</button>
                    </div>
                </form>
            </div>
            <div v-if="users.length" v-for="user in users" :key="user.id" class="p-4 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-5">
                <div  class="p-6 text-center bg-gray-100 rounded-lg" >
                <img src="https://i.pravatar.cc/300?img=67" class="mb-6 rounded-full">

                    <RouterLink :to="{ name: 'profile', params: { 'id': user.id } }"><strong class="text-purple-600 underline">{{
                        user.name }}</strong></RouterLink>
                    <br />
                    <small>{{ user.email }}</small>

                    <div class="mt-6 flex space-x-8 justify-around">
                        <p class="text-xs text-gray-500">182 friends</p>
                        <p class="text-xs text-gray-500">120 posts</p>
                    </div>
                </div>
            </div>
            <div v-if="posts.length" v-for="post in posts" :key="post.id">
                <PostItem :post="post" />
            </div>
        </div>
        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>

<script>
import { RouterLink } from 'vue-router';
import PeopleYouMayKnow from '../components/PeopleYouMayKnow.vue'
import Trends from '../components/Trends.vue'
import PostItem from '../components/PostItem.vue';
import { useToastStore } from '@/stores/toast';
import axios from 'axios'

export default {
    name: 'SearchView',
    components: {
        PeopleYouMayKnow,
        PostItem,
        Trends,
        RouterLink,
    },
    setup() {
        const toastStore = useToastStore()
        return {
            toastStore
        }
    },
    data() {
        return {
            'query': '',
            users: [],
            posts: [],
        }
    }
    ,
    methods: {
        submitSearchForm() {
            axios
                .get(`/api/search/${this.query}`)
                .then(response => {
                    console.log(response.data.users);
                    this.users = response.data.users
                    this.posts = response.data.posts
                })
                .catch(error => this.toastStore.showToast(5000, error, 'bg-red-300'))

            this.query = ''
        }
    }
}
</script>
