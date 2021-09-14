from q_functions_split import db_interface, db_query

# --- LEAVE ALONE ---
steamdb = db_interface('steamdata.db')

# --- FOR DF/CSV/JSON, PUT SQL FILE PATH HERE ---
steamdb.set_query('test.sql')

# --- RUN THIS TO GET DATAFRAME / TEST YOUR OUTPUT ---
# print(steamdb.get_df())

# --- RUN THIS TO GET CSV FILE FROM QUERY ---
# For memory issues, use parameter "chunk=number" example: steamdb.get_csv(chunk=1000)
steamdb.get_csv()

# --- RUN THIS TO GET JSON FILE FROM QUERY ---
# steamdb.get_json()

# # --- RUN THIS TO DELETE NON-GAME GENRE ---
# steamdb.csv_to_table('queries\delete_genres.sql')

# # --- RUN THESE IN ORDER FOR COUNTRY DATA ---
# steamdb.csv_to_table('resources\countries_codes_and_coordinates.csv')
# steamdb.exec_script('queries\create_games_countries.sql')
# steamdb.exec_script('queries\create_game_ownership_by_country.sql')

# # # --- RUN THESE PRIOR TO DOING VISUALIZATION ---
# steamdb.exec_script('queries\create vw_games.sql')
# steamdb.exec_script('queries\create vw_game_ownership.sql')
# steamdb.exec_script('queries\create vw_genre_achievements.sql')

# steamdb.exec_script('test.sql')