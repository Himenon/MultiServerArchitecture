<template lang="pug">
  v-app
    v-toolbar(fixed app dark)
      v-toolbar-title
        v-btn(flat to='/') {{ siteTitle }}
      v-spacer
      v-toolbar-items
        v-btn(flat) Flask
        v-btn(flat) Sinatra
    v-content
      <nuxt/>
</template>

<script>
import * as pkg from '~/package.json'

export default {
  data: () => ({
    siteTitle: pkg.name
  }),
}
</script>

<style>
body {
  background-color: #eeeeee
}
</style>
