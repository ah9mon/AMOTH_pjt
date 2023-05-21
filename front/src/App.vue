<template>
  <v-app id="background">
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>
<script>

export default {
  name: 'App',

  data: () => ({
    //
  }),
};
</script>

<style>
#background{
	background-image: url("@/assets/Background.jpg");
	background-size: cover;
}
</style>