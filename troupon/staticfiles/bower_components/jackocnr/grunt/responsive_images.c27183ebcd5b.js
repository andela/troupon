module.exports = function(grunt) {
  return {
    // main: {
    //   options: {
    //     engine: "im",
    //     sizes: [{
    //       width: 20,
    //       height: 30
    //     }],
    //     rename: false
    //   },
    //   files: [{
    //     expand: true,
    //     cwd: "region-flags/png/",
    //     src: ['*.png'],
    //     dest: 'src/img/flags/'
    //   }]
    // },
    retina: {
      options: {
        engine: "im",
        sizes: [{
          width: 40,
          height: 30
        }],
        rename: false
      },
      files: [{
        expand: true,
        cwd: "bower_components/region-flags/png/",
        // only 2-letter files (not sub-regions)
        src: ['??.png'],
        dest: 'src/img/flags/@2x/'
      }]
    }
  }
}