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
import ArticleCard from '@/components/ArticleCard.vue';

export default {
	name: 'ArticleListView',
	components: {
		ArticleCard
	},
	// computed: {
	// 	articleList() {

	// 	}
	// },
	data() {
		return {
			articleList: [
				{
					title: 'first article',
					writer: 'man1',
					id: '1'
				},
				{
					title: 'second article',
					writer: 'man2',
					id: '2'
				}
			]
		}
	}
}
</script>

<style>

</style>