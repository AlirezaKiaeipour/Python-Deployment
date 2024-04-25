import os
import time
import requests
import asyncio
import aiohttp
import dotenv

env = dotenv.load_dotenv()
Rhyming_API_KEY = os.getenv("Rhyming_API_KEY")

async def rhyme_finder(word):
    async with aiohttp.ClientSession() as session: 
        print("Rhyming Started")
        url = f"https://rhyming.ir/api/rhyme-finder?api={Rhyming_API_KEY}&w={word}&sb=1&mfe=2&eq=1"
        response = await session.request("GET", url)
        print("Rhyming Ended")
        return await response.json()

def get_states():
    url = "https://iran-locations-api.vercel.app/api/v1/fa/states"
    response = requests.request("GET", url)
    return response.json()

def get_cities(state_id):
    url = f"https://iran-locations-api.vercel.app/api/v1/fa/cities?state_id={state_id}"
    response = requests.request("GET", url)
    return response.json()

async def get_coordinates(state_name, city_name):
    print("Coordinates Started")
    states = get_states()
    for state in states:
        if state["name"] == state_name:
            info_cities = get_cities(state["id"])
            cities = info_cities["cities"]
            for city in cities:
                if city["name"] == city_name:
                    print(f"Name: {city['name']}")
                    print(f"Latitude: {city['latitude']}")
                    print(f"Longitude: {city['longitude']}")
    print("Coordinates Ended")

async def main():
    print("Process Started")
    print(await asyncio.gather(rhyme_finder("سلام"), get_coordinates("آذربايجان شرقی","تبريز")))
    print("All Process Ended Successfully")


if __name__ == "__main__":
    start_time = time.perf_counter()
    asyncio.run(main())
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Total Time IS: {total_time}")
