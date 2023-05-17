<template>
	<v-container>
		<!-- side bar -->
		<SideBar/>

		<!-- weather -->
		<v-row>
			<v-col
				cols="12"
				class="box"
				align="center"
			>
				<h1 @click="getWeather" style="color:white">WEATHER</h1>
				<h4>{{ latitude }} / {{ longitude }}</h4>
				<h2 style="color:white">{{ weather }}</h2>
				<h4>{{ query }}</h4>
			</v-col>
		</v-row>

		<!-- search bar -->
		<v-row
			justify="center"
		>
			<v-col
				cols="6"
				class="box"
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
			<MovieCard
				v-for="(movie, index) in movieList"
				:key="index"
				:movie="movie"
			/>
		</v-row>
	</v-container>
</template>

<script>
import SideBar from '@/components/SideBar.vue'
import MovieCard from '@/components/MovieCard.vue'
import axios from 'axios'
import { Configuration, OpenAIApi } from 'openai'

export default {
	name: 'SearchView',
	components: {
		SideBar,
		MovieCard
	},
	data: () => ({
		drawer: null,
		latitude: null,
		longitude: null,
		weather: null,
		query: null,
	}),
	computed: {
		movieList() {
			return [{title:'first', content:'first_content'},
							null,
							{title:'second', content:'second_content'}]
		},
	},
	methods: {
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
				lat: this.latitude,
				params:params
			})
				.then((res) => {
					console.log(res.data.weather[0])
					this.weather = res.data.weather[0].description
				})
				.catch((err) => {
					console.log('wsaefwae', this.latitude)
					console.log('sdafads',this.longitude)
					console.log(err)
				})
		},
		sendQuery() {
			console.log('sendQuery')
			this.askChatGPT()
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
							content: 'You are the Movie sommelier, an AI model created to give people best movie suggestion for their unique needs.'
						},
						{
							role: 'assistant',
							content: 'Recommend me 10 movies as form "title:title, reason:reason"'
						},
						{
							role: 'assistant',
							content: `You must suggest movie perfect for weather like ${this.weather}. Write your reason related to the weather.`
						},
						{role: "user", 
						content: `${this.query}. Make recommendation according to the weather and my query. Also give me TMDB API movie _id of each movies as python list form. `
					}],
					temperature: 0.7
				})
				console.log('completion:', completion)
				console.log('completion.data', completion.data)
				console.log('completion.data.choices', completion.data.choices)
				console.log('end: ', completion.data.choices[0].message.content)

				// this.answer = JSON.parse(completion.data.choices[0].message.content)
				// this.reason = this.answer.reason
				// return this.searchMovie(this.answer.movieTitle, this.answer.releaseYear)
			} catch (error) {
				console.log('gpt error:', error)
				// this.movie = null
				// this.error = error.message
			}
		}
	},
	created() {
		this.getGeolocation()
		// this.getWeather()
	}
}
</script>

<style>
.box {
	background-color: rgb(255 255 255 / 0.6);
	backdrop-filter: blur(10px);
	border: 3px solid red;
}
.box1 {
	background-color: rgb(255 255 255 / 0.6);
	backdrop-filter: blur(10px);
}
.hamburger {
	color:white !important;
	font-size: large !important;
	width: 100px !important;
}

</style>