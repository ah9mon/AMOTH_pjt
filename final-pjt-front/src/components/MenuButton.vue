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
					v-if="isLoggedIn"
					@click="logout"
        >
          Logout
        </v-list-item>
				<v-list-item 
					v-if="isLoggedIn"
					@click="toProfileView"
					>
					Profile
        </v-list-item>
				<v-list-item
					v-if="isLoggedIn"
          @click="toArticleListView"
        >
          Articles
				</v-list-item>

				<v-list-item
					v-if="isLoggedIn"
					@click="articleCreate"
				>
				<v-list-item-title>Create Article</v-list-item-title>
				
				</v-list-item>
				
				<v-list-item
					v-if="isLoggedIn"
					@click="toSearchView"
				>
				<v-list-item-title>To Main</v-list-item-title>
				
				</v-list-item>
				
				<v-list-item
					@click="toggleDarkMode"
				>
				<v-list-item-title
					v-if="isDark"
				>Light Mode</v-list-item-title>
				<v-list-item-title
					v-else
				>Dark Mode</v-list-item-title>
				
				</v-list-item>

				<v-list-item
					v-if="isLoggedIn"
					@click="goBack"
				>
				<v-list-item-title>Go Back</v-list-item-title>
				</v-list-item>

				<v-list-item
					v-if="isLoggedIn"
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
	computed: {
		isLoggedIn() {
			if (this.$store.state.token === null) {
				return false
			}
			return true
		},
		isDark() {
			return this.$vuetify.theme.dark
		}
	},
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
					params: {id: String(this.$store.state.user_id)}
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
		toggleDarkMode() {
			this.$vuetify.theme.dark = !this.$vuetify.theme.dark
			this.$store.dispatch('toggleDarkMode', this.$vuetify.theme.dark)
		}
	}
}
</script>

<style>
.text-color {
	/* mix-blend-mode: difference; */
	text-shadow: 0px 0px 5px black;
	background-position: center;
}
.menu {
	position: fixed;
	bottom: 5%;
	right: 16px;
}
</style>