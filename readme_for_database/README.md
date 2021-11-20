# Steam Database Dashboard
[Ryan Mangeno](https://github.com/Ryndine) | [Anny Tritchler](https://github.com/tritchlin/) | [Melissa Cardenas](https://github.com/melcardenas28)

## Readme for main database files.
Going to go through the python files that were used during this project.

### q_execute_scripts:

Please refer to the [query folder readme](https://github.com/Ryndine/steam_analysis_database/blob/main/user_queries/README.md) for information on this file.

### q_functions_split:

**class db_query**

You won't need to change anything to this class, we're using this for query paths.

**class db_interface**
* set_query()
  * In order to return a Dataframe, CSV, or JSON from an sql file we need to use this to set which sql query we're going to use. The perameter for the query is an sql query file path.
* export_path()
  * Export path for our files we're retreiving.
* get_df(), get_chunky_df(), get_csv(), get_json()
  * All of these functions are straight forward. We're using these to output the queries into a format we need. If a dataframe was too large to output there is the option to use chunks. Adjust size to memory needs.
* csv_to_table()
  * This function is to let us import all the csv files back into the database, allowing members of the team with memory issues to still be able to contribute to the project.
* exec_script()
  * This is the main function we're using for our database. Whenever you need to run an sql query you'll be using this function to do so. The perameter for this is your sql query location.

### app

Feel free to ignore this file. We're using app.py to initialize our dash app.

### index

This is the file that creates the layout for our dashboard. It's setup to utilize multiple pages, but we never expanded the project that far. The most important part of this file is the callback that allows the user to view our database live and interactively. The other part is setting the server for the app, change if needed.

### layouts

This is the dashboard the user will be utilizing.

**Setup**

First we're setting up the database, without this step the dashboard won't display visuals.
```
# Data
steamdb = db_interface('steamdata.db')
# steamdb = db_interface('D:\steam\steamdata.db')
```
Next we're getting a dataframe of all the unique values in games_genre.
```
steamdb.set_query(text='select * from games_genres')
genres = steamdb.get_df().Genre.unique()
```
Which is later used here in order to create our dropdown menu of selectable genres.
```
options = [{'value': x, 'label': x} for x in genres]
# items = [dbc.DropdownMenuItem(i) for i in options] #remove curly brackets on this line
dropdown = dbc.Row(
    [
        dbc.Col(dcc.Dropdown(
            id='genre', 
            options=[{'value': x, 'label': x} 
                    for x in genres],
            value=genres[0]
            ),
        ),
    ],
    no_gutters=True,
)
```
Next is making sure the geojson file for the countries has a path, without this our map won't be able to display regional data.
```
geojson = json.loads(open("resources\countries.geojson", 'r').read())
```
**Visualization**

The navigation bar is under the function **nav_bar()**. Straight forward code.

The callbacks for the dashboard are connected to the choropleth map, and the bar graph using the following code:
```
@app.callback(
    Output("choropleth", "figure"), 
    [Input("genre", "value")])
```
Here you'll be able to see the information of the live queries. Right now the data we provide is limited.

The pie chart is not interactive due to time and limitations of plotly, our member did the best they could on short time. In order to get the pie chart to work a query is needed. In this case our pie chart is set to dsiplay the follow query:
```
pie_query = f"select * from vw_genre_achieve;"
steamdb.set_query(text = pie_query)
pie_df = steamdb.get_df()
```
*The chord chart is not in this file. It's an external file being imported in the template file, then called to in the page layout inside here.*

**Pages**

We only had time for one page, so everything after "# Page Layouts" is structuring all of our visualizations. This is done using the "dash.bootstrap" module.
