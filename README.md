# ScholarsNet
"A Data Portal for Scholars" - COMP4332 course project @ HKUST

## Features
- A minimalist Computer Science papers data portal
- Easy papers & authors searching
- High navigability
- Detailed paper/author information
- Relevance ranking

## Live Demo
https://scholarsnet.herokuapp.com/

## Install Dependencies:
- Update your system:

`sudo apt-get update`
- Install Linux dependencies: 

`sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`
- Install Python virtual environment: 

`sudo apt-get install python-virtualenv`
- `cd COMP4332-data-portal`
- Create a new virtual environment: 

`virtualenv -p python3 env --no-site-packages`
- Switch to virtual environment: 

`source env/bin/activate`
- Install Python dependencies: 

`pip install -r requirements.txt`

## Data Collection
- ### Arxiv
    - Go to project root directory
    - `cd data_retrieval`
    - `cd arxiv`
    - `python arxiv_updater.py`
    - After running the script, data from Arxiv will be retrieved
- ### DBLP
    - Go to project root directory
    - `cd data_retrieval`
    - `cd dblp`
    - `python dblp_updater.py`
    - After running the script, data from DBLP will be retrieved
- ### IEEE
    - Go to project root directory
    - `cd data_retrieval`
    - `cd paper_crawlers`
    - `scrapy crawl ieee -o ieee.json`
    - After running the script, data from IEEE will be retrieved
- ### ACM
    - `cd data_retrieval`
    - `cd paper_crawlers`
    - `scrapy crawl acm_journal -o acm.json`
    - After running the script, data from IEEE will be retrieved


## Running Locally - Tested on Ubuntu 16.04
- `./run.py`
- Head to browser and enter `http://localhost:5000`

## CONTRIBUTORS:
- Budi RYAN (bryanaa) (https://github.com/budiryan)
- Dicky CHIU (mtchiu) (https://github.com/Dickyhaha)
- Catherine ELEONORA (celeonora)

