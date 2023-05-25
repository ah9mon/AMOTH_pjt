<template>
	<a 
		target="_blank"
		:href="goId" 
		v-if="youtubeInfo"
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
		}
	},
	computed: {
		videoId() {
			if (this.youtubeInfo != null) {
				return this.youtubeInfo.id.videoId
			} else {
				return null
			}
		},
		playlistId() {
			console.log(this.youtubeInfo)
			if (this.youtubeInfo != null) {
				return this.youtubeInfo.id.playlistId
			} else {
				return null
			}
		},
		goId() {
			if (this.videoId === undefined) {
				return this.youtubePlaylistURL + this.playlistId + '&index=1'
			} else {
				return this.youtubeURL + this.videoId
			}
		},
	}
}
</script>

<style>

</style>