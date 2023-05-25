<template>
	<v-container id="search">
		<div class="mt-5" style='height: 100px;'>
		</div>
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
								v-bind="attrs"
								v-on="on"
								icon
							>
							<v-icon size="32">
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
		
		<!-- loading -->
		<v-row
			justify="center"
			class="pt-5"
		>
			<v-progress-circular
				color="primary"
				indeterminate
				v-if="isAsking"
				size="90"
				width="7"
			>
			</v-progress-circular>
			<h1>{{ GPTerror }}</h1>
		</v-row>

		<!-- Movie Cards -->
		<v-row
			class="d-flex flex-column"
			align-content="center"
			v-if="movieList && ask"
		>
			<v-col
				lg="8"
				class="px-5"
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
		scrollUp() {
			window.scroll({
				top: 0,
				left: 0,
				behavior: 'smooth'
			})
		},	
		toggleGPT() {
			this.ask = true
			if (this.query != null) {
				this.sendQuery()
			}
		},
		toggleDB() {
			this.ask = false
			if (this.query != null) {
				this.sendQuery()
			}
		},
		sendQuery() {
			if (this.isAsking) {
				this.ask = !this.ask
				alert('GPT is working. Please wait......')
				return
			}
			this.isAsking = true
			console.log('sendQuery')
			if (this.ask === true) {
				this.askChatGPT()
			} else {
				this.findDB()
			}
		},
		getWeather(weather) {
			this.weather = weather
		},
		findDB() {
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8001/api/tmdb/movies/search',
				params: {
					'q': this.query
				}
			})
				.then((res) => {
					console.log('found at DB:', res)
					this.$store.dispatch('updateDatabaseList', res.data)
					this.isAsking = false
					this.scrollUp()
					this.query = null
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
				url: `http://127.0.0.1:8000/api/${this.$store.state.source}/auth`,
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
							this.scrollUp()
							this.query = null
						})
				})
				.catch((error) => console.log(error))
		},
		async askChatGPT() {
			try {
				console.log('GPT START:')
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
#search {
	max-height: none;
}
.hamburger {
	color:white !important;
	font-size: large !important;
	width: 100px !important;
}
.searchMenu {
	position: absolute;
	top: 25%;
	right: 2.5vw;
}
</style>