
from flask import Blueprint, render_template, request, make_response, jsonify
from db_connector import add_vessel, get_vessels, remove_vessel, update_vessel


admin = Blueprint("admin", __name__, static_folder="static", template_folder="templates")

# vessel registration
@admin.route("/vessel/registration", methods=['POST','GET'])
def register_vessel():
    if request.method == "POST":
        
        try:
            # pretvaranje praznog polja forme u vrijednost None
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
        response = add_vessel(json_request)

        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Vessel successfuly added to register!"} 
        return make_response(render_template("success.html",data=msg), 200)    
    else:
        return make_response(render_template("vessel_reg.html"), 200)



@admin.route("/vessel/delete/<int:id>", methods=['GET'])
def delete_vessel(id):
        # poziv bazi podataka
        response = remove_vessel(id)
 
        if 'error' in response: 
                return make_response(render_template("fail.html",error=str(response['error'])),400)

        msg = {"msg":"Vessel successfuly deleted from register!"}
        return make_response(render_template("success.html",data=msg), 200)    
    

@admin.route("/vessel/edit/<int:id>", methods=['POST','GET'])
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