<template>
	<v-container class="blur big-tile">
		<!-- title/number of likes -->
		<v-row class="top-row">
			<v-col
				cols="8"
			>
				<h1>{{ article.title }}</h1>
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
				<h2>{{ article.movie_title }}</h2>
				<h3>{{ article.music_title }}</h3>
				{{ article.content }}
				{{ isLiked }}
				{{ likedCount }}
				<v-btn
					@click="likeArticle"
				>
					LIKE
				</v-btn>
				<v-btn @click="getYoutubeId">
					getYOUTUBEID
				</v-btn>
				<a 
					target="_blank"
					:href="youtubeURL + youtubeInfo.id.videoId" 
					v-if="youtubeInfo"
				>
					<v-img 
						style="width:100px height:425px" :src="youtubeInfo.thumbnails.url">
					</v-img>
				</a>

			</v-col>
			<v-col
				cols="4"
			>
				<v-list-item
					v-for="(comment, index) in comments"
					:key="index"
				>
					{{ comment }}
				</v-list-item>
				<!-- create comment dialog -->
				<v-dialog
					v-model="dialog"
					persistent
					max-width="600px"
				>
					<template v-slot:activator="{ on, attrs }">
						<v-btn
							color="primary"
							dark
							v-bind="attrs"
							v-on="on"
						>
						Add Comment
						</v-btn>
					</template>
					<v-form
						ref="form"
						lazy-validation
					>
						<v-card>
							<v-card-title>
								<span class="text-h5">Add Comment</span>
							</v-card-title>
							<v-card-text>
								<v-container>
									<v-row>
										<v-col
											cols="12"
										>
										
											<v-textarea
												label="Comment Content"
												:counter="400"
												v-model="commentContent"
												:rules="commentContentRules"
												required
											></v-textarea>
										</v-col>
									</v-row>
								</v-container>
							</v-card-text>
							<v-card-actions>
								<v-spacer></v-spacer>
								<v-btn
									color="blue darken-1"
									text
									@click="closeCommentDialog"
								>
									Close
								</v-btn>
								<v-btn
									color="blue darken-1"
									text
									@click="submitCommentDialog"
								>
									Save
								</v-btn>
							</v-card-actions>
						</v-card>
					</v-form>
				</v-dialog>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'

export default {
	name: 'ArticleDetailView',
	props: {
		id: String
	},
	data() {
		return {
			article: {
				title: '',
				content: '',
				movie_title: '',
				music_title: ''
			},
			comments: null,
			dialog: false,
			commentContent: null,
			commentContentRules: [
				v => !!v || 'Content is required',
				v => (v && v.length <= 400) || 'Comment must be less than 400 characters'
			],
			likedCount: 0,
			isLiked: false,
			userId: null,
			youtubeInfo: null,
			youtubeURL: 'https://www.youtube.com/watch?v=',
		}
	},
	methods: {
		getYoutubeId() {
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8003/api/youtube/soundtrack',
				params: {
					'movie_title': this.article.movie_title,
					'music_title': this.article.music_title
				}
			})
				.then((res) => {
					console.log(res)
					this.youtubeInfo = res.data
				})
		},
		likeArticle() {
			axios({
				method: 'POST',
				url: `http://127.0.0.1:8002/api/community/articles/${this.id}/likes`,
				data: {
					'user_id': this.userId
				}
			})
				.then(() => {
					this.getArticle()
				})
		},
		getArticle() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8002/api/community/articles/${this.id}`,
				params : {
					"user_id" : this.userId
				}

			})
				.then((res) => {
					this.article = res.data.article
					this.likedCount = res.data.liked_count,
					this.isLiked = res.data.liked
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
		},
		closeCommentDialog() {
			this.dialog = false
			this.commentContent = null
		},
		submitCommentDialog() {
			this.$refs.form.validate()
			const temp = this.commentContent
			axios({
				method: 'POST',
				url: `http://127.0.0.1:8002/api/community/articles/${this.id}/comments`,
				data: {
					user_id: this.user_id,
					content: temp
				}
			})
				.then(() => {
					this.getComments()
				})
			this.dialog = false
			this.commentContent = null
		}
	},
	created() {
		axios({
				method: 'GET',
				url: 'http://127.0.0.1:8000/api/kakao/auth',
				headers: {
					'authorization': this.$store.state.token
				}
			})
			.then((res) => {
				this.userId = res.data.user_id
				this.getArticle()
				this.getComments()
			})
	}
}
</script>

<style>
.top-row {
	border-bottom-style: solid;
	height: 12%;
}

</style>