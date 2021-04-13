import json

def read_in_json(filename):
   with open(filename) as f_in:
       return(json.load(f_in))
