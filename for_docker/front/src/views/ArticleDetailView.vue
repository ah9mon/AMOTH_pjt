<template>
	<v-container class="blur big-tile" v-if="article">
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
				
				{{ isLiked }}
				{{ likedCount }}
				<v-btn
					@click="likeArticle"
				>
					LIKE
				</v-btn>
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
				<SoundtrackCard
					v-if="youtubeInfo"
					:youtube-info="youtubeInfo"
				/>
				<v-btn
					:absolute="true"
					:bottom="true"
					:left="true"
					@click="deleteArticle"
				>
					delete article
				</v-btn>

			</v-col>
			<v-col
				cols="4"
			>

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
				
				<!-- comments -->
				<v-list dense
					max-height="85%"
					width="100%"
					:flat=true
					style="background-color: transparent"
				>
					<v-subheader>Comments</v-subheader>
					<v-list-item-group
						color="primary"
					>
						<v-list-item
							v-for="(comment, index) in comments"
							:key = index
						>
							<v-list-item-content>
								<v-list-item-title>
									{{ comment.content }}
								</v-list-item-title>
							</v-list-item-content>
							<v-list-item-content>
								<v-btn
										v-if="comment.user_id == user_id"
										@click="deleteComment(comment.id)"
										max-width="1"
										:absolute="true"
										:right="true"
									>
										x
									</v-btn>
							</v-list-item-content>
						</v-list-item>
					</v-list-item-group>
				</v-list>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
import SoundtrackCard from '@/components/SoundtrackCard.vue'

export default {
	name: 'ArticleDetailView',
	props: {
		id: String,
	},
	components: {
		SoundtrackCard
	},
	data() {
		return {
			article: null,
			comments: null,
			dialog: false,
			commentContent: null,
			commentContentRules: [
				v => !!v || 'Content is required',
				v => (v && v.length <= 400) || 'Comment must be less than 400 characters'
			],
			likedCount: 0,
			isLiked: false,
			youtubeInfo: null,
		}
	},
	computed: {
		user_id() {
			return this.$store.state.user_id
		}
	},
	methods: {
		getYoutubeId() {
			axios({
				method: 'GET',
				url: 'http://localhost:8003/api/youtube/soundtrack',
				params: {
					'movie_title': this.article.movie_title,
					'music_title': this.article.music_title
				}
			})
				.then((res) => {
					this.youtubeInfo = res.data
				})
		},
		deleteArticle() {
			axios({
				method: 'DELETE',
				url: `http://localhost:8002/api/community/articles/${this.id}`,
				params : {
					user_id : this.user_id
				}
			})
				.then(() => {
					this.$router.push({name: 'articleList'})
				})
				.catch(() => {
					alert('본인이 작성한 게시글이 아닙니다!')
				})
		},
		likeArticle() {
			axios({
				method: 'POST',
				url: `http://localhost:8002/api/community/articles/${this.article.id}/likes`,
				data: {
					user_id: this.user_id
				}
			})
				.then(() => {
					this.getArticle()
				})
		},
		getArticle() {
			axios({
				method: 'GET',
				url: `http://localhost:8002/api/community/articles/${this.id}`,
				params : {
					user_id : this.user_id
				}

			})
				.then((res) => {
					console.log(res.data)
					this.likedCount = res.data.liked_count,
					this.article = res.data.article,
					this.isLiked = res.data.liked
					this.getYoutubeId()
				})
		},
		getComments() {
			axios({
				method: 'GET',
				url: `http://localhost:8002/api/community/articles/${this.id}/comments`
			})
				.then((res) => {
					this.comments = res.data
				})
		},
		deleteComment(comment_pk) {
			axios({
				method: 'DELETE',
				url: `http://localhost:8002/api/community/comments/${comment_pk}`,
				params: {
					'user_id': this.user_id
				}
			})
				.then(() => {
					this.getComments()
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
				url: `http://localhost:8002/api/community/articles/${this.article.id}/comments`,
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
				url: 'http://localhost:8000/api/kakao/auth',
				headers: {
					'authorization': this.$store.state.token
				}
			})
			.then(() => {
				this.getArticle()
				this.getComments()
			})
		console.log('this is article: ', this.article)
	}
}
</script>

<style>
.top-row {
	border-bottom-style: solid;
	height: 12%;
}

</style>