from flask import Flask, render_template
from q_functions_split import db_interface

app = Flask(__name__)
steamdb = db_interface('steamdata.db')

@app.route('/')
def hello():
    steamdb.set_query('vw_games')
    df = steamdb.get_df()

    return render_template(
        'simple.html',  
        tables=[df.to_html(classes='data', index=False)], 
        titles=df.columns.values
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
