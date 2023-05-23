<template>
	<v-container class="blur small-tile d-flex">
		<v-row
			justify="center"
		>
			<v-col
				lg="4"
			>
				<div 
					class="login d-flex flex-column pt-lg-15"
					align="center"
					
				>
					<h1>LOGIN</h1>
					<div class="d-flex mt-9" style="justify-content: space-evenly">
						<a href="http://127.0.0.1:8000/api/kakao"><v-btn>
							kakao
						</v-btn></a>
						<v-btn>
							google
						</v-btn>
					</div>
				</div>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: 'LoginView',
	data() {
		return {
			userName: null,
			password: null
		}
	},
	created() {
		if (this.$route.query.access_token != null) {
			this.$store.dispatch('saveToken', this.$route.query.access_token)
			this.getUserInfo()
			this.$router.push({name: 'search'})
		}
	},
	methods: {
		getUserInfo() {
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8000/api/kakao/auth',
				headers: {
					'authorization': this.$store.state.token
				}
			})
				.then((res) => {
					console.log('Logged In')
					const payload = {
						'user_id': res.data.user_id,
						'profile_picture': res.data.profile_picture
					}
					this.$store.dispatch('saveUserInfo', payload)
				})
		}
	}
}
</script>

<style>
.login {
	background-color: red;
	height: 90%;
}
</style>