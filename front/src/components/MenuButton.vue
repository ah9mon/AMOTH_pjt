<template>
	
	<v-menu
      open-on-hover
      top
      offset-y
    >
      <template v-slot:activator="{ on, attrs }">
        <v-btn
					class="menu"
          color="primary"
          dark
          v-bind="attrs"
          v-on="on"
        >
          MENU
        </v-btn>
      </template>

      <v-list>
				<v-list-item
            @click="logout"
        >
          Logout
        </v-list-item>
				<v-list-item
            @click="toProfileView"
						:style="'background: url(' + this.$store.state.profile_picture + ')'"
						class="back"
        >
          <span style="color: white">Profile</span>
        </v-list-item>
				<v-list-item
          @click="toArticleListView"
        >
          Articles
				</v-list-item>

				<v-list-item
					@click="articleCreate"
				>
				<v-list-item-title>Create Article</v-list-item-title>
				
				</v-list-item>
				
				<v-list-item
					@click="toSearchView"
				>
				<v-list-item-title>To Main</v-list-item-title>
				
				</v-list-item>

				<v-list-item
					@click="goBack"
				>
				<v-list-item-title>Go Back</v-list-item-title>
				</v-list-item>

				<v-list-item
					@click="scrollUp"
				>
				<v-list-item-title>Scroll Up</v-list-item-title>
				</v-list-item>
      </v-list>
    </v-menu>
</template>

<script>
export default {
	name: 'MenuButton',
	methods: {
		scrollUp() {
			window.scroll({
				top: 0,
				left: 0,
				behavior: 'smooth'
			})
		},
		goBack() {
			this.$router.back()
		},
    toArticleListView() {
			if (this.$route.path === `/article`) {
				console.log('blocked')
			} else {
				this.$router.push({
					name: 'articleList',
				})
			}
    },
		toProfileView() {
			if (this.$route.path === `/profile/${this.$store.state.user_id}`) {
				console.log('blocked')
			} else {
				this.$router.push({
					name: 'profile',
					params: {id: this.$store.state.user_id}
				})
			}
		},
		toSearchView() {
			if (this.$route.path === '/') {
				console.log('blocked')
			} else {
				this.$router.push({
					name: 'search',
				})
			}
		},
    logout() {
      this.$store.dispatch('deleteLocalStore')
      this.$router.push({name: 'login'})
    },
		articleCreate() {
			if (this.$route.path === `/create`) {
				console.log('blocked')
			} else {
				this.$router.push({
					name: 'articleCreate',
				})
			}
		},
	}
}
</script>

<style>
.back {
	background: url('@/assets/Background.jpg');
	background-size: auto 100%;
}
</style>