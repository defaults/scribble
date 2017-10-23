// Gulp.js configuration
var
    // Include gulp
    gulp = require('gulp'),

    // Include Our Plugins
    jshint = require('gulp-jshint'),
    sass = require('gulp-sass'),
    postcss = require('gulp-postcss'),
    assets = require('postcss-assets'),
    autoprefixer = require('autoprefixer'),
    mqpacker = require('css-mqpacker'),
    cssnano = require('cssnano'),
    concat = require('gulp-concat'),
    deporder = require('gulp-deporder'),
    stripdebug = require('gulp-strip-debug'),
    uglify = require('gulp-uglify'),
    newer = require('gulp-newer'),
    imagemin = require('gulp-imagemin'),
    htmlclean = require('gulp-htmlclean'),
    sourcemaps = require('gulp-sourcemaps'),
    del = require('del'),
    rev = require('gulp-rev-all'),
    useref = require('gulp-useref'),
    runSequence = require('run-sequence'),
    // development mode?
    devBuild = true,

    // folders
    folder = {
        src: 'public/src/',
        temp: 'public/temp/',
        build: 'public/build/'
    },

    postCssOpts = [
        assets({ loadPaths: ['images/'] }),
        autoprefixer({ browsers: ['last 2 versions', '> 2%'] }),
        mqpacker
    ],

    scssOpts = {
        outputStyle: 'nested',
        imagePath: 'images/',
        precision: 3,
        errLogToConsole: true
    }
;

// Lint Task
gulp.task('lint', function() {
    return gulp.src('scripts/**/*.js')
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});

// JavaScript processing for blog js
gulp.task('scripts-zenpen', function() {
    var jsbuild = gulp.src(folder.src + 'zenpen/js/**/*.js')
        .pipe(deporder())
        .pipe(concat('blog.js'));

    if (!devBuild) {
        jsbuild = jsbuild
            .pipe(stripdebug())
            .pipe(uglify());
    }
    return jsbuild.pipe(gulp.dest(folder.temp + 'zenpen/js/'));
});

// Javascript processing for js files required for blog frontend
gulp.task('scripts-blog_public', function() {
    var jsbuild = gulp.src(folder.src + 'scripts/public/*.js')
        .pipe(deporder())
        .pipe(concat('app.js'));

    if (!devBuild) {
        jsbuild = jsbuild
            .pipe(stripdebug())
            .pipe(uglify());
    }
    return jsbuild.pipe(gulp.dest(folder.temp + 'scripts/'));
});

// Javascript processing for js files required for blog frontend
gulp.task('scripts-blog_admin', function() {
    var jsbuild = gulp.src(folder.src + 'scripts/admin/*.js')
        .pipe(deporder())
        .pipe(concat('admin.js'));

    if (!devBuild) {
        jsbuild = jsbuild
            .pipe(stripdebug())
            .pipe(uglify());
    }
    return jsbuild.pipe(gulp.dest(folder.temp + 'scripts/'));
});

// All Js master task
gulp.task('scripts', [
    'scripts-zenpen',
    'scripts-blog_public',
    'scripts-blog_admin'
]);

// compress and optimize images
gulp.task('images', function() {
    var out = folder.temp + 'images/';
    return gulp.src(folder.src + 'images/**/*')
        .pipe(newer(out))
        .pipe(imagemin(
            {
                optimizationLevel: 5,
                progressive: true,
                interlaced: true
            }
        ))
        .pipe(gulp.dest(out));
});

// HTML processing
gulp.task('html_blog', function() {
    var
        out = folder.temp + 'templates/',
        page = gulp.src(folder.src + 'templates/**/*')
            .pipe(newer(out))
            .pipe(useref());

    // minify production code
    if (!devBuild) {
        page = page.pipe(htmlclean());
    }

    return page.pipe(gulp.dest(out));
});

gulp.task('html_zenpen', function() {
    var
        out = folder.temp + 'zenpen/',
        page = gulp.src(folder.src + 'zenpen/**/*.html')
            .pipe(newer(out))
            .pipe(useref());

    // minify production code
    if (!devBuild) {
        page = page.pipe(htmlclean());
    }

    return page.pipe(gulp.dest(out));
});

// All HTML task
gulp.task('html', [
    'html_blog',
    'html_zenpen'
]);

// CSS processing
gulp.task('css-home', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/home.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});

gulp.task('css-article_list', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/article_list.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});

gulp.task('css-article', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/article.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});

gulp.task('css-zenpen', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'zenpen/css/*.css')
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'zenpen/css'));
});

gulp.task('css-dashboard', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/dashboard.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});

gulp.task('css-setup', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/setup.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});

gulp.task('css-setting', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/setting.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});
gulp.task('css-error', function() {

    if (!devBuild) {
        postCssOpts.push(cssnano);
    }

    return gulp.src(folder.src + 'stylesheets/error.scss')
        .pipe(sass(scssOpts))
        .pipe(postcss(postCssOpts))
        .pipe(gulp.dest(folder.temp + 'stylesheets/'));
});

// All css tasks
gulp.task('css', [
    'css-home',
    'css-article_list',
    'css-article',
    'css-zenpen',
    'css-dashboard',
    'css-setup',
    'css-setting',
    'css-error'
]);

// copy remaining css files
gulp.task('copy',['copy-zenpen'], function() {
    return gulp.src(folder.src + '**/*.{xml,txt,json,css,ico,png}')
        .pipe(gulp.dest(folder.temp));
});

// copy remaining css files
gulp.task('copy-zenpen', function() {
    return gulp.src(folder.src + 'zenpen/css/fonts/**/*')
        .pipe(gulp.dest(folder.temp + 'zenpen/css/fonts'));
});

// gulp task to add revision
gulp.task('rev', function() {
    revisionTask = gulp.src(folder.temp + '**/*')
    if (!devBuild) {
        revisionTask = revisionTask
            .pipe(rev.revision({
                dontRenameFile: ['.ico','.png','.html','.xml','.json','.txt'],
                dontUpdateReference: ['.png','.html','.xml','.json','.txt']
            }))
            .pipe(gulp.dest(folder.build))
            .pipe(rev.manifestFile())

    }

    return revisionTask.pipe(gulp.dest(folder.build))
});

// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch(folder.src + '**/*.js', ['lint', 'scripts', 'rev']);
    gulp.watch(folder.src + '**/*.scss', ['css', 'rev']);
    gulp.watch(
        folder.src + '**/*.{svg,jpeg,jpg,img,png}',
        ['images', 'html', 'css', 'rev']
    );
    gulp.watch(folder.src + 'templates/**/*', ['html', 'rev']);
    gulp.watch(folder.src + '**/*.{css,xml,txt,json}', ['copy', 'rev'])
});

// Clean Output Directory
gulp.task('clean', function() {
    return del(folder.build + '**');
});

//finish task to delete temp folders
gulp.task('finish', function() {
    return del(folder.temp + '**/*', {force: true});
});

// Default Task
gulp.task('default', function() {
    devBuild = false;
    return runSequence(
        'clean', 'lint', 'css', 'scripts', 'images',
        'html', 'copy', 'rev', 'finish'
    );
});

// Dev tasks
gulp.task('dev', function() {
    return runSequence(
        'clean', 'lint', 'css', 'scripts',
        'images', 'html', 'copy', 'rev', 'watch'
    );
});
