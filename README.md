## :octocat: Github CLI application
[![Build Status](https://travis-ci.org/miskopo/github_cli_app.svg?branch=master)](https://travis-ci.org/miskopo/github_cli_app)
[![codecov](https://codecov.io/gh/miskopo/github_cli_app/branch/master/graph/badge.svg)](https://codecov.io/gh/miskopo/github_cli_app)
![License](https://img.shields.io/github/license/miskopo/github_cli_app.svg)
![GitHub commit activity the past week](https://img.shields.io/github/commit-activity/w/miskopo/github_cli_app.svg)
[![Requirements Status](https://requires.io/github/miskopo/github_cli_app/requirements.svg?branch=master)](https://requires.io/github/miskopo/github_cli_app/requirements/?branch=master)
![Platform](https://img.shields.io/badge/platform-linux-%23FCC624.svg?logo=linux)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e2df8b89fe57485b8a9b798af0578acc)](https://www.codacy.com/app/miskopo/github_cli_app?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=miskopo/github_cli_app&amp;utm_campaign=Badge_Grade)
![Python versions](https://img.shields.io/badge/python-3.6|3.7-3776AB.svg?logo=python)
![GitHub repo size in bytes](https://img.shields.io/github/repo-size/miskopo/github_cli_app.svg)
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/miskopo)

Ever wanted to browse your repos through CLI? Or create a new one without the hassle of opening the browser? Now you can!

### What is this project? :camel: 
This project uses Github v4 API, Github v3 API and Python to provide you with command line interface. Thus you don't have to leave Guake (or you other favourite terminal) in order to
create new repo for your next project, or to see URL of you existing projects, or do whatever the API allows you.

Focus of this project is on simplicity - arguments are intuitive and provided as keywords (some flags are also available).

### Requirements :rocket: 
All you have to do (except installing this application, of course) is to register you API key within Github. To do so, navigate to your settings and choose `Developer settings`.
There, in `Personal access tokens` section, create new token with full rights (you can actually omit rights you know you don't want to use). Copy this token and save it to file 
`api_key` in project directory. **Beware, make sure no one shady gains access to it, as this key enables anyone to do anything with your Github account.**


### Installation  :whale:
As this project is currently only available on Github :octocat:, you need to perform following steps:

1. clone this repository and navigate to its root

2. execute `pip install .`
If you want to install only as a user, execute `pip install --user .`
If you want to always use the newest version, execute `pip install -e .` (or also with user flag). This will allow executing `github` dynamically, so you can have new functionality with every `pull` .

### Features and usage :construction: 
(tick marks implemented features) 

execute `github` with following options and/or arguments `[ this means optional ]`:

- [x]  `list-my-repositories `
- [x]  `list-user-repositories USERNAME `
- [x]  `create-repository REPOSITORY_NAME [--private] [--description DESCRIPTION]`
- [x]  `delete-repository REPOSITORY_NAME `
- [ ]  `create-new-project REPOSITORY_NAME PROJECT_NAME`


more to come!

#### Collaborators
- Michal Polovka    @miskopo
- Katarina Bulkova  @cathelyn 
- Miki Bankovic     @xbankov

#### Disclaimer
This project is in no way affiliated with Github and it's not official part of Github :octocat: per se (yet).
