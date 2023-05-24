<template>
	<v-container class="blur big-tile">
		<v-row
			v-if="pageLength"
			justify="center"
		>
			<v-col
				lg="10"
				style="max-height: 90vh;"
			>
				<ArticleCard
					v-for="(article, index) in articleList.slice((page - 1) * 9, page * 9)"
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
			if (this.articleList === null) {
				return 0
			}
			return Math.ceil(this.articleList.length / 8)
		}
	},
	methods: {
		getArticleList() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8000/api/${this.$store.state.source}/auth`,
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
		console.log('aaaa',this.articleList)
	}
}
</script>

<style>
</style>