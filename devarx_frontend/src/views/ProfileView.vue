<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="p-4 bg-white border border-gray-200 text-center rounded-lg">
                <img :src="user.get_avatar" class="mb-6">
                <p><strong>{{ user.name }}</strong></p>

                <div class="mt-6 flex space-x-8 justify-around">
                    <RouterLink :to="{ name: 'friends' }" class="text-xs text-gray-500 underline">{{ this.friendsCount }}
                        friends</RouterLink>
                    <p class="text-xs text-gray-500">{{ totalPosts }} posts</p>
                </div>
                <RouterLink :to="{name: 'editProfile'}" v-if="user && user.id == userStore.user.id"
                    class="inline-block mt-4 py-3 px-3 bg-purple-600 text-white text-xs rounded-md">Edit Profile
                </RouterLink>
                <button v-if="user && user.id != userStore.user.id && !isAlreadyFriend" @click.prevent="sendFriendRequest"
                    class="inline-block mt-4 py-3 px-3 bg-purple-600 text-white text-xs rounded-md">Send Friend
                    Request</button>
                <button v-if="user && user.id != userStore.user.id && isAlreadyFriend" @click.prevent="unFriend"
                    class="inline-block mt-4 py-3 px-3 bg-red-600 text-white text-xs rounded-md">UnFriend</button>
                <button v-if="user && user.id != userStore.user.id" @click.prevent="startConversation"
                    class="inline-block ml-3 mt-4 py-3 px-3 bg-emerald-500 text-white text-xs rounded-md">Send
                    Message</button>
            </div>
        </div>

        <div class="main-center col-span-2 space-y-4">
            <template v-if="user.id==userStore.user.id && posts && totalPosts">
                <CreatePost :posts="posts" @post-created="totalPosts++" />
            </template>
            <template v-for="post in posts" :key="post.id">
                <PostItem :post="post" :current_user_id="userStore.user.id" :profileViewPage=true @post-deleted="()=>{ posts = posts.filter(p=>p != post ); totalPosts--}" />
            </template>
        </div>

        <div class="main-right col-span-1 space-y-4">
            <PeopleYouMayKnow :current_profile_opened="user.id" />
            <Trends />
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import PeopleYouMayKnow from '@/components/PeopleYouMayKnow.vue';
import PostItem from '@/components/PostItem.vue';
import Trends from '@/components/Trends.vue';
import CreatePost from '@/components/CreatePost.vue';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import { RouterLink } from 'vue-router';

export default {
    name: 'ProfileView',
    components: {
        CreatePost,
        PeopleYouMayKnow,
        PostItem,
        Trends,
        RouterLink
    },
    props:{
        toggleMenu: Function
    },
    emits:['post-deleted', 'post-created'],
    setup() {
        const toast = useToastStore()
        const userStore = useUserStore()
        return {
            'toast': toast,
            'userStore': userStore
        }
    },
    data() {
        return {
            posts: [],
            user: {},
            isAlreadyFriend: 0,
            friendsCount: 0,
            totalPosts: 0,
        }
    },
    watch: {
        "$route.params.id": {
            handler() {
                this.loadPosts()
            },
            deep: true,
            immediate: true,
        }
    },
    mounted()
    {
        if (document.getElementById('dropdownMenu').style.display == 'block')
            this.toggleMenu()
    },
    methods: {
        loadPosts() {
            axios
                .get(`/api/posts/profile/${this.$route.params.id}/`)
                .then(response => {
                    this.posts = response.data.posts
                    this.user = response.data.user
                    this.isAlreadyFriend = this.user.friends.filter((id) => this.userStore.user.id == id).length
                    this.friendsCount = this.user.friends.length
                    this.totalPosts = this.posts.length
                })
                .catch((err) => this.toast.showToast(5000, err, 'bg-red-300'))
        },
        sendFriendRequest() {
            axios
                .post('/api/user/sendFriendRequest/', { 'id': this.user.id })
                .then(response => {
                    this.toast.showToast(5000, response.data.status, 'bg-emerald-300')
                })
                .catch(error => this.toast.showToast(5000, error, 'bg-red-300'))
        },
        unFriend() {
            axios
                .post('/api/user/unFriend/', { 'id': this.user.id })
                .then(response => {
                    this.toast.showToast(5000, response.data.status, 'bg-emerald-300')
                    this.isAlreadyFriend = 0
                })
                .catch(error => this.toast.showToast(5000, error, 'bg-red-300'))
        },
        startConversation() {
            axios
                .post(`/api/chat/initialize/`, { 'userId': this.user.id })
                .then(response => {
                    let activeConversation =  response.data.conversation
                    console.log(activeConversation);
                    this.$router.push({name: 'chat', query: { 'activeConversation': JSON.stringify(activeConversation)} })
                })
                .catch(error => this.toast.showToast(5000, error, 'bg-red-300'))
        }
    }

}

</script>
