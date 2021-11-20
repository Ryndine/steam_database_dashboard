# Steam Database Dashboard
[Ryan Mangeno](https://github.com/Ryndine) | [Anny Tritchler](https://github.com/tritchlin/) | [Melissa Cardenas](https://github.com/melcardenas28)

## Geojson Files

These files were needed in order to add regional data to the visualizations. Steam database has Alpha 2 codes for country locations. The world map we're uing uses Alpha 3 codes for all the countries. In order to pair the database information to the choropleth map, we had to find a file with both Alpha 2 and Alpha 3 codes for every country. From there we created new tables, one for alpha codes and another for the country data. From there we could join the steam data to the country data using the alpha codes table as a bridge.