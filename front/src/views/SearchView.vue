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
					<!-- <infinite-loading 
						@infinite="load"
					></infinite-loading> -->
			</v-col>
		</v-row>
		<!-- menu button -->
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
					@click="articleCreate"
				>
				<v-list-item-title>Create Article</v-list-item-title>
				</v-list-item>
				
				<v-list-item
					@click="scrollUp"
				>
				<v-list-item-title>Scroll Up</v-list-item-title>
				</v-list-item>
      </v-list>
    </v-menu>
	</v-container>
</template>

<script>
// import axios from 'axios'
import SideBar from '@/components/SideBar.vue'
import MovieCard from '@/components/MovieCard.vue'
import WeatherCard from '@/components/WeatherCard.vue'
// import InfiniteLoading from 'vue-infinite-loading'
import { Configuration, OpenAIApi } from 'openai'
// import axios from 'axios'

export default {
	name: 'SearchView',
	components: {
		SideBar,
		MovieCard,
		WeatherCard,
		// InfiniteLoading,
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
		articleCreate() {
			this.$router.push({name:'articleCreate'})
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
			this.parseMessage('aaa')
			console.log(this.$store.state.token)
		},
		parseMessage(content) {
			console.log('answer: ',content)
			const ml = [
				{
					title: '대부',
					poster_path: '/cOwVs8eYA4G9ZQs7hIRSoiZr46Q.jpg',
					genre: [18, 80],
					soundtracks: ['soundtrack1', 'soundtrack2', 'soundtrack3'],
					answer: '대부이기때문',
					id: 1,
					youtubeId: '1glMKLFRrnI'
				},
				{
					title: '쇼생크 탈출',
					poster_path: '/oAt6OtpwYCdJI76AVtVKW1eorYx.jpg',
					genre: [18, 80],
					soundtracks: ['soundtrack1', 'soundtrack2', 'soundtrack3'],
					answer: '쇼생크탈출이기때문',
					id: 2,
					youtubeId: '6ZUIwj3FgUY'
				},
				{
					title: '센과 치히로의 행방불명',
					poster_path: '/u1L4qxIu5sC2P082uMHYt7Ifvnj.jpg',
					genre: [16, 10751, 14],
					soundtracks: ['soundtrack1', 'soundtrack2', 'soundtrack3'],
					answer: '센과치히로의행방불명이기때문',
					id: 3,
					youtubeId: '6ZUIwj3FgUY'
				},
			]
			const start = content.indexOf('{')

			const end = content.lastIndexOf('}')
			console.log('start/end', start, end)
			console.log('json: ', content.slice(start, end + 1))
			// const payload = JSON.parse(content.slice(start, end + 1))

		// 	axios({
		// 		method: 'GET',
		// 		url: 'http://127.0.0.1:8000/api/kakao/auth',
		// 		headers: {
		// 			'authorization': this.$store.state.token
		// 		}
		// 	})
		// 		.then(() => {
		// 			axios({
		// 				method: 'POST',
		// 				url: 'http://127.0.0.1:8001/api/tmdb/movies',
		// 				data: payload
		// 			})
		// 				.then((res) => {
		// 					console.log(res)
		// 					this.$store.dispatch('getMovieList', res)
		// 				})
		// 		})
		// 		.catch((error) => console.log(error))
		this.$store.dispatch('getMovieList', ml)
		},
		async askChatGPT() {
			try {
				console.log('ASK START:')
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
							content: `And ${this.query}. Please recommend 10 movies in sunny weather and JSON format. {
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
.menu {
	position: fixed;
	bottom: 5%;
	right: 16px;
}
</style>