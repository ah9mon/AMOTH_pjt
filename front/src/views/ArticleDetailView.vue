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
				{{ article.comments }}
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: 'ArticleDetailView',
	props: {
		id: String
	},
	computed: {
		article() {
			// get article by id
			return {
					title: 'first article',
					writer: 'man1',
					id: '1',
					content: 'first article content',
					comments: [
						'first comment',
						'second comment'
					]
				}
		}
	}
}
</script>

<style>


</style>