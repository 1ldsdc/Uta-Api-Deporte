import asyncpg
import os

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()



# Conexión a la base de datos PostgreSQL
async def connect_to_postgres():
    DATABASE_URL = os.environ['DATABASE_URL']
    return await asyncpg.connect(DATABASE_URL)

# Modelos de datos
class Deporte(BaseModel):
    nombre: str

class Liga(BaseModel):
    nombre: str

# Modelos de datos
class Equipo(BaseModel):
    nombre: str
    deporte_id: int
    logo_url: str
    puntos: int  # Nueva columna para almacenar puntos

class Resultado(BaseModel):
    equipo_local: str
    equipo_visitante: str
    resultado: str
# Etiquetas
tags_metadata = [
    {"name": "Deportes", "description": "Operaciones CRUD para Deportes."},
    {"name": "Ligas", "description": "Operaciones CRUD para Ligas."},
    {"name": "Equipos", "description": "Operaciones CRUD para Equipos."},
    {"name": "Resultados", "description": "Operaciones CRUD para Resultados."},
]

    

@app.get("/", tags=["Bienvenido A la Api Notifutboll Developers"])
async def root():
    return {
        "message": "Notifutboll Developers",
        "endpoints": {
            "deportes": "/deportes/",
            "ligas": "/ligas/",
            "equipos": "/equipos/",
            "resultados": "/resultados/"
        }
    }

@app.post("/deportes/", response_model=Deporte, tags=["Deportes"])
async def crear_deporte(deporte: Deporte , conn = Depends(connect_to_postgres)):
    deporte_id = await conn.fetchval("INSERT INTO deportes (nombre) VALUES ($1) RETURNING id", deporte.nombre)
    return {"id": deporte_id, "nombre": deporte.nombre}

@app.get("/deportes/", response_model=List[Deporte],tags=["Deportes"]) 
async def listar_deportes(conn = Depends(connect_to_postgres)):
    deportes = await conn.fetch("SELECT * FROM deportes")
    return [{"id": deporte['id'], "nombre": deporte['nombre']} for deporte in deportes]

@app.put("/deportes/{deporte_id}/", response_model=Deporte, tags=["Deportes"])
async def actualizar_deporte(deporte_id: int, deporte: Deporte, conn = Depends(connect_to_postgres)):
    await conn.execute("UPDATE deportes SET nombre = $1 WHERE id = $2", deporte.nombre, deporte_id)
    return {"id": deporte_id, "nombre": deporte.nombre}

@app.delete("/deportes/{deporte_id}/", response_model=Deporte, tags=["Deportes"])
async def eliminar_deporte(deporte_id: int, conn = Depends(connect_to_postgres)):
    deporte = await conn.fetchrow("SELECT nombre FROM deportes WHERE id = $1", deporte_id)
    if not deporte:
        raise HTTPException(status_code=404, detail="Deporte no encontrado")
    await conn.execute("DELETE FROM deportes WHERE id = $1", deporte_id)
    return {"id": deporte_id, "nombre": deporte['nombre']}

# Operaciones CRUD para Ligas
@app.post("/ligas/", response_model=Liga, tags=["Ligas"])
async def crear_liga(liga: Liga, conn = Depends(connect_to_postgres)):
    liga_id = await conn.fetchval("INSERT INTO ligas (nombre) VALUES ($1) RETURNING id", liga.nombre)
    return {"id": liga_id, "nombre": liga.nombre}

@app.get("/ligas/", response_model=List[Liga], tags=["Ligas"])
async def listar_ligas(conn = Depends(connect_to_postgres)):
    ligas = await conn.fetch("SELECT * FROM ligas")
    return [{"id": liga['id'], "nombre": liga['nombre']} for liga in ligas]

@app.put("/ligas/{liga_id}/", response_model=Liga,tags=["Ligas"])
async def actualizar_liga(liga_id: int, liga: Liga, conn = Depends(connect_to_postgres)):
    await conn.execute("UPDATE ligas SET nombre = $1 WHERE id = $2", liga.nombre, liga_id)
    return {"id": liga_id, "nombre": liga.nombre}

@app.delete("/ligas/{liga_id}/", response_model=Liga,tags=["Ligas"])
async def eliminar_liga(liga_id: int, conn = Depends(connect_to_postgres)):
    liga = await conn.fetchrow("SELECT nombre FROM ligas WHERE id = $1", liga_id)
    if not liga:
        raise HTTPException(status_code=404, detail="Liga no encontrada")
    await conn.execute("DELETE FROM ligas WHERE id = $1", liga_id)
    return {"id": liga_id, "nombre": liga['nombre']}

