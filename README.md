# State-County-City
This repo contains state-county-city data for the U.S. as well as the python script used to scrape the data from Wikipedia.
Currently, the script can scrape data for every U.S. state except: Delaware, Hawaii, Oregon and Virginia.

### Obtaining the data
If you just want the JSON file with all of the data [click here](https://github.com/raphaelreyna/State-County-City/raw/master/state-county-city_data.json).

Otherwise, if you'd like to export the data in some other way, you can use the functions in the included python script to download and export the data however you want.
The two functions you'll want to use are `getDict()` and `getDictForState(state)` which scrape the data for all states and the given state respectively.

### Format
The data is currently only available as JSON.
The root object contains keys for each state, whose value is another object whose keys are the states counties and values are the counties cities.

Example:
```javascript
{
	...,
	"California": {
		...,
		"Los Angeles": [
			...,
			"Artesia",
			"Azusa",
			...,
		],
		...,
		"San Bernardino": [
			...,
			"Chino",
			"Fontana",
			...,
		},
		...,
	},
	...,
	"Wisconsin": {
		...,
		"Buffalo": [
			"Buffalo City",
			"Mondovi",
		},
		...,
	},
}
```

## Contributing
Pull requests are welcome!
There are a few states that need some love and attention: Delaware, Hawaii, Oregon and Virgina.
Also, this currently is missing a lot of smaller towns and villages for several states.
