<template>
    <div class="p-4 bg-white border border-gray-200 rounded-lg" style="margin-bottom: 2rem; padding-bottom: 0;">
        <div class="mb-6 flex items-center justify-between">
            <div class="flex items-center space-x-6">
                <img src="https://i.pravatar.cc/300?img=67" class="w-[40px] rounded-full">
                <template v-if="current_user_id == mutablePost.created_by.id">
                    <p><strong>{{ mutablePost.created_by.name }}</strong></p>
                </template>
                <template v-else-if="profileViewPage">
                    <p><strong>{{ mutablePost.created_by.name }}</strong></p>
                </template>
                <template v-else>
                    <RouterLink :to="{ name: 'profile', params: { 'id': mutablePost.created_by.id } }">
                        <strong class="text-purple-600">{{ mutablePost.created_by.name }}
                        </strong>
                    </RouterLink>
                </template>
            </div>

            <p class="text-gray-600">{{ mutablePost.created_at_formatted }} ago</p>
        </div>

        <p>{{ mutablePost.body }}</p>

        <div class="mb-6 mt-8 flex justify-between">
            <div class="flex space-x-6">
                <div class="flex items-end space-x-2" style="cursor: pointer;">
                    <svg @click.prevent="reactOnPost" :id="mutablePost.id + '-likeBtn'" xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                        <path stroke-linecap="round" stroke-linejoin="round"
                            d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z">
                        </path>
                    </svg>
                    <span @click.prevent="usersWhoLiked" class="text-gray-500 text-xs mb-1 underline">{{ mutablePost.likes.length  }}
                        likes</span>
                    <div :id="mutablePost.id + '-likesDropdown'" class="z-10 bg-gray-100 rounded-lg shadow w-44"
                        style="display: none;position: relative;bottom: 30px;right: 50px;overflow-y: auto;max-height: 150px;min-height: 50px">
                        <ul class="py-2 text-sm text-gray-700">
                        </ul>
                    </div>
                </div>
            </div>
            <div class="flex items-center space-x-2" @click.prevent="addComment" style="cursor: pointer;">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                    stroke="currentColor" class="w-6 h-6">
                    <path stroke-linecap="round" stroke-linejoin="round"
                        d="M12 20.25c4.97 0 9-3.694 9-8.25s-4.03-8.25-9-8.25S3 7.444 3 12c0 2.104.859 4.023 2.273 5.48.432.447.74 1.04.586 1.641a4.483 4.483 0 01-.923 1.785A5.969 5.969 0 006 21c1.282 0 2.47-.402 3.445-1.087.81.22 1.668.337 2.555.337z">
                    </path>
                </svg>

                <span class="text-gray-500 text-xs">{{ mutablePost.comments.length }} comments</span>
            </div>
        </div>
    </div>
    <div class="p-4 m-0 bg-gray-100 border border-gray-300 rounded-lg" :id="mutablePost.id + '-commentSection'" style="display: none;">
        <div class="ml-6" id="commentInputSection">
            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="p-4 pb-0">
                    <textarea v-model="commentBody" @keyup.prevent="handleKeyEventOnInput" class="p-4 w-full bg-gray-100 rounded-lg" placeholder="What u think about this post.."></textarea>
                </div>

                <div class="p-4 border-t border-gray-100 flex justify-end">
                    <button @click.prevent="postComment" class="inline-block text-md py-2 px-4 bg-purple-600 text-white rounded-lg">Comment</button>
                </div>
            </div>
        </div>
        <div v-for="comment in mutablePost.comments" :key="comment.id" class="ml-6 my-3 p-4 bg-white border border-gray-200 rounded-lg">
        <div class="flex flex-col justify-between">
            <div class="mb-6 flex items-center space-x-12">
            <img src="https://i.pravatar.cc/300?img=67" class="w-[40px] rounded-full">
            <template v-if="current_user_id === mutablePost.created_by.id">
            <p><strong>{{ comment.created_by.name }}</strong></p>
            </template>
            <template v-else>
            <RouterLink :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">
                <strong class="text-purple-600">{{ comment.created_by.name }}</strong>
            </RouterLink>
            </template>
            <p class="text-gray-600">{{ comment.created_at_formatted }} ago</p>
        </div>
        <p class="text-gray-500 bg-gray-100 p-3">{{ comment.body }}</p>
        </div>
        </div>
 </div>
</template>

