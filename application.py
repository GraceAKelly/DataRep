from flask import Flask, jsonify, request, abort
from shoesDAO import shoesDAO

app = Flask(__name__, static_url_path='', static_folder='.')

#app = Flask(__name__)

#@app.route('/')
#def index():
# return "Hello World"

# curl "http://127.0.0.1:5000/shoes"
@app.route('/shoes')
def getAll():    
    #print("in getall")
    results = shoesDAO.getAll()
    return jsonify(results)

# "http://127.0.0.1:5000/shoes/3"
@app.route('/shoes/<int:id>')
def findById(id):
    foundshoes = shoesDAO.findByID(id)

    return jsonify(foundshoes)

# curl -i -H "Content-Type:application/json" -X POST -d "{\"Style\":\"boot\",\"Designer\":\"Doc Marten\",\"Price\":50}" "http://127.0.0.1:5000/shoes"
@app.route('/shoes', methods=['POST'])  
def create():
    
    if not request.json:
        abort(400)
    # other checking for more marks
    shoe = {
        "Style": request.json['Style'], 
        "Designer": request.json['Designer'], 
        "Price": request.json['Price'],
    }
    values =(shoe['Style'],shoe['Designer'],shoe['Price'])
    newID = shoesDAO.create(values)
    shoe['id'] = newId
    return jsonify(shoe)

# curl -i -H "Content-Type:application/json" -X PUT -d "{\"Style\":\"boot\",\"Designer\":\"Doc Marten\",\"Price\":50}" http://127.0.0.1:5000/shoes/1
@app.route('/shoes/<int:id>', methods=['PUT'])
def update(id):
    foundshoes = shoesDAO.findByID(id)
    if not foundshoes:
        abort(404)

    if not request.json:
        abort(400)
    reqJson = request.json
    if 'Price' in reqJson and type(reqJson['Price']) is not int:
        abort(400)

    if 'Style' in reqJson:
        foundshoes['Style'] = reqJson['Style']
    if 'Designer' in reqJson:
        foundshoes['Designer'] = reqJson['Designer']
    if 'Price' in reqJson:
        foundshoes['Price'] = reqJson['Price']
    values = (foundshoes['Style'],foundshoes['Designer'],foundshoes['Price'], foundshoes['id'])
    shoesDAO.update(values)
    return jsonify(foundshoes)




@app.route('/shoes/<int:id>', methods=['DELETE'])
def delete(id):
    shoesDAO.delete(id)
    return jsonify({"done":True})

if __name__ =='_main_' :
    app.run(debug= True )
