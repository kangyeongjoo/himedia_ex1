import uvicorn

# cli 실행 : uvicorn main:app [--port=8000] --reload

if __name__ == "__main__":
#uvicorn.run('main:app',
   uvicorn.run('main1:app', #Fastapi ToDo App 기본 
              host='localhost', port=9000, reload=True)