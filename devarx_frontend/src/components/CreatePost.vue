<template>
    <div class="bg-white border border-gray-200 rounded-lg">
        <div class="p-4">
            <textarea v-model="postData.body" class="p-4 w-full bg-gray-100 rounded-lg"
            placeholder="What are you thinking about?"></textarea>
        </div>

        <div class="p-4 border-t border-gray-100 flex justify-between">
            <a href="#" class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg">Attach image</a>

            <a href="#" @click.prevent="createPost"
            class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</a>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useToastStore } from '@/stores/toast';

export default{
    setup() {
        const toast = useToastStore()
        return {
            'toast': toast,
        }
    },
    data()
    {
        return{
            postData: {
                'body': '',
            },
        }
    },
    props: {
        posts: Array
    },
    emits:['post-created'],
    methods:{
        createPost() {
            axios
                .post('/api/posts/createPost/', this.postData)
                .then(response => {
                    const newPost = response.data.newPost
                    if (newPost)
                        {
                            this.posts.unshift(newPost)
                            this.$emit('post-created')
                        }
                    else
                        this.toast.showToast(5000, 'Failed to create the post!!', 'bg-red-300')
                    this.postData = {}
                })
                .catch(error => this.toast.showToast(5000, error, 'bg-red-300'))
        },
    }
}
</script>
