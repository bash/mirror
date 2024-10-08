#!/usr/bin/env python3

from github import Github, Auth
from subprocess import check_call
import os
from os import path
from urllib.parse import urlsplit, urlunsplit
from termcolor import colored
import sys
import time

def origin(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, '', '', ''))

username = os.environ['GITHUB_USERNAME']
token = os.environ['GITHUB_TOKEN']
auth = Auth.Token(token)
g = Github(auth=auth)
mirror_dir = os.environ['MIRRORED']


for i, repo in enumerate(g.get_user().get_repos()):
    if i % 20 == 0 and i != 0:
        print(f'{colored('info:', attrs=['bold'])} sleeping for a bit', file=sys.stderr)
        time.sleep(5)
    clone_dir = path.join(mirror_dir, repo.full_name)
    os.makedirs(clone_dir, exist_ok=True)
    if path.exists(path.join(clone_dir, 'config')):
        print(f'{colored('info:', attrs=['bold'])} updating {colored(repo.full_name, 'cyan')}', file=sys.stderr)
        check_call(['git', '-C', clone_dir, 'fetch', '--tags'])
    else:
        print(f'{colored('info:', attrs=['bold'])} cloning {colored(repo.full_name, 'cyan')}', file=sys.stderr)
        check_call(
            [
                'git', 'clone', '--mirror',
                '--config', f'credential.{origin(repo.clone_url)}.username={username}',
                '--config', 'credential.helper=!f() { test "$1" = get && echo "password=$GITHUB_TOKEN"; }; f',
                '--', repo.clone_url, clone_dir])
