import datetime
from typing import Dict, List, Optional, Tuple, Union

from app.models import ErrorModel, TileDataCooler, TilesetInfoCooler, TilesetPublic

# Dummy data for stubbing
stub_tilesets_db: Dict[str, TilesetPublic] = {
    "stub_cooler_1": TilesetPublic(
        uuid="stub_cooler_1",
        filetype="cooler",
        datatype="matrix",
        name="My Stub Cooler 1",
        coordSystem="hg19",
        created=datetime.datetime.now(datetime.timezone.utc),
        owner="stub_user",
        project_name="Stub Project",
        description="A cooler file for testing.",
    ),
    "stub_cooler_2": TilesetPublic(
        uuid="stub_cooler_2",
        filetype="cooler",
        datatype="matrix",
        name="Another Cooler Example",
        coordSystem="hg38",
        created=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1),
        owner="stub_user",
        project_name="Stub Project",
        description="Second cooler tileset.",
    ),
}

stub_tileset_info_db: Dict[str, TilesetInfoCooler] = {
    "stub_cooler_1": TilesetInfoCooler(
        name="My Stub Cooler 1",
        filetype="cooler",
        datatype="matrix",
        coordSystem="hg19",
        min_pos=[1, 1],
        max_pos=[300000000, 300000000],
        max_zoom=10,
        tile_size=256,
        chromsizes=[["chr1", 249250621], ["chr2", 243199373]],
        resolutions=[1000, 2000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000],
    ),
    "stub_cooler_2": TilesetInfoCooler(
        name="Another Cooler Example",
        filetype="cooler",
        datatype="matrix",
        coordSystem="hg38",
        min_pos=[1, 1],
        max_pos=[250000000, 250000000],
        max_zoom=9,
        tile_size=256,
        chromsizes=[["chr1", 248956422], ["chrX", 156040895]],
        resolutions=[5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000],
    ),
}


class StubTilesetRepository:
    def __init__(self):
        # In a real scenario, this would connect to a DB or load from files
        self._tilesets = stub_tilesets_db
        self._tileset_info = stub_tileset_info_db

    async def list_tilesets(
        self,
        autocomplete: Optional[str] = None,
        filetype: Optional[str] = None,
        datatype: Optional[List[str]] = None,
        order_by: Optional[str] = None,
        reverse_order: Optional[bool] = False,
        page: int = 1,
        page_size: int = 10,
    ) -> Tuple[List[TilesetPublic], int]:
        """Stub method to list tilesets with basic filtering and pagination."""
        results = list(self._tilesets.values())

        # Basic filtering (can be expanded)
        if autocomplete:
            results = [ts for ts in results if ts.name and autocomplete.lower() in ts.name.lower()]
        if filetype:
            results = [ts for ts in results if ts.filetype == filetype]
        if datatype:
            results = [ts for ts in results if ts.datatype in datatype]

        # Basic sorting (can be expanded)
        if order_by and hasattr(TilesetPublic, order_by):
            actual_reverse_order = reverse_order if reverse_order is not None else False
            results.sort(key=lambda ts: getattr(ts, order_by) or "", reverse=actual_reverse_order)

        total_count = len(results)
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        paginated_results = results[start_index:end_index]

        return paginated_results, total_count

    async def get_tileset_by_uuid(self, uuid: str) -> Optional[TilesetPublic]:
        """Stub method to get a single tileset by UUID."""
        return self._tilesets.get(uuid)

    async def get_tileset_infos(self, uuids: List[str]) -> Dict[str, Union[TilesetInfoCooler, ErrorModel]]:
        """Stub method to get tileset info for multiple UUIDs."""
        infos: Dict[str, Union[TilesetInfoCooler, ErrorModel]] = {}
        for uid in uuids:
            if uid in self._tileset_info:
                infos[uid] = self._tileset_info[uid]
            else:
                infos[uid] = ErrorModel(error=f"Tileset info for {uid} not found (stub)")
        return infos

    async def get_tiles_data(self, tile_ids: List[str]) -> Dict[str, Union[TileDataCooler, ErrorModel]]:
        """Stub method to get data for multiple tiles. Tile ID format: uuid.zoom.x[.y]"""
        data: Dict[str, Union[TileDataCooler, ErrorModel]] = {}
        for tile_id in tile_ids:
            parts = tile_id.split(".")
            if len(parts) < 3:
                data[tile_id] = ErrorModel(error=f"Invalid tile ID format: {tile_id}")
                continue

            uuid = parts[0]
            # zoom = parts[1]
            # x_pos = parts[2]
            # y_pos = parts[3] if len(parts) > 3 else None

            if uuid in self._tilesets:  # Check if tileset exists
                # For stub, return some generic data or an error if not specifically handled
                # This is highly simplified. Real tile generation is complex.
                data[tile_id] = TileDataCooler(values=[0.1, 0.2, 0.3, 0.4])  # Dummy data
            else:
                data[tile_id] = ErrorModel(error=f"Tileset for tile {tile_id} not found (stub)")
        return data