# Operaciones CRUD para Equipos
@app.post("/equipos/", response_model=Equipo, tags=["Equipos"])
async def crear_equipo(equipo: Equipo, conn = Depends(connect_to_postgres)):
    equipo_id = await conn.fetchval("INSERT INTO equipos (nombre, deporte_id, logo_url, puntos) VALUES ($1, $2, $3, $4) RETURNING id",
                                    equipo.nombre, equipo.deporte_id, equipo.logo_url, equipo.puntos)
    return {"id": equipo_id, "nombre": equipo.nombre, "deporte_id": equipo.deporte_id, "logo_url": equipo.logo_url, "puntos": equipo.puntos}

@app.get("/equipos/", response_model=List[Equipo],tags=["Equipos"])
async def listar_equipos(conn = Depends(connect_to_postgres)):
    equipos = await conn.fetch("SELECT id, nombre, deporte_id, logo_url, puntos FROM equipos")
    return [{"id": equipo['id'], "nombre": equipo['nombre'], "deporte_id": equipo['deporte_id'], "logo_url": equipo['logo_url'], "puntos": equipo['puntos']} for equipo in equipos]

@app.put("/equipos/{equipo_id}/", response_model=Equipo,tags=["Equipos"])
async def actualizar_equipo(equipo_id: int, equipo: Equipo, conn = Depends(connect_to_postgres)):
    await conn.execute("UPDATE equipos SET nombre = $1, deporte_id = $2, logo_url = $3, puntos = $4 WHERE id = $5",
                       equipo.nombre, equipo.deporte_id, equipo.logo_url, equipo.puntos, equipo_id)
    return {"id": equipo_id, "nombre": equipo.nombre, "deporte_id": equipo.deporte_id, "logo_url": equipo.logo_url, "puntos": equipo.puntos}

@app.delete("/equipos/{equipo_id}/", response_model=Equipo,tags=["Equipos"])
async def eliminar_equipo(equipo_id: int, conn = Depends(connect_to_postgres)):
    equipo = await conn.fetchrow("SELECT nombre, deporte_id, logo_url, puntos FROM equipos WHERE id = $1", equipo_id)
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    await conn.execute("DELETE FROM equipos WHERE id = $1", equipo_id)
    return {"id": equipo_id, "nombre": equipo['nombre'], "deporte_id": equipo['deporte_id'], "logo_url": equipo['logo_url'], "puntos": equipo['puntos']}


# Operaciones CRUD para Resultados
@app.post("/resultados/", response_model=Resultado,tags=["Resultados"])
async def crear_resultado(resultado: Resultado, conn = Depends(connect_to_postgres)):
    resultado_id = await conn.fetchval("INSERT INTO resultados (equipo_local, equipo_visitante, resultado) VALUES ($1, $2, $3) RETURNING id",
                                       resultado.equipo_local, resultado.equipo_visitante, resultado.resultado)
    return {"id": resultado_id, "equipo_local": resultado.equipo_local, "equipo_visitante": resultado.equipo_visitante, "resultado": resultado.resultado}

@app.get("/resultados/", response_model=List[Resultado],tags=["Resultados"])
async def listar_resultados(conn = Depends(connect_to_postgres)):
    resultados = await conn.fetch("SELECT * FROM resultados")
    return [{"id": res['id'], "equipo_local": res['equipo_local'], "equipo_visitante": res['equipo_visitante'], "resultado": res['resultado']} for res in resultados]

@app.put("/resultados/{resultado_id}/", response_model=Resultado,tags=["Resultados"])
async def actualizar_resultado(resultado_id: int, resultado: Resultado, conn = Depends(connect_to_postgres)):
    await conn.execute("UPDATE resultados SET equipo_local = $1, equipo_visitante = $2, resultado = $3 WHERE id = $4",
                       resultado.equipo_local, resultado.equipo_visitante, resultado.resultado, resultado_id)
    return {"id": resultado_id, "equipo_local": resultado.equipo_local, "equipo_visitante": resultado.equipo_visitante, "resultado": resultado.resultado}

@app.delete("/resultados/{resultado_id}/", response_model=Resultado,tags=["Resultados"])
async def eliminar_resultado(resultado_id: int, conn = Depends(connect_to_postgres)):
    resultado = await conn.fetchrow("SELECT equipo_local, equipo_visitante, resultado FROM resultados WHERE id = $1", resultado_id)
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    await conn.execute("DELETE FROM resultados WHERE id = $1", resultado_id)
    return {"id": resultado_id, "equipo_local": resultado['equipo_local'], "equipo_visitante": resultado['equipo_visitante'], "resultado": resultado['resultado']}