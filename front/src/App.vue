<template>
  <v-app id="background">
    <v-main>
      <v-row>
        <v-col
          cols="3"
          aspect-ratio="1"
        >
          <v-img :src="profile_picture"></v-img>
        </v-col>
      </v-row>
      <router-view/>
    </v-main>
  </v-app>
</template>
<script>

export default {
  name: 'App',
  computed: {
    profile_picture() {
      return this.$store.state.profile_picture
    }
  }
};
</script>

<style>
</style>