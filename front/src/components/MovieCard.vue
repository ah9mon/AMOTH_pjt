<template>
	<v-card 
		v-if="movie" tile
		class="mt-3 pa-1 blured d-flex flex-no-wrap" 
		style="height:140px"
		@click="toMovieDetail"
	>
		<div class="poseter">
			<v-img :src="url + movie.posterPath" contain class="posterImage"></v-img>
		</div>
		<div class='content'>
			<h2>{{ movie.title }}</h2>
			{{ movie.answer }}
		</div>
		<div class="soundtracks">
			<p v-for="(track, index) in movie.soundtracks" :key="index">
				{{ track }}
			</p>
		</div>

	</v-card>
</template>

<script>
// image: 92, 154, 185, 342, 500, 780
export default {
	name: 'MovieCard',
	props:{
		movie: Object,
	},
	data() {
		return {
			url: 'https://image.tmdb.org/t/p/w92/'
		}
	},
	methods: {
		toMovieDetail() {
			this.$router.push({
				name:'movieDetail',
				params: {id: this.movie.id}
			})
			console.log(this.movie.id)
		}
	}

}
</script>

<style>
.blured {
	background-color: rgb(255 255 255 / 0.6) !important;
	backdrop-filter: blur(10px) !important;
}
.posterImage {
	height: 132px;
}
.poster {
	flex-basis: 10%;
}
.content {
	flex-basis: 60%;
	background-color: red;
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
}
.soundtracks {
	flex-basis: 30%;
	background-color: blue;
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
}
</style>