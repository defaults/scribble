# Scribble - Blogging Platform

Scribble is a light weight blogging platform build with Jekyll to deploy on [Google Cloud Functions](https://cloud.google.com/functions?hl=en). 

Its as simple as possible, with least dependencies and responsive to write in markdown (preferably using Obsidian). 
 It specifically uses free tier of Google Cloud Platform. So, till you reach a decent user base and traffic you mostly will pay nothing. Check tech stack below for detail.

## Features(implemented/upcoming):

Features in *italics* are coming soon. Check open pull requests and help by contributing. :smiley:

* Landing/About page
* Manage, publish and unpublish writings
* Write blog in markdown, in offline mode
* dark/light toggle
* Comments using Discus
* *RSS feed and subscribe*

## Installation:
### For usages/deploy:
1. Clone the repo `git clone https://github.com/codervikash/scribble.git`.
2. Run `npm install` to install npm dependencies.
3. Run `gulp build` for prod build
4 TODO


### For Development:
1. Clone the repo `git clone https://github.com/codervikash/scribble.git`.
2. Run `npm install` to install npm dependencies.
3. Run `gulp watch` for dev build and watch for changes in front end assets.
4. Run `setup.py` and add your initial details like name, email, mobile no(optional). This is used for signing in.
5. To run server locally `dev_appserver.py app.yaml`.

### Language/Libraries/Tools
* Go
* SCSS, HTML5(of course!), Gulp(frontend workflow), Jekyll (build)
* [Font Awesome](https://fontawesome.com) (because its awsome! :bowtie:)

### Inspiration
* @kepano blog https://stephango.com
* [simply-jekyll](https://github.com/raghudotcc/simply-jekyll)/[notenote.link](https://github.com/Maxence-L/notenote.link/)
* 

## Contributing:
Your contributions are always welcome, please fork thhe repo and send a PR.
To file bug raise a issue or directly contact me on my [mail](mailto:mailkumarvikash@gmail.com) or reach on twitter [@_vikashk](https://twitter.com/_vikashk)

## Licence:
MIT
