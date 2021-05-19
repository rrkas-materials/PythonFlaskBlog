import os
from flaskblog import create_app, db

app = create_app()
app.run(debug=True)
