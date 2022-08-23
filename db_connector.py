from enum import unique
from pony import orm
from datetime import datetime

DB = orm.Database()

# izrada tablica
class Vessel(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    IMO = orm.Required(str,unique=True)
    MMSI = orm.Required(str,unique=True)
    name = orm.Required(str)

    port = orm.Required(str)
    year = orm.Required(int)
    type = orm.Required(str)
    prop = orm.Required(str)

    area = orm.Required(str)

    power = orm.Optional(int) 
    shafts = orm.Optional(int)
    pass_cap = orm.Optional(int)
    cargo_cap = orm.Optional(int)
    voyages = orm.Set('Voyage')

class Voyage(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    IMO = orm.Required(str)
    name = orm.Required(str)
    port_dep = orm.Required(str)
    port_dest = orm.Required(str)
    passengers = orm.Optional(int)

    ATD = orm.Required(datetime)
    ETA = orm.Required(datetime)
    ATA = orm.Optional(datetime)
    DG = orm.Optional(int)
    status = orm.Required(str, default="On route")
    vessel = orm.Required(Vessel)

class Alert(DB.Entity):
    id = orm.PrimaryKey(int, auto=True)
    IMO = orm.Required(str)
    name = orm.Required(str)
    passengers = orm.Required(int)
    pass_cap = orm.Required(int)

    DG = orm.Optional(int)
    


DB.bind(provider="sqlite", filename="ShippingRegister.sqlite", create_db=True)
DB.generate_mapping(create_tables=True)




def add_vessel(vessel_data):
    # print("vessel data:",vessel_data)
    try:
        # id = vessel_data["id"] 
        IMO = vessel_data["IMO"] 
        MMSI = vessel_data["MMSI"] 
        name = vessel_data["name"] 

        port = vessel_data["port"] 
        year = vessel_data["year"] 
        type = vessel_data["type"] 
        prop = vessel_data["prop"] 

        area = vessel_data["area"] 

       

        #optional
        try:
            power = vessel_data["power"]
        except ValueError:
            power = None
        try:
            shafts = vessel_data["shafts"]
        except ValueError:
            shafts = None
        try:
            pass_cap = vessel_data["pass_cap"]
        except ValueError:
            pass_cap = None
        try:
            cargo_cap = vessel_data["cargo_cap"]
        except ValueError:
            cargo_cap = None

        
        with orm.db_session:
            Vessel(IMO=IMO,MMSI=MMSI,name=name,port=port,year=year,type=type,prop=prop,area=area,power=power,shafts=shafts,pass_cap=pass_cap,cargo_cap=cargo_cap)
            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Fail","error":str(e)}


def add_voyage(voyage_data):

    try:
        IMO = voyage_data["IMO"] 
        
        
        port_dep = voyage_data["port_dep"]
        port_dest = voyage_data["port_dest"]
        
        ATD = voyage_data["ATD"]
        ETA = voyage_data["ETA"]

        if "ATA" in voyage_data:
            ATA = voyage_data["ATA"]
        else:
            ATA = None
        
        #optional
        try:
            passengers = voyage_data["passengers"]
        except ValueError:
            passengers = None
        try:
            DG = voyage_data["DG"]
        except ValueError:
            DG = None


        with orm.db_session:

            try:
                vessel = Vessel.select(lambda c: c.IMO == IMO)[:][0]
            except Exception as e:
                msg = "IMO number not found in vessel register!"
                return {"response":"Fail","error":msg}

            vsl = vessel.to_dict()
            name = vsl["name"]
            Voyage(IMO=IMO,name=name,port_dep=port_dep,port_dest=port_dest,passengers=passengers,ATD=ATD,ETA=ETA,ATA=ATA,DG=DG,vessel=vessel)
            response = {"response":"Success"}

            # checking for overloading and DG cargo onboard with passengers
            if passengers != None:
                vsl_pass_cap = vsl["pass_cap"]
                declared_pass = int(passengers)
                if declared_pass > vsl_pass_cap or DG != None:
                    alert_data = {}

                    voyage_ids = orm.select(voyage.id for voyage in Voyage)[:]
                    voyage_ids.sort()
                    print(voyage_ids)
                    print(voyage_ids[-1])

                    alert_data["id"] = voyage_ids[-1]
                    alert_data["IMO"] = IMO
                    alert_data["name"] = name
                    alert_data["passengers"] = passengers
                    alert_data["pass_cap"] = vsl_pass_cap
                    alert_data["DG"] = DG
                
                    add_alert(alert_data)


            return response
    except Exception as e:
        return {"response":"Fail","error":str(e)}


def add_alert(alert_data):

    try:
        id = alert_data["id"]
        IMO = alert_data["IMO"] 
        name = alert_data["name"]
        passengers = alert_data["passengers"]
        pass_cap = alert_data["pass_cap"]
        
        #optional
        try:
            DG = alert_data["DG"]
        except ValueError:
            DG = None


        with orm.db_session:
            
            Alert(id=id,IMO=IMO,name=name,passengers=passengers,pass_cap=pass_cap,DG=DG)
            response = {"response":"Success"}
            return response
    except Exception as e:
        return {"response":"Fail","error":str(e)}


def get_vessels(search_data):
    try:
        
        with orm.db_session:

            search_term = search_data["search_term"]
            # traži prema određenom identifikatoru ili ako nije specificiran (home page search forma) koristi ime za pretragu
            if "identificator" in search_data:
                identificator = search_data["identificator"]
            else:
                identificator = "name"

            #lista rezultata
            results = orm.select(row for row in Vessel if str(getattr(row, identificator)).lower() == search_term.lower() )[:]
            #pretvaranje liste Vessel objekata u dictionary json_results
            json_results = [r.to_dict() for r in results]
            #Zamjena None vrijednosti sa stringom "N/A"
            for item in json_results:               
                for key,v_ in item.items():
                    if item[key] == None:
                        item[key] = "N/A"

           
            response = {"response":"Sucess","data":json_results}
            return response

    except Exception as e:
        return {"response":"Fail","error":e}

def get_departures():
    try:
        with orm.db_session:
            
            #lista rezultata
            results = orm.select(row for row in Voyage)[:]
            #pretvaranje liste Vessel objekata u dictionary json_results
            json_results = [r.to_dict() for r in results]
            #Zamjena None vrijednosti sa stringom "N/A"
            for item in json_results:               
                for key,v_ in item.items():
                    if item[key] == None:
                        item[key] = "N/A"

            # sending last 12 voyages
            response = {"response":"Success","data":json_results[-12:]}
            return response

    except Exception as e:
        return {"response":"Fail","error":e}

def get_alerts():
    try:
        with orm.db_session:
            
            #lista rezultata
            results = orm.select(row for row in Alert)[:]
            #pretvaranje liste Vessel objekata u dictionary json_results
            json_results = [r.to_dict() for r in results]
            #Zamjena None vrijednosti sa stringom "N/A"
            for item in json_results:               
                for key,v_ in item.items():
                    if item[key] == None:
                        item[key] = "N/A"

            # sending last 12 alerts
            response = {"response":"Success","data":json_results[-12:]}
            return response

    except Exception as e:
        return {"response":"Fail","error":e}


def get_stats():
    try:
        with orm.db_session:
            
            #lista rezultata
            #Top 7 najposjećenijih destinacija ( kako bi se destinacija smatrala posjećenom potrebno je da ima status Arrived)
            results_ports_visits = orm.select((v.port_dest, orm.count()) for v in Voyage if v.status == "Arrived")[:7] # list of tuples
            #Top 7 brodova po broju putovanja
            results_ship_voyages = orm.select((v.IMO, v.name, orm.count()) for v in Voyage if v.status == "Arrived")[:7] # list of tuples
            #Top 7 brodova po broju putnika
            results_ship_passangers = orm.select((v.IMO, v.name, orm.sum(v.passengers)) for v in Voyage if v.status == "Arrived" and v.passengers != None)[:7] # list of tuples

            #sorting tuple lists
            results_ports_visits_sorted = sorted(results_ports_visits, reverse=True, key = lambda x: x[1])
            results_ship_voyages_sorted = sorted(results_ship_voyages, reverse=True, key = lambda x: x[2])
            results_ship_passangers_sorted = sorted(results_ship_passangers, reverse=True, key = lambda x: x[2])

            print(results_ports_visits)
            print(results_ports_visits_sorted)
            
  
            results = {"graph1":results_ports_visits_sorted,
                        "graph2":results_ship_voyages_sorted,
                        "graph3":results_ship_passangers_sorted
            }
            response = {"response":"Success","data":results}
            return response

    except Exception as e:
        return {"response":"Fail","error":e}


def remove_vessel(vessel_id):
    try:
        with orm.db_session:
            to_delete = Vessel.select(lambda c: c.id == int(vessel_id))[:][0]
            to_delete.delete()
            response = {"response":"Vessel successfuly deleted!"}
            return response

    except Exception as e:
        return {"response":"Fail","error":str(e)}

def update_vessel(id,patch_data):
    try:
        with orm.db_session:
            
            to_update = Vessel.select(lambda c: c.id == id)[:][0]
            to_update.set(**patch_data)
            
            response = {"response":"Vessel successfuly updated!"}
            return response

    except Exception as e:
        return {"response":"Fail","error":str(e)}

def update_voyage(patch_data):
    try:
        with orm.db_session:
            id = patch_data["id"]
            if "ATA" not in patch_data:
                patch_data["ATA"] = None
            else:
                ATA_datetime_obj = datetime.strptime(patch_data["ATA"], '%Y-%m-%dT%H:%M')

            to_update = Voyage.select(lambda c: c.id == id)[:][0]
            voyage_dict = to_update.to_dict()

            #Putovanje se moze zakljuciti samo ako:
            # 1. je trenutni stats On route
            # 2. Ako je ATA > ATD
            # 3. Ako je status Arrived mora postojati ATA podatak 
            
            if voyage_dict["status"] == "On route":
                if patch_data["ATA"] == None and patch_data["status"] == "Cancelled":
                    to_update.set(**patch_data)
                    response = {"response":"Voyage successfuly updated!"}

                elif patch_data["ATA"] == None and patch_data["status"] == "Arrived":
                    response = {"response":"Fail","error":"ATA missing!"}

                elif ATA_datetime_obj > voyage_dict["ATD"]:
                    to_update.set(**patch_data)
                    response = {"response":"Voyage successfuly updated!"}
                else:
                    response = {"response":"Fail","error":"ATA must be > than ATD!"}
            else:
                response = {"response":"Fail","error":"Voyage already completed!"}
            return response


    except Exception as e:
        return {"response":"Fail","error":str(e)}



if __name__ == '__main__':
    pass
    