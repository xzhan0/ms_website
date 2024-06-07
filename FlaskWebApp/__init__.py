from flask import Flask




def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'  
    
    from .views import views
    
    
    app.register_blueprint(views, url_prefix='/')
    # app.register_blueprint(views, url_prefix='/with')
    # app.register_blueprint(views, url_prefix='/without')
    #app.register_blueprint(chatbot_with, url_prefix='/with')
    #app.register_blueprint(chatbot_without, url_prefix='/without')
    
    return app


