from flask import Flask, request, make_response, jsonify, render_template,Blueprint
from db_connector import get_vessels, add_voyage, get_departures, update_voyage, get_stats

user = Blueprint("user", __name__, static_folder="static", template_folder="templates")

### voyage registration ###
@user.route("/voyage/registration", methods=['POST','GET'])
def register_voyage():
    if request.method == "POST":
        
        try:
            # json_request = request.form --> ne moze! jer ce cijena biti zapisana kao prazan string ''
            # kako bi rijesili taj problem prepisati cemo dict "form" u dict "json_request" uz uvjet da cijena nije ''
            json_request = {}
            for key,value in request.form.items(): # reminder! .items sluzi da bi mogli rastaviti dict na key i value
                if value == '':
                    json_request[key] = None
                else:    
                    json_request[key] = value
            
        except Exception as e:
            response = {"response":str(e)}
            return make_response(jsonify(response),400)    

        # poziv bazi podataka
        response = add_voyage(json_request)

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Voyage successfully registered!"} 
        return make_response(render_template("success.html",data=msg), 200)    
    else:
        return make_response(render_template("voyage_reg.html"), 200)



### search and show vessel information ###
@user.route("/vessel/info", methods=['POST','GET'])
def search_vessel():
    if request.method == "POST":
        try:
            json_request = {}
            for key,value in request.form.items(): 
                if value == '':
                    json_request[key] = None
                else:    
                    json_request[key] = value

        except Exception as e:
            response = {"response":str(e)}
            return make_response(jsonify(response),400)    

        # poziv bazi podataka
        response = get_vessels(json_request)
        

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

           
        return make_response(render_template("vessel_info.html",data=response["data"]), 200)    
    else:
        return make_response(render_template("vessel_search.html"), 200)


### show departures ###
@user.route("/departures")
def show_departures():

        # poziv bazi podataka
        response = get_departures()
        
        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)
   
        return make_response(render_template("departures.html",data=response["data"]), 200)    
    

### complete the voyage ###
@user.route("/voyage/complete/", methods=['GET','POST'])
def complete_voyage():
    if request.method == "POST":
        
        try: 
            # ukloni prazne vrijednosti (elementi iz forme koji su ostali ne popunjeni)
            json_request = {}
            for key,value in request.form.items(): 
                if value != '':
                    json_request[key] = value
                if value == "N/A":
                    json_request[key] = None    

        except Exception as e:
            response = {"response":str(e)}
            return make_response(jsonify(response),400)    

        print(json_request)
        # poziv bazi podataka
        response = update_voyage(json_request)

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Voyage successfuly updated!"}   
        return make_response(render_template("success.html",data=msg), 200)    
    else:
        return make_response(render_template("voyage_complete.html"), 200)


### show statistics ###
@user.route("/stats")
def show_stats():
        
        # poziv bazi podataka
        response = get_stats()
        graph1_data = response["data"]["graph1"] 
        graph2_data = response["data"]["graph2"] 
        graph3_data = response["data"]["graph3"] 

        ports = [data_pair[0] for data_pair in graph1_data]
        visits = [data_pair[1] for data_pair in graph1_data]

        ships = [data_pair[1] for data_pair in graph2_data]
        voyages = [data_pair[2] for data_pair in graph2_data]

        vessels = [data_pair[1] for data_pair in graph3_data]
        passengers = [data_pair[2] for data_pair in graph3_data]

        
        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)
   
        return make_response(render_template("stats.html", x_graph1 = ports, y_graph1 = visits,x_graph2 = ships, y_graph2 = voyages,x_graph3 = vessels, y_graph3 = passengers), 200)  
