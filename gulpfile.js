const gulp = require('gulp');
const cleanCSS = require('gulp-clean-css');

function processTailwind(cb) {
    const postcss = require('gulp-postcss')

    return gulp.src('css/styles-tailwind.css')
        .pipe(postcss([
            require('tailwindcss'),
            require('autoprefixer'),
        ]))
        .pipe(cleanCSS())
        .pipe(gulp.dest('django/photos/static/css'))
}

exports.default = processTailwind;