<script>
import axios from 'axios'
export default {
    props: {
        post: Object,
        current_user_id: String,
        profileViewPage: Boolean,
    },
    data() {
        return {
            likesCount: 0,
            commentBody: '',
            mutablePost: this.post
        }
    },
    mounted() {
        const likeBtn = document.getElementById(this.mutablePost.id + '-likeBtn')
        likeBtn.style.fill = this.getfillValue()
        this.insertUsersWhoLikedToHtml()
        // this.insertCommentToHtml()
    },
    methods: {
        usersWhoLiked() {
            const dropdownMenu = document.getElementById(this.mutablePost.id + '-likesDropdown')
            if (dropdownMenu.style.display == 'none') {
                dropdownMenu.style.display = 'block'
            }
            else
                dropdownMenu.style.display = 'none'
        },
        getfillValue() {
            for (let i = 0; i < this.mutablePost.likes.length; i++) {
                if (this.mutablePost.likes[i].id == this.current_user_id)
                    return 'purple'
            }
            return 'none'
        },
        async reactOnPost() {
            const likeBtn = document.getElementById(this.mutablePost.id + '-likeBtn')
            if (likeBtn.style.fill == 'none') {
                await axios
                    .post(`/api/posts/profile/${this.mutablePost.created_by.id}/likePost/`, { 'postId': this.mutablePost.id })
                    .then(response => {
                        likeBtn.style.fill = 'purple';
                        this.mutablePost = response.data.post
                        console.log(this.mutablePost);
                    })
                    .catch(err => alert(err))
            }
            else {
                await axios
                    .post(`/api/posts/profile/${this.mutablePost.created_by.id}/dislikePost/`, { 'postId': this.mutablePost.id })
                    .then(response => {
                        likeBtn.style.fill = 'none';
                        this.mutablePost = response.data.post
                        console.log(this.mutablePost);
                    })
                    .catch(err => alert(err))
            }
            this.insertUsersWhoLikedToHtml()
        },
        insertUsersWhoLikedToHtml() {
            const dropdownMenu = document.getElementById(this.mutablePost.id + '-likesDropdown').querySelector('ul')
            dropdownMenu.innerHTML = ''
            if (this.mutablePost.likes.length == 0) {
                dropdownMenu.innerHTML += `<p class="block px-4 py-2 text-gray-500">No likes yet!</p>`
            }
            else {
                this.mutablePost.likes.map(likedBy => {
                    dropdownMenu.innerHTML += `
                            <li class='flex items-center justify-start px-2 py-2 hover:bg-white'>
                                <img class="w-8 h-8 rounded-full" src="https://i.pravatar.cc/40?img=62" alt="user photo">
                                <a href="/profile/${likedBy.id}" class="block px-6 underline"><small>${likedBy.name}</small></a>
                            </li>`
                })
            }
        },
        addComment()
        {
            const commentSection = document.getElementById(this.mutablePost.id + '-commentSection')
            if ( commentSection.style.display == 'none' )
            {
                commentSection.style.display = 'block'
            }
            else
            commentSection.style.display = 'none'
        },
        async postComment()
        {
            this.commentBody = this.commentBody ? this.commentBody.trim() : '<i>empty comment</i>'

            await axios
            .post(`/api/posts/profile/${this.mutablePost.created_by.id}/comment/`, { 'postId': this.post.id , 'body': this.commentBody})
            .then(response => {
                this.mutablePost = response.data.post;
            })
            .catch(error => alert(error))

            this.commentBody = ''

        },
        handleKeyEventOnInput(e)
        {
            if ( e.key == 'Enter' && !e.shiftKey )
                    this.postComment()
        },
        insertCommentToHtml(){
            const commentSection = document.getElementById(this.mutablePost.id + '-commentSection')
            this.mutablePost.comments.map(comment=>{
            commentSection.innerHTML += `
                <div class="mb-6 flex items-center justify-between">
                    <div class="flex items-center space-x-6">
                        <img src="https://i.pravatar.cc/300?img=67" class="w-[40px] rounded-full">
                        <template v-if="${this.current_user_id == this.mutablePost.created_by.id}">
                            <p><strong>${comment.created_by.name}</strong></p>
                        </template>
                        <template v-else-if="${true}">
                            <p><strong>${comment.created_by.name}</strong></p>
                        </template>
                        <template v-else>
                            <RouterLink :to="{ name: 'profile', params: { 'id': comment.created_by.id } }">
                                <strong class="text-purple-600">${comment.created_by.name}
                                </strong>
                            </RouterLink>
                        </template>
                    </div>
                    <p class="text-gray-600">${ comment.created_at_formatted } ago</p>
                </div>
                <p>${ comment.body }</p>`
            })
        }
    }
}
</script>

