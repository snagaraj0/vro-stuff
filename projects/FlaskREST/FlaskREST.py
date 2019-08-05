#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
A simple Flask-based user management application that might be used for demos.
"""
import json
import sqlite3
import atexit
from flask import Flask, request, Response, render_template
APP = Flask(__name__)

#DB_CONN = None
#DB_CUR = None
#TODO: implement database class to avoid globals?



#GENERIC FUNCTIONS
def shutdown():
    """
    This function ensures the database is gracefully closed when
    shutting down the application.
    """
    global DB_CONN

    #close database
    DB_CONN.commit()
    DB_CONN.close()
    print("Graceful shutdown, bye!")

def get_data(data):
    """
    This function deserializes an JSON object.

    :param data: JSON data
    :type data: str
    """
    json_data = json.loads(data)
    print("Deserialized data: {}".format(data))
    return json_data

def return_result(result):
    """
    This function simply returns an operation's status in JSON.

    :param result: boolean whether successful
    :type result: bool
    """
    ret = {}
    if result:
        ret["code"] = 0
        ret["message"] = "SUCCESS"
    else:
        ret["code"] = 1
        ret["message"] = "FAILURE"
    return json.dumps(ret)



#DATABASE FUNCTIONS
#TODO: creating and editing users in ONE function?
def algo_params_create(algo_id, algo_name, algo_param1, algo_param2, algo_param3):
    """
    This function creates an user.

    :param algo_id: query in order id
    :type algo_id: int
    :param algo_name: name
    :type algo_name: str
    :param algo_param1: parameter 1
    :type algo_param1: str
    :param algo_param2: parameter 2
    :type algo_param2: str
    :param algo_param3: parameter 3
    :type algo_param3: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """INSERT INTO algo_params (algo_id, algo_name, algo_param1, algo_param2, algo_param3)
            VALUES (?, ?, ?, ?, ?)""",
            (algo_id, algo_name, algo_param1, algo_param2, algo_param3)
        )
        DB_CONN.commit()
        print(
            "Added algo_paramater #{} with name={},param1={}, param2={}, param3={}".format(
                algo_id, algo_name, algo_param1, algo_param2, algo_param3)
            )
        return True
    except Exception as err:
        print("Unable to create algo_paramater #{} with name={},param1={}, param2={}, param3={}: {}".format(
                algo_id, algo_name, algo_param1, algo_param2, algo_param3, err)
        )
        return False

