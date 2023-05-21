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
					profile picture???
				</v-row>
				<v-row
					class="my-articles"
					style="height: 30%"
				>
					my articles
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
export default {
	name: 'ProfileView',

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