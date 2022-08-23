
from flask import Blueprint, render_template, request, make_response, jsonify
from db_connector import add_vessel

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