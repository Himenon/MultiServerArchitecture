<template lang="pug">
  v-container(grid-list-md)
    v-layout(row wrap)
      v-flex.xs12.sm4
        v-form
          v-card
            v-container
              v-text-field(label="ユーザー名" v-model='username' required)
              v-text-field(label="メッセージ" v-model='body' required)
            v-card-actions
              v-spacer
              v-btn(flat color='primary' @click='onSubmitMessage') Submit
      v-flex.xs12.sm8
        v-card
          v-list(subheader two-line)
            v-list-tile(v-for="(message, username) in messages" :key="username" v-model='messages')
              v-list-tile-content
                v-list-tile-title {{ message.username }}
                v-list-tile-sub-title {{ message.body }}
</template>

<script>
import { mapActions, mapState, mapGetters } from 'vuex'

export default {
  data: () => ({
    username: '',
    body: '',
  }),
  computed: {
    ...mapState('Message', {
      messages: state => state.messages
    })
  },
  components: {
  },
  methods: {
    onSubmitMessage: async function(event) {
      const payload = {
        username: this.username,
        body: this.body,
      }
      this.body = ''
      this.$store.dispatch('Message/sendMessage', payload)
    }
  },
  mounted () {
    const payload = {
      socketUrl: 'http://localhost:5000/test'
    }
    this.$store.dispatch('Message/initializeWebSocket', payload)
  }
}
</script>

<style>
</style>
