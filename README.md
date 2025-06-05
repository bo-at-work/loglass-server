# Loglass FastAPI Clone

A FastAPI-based partial clone of the HiGlass Server API, focusing on tileset routes for Cooler files. This project aims to replicate the core read-only functionality for displaying tileset data as specified in the HiGlass documentation.

## Setup

1.  **Ensure you are in the `loglass_fastapi_clone` directory.**

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies (using Poetry):**
    It's recommended to use Poetry for managing dependencies.
    ```bash
    pip install poetry
    poetry install
    ```
    Alternatively, if not using Poetry, ensure `fastapi`, `uvicorn[standard]`, and `pydantic` are installed via pip from the `pyproject.toml` specifications.

## Running the Server

Using Poetry:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or, if not using Poetry (ensure virtual environment is active):
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`. The tileset API endpoints will be under `/api/v1/` (e.g., `http://localhost:8000/api/v1/tilesets/`).

## Development Plan (MVP for Cooler Files)

This plan outlines the steps to create a Minimum Viable Product (MVP) focusing on the read-only tileset API endpoints for "cooler" files, using stubbed data.

**Phase 1: Project Foundation & Core Models**

1.  **Project Directory and `pyproject.toml` Setup:** (Completed)
    *   Directory: `/home/blu/Github/loglass-server/loglass_fastapi_clone`
    *   `pyproject.toml` with `fastapi`, `uvicorn[standard]`, and `pydantic`.

2.  **Basic Directory Structure:** (Completed)
    ```
    loglass_fastapi_clone/
    ├── pyproject.toml
    ├── README.md
    └── app/
        ├── __init__.py
        ├── main.py         # FastAPI app instance
        ├── models.py       # Pydantic models
        ├── routers/
        │   ├── __init__.py
        │   └── tilesets.py # Tileset-specific routes
        └── services/       # Or repositories/
            ├── __init__.py
            └── tileset_repository.py # Stubbed data access
    ```

3.  **Define Core Pydantic Models (`app/models.py`):**
    *   `TilesetPublic`: For individual tileset representation (uuid, filetype, datatype, name, coordSystem, created, owner, etc. based on `tilesets_api.md`).
    *   `TilesetListResponse`: For `GET /api/v1/tilesets/` response (count, next, previous, results: List[TilesetPublic]).
    *   `ErrorModel`: A simple `{"error": "message"}` structure for API error responses.
    *   `TilesetInfoCooler`: Specific metadata model for cooler files (`min_pos`, `max_pos`, `max_zoom`, `tile_size`, `resolutions`, `chromsizes`, etc. as per `tilesets_api.md`).
    *   `TilesetInfoResponse`: A dictionary where keys are tileset UUIDs and values are `Union[TilesetInfoCooler, ErrorModel]`. To be used for `/api/v1/tileset_info/`.
    *   `TileDataCooler`: Stubbed representation for cooler tile data. This will be simplified for the MVP (e.g., a list of numbers or a simple structure like `{"dense": [...], "min_value": ..., "max_value": ...}`).
    *   `TilesDataResponse`: A dictionary where keys are tile IDs (e.g., `uuid.zoom.x.y`) and values are `Union[TileDataCooler, ErrorModel]`. For `/api/v1/tiles/`.

**Phase 2: Stubbed Service & API Routers**

4.  **Implement Stubbed Tileset Repository (`app/services/tileset_repository.py`):**
    *   Create a class `StubTilesetRepository`.
    *   Initialize with in-memory data for a few sample "cooler" tilesets (e.g., 1-2 example tilesets with predefined metadata and a way to generate dummy tile data).
    *   Implement methods:
        *   `list_tilesets(limit: int, offset: int, type_filter: Optional[str], datatype_filter: Optional[str]) -> TilesetListResponse`: Returns a paginated list of stubbed tilesets.
        *   `get_tileset_by_uuid(uuid: str) -> Optional[TilesetPublic]`: Retrieves a single stubbed tileset by its UUID.
        *   `get_tileset_info(uuids: List[str]) -> TilesetInfoResponse`: Returns `TilesetInfoCooler` metadata for known cooler UUIDs. For unknown UUIDs or non-cooler types (in this MVP), it can return an error model for that UUID.
        *   `get_tiles(tile_ids: List[str]) -> TilesDataResponse`: Parses tile IDs (e.g., `uuid.z.x.y`), generates dummy `TileDataCooler` based on these parameters for known cooler UUIDs, and returns an error for others.

5.  **Implement FastAPI Routers (`app/routers/tilesets.py`):**
    *   Create an `APIRouter` instance with the prefix `/api/v1` (or as defined in `tilesets_api.md`).
    *   Inject an instance of `StubTilesetRepository` (e.g., using FastAPI's dependency injection).
    *   Implement the following path operations, ensuring exact path and parameter matching with `tilesets_api.md`:
        *   `GET /tilesets/`: Lists available tilesets. Uses `list_tilesets` from the repository. Handles query parameters like `t` (filetype), `dt` (datatype), and basic pagination (limit/offset if not full pagination URLs).
        *   `GET /tilesets/{uuid}/`: Retrieves a specific tileset. Uses `get_tileset_by_uuid`.
        *   `GET /tileset_info/`: Retrieves detailed metadata. Parses `d=<uuid>` query parameters (can be multiple). Uses `get_tileset_info`.
        *   `GET /tiles/`: Fetches tile data. Parses `d=<uuid>.<zoom>.<x>[.<y>]` query parameters (can be multiple). Uses `get_tiles`.
    *   Ensure appropriate HTTP status codes are returned (e.g., `200 OK`, `404 Not Found`).

**Phase 3: Application Assembly & Final Touches**

6.  **Create Main Application File (`app/main.py`):**
    *   Initialize the FastAPI application: `app = FastAPI()`.
    *   Include the tilesets router: `app.include_router(tilesets_router_instance)`.
    *   (Optional for MVP) Add basic error handling or root endpoint.

7.  **Testing (Manual):**
    *   Run the development server using `uvicorn`.
    *   Use a tool like `curl`, Postman, or a web browser to send requests to the implemented API endpoints.
    *   Verify:
        *   Correct URL paths and query parameters are accepted.
        *   Response structures match the Pydantic models and `tilesets_api.md`.
        *   Stubbed data is returned as expected.
        *   Error conditions (e.g., non-existent UUID) are handled gracefully.

**Future Considerations (Post-MVP):**

*   Implement other filetypes (BigWig, etc.).
*   Connect to a real data source/database instead of stubs.
*   Implement `POST /tilesets/` for file uploads and ingestion.
*   Add authentication and authorization.
*   Implement more sophisticated filtering and sorting for list endpoints.
*   Add comprehensive automated tests.
