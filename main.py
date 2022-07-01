import uvicorn
import logging

if __name__ == "__main__":
    logging.basicConfig(format=f'%(levelname)s - {__name__} - %(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    uvicorn.run("v1.api:app", host="0.0.0.0", port=8000, reload=True)
