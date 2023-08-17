<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-3 space-y-4">
        <template v-if="$route.params.id == userStore.user.id">
            <template v-if="friendRequests.length">
            <h1 class="font-bold p-5 bg-white text-gray-700 rounded-full ">Friend Requests</h1>
            <div class="p-6 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4">
                <div v-for="request in friendRequests" :key="request.id">
                    <div  class="p-3 text-center bg-gray-100 rounded-lg" >
                        <img src="https://i.pravatar.cc/300?img=67" class="mb-6 p-4 rounded-full">
                        <RouterLink :to="{ name: 'profile', params: { 'id': request.send_by.id } }">
                            <strong
                                class="text-purple-600 underline">{{ request.send_by.name }}
                            </strong>
                        </RouterLink>
                        <br />
                        <small>{{ request.send_by.email }}</small>
                        <div class="mt-6 flex space-x-8 justify-around">
                            <button @click.prevent="acceptRequest(request.send_by.id)" class="inline-block mt-4 p-2 bg-purple-600 text-white text-s rounded-md">Accept</button>
                            <button @click.prevent="rejectRequest(request.send_by.id)" class="inline-block mt-4 p-2 bg-red-600 text-white text-s rounded-md">Reject</button>
                        </div>
                    </div>
                </div>
            </div>
            </template>
            <template v-else>
                <p class="text-gray-500 p-5"> No Friend Requests :( </p>
            </template>
        </template>
            <h1 class="font-bold mt-6 p-5 bg-white text-gray-700 rounded-full ">All Friends</h1>
            <div v-if="friends.length" class="p-6 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4">
                <AllFriends :friends="friends" />
            </div>
            <div v-else>
                <p class="text-gray-500 p-5"> No Friends yet! :( </p>
            </div>
            <h1 class="font-bold mt-6 p-5 bg-white text-gray-700 rounded-full ">Mutual Friends</h1>
            <div v-if="mutualFriends.length" class="p-6 bg-white border border-gray-200 rounded-lg grid grid-cols-3 gap-4">
                <AllFriends :friends="mutualFriends" />
            </div>
            <div v-else>
                <p class="text-gray-500 p-5"> No Mutual Friends to show! </p>
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
import UserCard from '../components/UserCard.vue';
import AllFriends from '../components/AllFriends.vue';
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
import axios from 'axios'

export default {
    name: 'SearchView',
    components: {
        AllFriends,
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
            friendRequests: [],
            friends:[],
            mutualFriends:[],
        }
    }
    ,
    mounted()
    {
        if(this.$route.params.id == this.userStore.user.id )
            this.getCurrentUserFriendsData()
        else
            this.getViewedUserFriendsData()
    },
    methods: {
        getCurrentUserFriendsData() {
            axios
                .get(`/api/user/friends/me/`)
                .then(response => {
                    this.friendRequests = response.data.friendRequests
                    this.friends = response.data.friends
                })
                .catch(error => this.toastStore.showToast(5000, error, 'bg-red-300'))
        },
        getViewedUserFriendsData()
        {
            this.friendRequests = []
            axios
            .get(`/api/user/friends/viewed/${this.$route.params.id}/`)
            .then(response => {
                this.friends = response.data.friends
                this.mutualFriends = response.data.mutualFriends
            })
        },
        acceptRequest(id){
            axios
            .post('/api/user/friends/accept', {id})
            .then(response=>{
                this.toastStore.showToast(3000, response.data.status, 'bg-emerald-300')
            })
            .catch(error => this.toastStore.showToast(3000, error, 'bg-red-300'))
            setTimeout(()=>{
                this.getCurrentUserFriendsData()
            }, 3000)
        },
        rejectRequest(id){
            axios
            .post('/api/user/friends/reject', {id})
            .then(response=>{
                this.toastStore.showToast(3000, response.data.status, 'bg-red-300')
            })
            .catch(error => this.toastStore.showToast(3000, error, 'bg-red-300'))
            setTimeout(()=>{
                this.getCurrentUserFriendsData()
            }, 3000)
        }
    }
}
</script>
