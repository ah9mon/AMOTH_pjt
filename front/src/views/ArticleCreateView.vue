<template>
	<v-container class="blur small-tile">
		<v-row justify="center">
			<v-col sm="10">
				<v-form
					ref="form"
					v-model="valid"
					lazy-validation
					@submit.prevent="createArticle"
				>
					<v-text-field
						v-model="title"
						:counter="100"
						:rules="titleRules"
						label="Title"
						required
						dark
					></v-text-field>
					<v-text-field
						v-model="movieTitle"
						:rules="movieTitleRules"
						label="Movie Title"
						required
						dark
					></v-text-field>
					<v-text-field
						v-model="soundtrackTitle"
						:rules="soundtrackTitleRules"
						label="Soundtrack Title"
						required
						dark
					></v-text-field>
		
					<v-textarea
						v-model="content"
						:rules="contentRules"
						label="Contents"
						outlined
						required
						dark
					></v-textarea>
		
					<v-btn
						:disabled="!valid"
						color="success"
						class="mr-4"
						@click="validate"
					>
						Submit
					</v-btn>
		
					<v-btn
						color="error"
						@click="reset"
					>
						Reset
					</v-btn>
				</v-form>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
import axios from 'axios'
export default {
	name: 'ArticleCreateView',
	data: () => ({
      valid: true,
      title: '',
      titleRules: [
        v => !!v || 'Title is required',
        v => (v && v.length <= 100) || 'Title must be less than 100 characters',
      ],
      content: '',
      contentRules: [
        v => !!v || 'Content is required',
      ],
      movieTitle: '',
      movieTitleRules: [
        v => !!v || 'Movie title is required',
      ],
      soundtrackTitle: '',
      soundtrackTitleRules: [
        v => !!v || 'Soundtrack title is required',
      ],
    }),
	methods: {
		validate () {
			this.$refs.form.validate()
			this.createArticle()
			this.$router.push({name: 'search'})
		},
		reset () {
			this.$refs.form.reset()
		},
		resetValidation () {
			this.$refs.form.resetValidation()
		},
		createArticle() {
			axios({
				method: 'GET',
				url: `http://127.0.0.1:8000/api/${this.$store.state.source}/auth`,
				headers: {
					'authorization': this.$store.state.token
				}
			})
				.then((res) => {
					axios({
						method: 'POST',
						url: 'http://127.0.0.1:8002/api/community/articles',
						data: {
							user_id: res.data.user_id,
							title: this.title,
							content: this.content,
							movie_title: this.movieTitle,
							music_title: this.soundtrackTitle
						}
					})
						.then((res) => {
							const temp = String(res.data.id)
							this.$router.push({
								name: 'articleDetail', 
								params:{
									article: res.data,
									id: temp
								}
							})
						})
						.catch((err)=>console.log(err))
				})
		}
	},
}
</script>

<style>

</style>