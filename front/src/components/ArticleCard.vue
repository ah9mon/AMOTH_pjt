<template>
	<v-card 
		v-if="article" tile
		class="article-card mt-3 pa-1 blur d-flex flex-no-wrap" 
		@click="toArticleDetail"
	>
		<div class="writer">
			<h2>{{ article.writer }}</h2>
			<!-- <v-img :src="url + movie.posterPath" contain class="posterImage"></v-img> -->
			<!-- profilepicture??? -->
		</div>
		<div class='title'>
			<h2>{{ article.title }}</h2>
		</div>
		<div class="like-button">
			<h2>need like button</h2>
		</div>

	</v-card>
</template>

<script>
export default {
	name: 'articleCard',
	props: {
		article: Object
	},
	methods: {
		toArticleDetail() {
			this.$router.push({name: 'articleDetail', params:{id:1}})
		}
	}
}
</script>

<style>
.article-card {
	height: 10%;
}
.writer {
	flex-basis: 20%;
	background-color: red;
}
.title {
	flex-basis: 70%;
	background-color: blue;
}
.like-button {
	flex-basis: 10%;
	background-color: green;
}

</style>