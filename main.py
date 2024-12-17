from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from user_jwt import createToken, validateToken
from fastapi.security import HTTPBearer
from bd.database import Session, engine, Base
from models.movie import Movie as ModelMovie


app = FastAPI(
    title='APRENDIENDO FASTAPI',
    description='CURSO DE UDEMY',
    version='0.0.1'
)


Base.metadata.create_all(bind=engine)

class BearerJWT(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validateToken(auth.credentials)
        if data['email'] != 'email@email.com':
            raise HTTPException(status_code=403, detail='Credenciales incorrectas')


class User(BaseModel):
     email: str
     password: str


class Movie(BaseModel):
     id: Optional[int] = None
     title: str = Field(default='Titulo', min_length=2, max_length=30)
     overview: str = Field(default='Descripcion', min_length=15, max_length=80)
     year: int = Field(default=2024)
     rating: float = Field(ge=1,le=10)
     category: str = Field(default='Categoria', min_length=4, max_length=20)


movies = [
     {
          'id': 1,
          'title': 'El Padrino',
          'overview': 'Peli de 1972 dirigida por..',
          'year': '1972',
          'rating': 9.2,
          'category': 'crimen'
     }
]


@app.post('/login', tags=['autentication'])
def login(user: User):
     token: str = createToken(user.dict())
     print(token)
     return token


@app.get('/', tags=['INICIO'])
def read_root():
#    return {'hello': 'world'}
     return HTMLResponse('<h2> Hola Mundo! </h2>'
                         '<br>'
                         '<h4> mostra este comentario en h4</h4>'
                         )


@app.get('/movies', tags=['MOVIES'], dependencies=[Depends(BearerJWT())])
def get_movies():
     return JSONResponse(content=movies)


@app.get('/movies/{id}', tags=['MOVIES'])
def get_movie(id: int= Path(ge=1,le=100)):
     for item in movies:
          if item['id'] == id:
               return item
     return HTMLResponse('<H1> No existe el elemento buscado </H1>')     


@app.get('/movies/', tags=['MOVIES'])
def get_movies_by_category(category: str=Query(min_length=4, max_length=20)):
     return category


@app.post('/movies', tags=['MOVIES'], status_code=201)
def create_movie(movie: Movie):
    db = Session()
    newMovie= ModelMovie(**movie.dict())
    db.add(newMovie)
    db.commit()
    return JSONResponse(content={'mensaje':'Se ha agregado una nueva pelicula', 'movie': [movie.dict() for m in movies]})


@app.put('/movies/{id}', tags=['MOVIES'])
def update_movie(id: int, movie: Movie):
     for item in movies:
          if item['id'] == id:
               item['title'] == movie.title,
               item['overview'] == movie.overview,
               item['year'] == movie.year,
               item['rating'] == movie.rating,
               item['category'] == movie.category,
               return JSONResponse(content={'mensaje':'Se ha modificado la pelicula'})
          

@app.delete('/movies/{id}', tags=['MOVIES'])
def delete_movie(id: int):
     print(movies)
     for item in movies:
          if item['id'] == id:
               movies.remove(item)
               print (movies)
               return JSONResponse(content={'mensaje':'Se ha eliminado la pelicula'})          