const gulp = require('gulp');
const { watch, series } = require('gulp');
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
    const ts = require('gulp-typescript');
    const merge = require('merge-stream');
    const jsFiles = [
        {
            outputFileName: 'index.js',
            files: [
                'js/imagesGridFooterControl.ts',
                'js/navbarControl.ts',
                'js/tagsControl.ts'
            ]
        },
        {
            outputFileName: 'search.js',
            files: [
                'js/imagesGridFooterControl.ts',
                'js/navbarControl.ts',
                'js/tagsControl.ts',
                'js/searchSideBarControl.ts'
            ]
        }
    ];

    let tasks = jsFiles.map(data =>
        gulp
            .src(data.files)
            .pipe(ts())
            .pipe(concat(data.outputFileName))
            .pipe(terser())
            .pipe(gulp.dest('django/photos/static/js'))
    );

    return merge(tasks);
}

// exports.default = series(processTailwind, processJavascript);

exports.default = function () {
    watch('css/*.css', processTailwind);
    watch('js/*.ts', processJavascript);
};
