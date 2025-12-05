# Frase Diaria API 📖

Una API REST desarrollada con FastAPI que proporciona versículos bíblicos completos de la Reina Valera 1909.

## ✨ Características

- **Biblia completa**: 31,102 versículos de la Reina Valera 1909
- **Búsqueda avanzada**: Filtrado por libro, capítulo y versículo
- **Versículo del día**: Algoritmo determinístico basado en fecha
- **API RESTful**: Endpoints bien documentados y estructurados
- **Arquitectura modular**: Código organizado y mantenible
- **Documentación automática**: Interfaz Swagger/OpenAPI integrada

## 📊 Estadísticas
- **31,102 versículos** (toda la Biblia)
- **66 libros** (Antiguo y Nuevo Testamento)
- **1,189 capítulos**

## 📚 Endpoints Principales

### `GET /` - Página de inicio
Información general de la API y lista de endpoints disponibles.

### `GET /api/daily-verse` - Versículo del día
Devuelve un versículo diferente cada día usando un algoritmo basado en la fecha.

### `GET /api/random-verse` - Versículo aleatorio
Devuelve un versículo aleatorio de toda la Biblia.

### `GET /api/verses` - Versículos con filtros
Lista de versículos con paginación y filtros opcionales.
**Parámetros:**
- `book` (opcional): Filtrar por libro (ej: 'Génesis')
- `chapter` (opcional): Filtrar por capítulo (ej: 1)
- `limit` (default: 50): Número máximo de resultados
- `offset` (default: 0): Para paginación

### `GET /api/verse/{book}/{chapter}/{verse}` - Versículo específico
Obtiene un versículo exacto por su referencia bíblica.
**Ejemplo:** `/api/verse/Génesis/1/1`

### `GET /api/stats` - Estadísticas de la Biblia
Información detallada sobre la estructura de la Biblia.

## 🛠️ Tecnologías

- **Python 3.8+** - Lenguaje principal
- **FastAPI** - Framework web moderno y rápido
- **Pydantic** - Validación de datos y serialización

## ⚡ Instalación

```bash
# Clonar repositorio
git clone https://github.com/KingZahard01/daily-phrase.git

# Entrar al directorio
cd daily-phrase

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
fastapi dev app/main.py 
```

## 🌐 Uso

Una vez ejecutado, la API estará disponible en:

API Local: http://localhost:8000

Documentación automática (Swagger UI): http://localhost:8000/docs

🤝 Contribuir

Si deseas contribuir:
1. Haz fork del proyecto
2. Crea una rama para tu feature (git checkout -b feature/nueva-funcionalidad)
3. Haz commit de tus cambios (git commit -m 'Agrega nueva funcionalidad')
4. Push a la rama (git push origin feature/nueva-funcionalidad)
5. Abre un Pull Request
