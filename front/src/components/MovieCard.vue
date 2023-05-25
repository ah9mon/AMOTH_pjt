<template>
	<v-card 
		v-if="movie" 
		class="mt-3 pt-1 d-flex flex-no-wrap blur" 
		style="height:110px; color: white;"
		@click="toMovieDetail"
		tile
	>
		<div class="poster">
			<v-img :src="url + movie.poster_path" contain class="posterImage"></v-img>
		</div>
		<div class='content'>
			<h2>{{ movie.title }}</h2>
			{{ movie.reason }}
		</div>
		<div class="soundtracks">
			<p v-for="(track, index) in soundtracks" :key="index">
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
			url: 'https://image.tmdb.org/t/p/w92/',
			soundtracks: null
		}
	},
	methods: {
		toMovieDetail() {
			this.$router.push({
				name:'movieDetail',
				params: {id: String(this.movie.id)}
			})
		},
	}

}
</script>

<style>
.posterImage {
	height: 103px;
}
.poster {
	flex-basis: 10%;
}
.content {
	flex-basis: 88%;
	overflow-y:scroll;
	white-space: pre-wrap;
	text-overflow: ellipsis;
}
::-webkit-scrollbar {
  width: 0.2em; /* 스크롤바 너비 */
}

::-webkit-scrollbar-track {
  background-color: transparent; /* 스크롤바 트랙 배경색 */
}

::-webkit-scrollbar-thumb {
  background-color: rgba(120, 120, 120, 0.5); /* 스크롤바 색상 */
}
</style>