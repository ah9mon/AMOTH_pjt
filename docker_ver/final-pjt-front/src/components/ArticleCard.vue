<template>
	<v-card 
		v-if="article"
		class="article-card mt-3 border-around"
		@click="toArticleDetail"
		tile
		style="color:white"
	>
		<v-row>
			<v-col class="writer" cols="12" sm="4">
				<div>
					<span class="text-h6">{{ article.movie_title }}</span>
				</div>
				<div>
					<span class="text-subtitle-1">{{ article.music_title }}</span>
				</div>
			</v-col>
			
			<v-col class="title" cols="9" sm="6">
				<span class="text-h4">{{ article.title }}</span>
			</v-col>
	
			<v-col class="like-button" cols="3" sm="2">
				<LikeButton
					:isLiked="isLiked"
					:article="article"
					:likedCount="likedCount"
					@update="getArticle"
				/>
			</v-col>
		</v-row>
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
			const temp = String(this.article.id)
			this.$router.push({name: 'articleDetail', 
				params:{
					id: temp
			}})
		},
		getArticle() {
			axios({
				method: 'GET',
				url: `http://localhost:8002/api/community/articles/${this.article.id}`,
				params : {
					user_id : this.user_id
				}
			})
				.then((res) => {
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
	background-color: transparent !important;
	backdrop-filter: blur(10px) !important;
}
.writer {
	text-overflow: ellipsis;
	overflow: hidden;
	white-space: nowrap;
}
.title {
	text-overflow: ellipsis;
	overflow: hidden;
	white-space: nowrap;
}
.border-around {
	border-top: 1px solid;
	border-color: rgba(120, 120, 120, 0.5) !important; 
	margin-bottom: 21px;
}
</style>