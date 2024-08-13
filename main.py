from fastapi import FastAPI, BackgroundTasks, HTTPException
from datetime import datetime
from models import WeatherRequest, WeatherData
from weather import get_weather_data
from typing import List
import datasave  # Import the datasave module

app = FastAPI()

# Load the data_store from the persistent archive
data_store = datasave.load_data_store()


@app.post("/weather/")
async def start_weather_collection(request: WeatherRequest, background_tasks: BackgroundTasks):
    user_id = request.user_id
    
    # Initialize progress tracking
    data_store[user_id] = {
        'total': len(request.city_ids),
        'completed': 0,
        'data': []  # This will hold WeatherData dicts
    }
    
    # Start the data collection in the background
    background_tasks.add_task(fetch_weather_data, user_id, request.city_ids)
    
    # Save the data store after updating
    datasave.save_data_store(data_store)
    
    return {"message": "Data collection started in background.", "user_id": user_id}

async def fetch_weather_data(user_id: str, city_ids: List[int]):
    max_ids_per_request = 20  # OpenWeather API limit
    request_time = datetime.utcnow()  # Get the current UTC time

    for i in range(0, len(city_ids), max_ids_per_request):
        weather_data = get_weather_data(city_ids[i:i+max_ids_per_request])
        if weather_data and 'list' in weather_data:
            for city in weather_data['list']:
                weather = WeatherData(
                    city_id=city['id'],
                    temperature=city['main']['temp'],
                    humidity=city['main']['humidity'],
                    request_datetime=request_time  # Store the request time
                )
                data_store[user_id]['data'].append(weather.dict())  # Save only the model's data
            data_store[user_id]['completed'] += len(weather_data['list'])
            datasave.save_data_store(data_store)  # Save after each batch
        else:
            print(f"Error fetching data: {weather_data}")  # Print the error for debugging


@app.get("/progress/{user_id}")
async def get_progress(user_id: str):
    if user_id not in data_store:
        raise HTTPException(status_code=404, detail="User ID not found.")
    
    total = data_store[user_id]['total']
    completed = data_store[user_id]['completed']
    progress = (completed / total) * 100
    
    return {
        "progress_percentage": progress,
        "collected_data": data_store[user_id]['data']  # Only the filtered data
    }
