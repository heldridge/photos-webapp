const gulp = require('gulp');
const { series } = require('gulp');
const cleanCSS = require('gulp-clean-css');

function processTailwind(cb) {
  const postcss = require('gulp-postcss');

  return gulp
    .src('css/styles-tailwind.css')
    .pipe(postcss([require('tailwindcss'), require('autoprefixer')]))
    .pipe(cleanCSS())
    .pipe(gulp.dest('django/photos/static/css'));
}

function processJavascript(cb) {
  const terser = require('gulp-terser');
  const concat = require('gulp-concat');

  return gulp
    .src('js/*.js')
    .pipe(concat('all.js'))
    .pipe(terser())
    .pipe(gulp.dest('django/photos/static/js'));
}

exports.default = series(processTailwind, processJavascript);
