Wagtail App Pages
=================

This module provides full MVC support for wagtail pages. Using it, it's possible to extend routing for a page by using
url configs and views. It addresses the same problem solved by wagtail's own RoutablePageMixin, without breaking clean
MVC principles.

* Free software: MIT license
* Documentation: https://wagtail-app-pages.readthedocs.io.


Features
--------

* Add URL endpoints to wagtail pages by simply providing a url config
* Use regular django views instead of routing methods in the page model
* Enrich (class based) views and request objects, so views always have access to the parent page
* Adds a *reverse()* method to pages, so we can do reverse lookups with respect to the page itself
* Provides a template tag to reverse urls within the same page (automatically detecting parent page if available)
* Full url conf support, including django 2.0's new *path()* urls
* Full support for app page revisions, explore older versions of the app page

[![Build Status](https://api.travis-ci.com/mwesterhof/wagtail_app_pages.svg?branch=master)](https://travis-ci.com/mwesterhof/wagtail_app_pages)
