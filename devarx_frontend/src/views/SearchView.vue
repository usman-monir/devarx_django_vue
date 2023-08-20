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
            <div v-if="users.length" class="p-6 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4">
                <div v-for="user in users" :key="user.id">
                    <UserCard :user="user" :current_user_id="userStore.user.id" />
                </div>
            </div>
            <div v-if="posts.length" v-for="post in posts" :key="post.id">
                <PostItem :post="post" :current_user_id="userStore.user.id" />
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
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue'
import Trends from '@/components/Trends.vue'
import PostItem from '@/components/PostItem.vue';
import UserCard from '@/components/UserCard.vue';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import axios from 'axios'

export default {
    name: 'SearchView',
    components: {
        PeopleYouMayKnow,
        PostItem,
        Trends,
        RouterLink,
        UserCard,
    },
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()
        return {
            toastStore,
            userStore,
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
