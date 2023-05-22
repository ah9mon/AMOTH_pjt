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

			<v-textarea
				v-model="content"
				:rules="contentRules"
				label="Contents"
				outlined
				required
			></v-textarea>

			<v-select
				v-model="select"
				:items="items"
				:rules="[v => !!v || 'Item is required']"
				label="Item"
				required
			></v-select>

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
      select: null,
      items: [
        'Item 1',
        'Item 2',
        'Item 3',
        'Item 4',
      ],
    }),
	methods: {
		validate () {
			this.$refs.form.validate()
		},
		reset () {
			this.$refs.form.reset()
		},
		resetValidation () {
			this.$refs.form.resetValidation()
		},
		createArticle() {
			axios({
				method: 'POST',
				url: 'http://127.0.0.1:8002/api/articles',
				data: {
					title: this.title,
					content: this.content,
					// movie id???
					// music title?????
				}
			})
				.then((res) => {
					this.$router.push({name: 'articleDetail', parms:{id:res.data.pk}})
				})
				.catch((err)=>console.log(err))
		}
	},
}
</script>

<style>

</style>