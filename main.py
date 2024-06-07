from FlaskWebApp import create_app
import os 
app = create_app()
#print("API Key:", os.getenv('OPENAI_API_KEY')) 
if __name__ == '__main__':
    app.run(debug=False)  
    