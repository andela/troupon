var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var uncss = require('gulp-uncss');

var parentTemplates = './troupon/templates/*.html';
var childTemplates = './troupon/**/**/**/*.html';

var input = './troupon/static/scss/**/*.scss';
var output = './troupon/static/css';
var baseStyles = output + '/base_styles.css';

var sassOptions = {
  errLogToConsole: true,
  outputStyle: 'expanded'
};
//compile sass
gulp.task('sass-compile', function () {
  return gulp
    .src(input)
    .pipe(sass(sassOptions).on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(gulp.dest(output));
});

//watch files
gulp.task('watch', function() {
  return gulp
    .watch(input, ['sass-compile'])
    .on('change', function(event) {
      console.log('File ' + event.path + ' was ' + event.type + ', running tasks...');
    });
});

gulp.task('uncss', function () {
    return gulp.src(baseStyles)
        .pipe(uncss({
            html: [parentTemplates, childTemplates]
        }))
        .pipe(gulp.dest(output + '/test'));
});
// set 'sass-compile' and 'watch'  as default tasks:
gulp.task('default', ['sass-compile', 'watch', 'uncss']);
