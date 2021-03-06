from flask import jsonify
from dao.request import RequestDAO


class RequestHandler:
    def build_request_dict(self, row):
        result = {}
        result['reqid'] = row[0]
        result['cid'] = row[1]
        result['is_void'] = row[2]
        result['reqdate'] = row[3]
        result['reqquantity'] = row[4]
        result['resid'] = row[5]
        result['catid'] = row[6]
        result['resname'] = row[7]
        result['resdescription'] = row[8]
        result['reslocation'] = row[9]
        return result

    def build_resource_dict(self, row):
        result = {}
        result['resid'] = row[0]
        result['catid'] = row[1]
        result['resname'] = row[2]
        result['resdescription'] = row[3]
        result['reslocation'] = row[4]
        return result

    def getAllRequests(self):
        dao = RequestDAO()
        request_list = dao.getAllRequests()
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Request=result_list)

    def getAllResourcesRequested(self):
        dao = RequestDAO()
        request_list = dao.getAllResourcesRequested()
        result_list = []
        for row in request_list:
            result = self.build_resource_dict(row)
            result_list.append(result)
        return jsonify(Resource=result_list)

    def getRequestById(self, reqid):
        dao = RequestDAO()
        row = dao.getRequestById(reqid)
        if not row:
            return jsonify(Error="Request Not Found"), 404
        else:
            result = self.build_request_dict(row[0])
        return jsonify(Request=result)

    def getResourceByRequestId(self, reqid):
        dao = RequestDAO()
        row = dao.getResourceByRequestId(reqid)
        if not row:
            return jsonify(Error="Request Not Found"), 404
        else:
            result = self.build_resource_dict(row[0])
        return jsonify(Resource=result)

    def searchRequest(self, args):
        resname = args.get("resname")
        cattype = args.get("cattype")
        if len(args) == 1 and resname:
            dao = RequestDAO()
            request_list = dao.getRequestByResourceName(resname)
        elif len(args) == 1 and cattype:
            dao = RequestDAO()
            request_list = dao.getRequestByCategory(cattype)
        else:
            return jsonify(Error="Malformed search string."), 400
        result_list = []
        for row in request_list:
            result = self.build_request_dict(row)
            result_list.append(result)
        return jsonify(Request=result_list)

    def insertRequest(self, form):
        if form and len(form) == 6:
            cid = form['cid']
            reqquantity = form['reqquantity']
            catid = form['catid']
            resdescription = form['resdescription']
            resname = form['resname']
            reslocation = form['reslocation']
            if cid and reqquantity and catid and resdescription and resname and reslocation:
                dao = RequestDAO()
                result = dao.insertRequest(catid, resdescription, resname, reslocation, cid, reqquantity)
                return jsonify(Request=result), 201
            else:
                return jsonify(Error="Malformed post request")
        else:
            return jsonify(Error="Malformed post request")


