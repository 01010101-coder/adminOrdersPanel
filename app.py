from flask import Flask, render_template, request
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
engine = create_engine('sqlite:///orders.db', echo = True)
meta = MetaData()


orders = Table('orders', meta,
               Column('id', Integer, primary_key=True),
               Column('name', String),
               Column('company', String),
               Column('cost', Integer)
               )

meta.create_all(engine)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    conn=engine.connect()
    db_urls = conn.execute('SELECT * FROM orders').fetchall()
    if request.method == 'POST':
        name = request.form['name']
        company = request.form['company']
        cost = request.form['cost']
        ins = orders.insert()
        ins = orders.insert().values(name=name, company=company, cost=cost)
        result = conn.execute(ins)
        return render_template('index.html', name=name, data=db_urls)

    return render_template('index.html', data=db_urls)


