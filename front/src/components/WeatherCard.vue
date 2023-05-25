<template>
	<v-row class="mx-1 mb-1">
		<v-col
			cols="12"
			class="blur"
			align="center"
			style="color: white;"
		>
			<h1 class="weather-title" @click="getWeather">WEATHER</h1>
			<v-img 
				v-if="icon"
				:src="imgURL + icon + urlTail"
				max-width="100px"
				></v-img>
			<h2 class="weather">{{ weather }}</h2>
			<MovieCard
				:movie="movie"
			/>
		</v-col>
	</v-row>
</template>

<script>
import axios from 'axios'
import MovieCard from './MovieCard.vue'
export default {
	name: 'WeatherCard',
	components: {
		MovieCard
	},
	data() {
		return {
			weather: null,
			latitude: null,
			longitude: null,
			imgURL: 'https://openweathermap.org/img/wn/',
			icon: null,
			urlTail: '@2x.png',
		}
	},
	computed: {
		movie() {
			return this.$store.state.initialMovie
		}
	},
	methods: {
		getGeolocation() {
				if ('geolocation' in navigator) {
					window.navigator.geolocation.getCurrentPosition((pos) => {
					this.latitude = pos.coords.latitude
					this.longitude = pos.coords.longitude
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
					this.weather = res.data.weather[0].description
					this.icon = res.data.weather[0].icon
					if (this.$vuetify.theme.dark) {
						this.icon = this.icon.replace('d', 'n')
					}
					// 일단 패스
					this.$emit('getWeather', this.weather)
				})
				.catch((err) => {
					console.log('Error at getWeather', err)
				})
		},
	},
	created() {
		this.getGeolocation()
	}
}
</script>

<style>
.weather-title {
	letter-spacing: 0.5rem;
}
</style>