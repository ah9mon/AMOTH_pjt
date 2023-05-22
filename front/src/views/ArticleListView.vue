<template>
	<v-container class="blur big-tile d-flex">
		<v-row
			v-if="articleList"
		>
			<v-col
				lg="10"
			>
				<ArticleCard
					v-for="(article, index) in articleList"
					:key="index"
					:article="article"
				/>
				<!-- need pagination! -->
			</v-col>
		</v-row>
		<h1 v-else>NO ARTICLE</h1>
	</v-container>
</template>

<script>
import axios from 'axios'
import ArticleCard from '@/components/ArticleCard.vue';

export default {
	name: 'ArticleListView',
	components: {
		ArticleCard
	},
	data() {
		return {
			articleList: null
		}
	},
	methods: {
		getArticleList() {
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8000/api/kakao/auth',
				headers: {
					'authorization': this.$store.state.token
				}
			})
				.then(() => {
					axios({
						method: 'GET',
						url: 'http://127.0.0.1:8002/api/community/articles'
					})
						.then((res) => {
							console.log(res)
							this.articleList = res.data
						})
				})
		}
	},
	created() {
		this.getArticleList()
	}
}
</script>

<style>

</style>