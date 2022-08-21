
from flask import Flask, request, make_response, jsonify, render_template, url_for, redirect
from db_connector import add_vessel, get_vessels, remove_vessel, update_vessel, add_voyage, get_departures, update_voyage, get_stats


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
    


@app.route("/vessel/registration", methods=['POST','GET'])
def register_vessel():
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
        response = add_vessel(json_request)

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Vessel successfuly added to register!"} 
        return make_response(render_template("success.html",data=msg), 200)    
    else:
        return make_response(render_template("vessel_reg.html"), 200)



@app.route("/voyage/registration", methods=['POST','GET'])
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


@app.route("/vessel/info", methods=['POST','GET'])
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


@app.route("/departures")
def show_departures():
        

        # poziv bazi podataka
        response = get_departures()
        

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)
   
        return make_response(render_template("departures.html",data=response["data"]), 200)    
    


@app.route("/vessel/delete/<int:id>", methods=['GET'])
def delete_vessel(id):
        # poziv bazi podataka
        response = remove_vessel(id)
 
        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Vessel successfuly deleted from register!"}
        return make_response(render_template("success.html",data=msg), 200)    
    

@app.route("/vessel/edit/<int:id>", methods=['POST','GET'])
def edit_vessel(id):
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

        # poziv bazi podataka
        response = update_vessel(id,json_request)

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Vessel successfuly edited!"}   
        return make_response(render_template("success.html",data=msg), 200)    
    else:

        # poziv bazi podataka - vrati podatke o plovilu koje želimo editirati
        json_data = {"identificator":"id","search_term":str(id)}
        response = get_vessels(json_data)
        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)
        # renderiraj stranicu za editiranje i popuni ju sa podacima o pronađenom plovilu        
        return make_response(render_template("vessel_edit.html",data=response["data"]), 200) 


@app.route("/voyage/complete/", methods=['GET','POST'])
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



@app.route("/stats")
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
















"""
        # poziv bazi podataka - vrati podatke o plovilu koje želimo editirati
        json_data = {"identificator":"id","search_term":str(id)}
        response = get_vessels(json_data)
        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)
        # renderiraj stranicu za editiranje i popuni ju sa podacima o pronađenom plovilu        
        return make_response(render_template("vessel_edit.html",data=response["data"]), 200)
    
        
        


# @app.route("/")
# def home():
#     return redirect(url_for("dodaj_stvar"))

@app.route("/stvar/vrati", methods=['GET'])
def vrati_stvar():
    if request.args:
        response = get_stvari(request.args)
        if response["response"] == "Success":
            return make_response(jsonify(response),200)
        else:
            return make_response(jsonify(response),400)    
    else:
        # povratak svih podataka iz baze
        # poziv bazi podataka    
        response =  get_stvari() 
        
        # hvatanje errora
        if 'error' in response: 
            return make_response(str(response['error']),400)

        return make_response(render_template("vrati.html",data=response["data"]),200)
        

###################################################################


@app.route("/show", methods=['GET'])
def show_data():
    q_string = request.args
    if not bool(q_string): # ako je q_string prazan tj. nema upita vrati sve iz baze
        get_stvari('ALL')
        return make_response(jsonify(get_stvari('ALL')), 200)   # vrati sve iz baze        
    else:
        stvar_to_get = q_string['stvar'] # note --> q_string je objekt

        # poziv bazi podataka    
        returned_stvar =  get_stvari(stvar_to_get) 
        
        # hvatanje errora
        if 'error' in returned_stvar: 
            return make_response(str(returned_stvar['error']),400)

        return make_response(jsonify(returned_stvar),200)
        
    

@app.route("/edit", methods=['PATCH'])
def edit_data():

    # uzmi objekt json koji je poslan i sadrži željene promjene
    json_request = request.json
    # napravi objekt sa upitima
    q_string = request.args
    stvar_to_patch = q_string['stvar']

    response = patch_stvar(stvar_to_patch,json_request)

    # hvatanje errora
    if 'error' in response: 
        return make_response(str(response['error']),400)   
               
    return make_response("Data updated!",200)

    #return make_response("No such data found! Error!",400)



@app.route("/delete", methods=['DELETE'])
def delete_data():
    # napravi objekt sa upitima
    q_string = request.args
    # provjeri je li objekt s upitima prazan
    if not bool(q_string):
        return make_response("No query! Error!",400)
    
    response = delete_stvar(q_string['stvar'])
    
    if 'error' in response:
        return make_response(str(response['error'],400))             
    return make_response("Data deleted!",200)
        

""" 
if __name__ == '__main__':
    app.run(port=5000, debug=True)

    #### TESTNE NAREDBE ####

    ## GET ##
    # curl "localhost:5000/show"
    # curl "localhost:5000/show?stvar=ploca"
   
    ## PATCH ##
    # curl -H "Content-Type: application/json" -X PATCH "localhost:5000/edit?type=car&year=1992" -d '{"year":"2007"}'
    # curl -H "Content-Type: application/json" -X PATCH "localhost:5000/edit?stvar=knjiga" -d '{"namjena":"zabava", "cijena":555}'
    ## POST ##
    # curl -X POST "localhost:5000/store?stvar=ploca&namjena=skola&cijena=12"

    ## DELETE ##
    # curl -X DELETE "localhost:5000/delete?year=1992&brand=bmw"
    # curl -X DELETE "localhost:5000/delete"



    
   