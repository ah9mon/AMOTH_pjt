<template>
	<v-container class="blur small-tile d-flex">
		<v-row
			justify="center"
		>
			<v-col
				lg="4"
			>
				<div 
					class="login d-flex flex-column pt-lg-15"
					align="center"
					
				>
					<h1>LOGIN</h1>
					<v-sheet 
						class="mx-auto"
						width="300"
					>
						<v-form
							validate-on="submit"
							@submit.prevent="login"
							class="pa-4"
						>
							<v-text-field
								v-model="userName"
								:rules="rules"
								label="User name"
							></v-text-field>
							<v-text-field
								v-model="password"
								:rules="rules"
								label="password"
							></v-text-field>
							<v-btn
								type="submit"
								block
							>
								Submit
							</v-btn>
						</v-form>
					</v-sheet>
					<div class="d-flex mt-9" style="justify-content: space-evenly">
						<v-btn>
							kakao
						</v-btn>
						<v-btn>
							google
						</v-btn>
					</div>
				</div>
			</v-col>
		</v-row>
	</v-container>
</template>

<script>
export default {
	name: 'LoginView',
	data() {
		return {
			rules: [
				value => this.checkValid(value),
			]
		}
	},
	methods: {
		checkValid() {

		}
	}
}
</script>

<style>
.login {
	background-color: red;
	height: 90%;
}
</style>