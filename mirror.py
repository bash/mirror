#!/usr/bin/env python3
# /// script
# dependencies = ["PyGithub~=2.4", "termcolor~=2.4.0"]
# ///

from github import Github, Auth
from subprocess import check_call
import os
from os import path
from urllib.parse import urlsplit, urlunsplit
from termcolor import colored

def origin(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, '', '', ''))

username = os.environ['GITHUB_USERNAME']
token = os.environ['GITHUB_TOKEN']
auth = Auth.Token(token)
g = Github(auth=auth)
mirror_dir = os.environ['MIRRORED']


for repo in g.get_user().get_repos():
    clone_dir = path.join(mirror_dir, repo.full_name)
    os.makedirs(clone_dir, exist_ok=True)
    if path.exists(path.join(clone_dir, 'config')):
        print(f'{colored('info:', attrs=['bold'])} updating {colored(repo.full_name, 'cyan')}')
        check_call(['git', '-C', clone_dir, 'fetch', '--tags'])
    else:
        print(f'{colored('info:', attrs=['bold'])} cloning {colored(repo.full_name, 'cyan')}')
        check_call(
            [
                'git', 'clone', '--mirror',
                '--config', f'credential.{origin(repo.clone_url)}.username={username}',
                '--config', 'credential.helper=!f() { test "$1" = get && echo "password=$GITHUB_TOKEN"; }; f',
                '--', repo.clone_url, clone_dir])
