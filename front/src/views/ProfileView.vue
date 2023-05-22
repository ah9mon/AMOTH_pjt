<template>
	<v-container class="blur big-tile">
		<v-row class="d-flex" style="height: 100%">
			<!-- left column for profile picture & articles-->
			<v-col
				cols="4"
			>
				<v-row
					class="profile-picture"
					style="height: 40%"
				>
					<v-img  style="width:100px height:425px" :src="profile_picture"></v-img>
				</v-row>
				<v-row
					class="my-articles"
					style="height: 30%"
				>
					{{ myArticles }}
				</v-row>
				<v-row
				class="liked-articles"
				style="height: 30%"
				>
					liked articles,
				</v-row>
			</v-col>
			<!-- right column for watched movies -->
			<v-col
				cols="8"
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
			user_id: null,
			profile_picture: null,
			myArticles: null
		}
	},
	methods: {
		getUserInfo() {
			axios({
				method: 'GET',
				url: 'http://127.0.0.1:8000/api/kakao/auth',
				headers: {
					'authorization': this.$store.state.token
				}
			})
				.then((res) => {
					console.log(res)
					this.user_id = res.data.user_id
					this.profile_picture = res.data.profile_picture
					axios({
						method: 'GET',
						url: 'http://127.0.0.1:8002/api/community/articles',
						params: {'user_id': this.user_id}
					})
						.then((res)=>{
							console.log(res)
							this.myArticles = res.data
						})
						.catch((err)=>console.log(err))
				})
		}
	},
	created() {
		this.getUserInfo()
	}
}
</script>

<style>
.profile-picture {
	background-color: red;

}
.my-articles {
	background-color: blue;
}
.liked-articles {
	background-color: brown;
}
.watched-movies {
	background-color: green;
}

</style>