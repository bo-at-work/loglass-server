from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException, Path, status, Depends
from app.models import TilesetListResponse, TilesetPublic, TilesetInfoResponse, TilesDataResponse, ErrorModel
from app.services.tileset_repository import StubTilesetRepository

router = APIRouter(
    prefix="/api/v1", tags=["tilesets"], responses={404: {"description": "Not found", "model": ErrorModel}}
)


# Dependency function to get repository instance
def get_repository():
    return StubTilesetRepository()


@router.get("/tilesets/", response_model=TilesetListResponse, summary="List available tilesets")
async def list_tilesets(
    repo: StubTilesetRepository = Depends(get_repository),
    ac: Optional[str] = Query(None, description="Autocomplete filter by tileset name"),
    t: Optional[str] = Query(None, description="Filter by filetype"),
    dt: Optional[List[str]] = Query(None, description="Filter by datatype (can be repeated)"),
    o: Optional[str] = Query(None, description="Order results by a specific field (e.g., name, created)"),
    r: Optional[bool] = Query(False, description="Reverse the order specified by o (e.g., r=True)"),
    page: Optional[int] = Query(1, ge=1, description="Page number for pagination"),
    page_size: Optional[int] = Query(10, ge=1, le=100, description="Number of items per page"),
):
    """
    Lists available tilesets using the stubbed repository.
    """
    tilesets, total_count = await repo.list_tilesets(
        autocomplete=ac, filetype=t, datatype=dt, order_by=o, reverse_order=r, page=page or 1, page_size=page_size or 10
    )
    next_url = None
    prev_url = None
    return TilesetListResponse(count=total_count, next=next_url, previous=prev_url, results=tilesets)


@router.get("/tilesets/{uuid}/", response_model=TilesetPublic, summary="Retrieve a specific tileset")
async def get_tileset(
    uuid: str = Path(..., description="The UUID of the tileset to retrieve"),
    repo: StubTilesetRepository = Depends(get_repository),
):
    """
    Retrieves a specific tileset by its UUID using the stubbed repository.
    """
    tileset = await repo.get_tileset_by_uuid(uuid)
    if not tileset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tileset with UUID {uuid} not found")
    return tileset


@router.get("/tileset_info/", response_model=TilesetInfoResponse, summary="Get detailed metadata for tilesets")
async def get_tileset_info(
    d: List[str] = Query(..., description="UUID of the tileset(s). E.g., d=uuid1&d=uuid2"),
    repo: StubTilesetRepository = Depends(get_repository),
):
    """
    Retrieves detailed metadata for one or more tilesets using the stubbed repository.
    """
    infos = await repo.get_tileset_infos(d)
    return TilesetInfoResponse(data=infos)


@router.get("/tiles/", response_model=TilesDataResponse, summary="Fetch tile data for tilesets")
async def get_tiles(
    d: List[str] = Query(..., description="Tile ID(s) in the format uuid.zoom.x[.y]. E.g., d=uuid1.0.1.2&d=uuid2.1.3"),
    repo: StubTilesetRepository = Depends(get_repository),
):
    """
    Fetches actual data tiles for one or more tilesets using the stubbed repository.
    """
    tile_data = await repo.get_tiles_data(d)
    return TilesDataResponse(data=tile_data)
