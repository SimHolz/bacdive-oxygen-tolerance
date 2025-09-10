# BacDive Oxygen Tolerance Data Fetcher

This repository contains a Python script to fetch oxygen tolerance data for given microbial species or genera from [BacDive](https://bacdive.dsmz.de/) using their API.

## Usage

Place your species or genus names line by line in the input file (default `species_list.txt`). The script returns oxygen tolerance data for all strains in the BacDive database matching these names. This also includes data predicted with AI (see [their paper](https://www.nature.com/articles/s42003-025-08313-3) for more information). Only strains with an oxygen tolerance entry are in the output. AI predicted values are returned including their confidence value.

```bash
python script/get_oxygen_tolerance.py -u <username> -p <password> -i species_list.txt -o oxygen_tolerance_results.csv
```

- `-u`, `--username` - Your BacDive username
- `-p`, `--password` - Your BacDive password
- `-i`, `--input` - Input file with species or genus names (default: species_list.txt)
- `-o`, `--output` - Output CSV file with results (default: oxygen_tolerance_results.csv)

## Requirements

- Python 3.x
- bacdive package
- pandas

Install dependencies with:

```bash
pip install bacdive pandas
```
