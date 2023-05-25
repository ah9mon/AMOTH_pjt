import Vue from 'vue';
import Vuetify from 'vuetify/lib';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);


const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.cyan.base,
        secondary: colors.grey.darken1,
        accent: colors.shades.black,
        success: colors.teal.accent3,
        error: colors.pink.accent3,
				background: colors.grey.lighten4,
        text: '#ffffff'
      },
      dark: {
        primary: colors.cyan.darken4,
        secondary: colors.grey.darken1,
        accent: colors.shades.black,
        success: colors.teal.accent4,
        error: colors.pink.accent4,
				background: colors.grey.darken4,
        text: colors.shades.white
      },
    },
  },
})

export default vuetify