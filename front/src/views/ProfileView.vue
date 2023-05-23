<template>
	<v-container class="blur big-tile">
		<v-row>
			<!-- left column for profile picture & articles-->
			<v-col
				cols="6"
			>
				<v-row
					class="profile-picture"
					style="height: 40%"
				>
					<v-img :src="profile_picture" style="height: 100%"></v-img>
				</v-row>
				<v-row
					class="my-articles"
					style="height: 30%"
				>
						<v-list dense
							class="overflow-y-auto"
							max-height="100%"
							width="100%"
							style="background-color: transparent"
						>
							<v-subheader>My Articles</v-subheader>
							<v-list-item-group
								color="primary"
							>
								<v-list-item
									v-for="(article, index) in myArticles"
									:key = index
									@click="toArticleDetail(article)"
								>
									<v-list-item-content>
										<v-list-item-title>
											{{ article.title }}
										</v-list-item-title>
									</v-list-item-content>
								</v-list-item>
							</v-list-item-group>
						</v-list>
				</v-row>

				<v-row
					class="liked-articles"
					style="height: 25%"
				>
					<v-list dense
						class="overflow-y-auto"
						max-height="100%"
						width="100%"
						style="background-color: transparent"
					>
						<v-subheader>Liked Articles</v-subheader>
						<v-list-item-group
							color="primary"
						>
							<v-list-item
								v-for="(article, index) in likedArticles"
								:key = index
								@click="toArticleDetail(article)"
							>
								<v-list-item-content>
									<v-list-item-title>
										{{ article.title }}
									</v-list-item-title>
								</v-list-item-content>
							</v-list-item>
						</v-list-item-group>
					</v-list>
				</v-row>
			</v-col>
			<!-- right column for watched movies -->
			<v-col
				cols="6"
				class="watched-movies"
			>
				watched movies
				
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: 'ProfileView',
	data() {
		return {
			myArticles: null,
			likedArticles: null,
			articleTitles: {},
		}
	},
	computed: {
		user_id() {
			return this.$store.state.user_id
		},
		profile_picture() {
			return this.$store.state.profile_picture
		}
	},
	methods: {
		toArticleDetail(article) {
			console.log(article)
			this.$router.push({
				name: 'articleDetail',
				params: {
					id: article.id,
					article: article
				}
			})
		},
		getMyArticles() {
			axios({
						method: 'GET',
						url: 'http://127.0.0.1:8002/api/community/articles',
						params: {'user_id': this.user_id}
					})
						.then((res)=>{
							this.myArticles = res.data.my_articles
							let temp = []
							for (const obj of res.data.liked_articles) {
								axios({
									method: 'GET',
									url: `http://127.0.0.1:8002/api/community/articles/${obj.article}`,
								})
									.then((res) => {
										temp.push(res.data.article)
									})
							}
							this.likedArticles = temp
						})
						.catch((err)=>console.log(err))
		},
	},
	created() {
		this.getMyArticles()
	}
}
</script>

<style>
.watched-movies {
	background-color: green;
}

</style>