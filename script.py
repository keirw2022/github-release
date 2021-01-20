#!/usr/bin/env python3

import requests
import os
import json


try:
    r = requests.get(f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}/releases/latest",
                       auth=('username', os.environ['INPUT_GITHUB_API_TOKEN']))
except Exception as e:
    print(f"Get Latest Release; Problem accessing Github API: {e}")

if r.ok:
    response = json.loads(r.text)
    latest_tag = response["tag_name"]

print(f"Latest release tag is: {latest_tag}")

try:
    t = latest_tag.split(".")
    t = t[:2]  # strip tertiary version number
    t[1] = str(int(t[1]) + 1)  # increment secondary version
    tag = ".".join(t)
    print(f"Incrementing release tag to: {tag}")
except Exception as e:
    print(f"Didnt work: {e}")

if tag:
    try:
        print(f"Creating a new release: {tag} for master branch")
        
        release_payload = {"tag_name": tag}
        if os.environ["INPUT_GIT_BRANCHTAG"]:
            release_payload = {"tag_name": tag, "target_commitish": os.environ["INPUT_GIT_BRANCHTAG"]}

        r = requests.post(f"{os.environ['GITHUB_API_URL']}/repos/{os.environ['GITHUB_REPOSITORY']}/releases",
                        auth=('username', os.environ['GITHUB_API']),
                        data = json.dumps(release_payload))
    except Exception as e:
        print(f"Create Release; Problem accessing Github API: {e}")
    
if r.ok:
    print("Release created.")
    