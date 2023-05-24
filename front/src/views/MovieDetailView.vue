<template>
	<v-container class="blur big-tile" :fluid="true">
		<!-- poster & youtube -->
		<v-row
		>
			<v-col
				cols="4"
				lg="3"
				class="pa-1"
			>
				<v-img 
					contain
					style="max-height: 500px; min-width:105px"
					:src="posterURL + movie.poster_path"
				></v-img>
			</v-col>
			<v-col
				cols="8"
				lg="9"
				class="pa-1"
			>
				<iframe width="100%" height="100%"
					:src='youtubeURL + youtubeId'
					allowfullscreen
				></iframe>
			</v-col>
		</v-row>

		<!-- content -->
		<v-row
		>
			<v-col
				cols="12"
				lg="8"
			>
				<v-row>
					<v-col>
						<h1>
							{{ movie.title }}
						</h1>
					</v-col>
				</v-row>

				<v-row>
					<v-col>
						{{ movie.overview }}
					</v-col>
				</v-row>
			</v-col>
			<v-col
				cols="12"
				lg="4"
			>
				<SoundtrackCard
					v-if="youtubeInfo"
					:youtube-info="youtubeInfo"
				/>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
// import imgURL from '@/assets/Background.jpg'
import SoundtrackCard from '@/components/SoundtrackCard.vue'

export default {
	name: 'MovieDetail',
	components: {
		SoundtrackCard
	},
	props: {
		id: String
	},
	data () {
		return {
			posterURL: 'https://image.tmdb.org/t/p/w500',
			backdropURL: 'https://image.tmdb.org/t/p/original',
			youtubeURL: 'https://www.youtube.com/embed/',
			youtubeId: null,
			soundtrackId: null,
			youtubeInfo: null
		}
	},
	computed: {
		movie() {
			return this.$store.getters.getMovie(Number(this.id))
		},
		isDark() {
			return this.$vuetify.theme.dark
		}
	},
	watch: {
		isDark() {
			this.changeMode()
		}
	},
	methods: {
		getYoutubeInfo() {
			// axios({
			// 	method: 'GET',
			// 	url: 'http://127.0.0.1:8003/api/youtube/soundtrack',
			// 	params: {
			// 		'movie_title': this.movie.title,
			// 	}
			// })
			// 	.then((res) => {
			// 		console.log(res.data)
			// 		this.youtubeInfo = res.data
			// 	})
		},
		getSoundtracks() {
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8003/api/youtube/soundtrack',
				params:{'movie_title': this.movie.title}
			})
				.then((res) => {
					console.log('youtube: ',res)
					this.soundtrackId = res.data.id.playlistId
					console.log(this.soundtrackId)
				})
				.catch((err) => console.log(err))
		},
		changeMode() {
			const darkstyle = `background-image: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.8)), url(${this.backdropURL}${this.movie.backdrop_path});`
			const lightstyle = `background-image: url(${this.backdropURL}${this.movie.backdrop_path});`
			const style2 = `background-position: center center;`
			const style3 = `background-attachment: fixed;`
			const style1 = this.$vuetify.theme.dark ? darkstyle : lightstyle
			document.querySelector('#background').setAttribute('style', style1 + style2 + style3)
		}
	},
	created() {
		window.scroll({
				top: 0,
				left: 0,
		})
		axios({
			method: 'GET',
			url: `https://api.themoviedb.org/3/movie/${String(this.movie.movie_id)}/videos`,
			params: {api_key:'1395a6d8b9a1c30c3699c8181b8663a6'}
		})
			.then((res) => {
				console.log(res)
				console.log('results', res.data.results)
				this.youtubeId = res.data.results.filter((elem) => {
					if (elem.type === 'Trailer') {
						return true
					}
					return false
				})[0].key
			})
			.catch((err) => {
				console.log(err)
			})
		this.getYoutubeInfo()
	},
	mounted() {
		this.changeMode()
	},
	beforeDestroy() {
		const lightBackground = `background: ${this.$vuetify.theme.themes.light.background.base};`
		const darkBackground = `background: ${this.$vuetify.theme.themes.dark.background.base};`
		const background = this.isDark ? darkBackground : lightBackground
		document.querySelector('#background').setAttribute('style', background)
	}

}
</script>

<style>
</style>