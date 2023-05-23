<template>
  <v-app id="background">
    <v-main>
      <router-view/>
      <!-- menu button -->
      <MenuButton/>
    </v-main>
  </v-app>
</template>
<script>
import MenuButton from './components/MenuButton.vue';

export default {
  name: 'App',
  components: {
    MenuButton
  },
  computed: {
    profile_picture() {
      return this.$store.state.profile_picture
    }
  }
};
</script>

<style>
</style>