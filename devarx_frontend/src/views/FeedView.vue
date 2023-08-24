<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">
        <div class="main-center col-span-2 space-y-4">
            <CreatePost :posts="posts" />
            <template v-for="post in posts" :key="post.id">
                <PostItem :post="post" :current_user_id="userStore.user.id" @post-deleted="()=>{ posts = posts.filter(p=>p != post );}" />
            </template>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow />
            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import PostItem from '@/components/PostItem.vue';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import CreatePost from '../components/CreatePost.vue';
import Trends from '@/components/Trends.vue';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';

export default {
    name: 'FeedView',
    components: {
        CreatePost,
        PeopleYouMayKnow,
        PostItem,
        Trends,
    },
    setup() {
        const toastStore = useToastStore()
        const userStore = useUserStore()
        return {
            toastStore,
            userStore
        }
    },
    emits:['post-deleted'],
    data() {
        return {
            posts: [],
        }
    },
    mounted() {
        this.loadPosts()
    },
    methods: {
        loadPosts() {
            axios
                .get('/api/posts/')
                .then(response => {
                    this.posts = response.data.posts
                    console.log(this.posts);
                })
                .catch(err => this.toastStore.showToast(5000, err, 'bg-red-300'))
        },
    }
}
</script>
