<template>
	<v-container class="blur big-tile">
		<v-row
			v-if="articleList"
			justify="center"
		>
			<v-col
				lg="10"
				style="padding-top: 3%"
			>
				<ArticleCard
					v-for="(article, index) in articleList.slice((page - 1) * 8, page * 8)"
					:key="index"
					:article="article"
				/>
				<!-- pagination! -->
				<v-pagination
					class="pagination"
					v-model="page"
					:length="pageLength"
				></v-pagination>
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
			articleList: null,
			page: 1,
		}
	},
	computed: {
		pageLength() {
			return Math.ceil(this.articleList.length / 8)
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
							console.log('articleList: ', res)
							this.articleList = res.data
						})
						.catch((err) => console.log(err))
				})
		}
	},
	watch: {
		page() {
			console.log(this.page)
		}
	},
	created() {
		this.getArticleList()
	}
}
</script>

<style>
</style>