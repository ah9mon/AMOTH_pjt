<template>
  <v-app id="base">
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
#base{
	background-image: url("@/assets/Background.jpg");
	background-size: cover;
}
</style>