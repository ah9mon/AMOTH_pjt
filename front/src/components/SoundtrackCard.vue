<template>
	<a 
		target="_blank"
		:href="goId" 
	>
		<v-img 
			style="max-height:59vh;" :src="youtubeInfo.thumbnails.url">
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
			youtubePlaylistURL: 'https://www.youtube.com/watch?v=&list=',
			videoId: this.youtubeInfo.id.videoId,
			playlistId: this.youtubeInfo.id.playlistId,
		}
	},
	computed: {
		goId() {
			if (this.videoId === undefined) {
				return this.youtubePlaylistURL + this.playlistId + '&index=1'
			} else {
				return this.youtubeURL + this.videoId
			}
		}
	}
}
</script>

<style>

</style>