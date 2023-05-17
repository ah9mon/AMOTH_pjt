<template>
	<v-card v-if="movie" class="mt-3">
		<h1>This is a MovieCard</h1>
		{{ movie }}
	</v-card>
</template>

<script>
export default {
	name: 'MovieCard',
	props:{
		movie: Object,
	}

}
</script>

<style>

</style>