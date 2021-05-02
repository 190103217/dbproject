import eel
import json
import connection
import cx_Oracle

eel.init("web")


@eel.expose

def authorize(user, pswrd):
	administrator=[]
	for row in connection.c.execute("select id,password from users where password='admin'"):
		administrator.append(row) 
	try:
		if user==str(administrator[0][0]) and pswrd==administrator[0][1]:
			return 1
		users=[]
		if connection.c.execute("select id,password from users where id = {}".format(user)):
			return 2
	except cx_Oracle.Error:
		print("No such user is found in DB")
		return 0

@eel.expose
def addEmp(string):
	x = string.split('&');
	try:
		connection.c.callproc("create_employee",[int(x[0]),x[1],x[2],x[3],int(x[6]),x[7],x[8],int(x[9])]);
		connection.connection.commit();
		print("employee successfully added")
		return 1
	except cx_Oracle.Error as e:
		print("Eror has ocured",e)
		return 2

@eel.expose
def addProd(string):
	x = string.split('&');
	image_path = "/assets/images/"+str(x[0])+".png"
	print(image_path)
	try:
		connection.c.callproc("create_product",[int(x[0]),x[1].replace('%'," "),x[2].replace('%'," "),image_path,int(x[4])]);
		print("Product is successfully added")
	except cx_Oracle.Error as e:
		print("Error message:",e)


@eel.expose
def infoEmp(empid):
	x = empid.replace(',','')
	query_result=[]
	for row in connection.c.execute("select * from employees where employeeid={}".format(x)):
		query_result.append(row)
	empdict = [
	{"Employee_id":query_result[0][0]},
	{"Name":query_result[0][1]},
	{"Surname":query_result[0][2]},
	{"Email":query_result[0][3]},
	{"Job_id":query_result[0][4]},
	{"Job_password":query_result[0][5]},
	{"Salary":query_result[0][6]},
	{"Manager_id":query_result[0][7]}
	]

	return empdict;



@eel.expose
def infoProd(prodid):
	x = prodid.replace(',','');
	query_result=[]
	
	for row in connection.c.execute("select * from products where product_id={}".format(x)):
		query_result.append(row)
	proddict = [
	{"Product_id":query_result[0][0]},
	{"Product_name":query_result[0][1]},
	{"Description":query_result[0][2]},
	{"Img":query_result[0][3]},
	{"Price":query_result[0][4]}
	]
	return proddict
	

@eel.expose
def delEmp(empid):
	x = empid.replace(',','');
	connection.c.callproc("delete_employee",[x]);

@eel.expose
def delProd(prodid):
	x = prodid.replace(',','');
	connection.c.callproc("delete_product",[x]);
	

def showprod():
	proddict = [
	{"Prodid":"1"},
	{"Pname":"Vanilla"},
	{"Pdesc":"Plane Vanilla Ice Cream"},
	{"Imgpath":"/assets/images/checked.png"},
	{"Price":"5$"}
	]
	return proddict;



eel.start("authorize.html" , size =(900,700));
