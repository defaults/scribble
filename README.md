#Scribble - Blogging Platform
=====

Scribble is a light weight blogging platform build on Google Cloud Platform. Its a light weight blogging platform ideal for developers or personal bloggers.

It has beautiful resposive UI to write and manage your blog posts. Mimics Medium writing UI for writings.

 It specifically uses free tier of Google Cloud Platform. So, till you reach a decent user base and traffic you mostly will pay nothing. Check tech stack below for detail.

##Features(implemented/upcoming):

Features in *italics* are coming soon. Check open pull requests and help by contributing. :smiley:

* Logging with Email/FB account kit/Github
* Manage, publish and unpublish writings
* Write blog in markdown, in offline mode
* Comments using Discus
* *Invite others to write/contribute*
* *Manager subscriptions, send subscription mails*

##Installation:
1. Clone the repo `git clone https://github.com/codervikash/scribble.git`.
2. Run `setup.py` and add your initial details like name, email, mobile no(optional). This is used for signing in.
3. If you want to run this as a subproject, redirect `<subdomain you wnat to use>` like:
```
    - url: /<sub_url_if_any>/api/.*
      script: api_router.app

    - url: /<sub_url_if_any>/.*
     script: router.app
```

##Tech stack:
###Platform
* Google App Engine (Google Cloud PaaS)
* Google Cloud Datastore (NoSQL datastore)
* Google Cloud Storage(Blog images and static data)

###Language/Libraries/Tools
* Python (Webapp2)
* SCSS, HTML5(of course!), Gulp(frontend workflow)
* [Medium editor](https://github.com/yabwe/medium-editor) (used for blog editor)
* [Bulma](https://bulma.io/)
* [Font Awesome](https://fontawesome.com) (because its awsome! :bowtie:)

##Contributing:
Your contributions are always welcome, please fork thhe repo and send a PR. TO file bug raise a issue or directly contact me on my [mail](mailto:mailkumarvikash@gmail.com) or reach on twitter [@codervikash](https://twitter.com/codervikash)

##Licence:
MIT
