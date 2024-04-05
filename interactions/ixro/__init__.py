import os
import pandas as pd
from pygbif import species, occurrences
from ixro.query import cube_query, download_cube

if __name__ == '__main__':
    vvkey = species.name_suggest(
        'Vitis vinifera', limit=1
    )[0]['speciesKey']
    vv_ix = pd.read_csv(
        '/data/interactions_globi_vitis_vinifera.csv'
    )
    vv_interactors = vv_ix[
        ['target_taxon_name','interaction_type']
    ].drop_duplicates()
    vv_interactors.target_taxon_name.value_counts()
    speciesCounts = {}
    for species_name, ix_amount in vv_interactors.target_taxon_name.value_counts().items():
        try:speciesKey = species.name_suggest(
            species_name, limit=1)[0]['speciesKey']
        except (KeyError, IndexError):
            print('No species key for', species_name)
            continue
        nameConfig = {f"speciesKey": speciesKey}
        for regionName in ['BE','FR','GB']:
            speciesCounts[(species_name,regionName)] = occurrences.search(
                country = regionName, limit=0, **nameConfig
           )['count']
        speciesCounts[(species_name,'EU')] = occurrences.search(
                continent = 'Europe', limit=0, **nameConfig
        )['count']
    speciesCounts = pd.Series(speciesCounts)
    speciesCounts = speciesCounts[
        speciesCounts > 0
    ].unstack().fillna(0)
    speciesCounts['speciesKey'] = speciesCounts.apply(
        lambda x: species.name_suggest(
            x.name, limit=1
        )[0]['speciesKey'], axis=1
    )
    cubes = {}
    for countryCode in ['BE','FR','GB']:
        cubes[countryCode] = cube_query(
            os.environ.get('GBIF_EMAIL'),
            country = countryCode,
            speciesKeyList = list(
                speciesCounts.speciesKey.astype('str')
            )+[str(vvkey)]
        )
    for countryCode in cubes:
        download_cube(
            cubes[countryCode],
            prefix=f"/results/{countryCode}_"
        )
    
