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
.container {
  max-height: 90vh;
  overflow-y: scroll;
}

.container::-webkit-scrollbar {
  width: 0.5em; /* 스크롤바 너비 */
}

.container::-webkit-scrollbar-track {
  background-color: transparent; /* 스크롤바 트랙 배경색 */
}

.container::-webkit-scrollbar-thumb {
  background-color: rgb(129, 129, 129); /* 스크롤바 색상 */
}
</style>