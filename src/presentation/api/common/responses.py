from rest_framework.response import Response


class HandleResponseMixin:
    def success_handle(self,msg ="success",data = None,code= 200):
        response ={
            "success": True,
            "message":msg,
            "data":data,
            "error":None
        }
        return Response(response,status=code)
    
    
    def error_handle(self,msg:str,error:str,code:int):
        response ={
            "success":False,
            "message":msg,
            "error":error,
            "data": None
        }
        return Response(response,status= code)
    
    
    def internal_server_error(self,code:int):
        response = {
            "success": False,
            "message":"Internal server error please tray agin!!"
        }
        return Response(response,status=code)
    
    def not_found(self,msg: str ,code= 404):
        response = {
            "success":False,
            "message":msg,
            "data":None
        }
        return Response(response,status= code)
    
    def delete_handle(self,msg: str,code: int):
        response = {
            "success":True,
            "message":msg,
            "data":None,
            "error":None
        }
        return Response(response,status=code)
    
    def validation_error_handle(self,msg= "validation error",error= None,code =400):
        response ={
            "success": False,
            "message":msg,
            "error":error,
            "data": None
        }
        return Response(response,status=code)