# Nighttime Lights Analysis – Somaliland
## Overview

This project analyzes annual VIIRS Nighttime Lights (NTL) data to study spatial and temporal patterns of electrification and economic activity in Somaliland from 2012–2023.
The analysis is conducted at three spatial levels:
* National
* Regional
* Urban / city level

## Data Sources

* VIIRS Data (VNP46A4) Annual Composites
* Somaliland Administrative Shapefiles ([Sababi](https://sababi.org/))
* Urban Boundary Geometries

## Repository Structure
### Main Notebooks
***1_NTL_Data_Downloads.ipynb***: Downloads annual VIIRS data using a NASA Earthdata bearer token.

***2_Exploratory_Analysis.ipynb***: Descriptive and distributional exploration of radiance and pixel dynamics.

***3_NTL_Data_Construction.ipynb***: Construction of national, regional, and urban aggregates.

***4_NTL_Results_Figures.ipynb***: Production of final analytical figures.

***5_Quality_Assurance.ipynb***: Temporal, spatial, and aggregation integrity checks.

### Supplementary Material
*Sup_Mat_Somaliland_Port_Expansion.R*
*Sup_Mat_Somaliland_Shapefile_Comparisons.ipynb*

Environment Setup
1. Clone the Repository
```python
git clone <your-repo-url>
cd <repo-folder>
```

3. Create a Virtual Environment
```python
python -m venv ntl_env
```

Activate the environment:
```python
ntl_env\Scripts\activate
```

3. Install Required Packages
```python
pip install -r requirements.txt
```

## NASA Earthdata Bearer Token Setup
Downloading VIIRS data requires a NASA Earthdata account and bearer token.

1. Create a NASA Earthdata Account
Register at:
[https://urs.earthdata.nasa.gov](https://urs.earthdata.nasa.gov)

2. Generate a Bearer Token
* Log in to Earthdata.
* Navigate to your user profile.
* Generate a personal access token.
* Copy the token string.

3. Store Token in a .env File
* In the root directory of the project, create a file named: .env
* Add the following line: `NASA_API_BEARER_TOKEN=your_token_here`
* Replace your_token_here with your actual token.
* Ensure .env is included in your .gitignore.

4. Load the Token in Python
The notebooks load the token using:
```python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("NASA_API_BEARER_TOKEN")
```
If token returns None, your .env file is not correctly configured.

### To fully reproduce the analysis:
Run 1_NTL_Data_Downloads.ipynb\
Run 2_Exploratory_Analysis.ipynb\
Run 3_NTL_Data_Construction.ipynb\
Run 4_NTL_Results_Figures.ipynb\
Run 5_Quality_Assurance.ipynb\

Have fun! :smiley:
