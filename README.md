# Cloropleth map in Python

## Data files

I downloaded each file directly from the links below and saved them in a folder titled 'data_files' within the main directory:

* [Opportunity Insights Social Capital Data by Zip Code](https://data.humdata.org/dataset/85ee8e10-0c66-4635-b997-79b6fad44c71/resource/ab878625-279b-4bef-a2b3-c132168d536e/download/social_capital_zip.csv)
* [Zip code shape files](https://www.census.gov/cgi-bin/geo/shapefiles/index.php?year=2020&layergroup=ZIP+Code+Tabulation+Areas) (Downloaded the 2020 National File)
* [HUD USPS Zip Code to county crosswalk](https://www.huduser.gov/apps/public/uspscrosswalk/home). Originally an Excel file, so I added it to this repo as a csv.

## Set up

Download this repository by running the following in the Terminal and then enter the directory:

```
git clone https://github.com/sofiaaj/chloropleth_dummy.git
cd make_cloropleth
```

Install all required packages:

```
pip install -r requirements.txt
```

## Data Format

The OI data contains a 5 digit zip code, a county fips code, and information at the zip code level. Due to the large number of zipcodes, the map for all of the US was less informative so I made the maps at the county or state level (though this is easy to modify). I pulled out the state fips from the county fips. 

I'm not sure if the data you have contains county information. If not, I added a function to the code that uses a crosswalk between zip code and county from HUD.

## Running the code

The script outputs a full static map of the US as well as a static county and interactive state map. For the latter two, it takes an optional county and state argument. The default is currently set to Cook County ('17031') and Illinois ('17'). This is also all easy to change!

```
python make_chloropleth.py county_num state_num
```
