<template>
	<v-container class="blur small-tile d-flex"
		style="flex-direction: column;"
	>
		<v-row
			justify="center"
			style="max-height: 20vh;"
		>
			<v-col
				lg="4"
			>
				<div 
					class="d-flex flex-column"
					style="align-items: center;"
				>
					<v-img 
						:src="logo"
						class="logo-img"
					></v-img>

					<h1 class="login-text">LOGIN</h1>
				</div>
			</v-col>
		</v-row>

		<v-row
			style="justify-content: center;"
		>
			<v-col>
				<div class="d-flex mt-9" 
					style="justify-content: center">
					<a href="http://127.0.0.1:8000/api/kakao">
						<v-img :src="kakaoLogin" class="login-img1"></v-img>
					</a>
					<a href="http://127.0.0.1:8000/api/naver">
						<v-img :src="naverLogin" class="login-img2"></v-img>
					</a>
				</div>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
import { Configuration, OpenAIApi } from 'openai'
import logo from '@/assets/logo.png'
import kakaoLogin from '@/assets/kakao.png'
import naverLogin from '@/assets/naver.png'

export default {
	name: 'LoginView',
	data() {
		return {
			userName: null,
			password: null,
			latitude: null,
			longitude: null,
			logo: logo,
			kakaoLogin: kakaoLogin,
			naverLogin: naverLogin
		}
	},
	created() {
		this.initiate()
		if (this.$route.query.access_token != null) {
			this.$store.dispatch('saveToken', this.$route.query.access_token)
			this.$store.dispatch('saveSource', this.$route.query.source)
			this.getUserInfo()
			this.$router.push({name: 'search'})
		}
	},
	methods: {
		initiate() {
			this.applyDarkMode()
			// this.getGeolocation()
		},
		applyDarkMode() {
			this.$vuetify.theme.dark = this.$store.state.darkmode
		},
		getUserInfo() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8000/api/${this.$store.state.source}/auth`,
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
		},
		getGeolocation() {
				if ('geolocation' in navigator) {
					window.navigator.geolocation.getCurrentPosition((pos) => {
					this.latitude = pos.coords.latitude
					this.longitude = pos.coords.longitude
					console.log(this.latitude)
					console.log(this.longitude)
					this.getWeather()
				})
			} else {
				console.log('Error: getGeolocation')
			}
		},
		getWeather() {
			const params = {
				lat: this.latitude,
				lon: this.longitude,
				appid: process.env.VUE_APP_WEATHER_KEY,
			}
			axios({
				url: 'https://api.openweathermap.org/data/2.5/weather',
				method: 'GET',
				params:params
			})
				.then((res) => {
					console.log(res.data.weather[0])
					this.weather = res.data.weather[0].description
					this.askChatGPT()
				})
				.catch((err) => {
					console.log('weather error', err)
				})
		},
		async askChatGPT() {
			try {
				console.log('INITIAL ASK START:')
				const configuration = new Configuration({
					apiKey: process.env.VUE_APP_GPT_KEY
				})
				const openai = new OpenAIApi(configuration)
				const completion = await openai.createChatCompletion({
					model: "gpt-3.5-turbo",
					messages: [
						{
							role: 'system',
							content: `You are the MovieGPT, an AI model trained to give people movie suggestion that fits perfectly for the weather.`
						},
						{
							role: 'assistant',
							content: `Today's weather is "${this.weather}". You must give user suggestion based on the weather. Explain your suggestion related to the weather.`
						},
						{
							role: "user",
							content: `Please recommend 10 movies perfect for today's weather in JSON format. {
								"movies" : {
									"movie1":{"title" : "title of movie1", "release_data":"date","reason": "reason for recommend"},
									"movie2":{"title" : "title of movie2", "release_data":"date", "reason": "reason for recommend"},
									...
									}
								}
								Like this. And please send me the reason for the recommendation in Korean. But the movie title should be English.`
						},
					],
					temperature: 0.62
				})
				const content = completion.data.choices[0].message.content
				this.parseMessage(content)
			} catch (error) {
				console.log('gpt error:', error)
			}
		},
		parseMessage(content) {
			console.log('INITIAL GPT answer:\n', content)
			const start = content.indexOf('{')
			const end = content.lastIndexOf('}')
			const payload = JSON.parse(content.slice(start, end + 1))
			console.log('INITIAL parsed answer:', payload)
			axios({
				method: 'POST',
				url: 'http://127.0.0.1:8001/api/tmdb/movies',
				data: payload
			})
				.then((res) => {
					let temp = []
					for (const obj of res.data) {
						let tempObj = obj
						for (const movieKey in payload.movies) {
							if (tempObj.title === payload.movies[movieKey].title) {
								tempObj.reason = payload.movies[movieKey].reason
								temp.push(tempObj)
							}
						}
					}
					this.$store.dispatch('updateMovieList', temp)
				})
		},
	}
}
</script>

<style>
.login-text {
	position: relative;
	left: 0.4rem;
	letter-spacing: 1rem;
}
.logo-img {
	max-width: 300px;
	margin-bottom: 20px;
}
.login-img1 {
	position: relative;
	right: 1rem;
	aspect-ratio: 3.8;
	max-width: 12vh;
}
.login-img2 {
	position: relative;
	left: 1rem;
	aspect-ratio: 3.8;
	max-width: 12vh;
}
</style>