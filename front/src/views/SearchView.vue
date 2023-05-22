<template>
	<v-container>
		<!-- side bar -->
		<SideBar/>
		<!-- weather -->
		<WeatherCard
			@getWeather="getWeather"
		/>
		<!-- search bar -->
		<h1>accessToken: {{ accessToken }}</h1>
		<v-row
				justify="center"
			>
				<v-col
					cols="8"
					lg="6"
					class="blur"
				>
				<v-toolbar
						dense
						rounded
					>
						<v-text-field
							hide-details
							append-icon="mdi-magnify"
							single-line
							v-model="query"
							@keyup.enter="sendQuery"
						></v-text-field>
					</v-toolbar>

				</v-col>
			</v-row>

		<!-- Movie Cards -->
		<v-row
			class="d-flex flex-column"
			align-content="center"
			v-if="movieList"
		>
			<v-col
				lg="8"
			>
					<MovieCard
						v-for="(movie, index) in movieList"
						:key="index"
						:movie="movie"
					/>
					<infinite-loading @infinite="load"></infinite-loading>
			</v-col>
		</v-row>
		<v-btn class="scroll-up" @click="scrollUp">
			click this
		</v-btn>
	</v-container>
</template>

<script>
// import axios from 'axios'
import SideBar from '@/components/SideBar.vue'
import MovieCard from '@/components/MovieCard.vue'
import WeatherCard from '@/components/WeatherCard.vue'
import InfiniteLoading from 'vue-infinite-loading'
import { Configuration, OpenAIApi } from 'openai'
import axios from 'axios'

export default {
	name: 'SearchView',
	components: {
		SideBar,
		MovieCard,
		WeatherCard,
		InfiniteLoading,
	},
	data: () => ({
		drawer: null,
		answer: null,
		query: null,
	}),
	computed: {
		movieList() {
			return this.$store.state.movieList
		},
		accessToken() {
			return this.$route.query.access_token
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
		load($state) {
			this.sendQuery()
			$state.loaded()
		},
		getWeather(weather) {
			this.weather = weather
		},
		sendQuery() {
			console.log('sendQuery')
			// this.askChatGPT()
			// this.parseMessage('aaa')
			console.log(this.$store.state.token)
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8000/api/kakao/auth',
				headers: {
					'access_token': this.$store.state.token,
				}
			})
				.then((res) => {
					console.log(res)
				})
		},
		parseMessage(content) {
			console.log(content)
			const movieList = [
				{
					title: '대부',
					posterPath: '/cOwVs8eYA4G9ZQs7hIRSoiZr46Q.jpg',
					genre: [18, 80],
					soundtracks: ['soundtrack1', 'soundtrack2', 'soundtrack3'],
					answer: '대부이기때문',
					id: '1',
					youtubeId: '1glMKLFRrnI'
				},
				{
					title: '쇼생크 탈출',
					posterPath: '/oAt6OtpwYCdJI76AVtVKW1eorYx.jpg',
					genre: [18, 80],
					soundtracks: ['soundtrack1', 'soundtrack2', 'soundtrack3'],
					answer: '쇼생크탈출이기때문',
					id: '2',
					youtubeId: '6ZUIwj3FgUY'
				},
				{
					title: '센과 치히로의 행방불명',
					posterPath: '/u1L4qxIu5sC2P082uMHYt7Ifvnj.jpg',
					genre: [16, 10751, 14],
					soundtracks: ['soundtrack1', 'soundtrack2', 'soundtrack3'],
					answer: '센과치히로의행방불명이기때문',
					id: '3',
					youtubeId: '6ZUIwj3FgUY'
				},
			]
			// const titleList = ['대부', '스즈메의 문단속', '가디언즈 오브 갤럭시 3']
			// axios({
			// 	method: 'GET',
			// 	url: ''
			// })
			// 	.then((res))
			// 	.catch((err) => console.log(err))
			// const movieList = []

			this.$store.dispatch('getMovieList', movieList)
		},
		async askChatGPT() {
			try {
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
							role: 'assistant',
							content: "First, give me 10 movies. "
						},
						{
							role: 'assistant',
							content: "Then pick 5 best which fits for today's weather."
						},
						{
							role: "user",
							content: `And ${this.query}. Give me the result as JSON form like '{title:{releaseDate:2020, reason:reason why you suggested}}'`
						},
					],
					temperature: 0.62
				})
				const content = completion.data.choices[0].message.content
				console.log('content:\n', content)
				const payload = this.parseMessage(content)
				this.$emit('getAnswer', payload)
				// this.answer = JSON.parse(completion.data.choices[0].message.content)
				// this.reason = this.answer.reason
				// return this.searchMovie(this.answer.movieTitle, this.answer.releaseYear)
			} catch (error) {
				console.log('gpt error:', error)
			}
		}
	},
}
</script>

<style>
.hamburger {
	color:white !important;
	font-size: large !important;
	width: 100px !important;
}
.scroll-up {
	position: fixed;
	background-color: red;
	bottom: 5%;
	right: 16px;
}
</style>