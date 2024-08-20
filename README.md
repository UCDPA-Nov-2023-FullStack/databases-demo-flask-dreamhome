# databases-demo-flask
Demos to show how to integrate flask with various databases

- Create a virtual environment and run

  ```bash
    pip install -m requirements.txt
  ```
- Create an empty database using PGAdmin called 'databases-flask-demo'. If you use a different name then remember that you will need to update the connection string in the ```config.py``` file accordingly. The same also applies if the new database uses a different username and password than from what's specified below.

  ```python
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:5432/databases-flask-demo"
  ```

- To start flask in the terminal 

  ```bash
    python app.py
  ```

