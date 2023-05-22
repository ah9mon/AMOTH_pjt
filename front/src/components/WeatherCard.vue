<template>
	<v-row>
			<v-col
				cols="12"
				class="blur"
				align="center"
			>
				<h1 @click="getWeather" style="color:white">WEATHER</h1>
				<h4>{{ latitude }} / {{ longitude }}</h4>
				<h2 style="color:white">{{ weather }}</h2>
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
					this.$emit('getWeather', this.weather)
				})
				.catch((err) => {
					console.log('wsaefwae', this.latitude)
					console.log('sdafads',this.longitude)
					console.log(err)
				})
		},
	},
	created() {
		this.getGeolocation()
	}
}
</script>

<style>

</style>