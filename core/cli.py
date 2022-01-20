#!/usr/bin/env python3
import os, json
from urllib.parse import urlparse
from git.repo.base import Repo
from py_console import console

class cli:


    def __init__(self):
        console.setShowTimeDefault(False)


    def get(self, url, cache="./.cache"):
        console.log(f"Downloading crawler -> {url}")

        '''
        Parse the repository URL to determine the repository
        domain and the namespace of the repository to minimalize
        conflicts. This will help us to place scripts in unique
        directories.
        '''
        parsed_url = urlparse(f"{url}")

        '''
        Clone the crawler script into local disk and handle any
        exceptions happen in the process.
        '''
        try:
            Repo.clone_from(f"https://{url}", os.path.join(cache, "scripts", parsed_url.path))
        except:
            console.warn("Repository already exists, please do a clean checkout if not working")

        '''
        Store basic meta data about the recently cloned repository
        in a basic JSON file. This will speedup script listing
        commands in the future & also take out the need of directory
        scanning to determine script paths
        '''
        metadata_file_path = os.path.join(cache, "scripts", "metadata.json")
        if os.path.isfile(metadata_file_path):

            metadata = ""
            with open(metadata_file_path, "r") as f:
                metadata = json.load(f)

            try:
                metadata.index(f"{url}")
            except:
                console.log("Updating meta data information")

                metadata.append(f"{url}")
                f = open(metadata_file_path, "w")
                f.write(json.dumps(metadata))
                f.close()

        else:
            console.log("Creating meta data information")
            f = open(metadata_file_path, "w")
            f.write(json.dumps([f"{url}"]))
            f.close()


        console.success(f"Successfully downloaded the crawler -> {url}")
