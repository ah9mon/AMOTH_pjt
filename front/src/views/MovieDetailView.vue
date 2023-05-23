<template>
	<v-container class="blur big-tile">
		<!-- poster & youtube -->
		<v-row
			class="d-flex"
		>
			<v-col
				cols="4"
				class="pa-1"
			>
				<v-img  style="width:100px height:425px" :src="posterURL + movie.poster_path"></v-img>
			</v-col>
			<v-col
				cols="8"
				class="pa-1"
			>
				<iframe width="100%" height="100%"
					:src='youtubeURL + youtubeId'
					allowfullscreen
				></iframe>
			</v-col>
		</v-row>

		<!-- content -->
		<v-row>
			<v-col
				cols="4"
				class="d-flex flex-column"
			>
				<div style="height: 100px">
					{{ movie.title }}
					{{ movie }}
				</div>
				<div style="height: 200px">
				</div>

			</v-col>
			<v-col
				cols="8"
			>
				<iframe width="100%" height="100%"
					:src='youtubeListURL + soundtrackId'
					allowfullscreen
				></iframe>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: 'MovieDetail',
	props: {
		id: Number
	},
	data () {
		return {
			posterURL: 'https://image.tmdb.org/t/p/w780',
			youtubeURL: 'https://www.youtube.com/embed/',
			youtubeId: null,
			youtubeListURL: 'https://www.youtube.com/embed/videoseries?list=',
			soundtrackId: null
		}
	},
	computed: {
		movie() {
			return this.$store.getters.getMovie(this.id)
		},
	},
	methods: {
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
		}
	},
	created() {
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
		this.getSoundtracks()
	}

}
</script>

<style>
</style>