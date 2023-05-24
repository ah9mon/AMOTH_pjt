import Vue from 'vue';
import Vuetify from 'vuetify/lib/framework';
import colors from 'vuetify/lib/util/colors'

Vue.use(Vuetify);


const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        primary: colors.cyan.base,
        secondary: colors.grey.darken1,
        accent: colors.shades.black,
        error: colors.pink.accent2,
				background: colors.grey.lighten4
      },
      dark: {
        primary: colors.cyan.darken4,
        secondary: colors.grey.darken1,
        accent: colors.shades.black,
        error: colors.pink.accent4,
				background: colors.grey.darken4
      },
    },
  },
})

export default vuetify