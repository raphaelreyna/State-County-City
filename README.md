# State-County-City
This repo contains state-county-city data for the U.S. as well as the python script used to scrape the data from Wikipedia.
Currently, the script can scrape data for every U.S. state except: Delaware, Hawaii, Oregon and Virginia.

## Format
The data is currently only available as JSON.
The root object contains keys for each state, whose value is another object whose keys are the states counties and values are the counties cities.

Example:
```
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
