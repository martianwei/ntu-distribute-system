from typing import Dict, List
from fastapi import APIRouter, HTTPException
from db.models.movie import MovieSchema, get_all_movies, get_movie_by_id, insert_movie

router = APIRouter()


@router.get("/movie/all", tags=["movie"])
async def get_movies() -> Dict[str, List[MovieSchema]]:
    movies = get_all_movies()
    return {"movies": movies}


@router.get("/movie/{movie_id}", tags=["movie"])
async def get_movie(movie_id: int) -> Dict[str, MovieSchema]:
    movie = get_movie_by_id(movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return {"movie": movie}


@router.post("/movie", tags=["movie"])
async def create_movie(movie: MovieSchema) -> Dict[str, str]:
    print("title:", movie.title)
    created_movie = insert_movie(movie)
    return {"message": "Movie created successfully", "movie_id": created_movie.id}
