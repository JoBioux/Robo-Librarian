#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Clears the tmp folder to free some space

#From the Robo-Librarian project

import os

def run():


    dir_name = "../tmp/"
    tmp = os.listdir(dir_name)

    for item in tmp:
        if item.endswith(".pdf"):
            os.remove(os.path.join(dir_name, item))


if __name__ == "__main__":
    
    run()

    