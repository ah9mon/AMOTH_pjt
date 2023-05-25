<template>
	<v-row>
			<v-col
				cols="12"
				class="blur"
				align="center"
			>
				<h1 class="weather-title" @click="getWeather">WEATHER</h1>
				<h2 class="weather">{{ weather }}</h2>
			</v-col>
		</v-row>
</template>

<script>
import axios from 'axios'
export default {
	name: 'WeatherCard',
	data() {
		return {
			weather: null,
			latitude: null,
			longitude: null,
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
	color: black;
	letter-spacing: 0.5rem;
}
.weather {
	color: black;
}
</style>