<template>
    <div class="max-w-7xl mx-auto grid grid-cols-3 gap-4">

        <div class="main-center bg-gray-800 p-4 text-white col-span-2 space-y-4">
            <h2>#{{ trend }}</h2>
        </div>
        <div class="main-center col-span-2 space-y-4">
            <template v-for="post in posts" :key="post.id">
                <PostItem :post="post" :current_user_id="userStore.user.id" />
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
import Trends from '@/components/Trends.vue';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';

export default {
    name: 'FeedView',
    components: {
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
    data() {
        return {
            posts: [],
            trend: '',
        }
    },
    mounted() {
        this.trend = this.$route.params.id
        this.loadPostsWithSpecificTrend()
    },
    watch: {
        "$route.params.id": {
            handler() {
                this.trend = this.$route.params.id
                this.loadPostsWithSpecificTrend()
            },
            deep: true,
            immediate: true,
        }
    },
    methods: {
        loadPostsWithSpecificTrend() {
            axios
                .get(`/api/posts/?trend=${this.trend}`)
                .then(response => {
                    this.posts = response.data.posts
                    this.toastStore.showToast(3000, `Trends with #${this.trend}'`, 'bg-emerald-300')
                })
                .catch(err => this.toastStore.showToast(5000, err, 'bg-red-300'))
        }
    }
}
</script>
