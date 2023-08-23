<template>
    <div class="max-w-7xl mx-auto grid grid-cols-2 gap-4">
        <div class="main-left">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <h1 class="mb-6 text-2xl">Edit Your Profile</h1>

                <p class="mb-6 text-gray-500">
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                    Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate. Lorem ipsum dolor sit mate.
                </p>
            </div>
        </div>

        <div class="main-right">
            <div class="p-12 bg-white border border-gray-200 rounded-lg">
                <form class="space-y-6" @submit.prevent="submitForm">
                    <div>
                        <label>Name</label><br>
                        <input v-model="form.name" type="text" placeholder="Your full name"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>E-mail</label><br>
                        <input v-model="form.email" type="email" placeholder="Your e-mail address"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Old Password</label><br>
                        <input v-model="form.old_password" type="password" placeholder="Your Old password (optional)"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>New password</label><br>
                        <input v-model="form.new_password" type="password" placeholder="Your New password (optional)"
                            class="w-full mt-2 py-4 px-6 border border-gray-200 rounded-lg">
                    </div>

                    <div>
                        <label>Add Avatar</label><br>
                        <input type="file" ref="avatar" class="mt-3"/>
                    </div>

                    <template v-if="errors.length > 0">
                        <div class="bg-red-300 text-white rounded-lg p-6">
                            <p v-for="error in errors" :key="error">{{ error }}</p>
                        </div>
                    </template>

                    <div>
                        <button class="py-4 px-6 bg-purple-600 text-white rounded-lg">Save Changes</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast'
import { useUserStore } from '@/stores/user'
export default {
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
            form: {
                email: this.userStore.user.email,
                name: this.userStore.user.name,
                old_password: '',
                new_password: '',
                avatar: null,
            },
            errors: [],
        }
    },
    methods: {
        submitForm() {
            this.errors = []
            if (this.form.email === '') {
                this.errors.push('email is required')
            }

            if (this.form.name === '') {
                this.errors.push('name is required')
            }

            if (this.form.new_password  && this.form.old_password === '') {
                this.errors.push('Enter your old password to verify!')
            }

            if (this.form.old_password  && this.form.new_password === '') {
                this.errors.push('Enter your new password to change or left both password fields empty !')
            }

            if(this.form.old_password && this.form.new_password.length >=1 && this.form.new_password.length < 5)
            {
                this.errors.push('Your New Password must be at least of 5 characters!')
            }

            if (this.errors.length === 0) {
                this.form.avatar = this.$refs.avatar.files[0]
                axios.post('/api/editProfile/', this.form, { 'headers': { 'Content-Type': 'multipart/form-data'}})
                    .then(response => {
                        if (response.data.status === 'success') {
                            this.toast.showToast(5000, response.data.message, 'bg-emerald-500')
                            this.userStore.setUserInfo({
                                id: this.userStore.user.id,
                                name: this.form.name,
                                email:  this.form.email,
                                avatar: response.data.avatar,
                            })
                            this.$router.back()
                        }
                        else if (response.data.status === 'failure')
                        {
                            this.toast.showToast(3000, response.data.message, 'bg-red-300')
                        }
                        else {
                            const data = JSON.parse(response.data.message)
                            for (const key in data) {
                                this.errors.push(data[key][0].message)
                            }
                            this.toast.showToast(5000, 'All conditions should be satisfied!', 'bg-red-300')
                        }
                    })
                    .catch(error => {
                        console.log(error)
                        this.toast.showToast(5000, error, 'bg-red-300')
                    })
            }
        }
    }
}
</script>
