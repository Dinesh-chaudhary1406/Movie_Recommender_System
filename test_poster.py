import requests

API_KEY = "b7b186ba37f1643a5c177965ff227650"

def get_movie_id(title):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
    response = requests.get(url, headers=headers, timeout=10)
    print("Status Code:", response.status_code)
    data = response.json()
    print("Results:", data.get("results"))
    if data.get("results"):
        return data["results"][0]["id"]
    return None

def fetch_poster(movie_id):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url, headers=headers, timeout=10)
    data = response.json()
    poster_path = data.get("poster_path")
    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    return "Poster not found"

movie_id = get_movie_id("Inception")
print("TMDb Movie ID:", movie_id)
poster_url = fetch_poster(movie_id)
print("Poster URL:", poster_url)
