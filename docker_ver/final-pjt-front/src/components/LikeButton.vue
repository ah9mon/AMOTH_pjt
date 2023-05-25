<template>
	<div>
		<div class="text-h4 like-cnt">
			{{likedCount}}
		</div>
		<div class="like-btn">
			<v-btn 
				icon color="primary lighten-2"
				v-if="isLiked"
				@click.stop="likeArticle"
			>
				<v-icon size="50">mdi-thumb-up</v-icon>
			</v-btn>
			<v-btn
				icon color="primary lighten-2"
				v-else
				@click.stop="likeArticle"
			>
				<v-icon size="50">mdi-thumb-up-outline</v-icon>
			</v-btn>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
export default {
	name: 'LikeButton',
	props: {
		isLiked: Boolean,
		likedCount: Number,
		article: Object
	},
	methods: {
		likeArticle() {
			axios({
				method: 'POST',
				url: `http://localhost:8002/api/community/articles/${this.article.id}/likes`,
				data: {
					user_id: this.$store.state.user_id
				}
			})
				.then(() => {
					this.$emit('update')
				})
		},
	}


}
</script>

<style>
.like-cnt {
	position: absolute;
	top: 1.2rem;
	right: 1rem;
}

.like-btn {
	position: absolute;
	top: 1.4rem;
	right: 3rem;
}

</style>