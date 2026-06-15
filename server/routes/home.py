from flask_restful import Resource

class Home(Resource):
    def get(self):
        return{
            'message': 'Welcome to Stitches by Mona API 🧶',
            'available_endpoints' : [
                '/products',
                '/customers',
                '/orders',
                '/custom_orders',
                '/auth/admin/profile',
             ]
            
          
            }, 200