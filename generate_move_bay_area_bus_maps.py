# python2 kmlwriter.py --agency_id 'BART' --style_csv_path './route_styles/Current_15.csv' sample_feeds/BA_gtfs.zip move_bay_area_bus_maps/bart_current_15_map.kml
# python2 kmlwriter.py --agency_id 'Muni' --style_csv_path './route_styles/Current_15.csv' sample_feeds/SF_gtfs.zip move_bay_area_bus_maps/muni_current_15_map.kml

# Requirements: pandas and togeojson (npm install -g @mapbox/togeojson)
# Note: this overwrites all KML and GeoJsons! Add shape IDs to the Hidden_Shapes column in styling csv
# to permanently remove certain route sections (like branches)

# Usage: python2 generate_move_bay_area_bus_maps.py

import subprocess

agencies = [ 
  { 'id': '3D', 'name': 'TriDelta' },
  { 'id': 'AC', 'name': 'AC' },
  # { 'id': 'AM', 'name': 'Capitol Corridor Joint Powers Authority' },
  # { 'id': 'AY', 'name': 'American Canyon Transit' },
  { 'id': 'BA', 'name': 'BART' },
  { 'id': 'CC', 'name': 'CC' }, # County Connection
  # { 'id': 'CE', 'name': 'Altamont Corridor Express' },
  # { 'id': 'CM', 'name': 'Commute.org Shuttle' },
  { 'id': 'CT', 'name': 'Caltrain' },
  # { 'id': 'DE', 'name': 'Dumbarton Express Consortium' },
  # { 'id': 'EM', 'name': 'Emery Go-Round' },
  # { 'id': 'FS', 'name': 'Fairfield and Suisun Transit' },
  { 'id': 'GF', 'name': 'GGFerry' },
  { 'id': 'GG', 'name': 'GGT' }, # Golden Gate Transit
  { 'id': 'MA', 'name': 'MarinT' },
  # { 'id': 'MS', 'name': 'Stanford Marguerite Shuttle' },
  # { 'id': 'PE', 'name': 'Petaluma Transit' },
  # { 'id': 'RV', 'name': 'Rio Vista Delta Breeze' },
  { 'id': 'SA', 'name': 'SMART' },
  { 'id': 'SB', 'name': 'SFBayFerry' },
  { 'id': 'SC', 'name': 'VTA' },
  { 'id': 'SF', 'name': 'Muni' },
  { 'id': 'SM', 'name': 'SamTrans' },
  # { 'id': 'SO', 'name': 'Sonoma County Transit' },
  # { 'id': 'SR', 'name': 'SantaRosa' }, skipping because gtfs is bad
  { 'id': 'ST', 'name': 'SolTrans' },
  # { 'id': 'TD', 'name': 'Tideline Marine Group Inc' },
  # { 'id': 'UC', 'name': 'Union City Transit' },
  # { 'id': 'VC', 'name': 'Vacaville City Coach' },
  { 'id': 'VN', 'name': 'Napa' },
  { 'id': 'WC', 'name': 'WestCat' },
  { 'id': 'WH', 'name': 'Wheels' }, # Livermore Amador Valley Transit Authority
]
skip_ahead_to_agency_name = None
keep_skipping = True
csv_filenames = [
  'Current_15',
  'Current_20',
  'Future_15',
  'Future_20',
  'Longer_Hours',
]
processes = []
for agency in agencies:
    if keep_skipping and agency['name'] != skip_ahead_to_agency_name and skip_ahead_to_agency_name != None:
      continue
    keep_skipping = False
    for csv_filename in csv_filenames:
        processes.append(
          subprocess.Popen(
            (
              "python2 kmlwriter.py --agency_id {agency_name} --style_csv_path './route_styles/{csv_filename}.csv' "
              "'sample_feeds/{agency_id}_gtfs' 'move_bay_area_bus_maps/{agency_name}_{csv_filename}_map.kml'"
              " && togeojson 'move_bay_area_bus_maps/{agency_name}_{csv_filename}_map.kml' > 'move_bay_area_bus_maps/{agency_name}_{csv_filename}_map.json'"
            ).format(agency_name=agency['name'], agency_id=agency['id'], csv_filename=csv_filename),
            shell=True,
        ))
# Collect statuses
output = [p.wait() for p in processes]

