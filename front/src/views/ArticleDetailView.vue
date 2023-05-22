<template>
	<v-container class="blur big-tile">
		<!-- title/number of likes -->
		<v-row>
			<v-col
				cols="8"
			>
				{{ article.title }}
			</v-col>
			<v-col
				cols="4"
			>
				Number of likes
			</v-col>
		</v-row>

		<!-- content & comments -->
		<v-row>
			<v-col
				cols="8"
			>
				{{ article.content }}
			</v-col>
			<v-col
				cols="4"
			>
				{{ comments }}
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: 'ArticleDetailView',
	props: {
		id: Number
	},
	data() {
		return {
			article: null,
			comments: null
		}
	},
	methods: {
		getArticle() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8002/api/community/articles/${this.id}`
			})
				.then((res) => {
					this.article = res.data
				})
		},
		getComments() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8002/api/community/articles/${this.id}/comments`
			})
				.then((res) => {
					this.comments = res.data
				})
		}
	},
	created() {
		this.getArticle()
		this.getComments()
	}
}
</script>

<style>


</style>