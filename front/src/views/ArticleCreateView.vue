<template>
	<v-container class="blur big-tile">
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
			></v-text-field>
			<v-text-field
				v-model="movieTitle"
				:rules="movieTitleRules"
				label="MovieTitle"
				required
			></v-text-field>
			<v-text-field
				v-model="soundtrackTitle"
				:rules="soundtrackTitleRules"
				label="SoundtrackTitle"
				required
			></v-text-field>

			<v-textarea
				v-model="content"
				:rules="contentRules"
				label="Contents"
				outlined
				required
			></v-textarea>

			<v-btn
				:disabled="!valid"
				color="success"
				class="mr-4"
				@click="validate"
			>
				Validate
			</v-btn>

			<v-btn
				color="error"
				class="mr-4"
				@click="reset"
			>
				Reset Form
			</v-btn>

			<v-btn
				color="warning"
				@click="resetValidation"
			>
				Reset Validation
			</v-btn>
		</v-form>
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
				url: 'http://127.0.0.1:8000/api/kakao/auth',
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
							console.log('articledetail', res)
							this.$router.push({name: 'articleDetail', params:{id:res.data.id}})
						})
						.catch((err)=>console.log(err))
				})
		}
	},
}
</script>

<style>

</style>