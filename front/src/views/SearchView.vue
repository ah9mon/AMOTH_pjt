<template>
	<v-container>
		<!-- side bar -->
		<!-- <SideBar/> -->
		<!-- weather -->
		<WeatherCard
			@getWeather="getWeather"
		/>
		<!-- search bar -->
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

					<v-menu
						open-on-hover
						bottom
						offset-y
					>
						<template v-slot:activator="{ on, attrs }">
							<v-btn
								class="searchMenu"
								:color="ask ? 'primary' : 'secondary'"
								dark
								v-bind="attrs"
								v-on="on"
							>
							<v-icon size="30">
								mdi-magnify</v-icon>
							</v-btn>
						</template>
						
						<v-list>
							<v-list-item
								@click="toggleGPT"
							>
							<v-list-item-title>askChatGPT</v-list-item-title>
							</v-list-item>
							<v-list-item
								@click="toggleDB"
							>
							<v-list-item-title>find DB</v-list-item-title>
							</v-list-item>
						</v-list>
					</v-menu>
				</v-col>
			</v-row>
		

		<!-- Movie Cards -->
		<v-row
			class="d-flex flex-column"
			align-content="center"
			v-if="movieList && ask"
		>
			<v-col
				lg="8"
			>
				<MovieCard
					v-for="(movie, index) in movieList"
					:key="index"
					:movie="movie"
				/>
			</v-col>
		</v-row>
		<v-row
			class="d-flex flex-column"
			align-content="center"
			v-if="databaseList && !ask"
		>
			<v-col
				lg="8"
			>
				<MovieCard
					v-for="(movie, index) in databaseList"
					:key="index"
					:movie="movie"
				/>
			</v-col>
		</v-row>

		<!-- loading -->
		<v-row
			justify="center"
			class="mt-5 mb-5"
		>
			<v-progress-circular
				color="primary"
				indeterminate
				v-if="isAsking"
				size="100"
				width="10"
			>
			</v-progress-circular>
			<h1>{{ GPTerror }}</h1>
			<div style="height: 100px">
				
			</div>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
import MovieCard from '@/components/MovieCard.vue'
import WeatherCard from '@/components/WeatherCard.vue'
import { Configuration, OpenAIApi } from 'openai'

export default {
	name: 'SearchView',
	components: {
		MovieCard,
		WeatherCard,
	},
	data: () => ({
		drawer: null,
		answer: null,
		query: null,
		ask: true,
		isAsking: false,
		GPTerror: null,
	}),
	computed: {
		movieList() {
			return this.$store.state.movieList
		},
		databaseList() {
			return this.$store.state.databaseList
		},
		accessToken() {
			return this.$route.query.access_token
		}
	},
	methods: {
		scrollDown() {
			window.scroll({
				top: document.body.scrollHeight,
				left: 0,
				behavior: 'smooth'
			})
		},	
		toggleGPT() {
			this.ask = true
			// this.sendQuery()
		},
		toggleDB() {
			this.ask = false
			// this.sendQuery()
		},
		sendQuery() {
			if (this.isAsking) {
				console.log('U R asking')
				return
			}
			this.isAsking = true
			console.log('sendQuery')
			if (this.ask === true) {
				this.askChatGPT()
			} else {
				this.findDB()
			}
			this.scrollDown()
		},
		getWeather(weather) {
			this.weather = weather
		},
		findDB() {
			axios({
				method: 'POST',
				url: 'http://127.0.0.1:8001/api/tmdb/movies/search',
				params: {
					'q': this.query
				}
			})
				.then((res) => {
					this.$store.dispatch('updateDatabaseList', res.data)
					this.isAsking = false
					this.scrollDown()
				})
		},
		parseMessage(content) {
			console.log('GPT answer:\n', content)
			const start = content.indexOf('{')
			const end = content.lastIndexOf('}')
			const payload = JSON.parse(content.slice(start, end + 1))
			console.log('parsed answer:', payload)
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8000/api/kakao/auth',
				headers: {
					'authorization': this.$store.state.token
				}
			})
				.then(() => {
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
							this.scrollDown()
						})
				})
				.catch((error) => console.log(error))
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
							content: `And ${this.query}. Please recommend 10 movies perfect for weather like "${this.weather}" in JSON format. {
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
				this.isAsking = false
			} catch (error) {
				this.isAsking = false
				console.log('gpt error:', error)
				this.GPTerror = error
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
.searchMenu {
	position: absolute;
	top: 24%;
	right: 1vw;
}
</style>