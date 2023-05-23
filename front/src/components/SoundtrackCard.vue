<template>
	<a 
		target="_blank"
		:href="youtubeURL + youtubeInfo.id.videoId" 
	>
		<v-img 
			style="width:100px height:425px" :src="youtubeInfo.thumbnails.url">
		</v-img>
	</a>
</template>

<script>
export default {
	name: 'SoundtrackCard',
	props: {
		youtubeInfo: Object
	},
	data() {
		return {
			youtubeURL: 'https://www.youtube.com/watch?v=',
		}
	}
}
</script>

<style>

</style>