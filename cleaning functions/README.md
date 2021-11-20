# Steam Database Dashboard
[Ryan Mangeno](https://github.com/Ryndine) | [Anny Tritchler](https://github.com/tritchlin/) | [Melissa Cardenas](https://github.com/melcardenas28)

## Cleaning Functions
This folder contains all the sql queries for the database.

### Functions:

**get_sample_data**

The primary use for this function is to extract the table schema from the mysql files. All the table schemas had to be manually be remade in Sqlite format, then inserted into the new sqlite file during creation.

**sanitize_sql_file**

This function was created to deal all the user name issues that were encountered. Somewhere during the process of opening the mysql files users that had names with backslashes, commas, or quotations that the editors read as lines of code all ended up corrupted. All sql files had to first be run through this script before insertion into database happened.

**mysql_to_sqlite**

This is the function that is used to convert the original mysql files downloaded into sqlite files for use. Reason we had to do this was because our team had no MySQL experience and due to complications with memory issues and opening the database I figured may as well convert to sqlite, which we had experience with.

Important part to this function is the "block size" variable. In order to get around the memory issues with converting the files to sqlite, the function is made to run blocks at a time.

**write_db**

This function is straight forward, when everythings good to go we're using this to write the new sqlite files to our database. During creation process we couldn't run this for large files due to memory issues. Instead we ran `.\sqlite3 [database] ".read [script.sql]"` through the sqlite3.exe command line. 

*Looking back and trying to understand why the exe worked, I believe it was due to the exe probably reading the files line by line. Knowing this it would be pretty easy to make a python script to do this for large files as well.*

**if __name__ == '__main__':**

Most important part to this file is making sure all the files are setup correctly. Here you can select what part of the cleaning process you want to do. Create a table schema for the new sqlite files, sanitize the insert statements, and writing files to the database.
```
if __name__ == '__main__':
    file_name = 'steam_13'
    sqlite_file_name = f'{file_name}_sqlite'
    original_sql = f'{file_name}.sql'
    sqlite_sql = f'{sqlite_file_name}.sql'
    sanitized_sql = f'{sqlite_file_name}_sanitized.sql'

#     table_schema  = b"""CREATE TABLE Games_Publishers (appid integer, Publisher text);
# insert into Games_Publishers
# """

#     # only call this for the steam_x.sql
#     new_sql_file = mysql_to_sqlite(
#         original_sql,
#         table_schema,
#         sqlite_sql
#     )

#     sanitized_file_path = sanitize_sql_file(sqlite_sql, sanitized_sql)

# only call this for small files
    # for large files call from command line
    # .\sqlite3 [database] ".read [script.sql]"
    # write_db()
```
