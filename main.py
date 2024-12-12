from fastapi import FastAPI, HTTPException
import uvicorn
import redis
import json
from fastapi.middleware.cors import CORSMiddleware
from scraper.scraper import scrape

app = FastAPI()

rd = redis.Redis(host="localhost", port=6379, db=0)

origins = ["http://127.0.0.1:5501", "http://localhost:5501"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Nothing here ^_^"}

@app.get("/scrape/")
async def scrape_url(prefecture: str, city: str,):
    location = {"prefecture": prefecture, "city": city}
    location_key = json.dumps({"prefecture": prefecture, "city": city})
    
    # res = scrape(location)
    # return res
    
    
    #### REDIS ####
    try:
        # Check the cache
        print("Checking cache...")
        cache = rd.get(location_key)
        if cache:
            print("Cache hit")
            return json.loads(cache)  # Deserialize the cached string into a Python dictionary

        print("Cache miss")
        # Call the scrape function
        res = scrape(location)
        if not res:  # Handle edge case if scrape fails or returns None
            raise HTTPException(status_code=500, detail="Scrape failed")
        
        # Store the result in Redis with a TTL (e.g., 86400 seconds (1 day))
        rd.setex(location_key, 86400, json.dumps(res))  # Serialize the dictionary to JSON
        return res

    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)