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
				{{ article.content }}
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
						Add Commen
						</v-btn>
					</template>
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
		id: Number
	},
	data() {
		return {
			article: {
				title: 'title',
				content: 'content'
			},
			comments: ['comment1', 'comment2'],
			dialog: false,
			commentContent: null,
			commentContentRules: [
				v => !!v || 'Content is required',
				v => (v && v.length <= 400) || 'Comment must be less than 400 characters'
			]
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
		},
		closeCommentDialog() {
			this.dialog = false
			this.commentContent = null
		},
		sumbitCommentDialog() {
			this.dialog = false
			axios({
				method: 'POST',
				url: `http://127.0.0.1:8002/api/community/articles/${this.id}/comments`,
				data: {
					content: this.commentContent
				}
			})
				.then(() => {
					this.getComments()
				})
			this.commentContent = null
		}
	},
	created() {
		// this.getArticle()
		// this.getComments()
	}
}
</script>

<style>
.top-row {
	border-bottom-style: solid;
	height: 12%;
}

</style>