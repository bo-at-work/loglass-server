import datetime
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field


class TilesetPublic(BaseModel):
    uuid: str
    filetype: str
    datatype: str
    private: bool = False
    name: Optional[str] = None
    coordSystem: Optional[str] = None
    coordSystem2: Optional[str] = None
    created: Optional[datetime.datetime] = None
    owner: Optional[str] = None  # username
    project_name: Optional[str] = None
    project_owner: Optional[str] = None  # username of project owner
    description: Optional[str] = None
    datafile: Optional[str] = None  # Path to the data file, might be included


class TilesetListResponse(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    results: List[TilesetPublic]


class ErrorModel(BaseModel):
    error: str


# Specific for Cooler files, based on tilesets_api.md examples
class TilesetInfoCooler(BaseModel):
    name: Optional[str] = None
    filetype: str = "cooler"
    datatype: str = "matrix"
    coordSystem: Optional[str] = None
    min_pos: List[int]  # e.g., [0, 0] or [1, 1]
    max_pos: List[int]  # e.g., [249250621, 249250621]
    max_zoom: int  # e.g., 22
    tile_size: Optional[int] = 256  # Default from higlass, can be overridden
    resolutions: Optional[List[int]] = None  # For Cooler, array of available resolutions
    chromsizes: Optional[List[List[Union[str, int]]]] = None  # e.g., [["chr1", 249250621], ...]
    bins_per_dimension: Optional[int] = None  # Often same as tile_size for cooler
    max_width: Optional[int] = None  # Max width of the tileset in base pairs
    mirror_tiles: Optional[str] = Field(None, pattern="^(false|true|yes|no)$")
    clodius_version: Optional[int] = None
    row_infos: Optional[List[str]] = None
    col_infos: Optional[List[str]] = None
    zoom_step: Optional[int] = None


class TilesetInfoResponse(BaseModel):
    # The key is the tileset UUID
    # The value can be the specific info model or an ErrorModel
    # Using a direct Dict field for simplicity with FastAPI response_model
    data: Dict[str, Union[TilesetInfoCooler, ErrorModel]]


# For Cooler tiles, data is often a dense array of numbers or an object with structure
class TileDataCooler(BaseModel):
    dense: List[float]
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    # nan_values: Optional[bool] = False # Could be added if needed


class TilesDataResponse(BaseModel):
    # The key is the tile ID (e.g., "uuid.zoom.x.y")
    # The value can be the specific tile data model or an ErrorModel
    # Using a direct Dict field for simplicity with FastAPI response_model
    data: Dict[str, Union[TileDataCooler, ErrorModel]]
