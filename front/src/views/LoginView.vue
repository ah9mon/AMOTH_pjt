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
					<v-sheet 
						class="mx-auto"
						width="300"
					>
						<v-form
							validate-on="submit"
							@submit.prevent="login"
							class="pa-4"
						>
							<v-text-field
								v-model="userName"
								:rules="rules"
								label="User name"
							></v-text-field>
							<v-text-field
								v-model="password"
								:rules="rules"
								label="password"
							></v-text-field>
							<v-btn
								type="submit"
								block
							>
								Submit
							</v-btn>
						</v-form>
					</v-sheet>
					<div class="d-flex mt-9" style="justify-content: space-evenly">
						<a href="http://127.0.0.1:8000/api/kakao"><v-btn>
							kakao
						</v-btn></a>
						<!-- <v-btn
							@click="kakaoLogin"
						>
							kakao
						</v-btn> -->
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
// import axios from 'axios'

export default {
	name: 'LoginView',
	data() {
		return {
			rules: [
				value => this.checkValid(value),
			],
			userName: null,
			password: null
		}
	},
	created() {
		if (this.$route.query.access_token != null) {
			this.$store.dispatch('saveToken', this.$route.query.access_token)
			this.$router.push({name: 'search'})
		}
	},
	methods: {
		checkValid() {

		},
		// kakaoLogin() {
		// 	axios({
		// 		method:'GET',
		// 		url: "http://127.0.0.1:8000/api/kakao"
		// 	})
		// 		.then((res) => console.log(res))
		// 		.catch((err) => console.log(err))
		// }
	}
}
</script>

<style>
.login {
	background-color: red;
	height: 90%;
}
</style>