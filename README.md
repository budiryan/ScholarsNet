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

## Installing Dependencies (Tested on Ubuntu 16.04):
- Update your system:

`sudo apt-get update`
- Install Linux dependencies: 

`sudo apt-get install build-essential libssl-dev libffi-dev python3-dev`
- Install Docker:

`sudo apt-get install docker`
- Install Python virtual environment: 

`sudo apt-get install python-virtualenv`
- `cd COMP4332-data-portal`
- Create a new virtual environment: 

`virtualenv -p python3 env --no-site-packages`
- Switch to virtual environment: 

`source env/bin/activate`
- Install Python dependencies: 

`pip install -r requirements.txt`

## Phase 1: Data Collection
- ### Arxiv
    - Go to project root directory
    - `cd data_retrieval`
    - `cd arxiv`
    - `python arxiv_updater.py`
    - After running the script, data from Arxiv will be retrieved
- ### DBLP
    - Open a new terminal
    - In the new terminal:

    `sudo docker run -p 8050:8050 scrapinghub/splash`
    - Go back to your old terminal
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
    - Go to project root directory
    - `cd data_retrieval`
    - `cd paper_crawlers`
    - `scrapy crawl acm_journal -o acm.json`
    - After running the script, data from ACM will be retrieved under 'acm.json'
- ### Authors
     - Go to project root directory
     - `cd data_retrieval`
     - `cd paper_crawlers`
     - `scrapy crawl author -o authors.json`
     - After running the script, data from ACM will be retrieved under 'authors.json'

## Phase 2: Schema Mapping & Entity Resolution
- ### Generating the string edit distance matrix:
    - Go to project root directory
    - `cd entity_resolution`
    - `python schema_mapping.py`
    - See the output in 'edit_distance_output.txt'
- ### Doing Entity resolution together with generating the unified schema:
    - Go to project root directory
    - cd sqlite
    - `python acm_interface.py`
    - `python arxiv_interface.py`
    - `python dblp_interface.py`
    - `python ieee_interface.py`
    - `python authors_interface.py`
    - `cd ..`
    - `cd entity_resolution`
    - `python merge_table.py`

## Phase 3: Data Fusion
- ### Exact String Match
    - Go to project root directory
    - `cd data_fusion`
    - `python jaccard_strict.py`
- ### Jaccard Similarity
    - Go to project root directory
    - `cd data_fusion`
    - `python jaccard_strict.py`
- ### String Edit Distance
    - Go to project root directory
    - `cd data_fusion`
    - `python string_edit_distance.py`
- ### Jaccard SED
    - Go to project root directory
    - `cd data_fusion`
    - `python jaccard_sed.py`

## Phase 4: Data Mining / Auto Categorization
- ### Generate Training Data
    - Go to project root directory
    - `cd text_mining`
    - `python generate_training_data.py`
- ### Train Machine Learning Model and Pickle
    - Go to project root directory
    - `cd text_mining`
    - `python model.py`

## Phase 5: Running the Portal Locally 
- `./run.py`
- Head to your favorite browser and enter `http://localhost:5000`

## CONTRIBUTORS:
- Budi RYAN (bryanaa) (https://github.com/budiryan)
- Dicky CHIU (mtchiu) (https://github.com/Dickyhaha)
- Catherine ELEONORA (celeonora)

