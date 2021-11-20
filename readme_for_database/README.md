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
1) set_query
This is the function that is used to convert the original mysql files downloaded into sqlite files for use. Reason we had to do this was because our team had no MySQL experience and due to complications with memory issues and opening the database I figured may as well convert to sqlite, which we had experience with.

Important part to this function is the "block size" variable. In order to get around the memory issues with converting the files to sqlite, the function is made to run blocks at a time.