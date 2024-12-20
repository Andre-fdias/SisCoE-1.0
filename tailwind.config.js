/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [],
  theme: {
    extend: {},
  },
  plugins: [],
}

module.exports = {

  plugins: [
      require('flowbite/plugin')
  ]

}


module.exports = {
  content: [
      './templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
module.exports = {
plugins: [
  require('flowbite/plugin')({
      datatables: true,
  }),
  // ... other plugins
]}

module.exports = {
  content: [
    '../templates/*/.html',
  ],
  theme: {},
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/line-clamp'),
    require('@tailwindcss/aspect-ratio'),
    require('daisyui'),
  ],
  daisyui: {},
  safelist: [
    'alert-info',
    'alert-success',
    'alert-warning',
    'alert-error',
  ],
}

tailwind.config = {
  darkMode: 'class',
  theme: {
    extend: {}
  }
}

