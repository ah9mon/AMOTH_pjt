<template>
	<v-card 
		v-if="article"
		class="article-card mt-3 pa-1 d-flex flex-no-wrap" 
		@click="toArticleDetail"
	>

		<div class="writer">
			<div>
				<span class="text-h6">{{ article.movie_title }}</span>
			</div>
			<div>
				<span class="text-subtitle-1">{{ article.music_title }}</span>
			</div>
			<!-- <v-img :src="url + movie.posterPath" contain class="posterImage"></v-img> -->
			<!-- profilepicture??? -->
		</div>
		<div class='title'>
			<span class="text-h4">{{ article.title }}</span>
		</div>
		<div class="like-button">
			<LikeButton
				:isLiked="isLiked"
				:article="article"
				:likedCount="likedCount"
				@update="getArticle"
			/>
		</div>
	</v-card>
</template>

<script>
import axios from 'axios'
import LikeButton from './LikeButton.vue'

export default {
	name: 'articleCard',
	props: {
		article: Object
	},
	components: {
		LikeButton
	},
	data() {
		return {
			likedCount: null,
			isLiked: null
		}
	},
	computed: {
		user_id() {
			return this.$store.state.user_id
		}
	},
	methods: {
		toArticleDetail() {
			this.$router.push({name: 'articleDetail', 
				params:{
					id: String(this.article.id)
			}})
		},
		getArticle() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8002/api/community/articles/${this.article.id}`,
				params : {
					user_id : this.user_id
				}
			})
				.then((res) => {
					console.log(res.data)
					this.likedCount = res.data.liked_count,
					this.isLiked = res.data.liked
				})
		},
	},
	created() {
		this.getArticle()
	}
}
</script>

<style>
.article-card {
	height: 7.8vh;
	background-color: transparent !important;
	backdrop-filter: blur(10px) !important;
}
.writer {
	flex-basis: 32%;
	text-overflow: ellipsis;
	overflow: hidden;
	white-space: nowrap;
	padding-left: 1vh;
	border-right-color: black;
	border-right-style: solid;
}
.title {
	flex-basis: 55%;
	text-overflow: ellipsis;
	overflow: hidden;
	white-space: nowrap;
	padding-left: 1vh;
}
.like-button {
	flex-basis: 10%;
	display: flex;
	justify-content: center;
}

</style>