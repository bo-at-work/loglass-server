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
    "hg19_chromsizes": TilesetPublic(
        uuid="hg19_chromsizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        name="Human (hg19) Chromosome Sizes",
        coordSystem="hg19",
        created=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
        owner="admin",
        project_name="Reference Genomes",
        description="Chromosome sizes for the hg19 human genome assembly.",
    ),
    "hg38_chromsizes": TilesetPublic(
        uuid="hg38_chromsizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        name="Human (hg38) Chromosome Sizes",
        coordSystem="hg38",
        created=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
        owner="admin",
        project_name="Reference Genomes",
        description="Chromosome sizes for the hg38 human genome assembly.",
    ),
    "mm10_chromsizes": TilesetPublic(
        uuid="mm10_chromsizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        name="Mouse (mm10) Chromosome Sizes",
        coordSystem="mm10",
        created=datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=30),
        owner="admin",
        project_name="Reference Genomes",
        description="Chromosome sizes for the mm10 mouse genome assembly.",
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
        bins_per_dimension=256,
        max_width=299999999,
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
        bins_per_dimension=256,
        max_width=249999999,
        max_zoom=9,
        tile_size=256,
        chromsizes=[["chr1", 248956422], ["chrX", 156040895]],
        resolutions=[5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000],
    ),
    "hg19_chromsizes": TilesetInfoCooler(
        name="Human (hg19) Chromosome Sizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        coordSystem="hg19",
        min_pos=[1],
        max_pos=[249250621],
        max_zoom=0,
        tile_size=1,
        chromsizes=[
            ["chr1", 249250621], ["chr2", 243199373], ["chr3", 198022430], ["chr4", 191154276],
            ["chr5", 180915260], ["chr6", 171115067], ["chr7", 159138663], ["chr8", 146364022],
            ["chr9", 141213431], ["chr10", 135534747], ["chr11", 135006516], ["chr12", 133851895],
            ["chr13", 115169878], ["chr14", 107349540], ["chr15", 102531392], ["chr16", 90354753],
            ["chr17", 81195210], ["chr18", 78077248], ["chr19", 59128983], ["chr20", 63025520],
            ["chr21", 48129895], ["chr22", 51304566], ["chrX", 155270560], ["chrY", 59373566], ["chrM", 16569]
        ],
    ),
    "hg38_chromsizes": TilesetInfoCooler(
        name="Human (hg38) Chromosome Sizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        coordSystem="hg38",
        min_pos=[1],
        max_pos=[248956422],
        max_zoom=0,
        tile_size=1,
        chromsizes=[
            ["chr1", 248956422], ["chr2", 242193529], ["chr3", 198295559], ["chr4", 190214555],
            ["chr5", 181538259], ["chr6", 170805979], ["chr7", 159345973], ["chr8", 145138636],
            ["chr9", 138394717], ["chr10", 133797422], ["chr11", 135086622], ["chr12", 133275309],
            ["chr13", 114364328], ["chr14", 107043718], ["chr15", 101991189], ["chr16", 90338345],
            ["chr17", 83257441], ["chr18", 80373285], ["chr19", 58617616], ["chr20", 64444167],
            ["chr21", 46709983], ["chr22", 50818468], ["chrX", 156040895], ["chrY", 57227415], ["chrM", 16569]
        ],
    ),
    "mm10_chromsizes": TilesetInfoCooler(
        name="Mouse (mm10) Chromosome Sizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        coordSystem="mm10",
        min_pos=[1],
        max_pos=[195471971],
        max_zoom=0,
        tile_size=1,
        chromsizes=[
            ["chr1", 195471971], ["chr2", 182113224], ["chr3", 160039680], ["chr4", 156508116],
            ["chr5", 151834684], ["chr6", 149736546], ["chr7", 145441459], ["chr8", 129401213],
            ["chr9", 124595110], ["chr10", 130694993], ["chr11", 122082543], ["chr12", 120129022],
            ["chr13", 120421639], ["chr14", 124902244], ["chr15", 104043685], ["chr16", 98207768],
            ["chr17", 94987271], ["chr18", 90702639], ["chr19", 61431566], ["chrX", 171031299],
            ["chrY", 91744698], ["chrM", 16299]
        ],
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
        """Stub method to get tileset info for multiple UUIDs.

        In a real implementation, this would involve:
        1. Resolving each UUID to its corresponding Cooler file path.
        2. Opening each Cooler file (e.g., using `cooler.Cooler('path/to/file.mcool::/resolutions/1000')`).
        3. Extracting metadata attributes like chromsizes, max_zoom, resolutions, min_pos, max_pos, etc.
           - `chromsizes` can be obtained from `c.chroms()[:]`.
           - `min_pos` and `max_pos` from `c.extent((0, 0))` and `c.extent((c.shape[0], c.shape[1]))` or similar.
           - `max_zoom` might be inferred from available resolutions or stored elsewhere.
           - `tile_size` is often a fixed value (e.g., 256).
           - `bins_per_dimension` is usually the same as `tile_size` for cooler.
           - `max_width` can be calculated from `max_pos[0] - min_pos[0]`.
        4. Formatting this metadata into the TilesetInfoCooler Pydantic model for each tileset.
        The `old_reference_impl` directory might contain examples of this logic.
        """
        infos: Dict[str, Union[TilesetInfoCooler, ErrorModel]] = {}
        for uid in uuids:
            if uid in self._tileset_info:
                infos[uid] = self._tileset_info[uid]
            else:
                infos[uid] = ErrorModel(error=f"Tileset info for {uid} not found (stub)")
        return infos

    async def get_tiles_data(self, tile_ids: List[str]) -> Dict[str, Union[TileDataCooler, ErrorModel]]:
        """Stub method to get data for multiple tiles. Tile ID format: uuid.zoom.x[.y]

        In a real implementation, this would involve, for each tile_id:
        1. Parsing the tile_id into UUID, zoom level, and x/y coordinates.
        2. Resolving the UUID to a Cooler file path and the specific resolution dataset within it.
        (e.g., `path/to/file.mcool::/resolutions/{resolution_value_for_zoom_level}`)
        3. Using a library like `clodius.tiles.cooler_tiles` or custom logic with the `cooler` library
        to fetch the raw tile data for the given coordinates and zoom level.
        - This involves identifying the genomic range for the tile and querying the Cooler matrix.
        - The data might be a dense numpy array.
        4. Potentially normalizing or processing the data (e.g., applying log transformations).
        5. Formatting the data into the TileDataCooler Pydantic model, including the 'dense' array
        and optionally 'min_value', 'max_value'.
        The `old_reference_impl` directory, particularly any clodius or cooler interaction code,
        would be highly relevant here.
        """
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
                # TODO: Implement actual tile data fetching logic here.
                # Steps would be:
                # 1. Parse tile_id: uuid, zoom, x_pos, (optional y_pos)
                #    zoom_level = int(parts[1])
                #    x_coord = int(parts[2])
                #    y_coord = int(parts[3]) if len(parts) > 3 else None (for 1D tiles/tracks)
                # 2. Get tileset metadata (e.g., file path, resolutions) from self._tileset_info.get(uuid)
                # 3. Determine the actual resolution value from zoom_level and tileset's resolutions list.
                # 4. Construct path to the specific cooler resolution (e.g., cooler_file_path + '::/resolutions/' + str(actual_resolution)).
                # 5. Call a function (e.g., from clodius or custom cooler logic) to get the tile data:
                #    tile_values_dense_array = fetch_cooler_tile(cooler_path_with_resolution, zoom_level, x_coord, y_coord)
                #    min_val, max_val = np.min(tile_values_dense_array), np.max(tile_values_dense_array)
                # This is highly simplified. Real tile generation is complex.
                # For now, returning a placeholder:
                data[tile_id] = TileDataCooler(
                    dense=[
                        0.1,
                        0.2,
                        0.3,
                        0.4,
                        0.5,
                        0.6,
                        0.7,
                        0.8,
                        0.1,
                        0.2,
                        0.3,
                        0.4,
                        0.5,
                        0.6,
                        0.7,
                        0.8,
                    ],  # Example 4x4 tile
                    min_value=0.0,
                    max_value=1.0,
                )  # Dummy dense data
                # Example for a 256x256 tile (if tile_size is 256):
                # data[tile_id] = TileDataCooler(
                #     dense=[random.random() for _ in range(256*256)],
                #     min_value=0.0,
                #     max_value=1.0
                # )
            else:
                data[tile_id] = ErrorModel(error=f"Tileset for tile {tile_id} not found (stub)")
        return data

    async def get_tilesets_by_coord_system(self, coord_system: str) -> List[TilesetPublic]:
        """Get tilesets by coordinate system (assembly)."""
        results = []
        for tileset in self._tilesets.values():
            if tileset.coordSystem == coord_system:
                results.append(tileset)
        return results

    async def get_tileset_info(self, uuid: str) -> Optional[TilesetInfoCooler]:
        """Get tileset info for a single UUID."""
        return self._tileset_info.get(uuid)
