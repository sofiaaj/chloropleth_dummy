import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import sys

def add_county_crosswalk(df):
	zip_to_county = pd.read_csv('data_files/zip_to_county.csv')
	# Find the index of the maximum 'RES_RATIO' within each group
	max_res_ratio_index = zip_to_county.groupby('ZIP')['RES_RATIO'].idxmax()
	# Select the rows with the maximum 'RES_RATIO' for each group
	zip_to_county = zip_to_county.loc[max_res_ratio_index]
	zip_to_county.columns = zip_to_county.columns.str.lower()
	zip_to_county['county'] =zip_to_county['county'].astype('int64').astype(str)
	zip_to_county['state'] = zip_to_county['county'].str[:-3]
	zip_to_county = zip_to_county[['zip','state','county']]
	df = df.merge(zip_to_county, on='zip')
	return(df)

def get_shapefile():
	# retrieves census zcta geometry boundaries
	shapefile = gpd.read_file('data_files/tl_2020_us_zcta520/tl_2020_us_zcta520.shp')
	shapefile.rename(columns={'ZCTA5CE20': 'zip'}, inplace=True)
	shapefile['zip'] = shapefile['zip'].astype('int64')
	return(shapefile)

def make_static_map(merged_data,county,all_counties):
	if all_counties:
		county_map = merged_data
		filename = "maps/static_all_counties.png"
	else:
		county_map = merged_data[merged_data['county']==county]
		filename = "maps/static_county_%s.png" % county
	fig, ax = plt.subplots(1, 1, figsize=(10, 10))
	# Plot the base map with zipcode boundaries
	county_map.boundary.plot(ax=ax, linewidth=1)
	# Plot filled polygons with a gradient based on the numeric variable
	county_map.plot(column='pop2018', cmap='viridis', linewidth=0, legend=True, ax=ax)
	# Customize the plot as needed
	ax.set_title('Map with Zipcode Boundaries and Gradient Fill')
	ax.set_axis_off()

	plt.savefig(filename)

def make_state_map(merged_data,state):
	# Assuming 'merged_data' is your GeoDataFrame with zipcode boundaries and numeric variable
	# Make sure 'zip' is a column with integer values for zipcode
	# Create a GeoJSON representation of the GeoDataFrame
	state_map = merged_data[merged_data['state']==state]
	geojson_data = state_map.to_json()
	# Create a Folium map centered on the mean of the geometry coordinates
	m = folium.Map(location=[state_map.geometry.centroid.y.mean(), state_map.geometry.centroid.x.mean()], zoom_start=7)
	# Add GeoJSON data to the map
	folium.GeoJson(geojson_data, name='geojson').add_to(m)
	# Add a choropleth layer with gradient fill based on the numeric variable
	folium.Choropleth(
		geo_data=geojson_data,
		name='choropleth',
		data=merged_data,
		columns=['zip', 'pop2018'],
		key_on='feature.properties.zip',
		fill_color='YlOrRd',
		fill_opacity=0.9,
		line_opacity=0.9,
		legend_name='Numeric Variable'
	).add_to(m)
	# Add layer control to switch between layers
	folium.LayerControl().add_to(m)
	# Save the map as an HTML file
	filename = "maps/interactive_state_%s.html" % state
	m.save(filename)


def make_chloropleth_data(merge_with_county=False):
	df = pd.read_csv('data_files/social_capital_zip.csv')
	# OI data connects zip codes to counties -- not necessary to use HUDS crosswalk
	if(merge_with_county):
		df = add_county_crosswalk(df)
	df = df[['zip','county','pop2018']]
	df.dropna(subset=['county'], inplace=True)
	df['county'] = df['county'].astype('int64').astype(str)
	# get state fips from county data
	df['state'] = df['county'].str[:-3]
	# add leading 0 for 2-digit state fips
	df['state'] = df['state'].astype(str).str.zfill(2)
	# get zipcode geometries
	shapefile = get_shapefile()
	merged_data = shapefile.merge(df, on='zip')
	return(merged_data)

if __name__ == "__main__":
	merged_data = make_chloropleth_data()
	args = sys.argv
	if(len(args) == 3):
		county_num = args[1]
		state_num = args[2]
	else:
		county_num='17031'
		state_num='17'
	make_static_map(merged_data,county_num,all_counties=True)
	make_static_map(merged_data,county_num,all_counties=False)
	make_state_map(merged_data,state_num)

