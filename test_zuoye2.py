# templates/a6.html
from flask import Flask, request, render_template
import json
import MySQLdb as mysql
app = Flask(__name__)

db = mysql.connect(user="root", passwd="glf123@", db="glf", charset="utf8")
cur = db.cursor()

@app.route("/")
def index():
	return render_template('test_a6.html')

@app.route("/get_data")
def get_data():
	data_list = []
	cur.execute('select * from test')
	data_tuple = cur.fetchall()
	for i in range(len(data_tuple)):
		data_dict = {}
		data_dict['name'] = data_tuple[i][0]
		data_dict['age'] = data_tuple[i][1]
		data_list.append(data_dict)
	res = json.dumps(data_list)
	return res


@app.route("/add")
def add():
	data_list = []
	name = request.args.get('name')
	age = request.args.get('age')
	cur.execute('select name from test')
	name_tuple = cur.fetchall()
	if not name or not age:
		data_dict = {}
		data_dict['name'] = 'not_full_input'
		data_dict['age'] = 'name or age error'
		data_list.append(data_dict)
	elif (name,) in name_tuple: 
		cur.execute('update test set age=%s where name=%s', [age, name])
		db.commit()
		data_list.append({'name': 'name_repeat', 'age': 'name already exist'})                                     
		data_dict = {}
		data_dict['name'] = name
		data_dict['age'] = age
		data_list.append(data_dict)
	else:
		cur.execute('insert into test values (%s, %s)',[name, age])   # MySQLdb's convert regulation!!!    
		db.commit()
		data_dict = {}
		data_dict['name'] = name
		data_dict['age'] = age
		data_list.append(data_dict)
	res = json.dumps(data_list)
	return res
	

@app.route("/delete")
def delete():
	data_list = []
	name = request.args.get('name')
	cur.execute('delete from test where name=%s', [name])     # MySQLdb's convert regulation!!!
	db.commit()
	return 

if __name__ == '__main__':
	app.run(host='0.0.0.0', port = 10092, debug = True)
