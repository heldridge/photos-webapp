const gulp = require('gulp');
const { watch, series } = require('gulp');
const cleanCSS = require('gulp-clean-css');

function processTailwind(cb) {
    const postcss = require('gulp-postcss');
    var tailwindcss = require('tailwindcss');

    return gulp
        .src('css/styles-tailwind.css')
        .pipe(
            postcss([
                tailwindcss('./tailwind.config.js'),
                require('autoprefixer')
            ])
        )
        .pipe(cleanCSS())
        .pipe(gulp.dest('django/photos/static/css'));
}

function processJavascript(cb) {
    const terser = require('gulp-terser');
    const concat = require('gulp-concat');
    const ts = require('gulp-typescript');
    const merge = require('merge-stream');

    default_files = [
        'js/navbarControl.ts',
        'js/classUtils.ts',
        'js/messagesControl.ts'
    ];

    const jsFiles = [
        {
            outputFileName: 'basic.js',
            files: default_files
        },
        {
            outputFileName: 'basic_grid.js',
            files: [...default_files, 'js/tagsControl.ts']
        },
        {
            outputFileName: 'search.js',
            files: [
                ...default_files,
                'js/imagesGridFooterControl.ts',
                'js/tagsControl.ts',
                'js/searchSideBarControl.ts',
                'js/getUrlParameter.ts'
            ]
        },
        {
            outputFileName: 'gallery.js',
            files: [
                ...default_files,
                'js/galleryControl.ts',
                'js/getUrlParameter.ts'
            ]
        },
        {
            outputFileName: 'picture.js',
            files: [...default_files]
        },
        {
            outputFileName: 'login.js',
            files: [...default_files, 'js/loginControl.ts']
        },
        {
            outputFileName: 'register.js',
            files: [...default_files, 'js/formsControl.ts']
        },
        {
            outputFileName: 'upload.js',
            files: [...default_files, 'js/formsControl.ts']
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

exports.default = function() {
    watch('css/*.css', processTailwind);
    watch('tailwind.config.js', processTailwind);
    watch('js/*.ts', processJavascript);
};
