<template lang="pug">
  v-container(grid-list-md)
    v-flex.xs-12
      v-card(dark color="primary")
        v-card-text Flask | {{socketUrl}}
    ChatView(:messages='messages', v-on:submit-message='onSubmitMessage')
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'
import ChatView from '~/components/chat'

export default {
  data: () => ({
    socketUrl: 'http://localhost:5000/websocket'
  }),
  computed: {
    ...mapState('Message', {
      messages: state => state.messages
    })
  },
  components: {
    ChatView,
  },
  methods: {
    onSubmitMessage: async function(event, payload) {
      this.$store.dispatch('Message/sendMessage', payload)
    }
  },
  mounted () {
    const settings = {
      socketUrl: this.socketUrl
    }
    this.$store.dispatch('Message/initializeWebSocket', settings)
  }
}
</script>

<style>
</style>
