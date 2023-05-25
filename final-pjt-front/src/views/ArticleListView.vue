<template>
	<v-container class="blur big-tile">
		<v-row
			v-if="pageLength"
			justify="center"
		>
			<v-col>
				<span
					v-for="(article, index) in articleList"
					:key="index"
				>
					<ArticleCard
						v-show="isInRange(index)"
						:article="article"
					/>
				</span>
				<!-- pagination! -->
				<v-pagination
					class="pagination mt-5"
					v-model="page"
					:length="pageLength"
					@input="updatePage"
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
			page: this.$store.state.page
		}
	},
	computed: {
		pageLength() {
			if (this.articleList === null) {
				return 0
			}
			return Math.ceil(this.articleList.length / 10)
		},
	},
	methods: {
		isInRange(idx) {
			if ((this.page - 1) * 10 <= idx && idx < this.page * 10) {
				return true
			}
			return false
		},
		updatePage() {
			this.$store.dispatch('updatePage', this.page)
		},
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
							this.articleList = res.data
						})
						.catch((err) => console.log(err))
				})
		}
	},
	created() {
		this.getArticleList()
	},
}
</script>

<style>
</style>