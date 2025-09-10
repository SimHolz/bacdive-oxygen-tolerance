import argparse
import bacdive
import pandas as pd

def get_best_oxygen_tolerance_entry(oxygen_data_list):
    """
    Selects the entry with the highest confidence value from a list of oxygen tolerance data.

    Missing confidence is treated as highest (100), 
    non-parsable confidence is treated as -1.
    """
    max_confidence = -1
    best_entry = None
    for entry in oxygen_data_list:
        conf = entry.get('confidence')

        if conf is not None:
            try:
                conf_value = float(conf)
            except (ValueError, TypeError):
                conf_value = -1
        else:
            # Treat missing confidence as highest priority (non-predicted data)
            conf_value = 100
        
        if conf_value > max_confidence:
            max_confidence = conf_value
            best_entry = entry
    return best_entry

def main():
    # Initialize BacDive client with credentials
    client = bacdive.BacdiveClient("simon.holzinger@ukr.de", "jvENt-RJDa7-Phi59-fMtFR")
    client.includePredictions()

    # Read species names from file
    with open('species_list.txt', 'r') as f:
        species_names = [line.strip() for line in f]

    results = []

    for species in species_names:
        # Search BacDive based on taxonomy species name
        search_response = client.search(taxonomy=species)

        if search_response > 0:
            # Retrieve oxygen tolerance data for matched strains
            results_generator = client.retrieve(['oxygen tolerance'])

            for item in results_generator:
                for strain_id, data in item.items():
                    oxygen_data = data
                    if not oxygen_data:
                        continue
                    
                    # Expect oxygen_data to be a list of records
                    oxygen_records = oxygen_data[0].get('oxygen tolerance')
                    
                    if isinstance(oxygen_records, list):
                        best_entry = get_best_oxygen_tolerance_entry(oxygen_records)
                        if best_entry:
                            oxygen_tolerance = best_entry.get('oxygen tolerance')
                            confidence = best_entry.get('confidence')
                            ref_id = best_entry.get('@ref')
                        else:
                            oxygen_tolerance = confidence = ref_id = None
                    elif isinstance(oxygen_records, dict):
                        oxygen_tolerance = oxygen_records.get('oxygen tolerance')
                        confidence = oxygen_records.get('confidence')
                        ref_id = oxygen_records.get('@ref')
                    else:
                        oxygen_tolerance = confidence = ref_id = None

                    results.append({
                        'species': species,
                        'strain': strain_id,
                        'ref_id': str(ref_id) if ref_id else None,
                        'oxygen_tolerance': oxygen_tolerance,
                        'confidence': confidence
                    })

    # Convert results to DataFrame and save
    df = pd.DataFrame(results)

def get_best_oxygen_tolerance_entry(oxygen_data_list):
    """
    Selects the entry with the highest confidence value from a list of oxygen tolerance data.

    Missing confidence is treated as highest (100),
    non-parsable confidence is treated as -1.
    """
    max_confidence = -1
    best_entry = None
    for entry in oxygen_data_list:
        conf = entry.get('confidence')

        if conf is not None:
            try:
                conf_value = float(conf)
            except (ValueError, TypeError):
                conf_value = -1
        else:
            # Treat missing confidence as highest priority (non-predicted data)
            conf_value = 100

        if conf_value > max_confidence:
            max_confidence = conf_value
            best_entry = entry
    return best_entry

def main():
    parser = argparse.ArgumentParser(description="Fetch oxygen tolerance data from BacDive.")
    parser.add_argument('-i', '--input', default='species_list.txt', help='Input file with species or genus names')
    parser.add_argument('-o', '--output', default='oxygen_tolerance_results.csv', help='Output CSV file for results')
    parser.add_argument('-u', '--username', required=True, help='BacDive username')
    parser.add_argument('-p', '--password', required=True, help='BacDive password')
    args = parser.parse_args()

    # Initialize BacDive client with credentials
    client = bacdive.BacdiveClient(args.username, args.password)
    client.includePredictions()

    # Read species names from file
    with open(args.input, 'r') as f:
        species_names = [line.strip() for line in f]

    results = []

    for species in species_names:
        # Search BacDive based on taxonomy species name
        search_response = client.search(taxonomy=species)

        if search_response > 0:
            # Retrieve oxygen tolerance data for matched strains
            results_generator = client.retrieve(['oxygen tolerance'])

            for item in results_generator:
                for strain_id, data in item.items():
                    oxygen_data = data
                    if not oxygen_data:
                        continue

                    # Expect oxygen_data to be a list of records
                    oxygen_records = oxygen_data[0].get('oxygen tolerance')

                    if isinstance(oxygen_records, list):
                        best_entry = get_best_oxygen_tolerance_entry(oxygen_records)
                        if best_entry:
                            oxygen_tolerance = best_entry.get('oxygen tolerance')
                            confidence = best_entry.get('confidence')
                            ref_id = best_entry.get('@ref')
                        else:
                            oxygen_tolerance = confidence = ref_id = None
                    elif isinstance(oxygen_records, dict):
                        oxygen_tolerance = oxygen_records.get('oxygen tolerance')
                        confidence = oxygen_records.get('confidence')
                        ref_id = oxygen_records.get('@ref')
                    else:
                        oxygen_tolerance = confidence = ref_id = None

                    results.append({
                        'species': species,
                        'strain': strain_id,
                        'ref_id': str(ref_id) if ref_id else None,
                        'oxygen_tolerance': oxygen_tolerance,
                        'confidence': confidence
                    })

    # Convert results to DataFrame and save
    df = pd.DataFrame(results)
    df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()

