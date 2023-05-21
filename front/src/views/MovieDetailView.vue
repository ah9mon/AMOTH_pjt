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
				<v-img  style="width:100px height:425px" :src="posterURL + movie.posterPath"></v-img>
			</v-col>
			<v-col
				cols="8"
				class="pa-1"
			>
				<iframe width="100%" height="100%"
					:src='youtubeURL + movie.youtubeId'
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
				</div>
				<div style="height: 200px">
					{{ movie.answer }}
				</div>

			</v-col>
			<v-col
				cols="8"
			>
				{{ movie.soundtracks }}
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: 'MovieDetail',
	props: {
		id: String
	},
	data () {
		return {
			posterURL: 'https://image.tmdb.org/t/p/w780/',
			youtubeURL: 'https://www.youtube.com/embed/'

		}
	},
	computed: {
		movie() {
			return this.$store.getters.getMovie(this.id)
		}
	}

}
</script>

<style>
</style>