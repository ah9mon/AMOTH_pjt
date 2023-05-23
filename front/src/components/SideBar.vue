<template>
    <v-row>
      <v-navigation-drawer
        v-model="drawer"
        temporary
        app
      >
        <v-list-item
          prepend-avatar='../assets/logo.png'
          title="hihi"
        >ProfilPicture</v-list-item>
        <v-divider></v-divider>
        <v-list nav>
          <v-list-item title="Profile" value="profile"
            @click="toProfileView"
          >
            Profile
          </v-list-item>
        </v-list>
      </v-navigation-drawer>
      <v-app-bar class="transparent" flat>
        <v-app-bar-nav-icon 
          @click="drawer = !drawer"
          color="rgb(255, 255, 255)"
        >
        </v-app-bar-nav-icon>
      </v-app-bar>
    </v-row>
</template>

<script>
export default {
	name: 'SearchView',
	data: () => ({ drawer: null }),
  methods: {
    toProfileView() {
      this.$router.push({name: 'profile', params:{id:1}})
    }
  }
}
</script>

<style>

</style>