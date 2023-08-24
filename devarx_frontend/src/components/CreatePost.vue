<template>
    <div class="bg-white border border-gray-200 rounded-lg">
        <div class="p-4">
            <textarea v-model="postData.body" class="p-4 w-full bg-gray-100 rounded-lg"
            placeholder="What are you thinking about?"></textarea>
            <div id="preview" v-if="postData.url">
                <img :src="postData.url" class="w-[150px] h-[150px] mt-3 rounded-xl" />
            </div>
        </div>
        <div class="p-4 border-t border-gray-100 flex justify-between">
            <label class="inline-block py-4 px-6 bg-gray-600 text-white rounded-lg" style="cursor: pointer;">
                <input type="file" ref="image" hidden @change="handleFileChange"/>
                Attach image
            </label>

            <button @click.prevent="createPost" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Post</button>
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
                url:null,
            },
        }
    },
    props: {
        posts: Array
    },
    emits:['post-created'],
    methods:{
        handleFileChange(e){
            const file = e.target.files[0]
            this.postData.url = URL.createObjectURL(file)
        },
        createPost() {
            let formData = new FormData()
            formData.append('body', this.postData.body)
            formData.append('image', this.$refs.image.files[0])
            axios
                .post('/api/posts/createPost/', formData,{
                    'headers': {
                        'Content-Type': 'multipart/form-data'
                    }
                })
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
                    this.$refs.image.value = null
                })
                .catch(error => this.toast.showToast(5000, error, 'bg-red-300'))
        },
    }
}
</script>
