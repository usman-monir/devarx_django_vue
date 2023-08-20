<template>
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <template v-if="conversations" v-for="conversation in conversations" :key="conversation.id">
                <div @click.prevent="setActiveConversation(conversation)"
                    class="p-4 px-6 m-1 hover:bg-purple-200 border border-gray-200 rounded-lg"
                    :class="activeConversation.id == conversation.id ? 'bg-purple-100' : 'bg-white'"
                    style="cursor: pointer;">
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                                <p class="text-xs"><strong>{{ getOtherUser(conversation.users).name }}</strong></p>
                            </div>
                            <span class="text-xs pl-4 text-gray-500">{{ conversation.created_at_formatted }}</span>
                        </div>
                    </div>
                </div>
            </template>
        </div>

        <div class="main-center col-span-3 space-y-4">
            <div class="bg-white border border-gray-200 rounded-lg" id="messageBox"
                style="min-height: 400px;max-height: 500px; overflow-y: auto;">
                <div class="flex flex-col flex-grow p-4">
                    <div v-if="activeConversation" v-for="message in activeConversation.messages"
                        @mouseleave.prevent="handleMouseOut">
                        <div v-if="message.sent_by.id == userStore.user.id"
                            class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                            <div class="w-full">
                                <div @mouseenter="handleMouseOver(message)"
                                    class="bg-purple-400 text-white p-3 rounded-l-lg rounded-br-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <div :id="message.id + '-mssgTooltip'" class="z-10 rounded-lg shadow w-44 mssgTooltip p-2"
                                    style="display: none;position: relative;max-width: 70px;background-color: rgba(255,255,255,.3);">
                                    <svg @click.prevent="deleteMessage" style="color: red; cursor: pointer;display: inline;"
                                        xmlns="http://www.w3.org/2000/svg" height="16" fill="currentColor"
                                        class="bi bi-trash" viewBox="0 0 16 16">
                                        <path
                                            d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"
                                            fill="red"></path>
                                        <path fill-rule="evenodd"
                                            d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"
                                            fill="red"></path>
                                    </svg>
                                    <svg @click.prevent="toggleMessageEditSection" xmlns="http://www.w3.org/2000/svg"
                                        viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor"
                                        stroke-width="3" stroke-linecap="round" stroke-linejoin="round"
                                        class="feather feather-edit-3"
                                        style="color: rgb(16, 207, 175); cursor: pointer;display: inline;margin-left: 15px;">
                                        <path d="M12 20h9"></path>
                                        <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                                    </svg>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}</span>
                            </div>
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            </div>
                        </div>

                        <div v-if="message.sent_to.id == userStore.user.id" class="flex w-full mt-2 space-x-3 max-w-md">
                            <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                                <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                            </div>
                            <div>
                                <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                    <p class="text-sm">{{ message.body }}</p>
                                </div>
                                <span class="text-xs text-gray-500 leading-none">{{ message.created_at_formatted }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="border border-purple-300 rounded-lg">
                <input @keyup.prevent="handleKeyEventOnInput" v-model="messageBody" id="sendMessageInput"
                    class="p-4 w-full bg-gray-100 rounded-lg hover:bg-purple-100 focus:bg-gray-100"
                    placeholder="Type a message..." />
                <input @keyup.prevent="handleKeyEventOnEditInput" v-model="editMessageBody" id="editMessageInput"
                    class="p-4 w-full bg-purple-100 rounded-lg" placeholder="Edit a message..." style="display: none;" />
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast';
import { useUserStore } from '@/stores/user';
export default {
    setup() {
        const toast = useToastStore()
        const userStore = useUserStore()
        return {
            toast,
            userStore
        }
    },
    data() {
        return {
            conversations: [],
            activeConversation: {},
            activeUser: {},
            messageBody: '',
            message: {},
            editMessageId: null,
            editMessageBody: '',
        }
    },
    mounted() {
        let activeConversation = undefined;
        if(this.$route.query.activeConversation != undefined)
        {
            activeConversation = JSON.parse(this.$route.query.activeConversation)
        }
        if(activeConversation)
        {
            console.log(activeConversation, 'from mounted');
            this.setActiveConversation(activeConversation)
            console.log(this.activeConversation, 'from mounted2');
        }
        this.loadConversations()
    },
    methods: {
        isProxyEmpty(proxy) {
            for (const prop in proxy) {
                if (proxy.hasOwnProperty(prop)) {
                return false; // Proxy has at least one property
                }
            }
            return true; // Proxy has no properties
            },
        loadConversations() {
            axios
                .get('/api/chat/')
                .then(response => {
                    console.log(response.data);
                    this.conversations = response.data.conversations;
                    console.log(this.activeConversation);
                    if(!this.isProxyEmpty(this.activeConversation))
                    {
                        this.loadMessagesForActiveConversation()
                        this.moveScrollBarOfMessageBox()
                        return;
                    }
                    else if(this.isProxyEmpty(this.activeConversation))
                    {
                        if (this.conversations.length) {
                            {
                                this.setActiveConversation(this.conversations[0])
                                console.log('redirected from other page');
                            }
                            this.loadMessagesForActiveConversation()
                            this.moveScrollBarOfMessageBox()
                        }
                        else
                        {
                            this.toast.showToast(5000, 'No Chats Available Yet!!', 'bg-orange-300')
                        }
                    }
                    else
                    {
                        console.log('redirecting');
                        this.$router.push({ name: 'chat', query: {'activeConversation': undefined}});
                    }
                })
                .catch((err) => this.toast.showToast(3000, "Couldn't load conversations", 'bg-red-300'))
        },
        loadMessagesForActiveConversation() {
            axios
                .post(`/api/chat/${this.activeConversation.id}/`)
                .then(response => {
                    this.activeConversation = response.data.activeConversation
                    this.moveScrollBarOfMessageBox()
                    console.log(this.activeConversation, 'from load active conversation');
                })
                .catch(() => {
                    this.$router.push({name: 'chat', query: {'activeConversation': undefined}})
                    this.toast.showToast(3000, 'Something went wrong.. Cannot load messages!!', 'bg-red-300')
                })
        },
        getOtherUser(users) {
            return users[0].id == this.userStore.user.id ? users[1] : users[0]
        },
        setActiveConversation(conversation) {
            console.log(conversation, 'from set active conversation');
            this.activeConversation = conversation
            this.activeUser = this.getOtherUser(conversation.users)
            this.loadMessagesForActiveConversation()
        },
        handleKeyEventOnInput(e) {
            if (e.key == 'Enter' && !e.shiftKey)
                this.sendMessage()
        }
        ,
        async sendMessage() {
            this.messageBody = this.messageBody.trim()
            if (this.messageBody) {
                await axios
                    .post(`/api/chat/${this.activeConversation.id}/sendMessage/`, { 'messageBody': this.messageBody, 'sent_to': this.activeUser.id })
                    .then(response => {
                        console.log(response.data.message, 'send');
                        if(this.activeConversation)
                        {
                            this.activeConversation.messages.push(response.data.message)
                            console.log(this.activeConversation, 'send ok');
                        }
                        else
                        {
                            this.activeConversation = undefined;
                            console.log('undefined', this.activeConversation);
                        }
                        console.log(this.activeConversation, 'send');
                        this.messageBody = ''
                    })
                    .catch(() => this.toast.showToast(3000, 'Something went wrong.. Cannot send message!!', 'bg-red-300'))
                document.getElementById('messageBox').scrollTop = document.getElementById('messageBox').scrollHeight
            }
            else {
                this.toast.showToast(2000, 'Cannot send empty message!', 'bg-orange-400')
            }
        }
        ,
        handleMouseOver(message) {
            document.getElementById(message.id + '-mssgTooltip').style.display = 'block';
            this.message = message;
        },
        handleMouseOut() {
            let mssgTooltip = document.getElementById(this.message.id + '-mssgTooltip')
            if (mssgTooltip)
                mssgTooltip.style.display = 'none';
        }
        , deleteMessage() {
            axios
                .post(`/api/chat/${this.activeConversation.id}/deleteMessage/`, { 'messageId': this.message.id })
                .then(response => {
                    this.activeConversation.messages = response.data.messages
                    this.toast.showToast(2000, 'Message deleted successfully!!', 'bg-emerald-300')
                    this.handleMouseOut()
                })
                .catch(() => this.toast.showToast(3000, 'Something went wrong..Cannot delete message!!', 'bg-red-300'))


        },
        toggleMessageEditSection() {
            this.setEditMessageValues()

            let sendMessageInput = document.getElementById("sendMessageInput")
            let editMessageInput = document.getElementById("editMessageInput")

            if (sendMessageInput.style.display == "block") {
                sendMessageInput.style.display = "none";
                editMessageInput.style.display = "block";
            }
            else {
                sendMessageInput.style.display = "block";
                editMessageInput.style.display = "none";
            }
        }
        ,
        setEditMessageValues() {
            this.editMessageBody = this.message.body;
            this.editMessageId = this.message.id;
        },
        setEditMessageValuesToDefault() {
            this.editMessageBody = '';
            this.editMessageId = null;
        }
        ,
        handleKeyEventOnEditInput(e) {
            if (e.key == 'Enter' && !e.shiftKey)
                this.updateMessage()
        },
        updateMessage() {
            axios
                .post(`/api/chat/${this.activeConversation.id}/editMessage/`, { 'messageId': this.editMessageId, 'messageBody': this.editMessageBody })
                .then(response => {
                    this.activeConversation.messages = response.data.messages
                    this.toast.showToast(2000, 'Message Updated successfully!!', 'bg-emerald-300')
                    this.handleMouseOut()
                    this.toggleMessageEditSection()
                    this.setEditMessageValuesToDefault()
                })
                .catch(() => this.toast.showToast(3000, 'Something went wrong..Cannot update message!!', 'bg-red-300'))

        },
        moveScrollBarOfMessageBox()
        {
            this.$nextTick(() => {
                        const messageBox = document.getElementById('messageBox');
                        if (messageBox) {
                            messageBox.scrollTop = messageBox.scrollHeight;
                        }
            });
        }
    }
}
</script>