def algo_params_update(algo_id, algo_newid, algo_name, algo_param1, algo_param2, algo_param3):
    """
    This function updates the algorithm parameters

    :param algo_id: query in order id
    :type algo_id: int
    :param algo_name: name
    :type algo_name: str
    :param algo_param1: parameter 1
    :type algo_param1: str
    :param algo_param2: parameter 2
    :type algo_param2: str
    :param algo_param3: parameter 3
    :type algo_param3: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """UPDATE algo_params SET algo_id=?, algo_name=?, algo_param1=?, algo_param2=?, algo_param3=?,
            WHERE algo_id=?""", (
                algo_newid, algo_name, algo_param1, algo_param2, algo_param3, algo_id)
            )
        
        DB_CONN.commit()
        print(
            "Updated algorithm parameters #{} with algorithm parameters={},name={},param1={}, param2={}, param3={}".format(
                algo_id, algo_newid, algo_name, algo_param1, algo_param2, algo_param3)
            )
            
        return True
    except Exception as err:
        print("Unable to update algorithm parameters #{} with algorithm parameters={},name={},param1={}, param2={}, param3={}: {}".format(
                algo_id, algo_newid, algo_name, algo_param1, algo_param2, algo_param3, err)
        )
        return False

    
def algo_params_update_byName(algo_name, algo_newname, algo_id, algo_param1, algo_param2, algo_param3):
    """
    This function updates the algorithm parameters

    :param algo_id: query in order id
    :type algo_id: int
    :param algo_name: name
    :type algo_name: str
    :param algo_param1: parameter 1
    :type algo_param1: str
    :param algo_param2: parameter 2
    :type algo_param2: str
    :param algo_param3: parameter 3
    :type algo_param3: str
    """
    global DB_CONN
    global DB_CUR

    try:
        DB_CUR.execute(
            """UPDATE algo_params SET algo_name=?, algo_name=?, algo_param1=?, algo_param2=?, algo_param3=?,
            WHERE algo_name=?""", (
                algo_newname, algo_id, algo_param1, algo_param2, algo_param3, algo_name)
            )
        
        DB_CONN.commit()
        print(
            "Updated algorithm parameters name {} with algorithm parameters name ={},id={},param1={}, param2={}, param3={}".format(
                algo_name, algo_newname, algo_id, algo_param1, algo_param2, algo_param3)
            )
            
        return True
    except Exception as err:
        print("Unable to update algorithm parameters name {} with algorithm parameters name ={},id={},param1={}, param2={}, param3={}: {}".format(
                algo_name, algo_newname, algo_id, algo_param1, algo_param2, algo_param3, err)
        )
        return False
def algo_params_remove(algo_id):
    """
    This function removes an algorithm param.

    :param algo_id: algorithm param id
    :type algo_id: int
    """
    global DB_CONN
    global DB_CUR

    print("About to remove algo param #{}".format(algo_id))
    try:
        DB_CUR.execute(
            "DELETE FROM users WHERE algo_id=?",
            (algo_id,)
        )
        DB_CONN.commit()
        #check whether an user was removed
        if DB_CUR.rowcount > 0:
            print("Removed algo param #{}".format(algo_id))
            return True
        return False
    except Exception as err:
        print("Unable to remove algo parm #{}: {}".format(
            algo_id, err
        ))
        return False

def algo_params_get(algo_id):
    """
    This function retrieves a user's information.

    :param algo_id: param id
    :type algo_id: int
    """
    global DB_CUR

    #execute database query
    if algo_id > 0:
        #return one algo param
        DB_CUR.execute(
            "SELECT * FROM algo_params WHERE algo_id=?;",
            (algo_id,)
        )
    else:
        #return all param names
        DB_CUR.execute("SELECT * FROM algo_params;")

    #prepare result
    json = {}
    results = []
    temp = {}
    #get _all_ the information
    for row in DB_CUR:
        temp[row[0]] = {}
        temp[row[0]]["id"] = row[0]
        temp[row[0]]["name"] = row[1]
        temp[row[0]]["param1"] = row[2]
        temp[row[0]]["param2"] = row[3]
        temp[row[0]]["param3"] = row[4]
        results.append(temp[row[0]])
    json["results"] = results
    return json



#FLASK FRONTEND FUNCTIONS
@APP.route("/")
def index():
    """
    This function simply presents the main page.
    """
    return render_template("index.html")

@APP.route("/algo_params/create", methods=["GET", "POST"])
def form_create():
    """
    This function presents the form to create users and returns the API result.
    """
    if request.method == "POST":
        #create user
        if algo_params_create(
                request.form["id"], request.form["name"], request.form["param1"], request.form["param2"], request.form["param3"]
            ):
            return "Algo params created!"
        return "Algo params could not be created!"
    else:
        #show form
        return render_template("create.html")

@APP.route("/algo_params/", methods=["GET"])
def form_users():
    """
    This function lists all users.
    """
    #get _all_ the users
    algos = algo_params_get(0)
    #render users in HTML template
    return render_template("users.html", result=algos)

@APP.route("/algo_params/<int:algo_id>", methods=["GET"])
def form_user(algo_id):
    """
    This function displays a particular user.

    :param user_id: user ID
    :type user_id: int
    """
    #display a particular users
    result = algo_params_get(algo_id)["results"][0]
    return render_template("user.html", algo_params=result)

@APP.route("/algo_params/delete/<int:user_id>", methods=["GET"])
def from_delete(algo_id):
    """
    This function deletes a particular user.

    :param user_id: user ID
    :type user_id: int
    """
    #try to delete user
    if algo_params_delete(algo_id):
        return "User deleted!"
    return "User could not be deleted!"

@APP.route("/algo_params/edit/<int:algo_id>", methods=["GET", "POST"])
def form_edit(algo_id):
    """
    This function presents the form to edit users and returns form
    data to the API.

    :param algo_id: algo ID
    :type algo_id: int
    """
    if request.method == "POST":
        #edit user
        if algo_params_update(
                algo_id, request.form["name"], request.form["id"], request.form["param1"], request.form["param2"], request.form["param3"]
            ):
            return "algo params edited!"
        return "algo params could not be edited!"
    else:
        #show form, preselect values
        try:
            result = algo_params_get(algo_id)["results"][0]
            return render_template("edit.html", algo_params=result)
        except IndexError:
            return render_template("nonexist.html")



#FLASK API FUNCTIONS
@APP.route("/api/algo_params/<int:algo_id>", methods=["GET"])
def user_show(algo_id):
    """
    This function shows a particular user.
    """
    #return a particular user
    print("Retrieve algo params {}".format(algo_id))
    result = algo_params_get(algo_id)
    return Response(json.dumps(result), mimetype="application/json")

@APP.route("/api/algo_params", methods=["POST"])
def user_add():
    """
    This function creates a new user.
    """
    #execute and return result
    json_data = get_data(request.data)
    print("Create algo_params {}".format(json_data["item"]["name"]))
    result = algo_params_create(
        json_data["item"]["id"], json_data["item"]["name"],
        json_data["item"]["param1"],
        json_data["item"]["param2"],
        json_data["item"]["param3"])
    return Response(return_result(result), mimetype="application/json")

@APP.route("/api/algo_params/<int:algo_id>", methods=["PUT"])
def user_change(algo_id):
    """
    This function updates an existing user.

    :param algo_name: algo name
    :type algo_name: str
    """
    #execute and return result
    print("Update algo params #{}".format(algo_id))
    json_data = get_data(request.data)
    result = algo_params_update(
        algo_id, json_data["item"]["name"], json_data["item"]["id"],
        json_data["item"]["param1"],
        json_data["item"]["param2"],
        json_data["item"]["param3"])
    return Response(return_result(result), mimetype="application/json")

@APP.route("/api/algo_params/<int:algo_id>", methods=["DELETE"])
def user_delete(algo_id):
    """
    This function removes an user.

    :param algo_id: algo ID
    :type algo_id: int
    """
    print("Delete algo params #{}".format(algo_id))
    result = algo_params_remove(algo_id)
    return Response(return_result(result), mimetype="application/json")

if __name__ == "__main__":
    global DB_CONN
    global DB_CUR

    #register atexit
    atexit.register(shutdown)
    #start database
    DB_CONN = sqlite3.connect("algo_params.db", check_same_thread=False)
    DB_CUR = DB_CONN.cursor()
    #enable if you also like to live dangerously
    #APP.run(debug=False, host="0.0.0.0")
    APP.run(debug=False)
