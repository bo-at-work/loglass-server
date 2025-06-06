from typing import List, Optional


from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse

from app.models import AvailableChromSizesResponse, ChromSizesResponse, ErrorModel
from app.services.tileset_repository import StubTilesetRepository

router = APIRouter(
    prefix="/api/v1", tags=["chromosome-sizes"], responses={404: {"description": "Not found", "model": ErrorModel}}
)


# Dependency function to get repository instance
def get_repository():
    return StubTilesetRepository()


@router.get("/chrom-sizes/", summary="Get chromosome sizes for a given assembly")
async def get_chrom_sizes(
    id: str = Query(..., description="Assembly ID or tileset UUID"),
    type: str = Query("json", description="Response format: json or tsv"),
    cum: int = Query(0, description="Include cumulative sizes (0 or 1)"),
    repo: StubTilesetRepository = Depends(get_repository),
):
    """
    Retrieve chromosome sizes for a given assembly or tileset.

    Parameters:
    - id: Assembly ID (e.g., 'hg19', 'mm10') or tileset UUID
    - type: Response format - 'json' (default) or 'tsv'
    - cum: Include cumulative sizes (0=no, 1=yes)

    Returns chromosome sizes in the requested format.
    """

    # First try to find a tileset with this ID
    tileset = await repo.get_tileset_by_uuid(id)

    if not tileset:
        # Try to find by coordinate system (assembly name)
        tilesets = await repo.get_tilesets_by_coord_system(id)
        if tilesets:
            # Use the first tileset found for this assembly
            tileset = tilesets[0]

    if not tileset:
        # Return some default chromosome sizes for common assemblies
        default_chromsizes = get_default_chromsizes(id)
        if not default_chromsizes:
            raise HTTPException(status_code=404, detail=f"No chromosome sizes found for assembly: {id}")
        chromsizes_data = default_chromsizes
    else:
        # Get chromsizes from tileset info
        tileset_info = await repo.get_tileset_info(tileset.uuid)
        if not tileset_info or not hasattr(tileset_info, "chromsizes") or not tileset_info.chromsizes:
            raise HTTPException(status_code=404, detail="No chromosome sizes available for this tileset")
        chromsizes_data = tileset_info.chromsizes

    # Handle cumulative sizes if requested
    if cum == 1:
        chromsizes_data = calculate_cumulative_sizes(chromsizes_data)

    # Return in requested format
    if type.lower() == "tsv":
        tsv_content = "\n".join([f"{chrom}\t{size}" for chrom, size in chromsizes_data])
        return PlainTextResponse(content=tsv_content, media_type="text/tab-separated-values")
    else:
        # Return JSON format
        return ChromSizesResponse(chromsizes=chromsizes_data)


@router.get(
    "/available-chrom-sizes/",
    response_model=AvailableChromSizesResponse,
    summary="List available chromosome size datasets",
)
async def get_available_chrom_sizes(
    repo: StubTilesetRepository = Depends(get_repository),
    page: Optional[int] = Query(1, ge=1, description="Page number"),
    page_size: Optional[int] = Query(10, ge=1, le=100, description="Number of items per page"),
):
    """
    List all available chromosome size datasets.
    These are typically tilesets with datatype='chromsizes'.
    """

    # Get tilesets with chromsizes datatype
    tilesets, total_count = await repo.list_tilesets(datatype=["chromsizes"], page=page or 1, page_size=page_size or 10)

    # TODO: Implement pagination URLs
    next_url = None
    prev_url = None

    return AvailableChromSizesResponse(count=total_count, next=next_url, previous=prev_url, results=tilesets)


def get_default_chromsizes(assembly_id: str) -> Optional[List[List]]:
    """
    Return default chromosome sizes for common assemblies.
    This is a fallback when no tileset is found.
    """
    defaults = {
        "hg19": [
            ["chr1", 249250621],
            ["chr2", 243199373],
            ["chr3", 198022430],
            ["chr4", 191154276],
            ["chr5", 180915260],
            ["chr6", 171115067],
            ["chr7", 159138663],
            ["chr8", 146364022],
            ["chr9", 141213431],
            ["chr10", 135534747],
            ["chr11", 135006516],
            ["chr12", 133851895],
            ["chr13", 115169878],
            ["chr14", 107349540],
            ["chr15", 102531392],
            ["chr16", 90354753],
            ["chr17", 81195210],
            ["chr18", 78077248],
            ["chr19", 59128983],
            ["chr20", 63025520],
            ["chr21", 48129895],
            ["chr22", 51304566],
            ["chrX", 155270560],
            ["chrY", 59373566],
            ["chrM", 16569],
        ],
        "hg38": [
            ["chr1", 248956422],
            ["chr2", 242193529],
            ["chr3", 198295559],
            ["chr4", 190214555],
            ["chr5", 181538259],
            ["chr6", 170805979],
            ["chr7", 159345973],
            ["chr8", 145138636],
            ["chr9", 138394717],
            ["chr10", 133797422],
            ["chr11", 135086622],
            ["chr12", 133275309],
            ["chr13", 114364328],
            ["chr14", 107043718],
            ["chr15", 101991189],
            ["chr16", 90338345],
            ["chr17", 83257441],
            ["chr18", 80373285],
            ["chr19", 58617616],
            ["chr20", 64444167],
            ["chr21", 46709983],
            ["chr22", 50818468],
            ["chrX", 156040895],
            ["chrY", 57227415],
            ["chrM", 16569],
        ],
        "mm10": [
            ["chr1", 195471971],
            ["chr2", 182113224],
            ["chr3", 160039680],
            ["chr4", 156508116],
            ["chr5", 151834684],
            ["chr6", 149736546],
            ["chr7", 145441459],
            ["chr8", 129401213],
            ["chr9", 124595110],
            ["chr10", 130694993],
            ["chr11", 122082543],
            ["chr12", 120129022],
            ["chr13", 120421639],
            ["chr14", 124902244],
            ["chr15", 104043685],
            ["chr16", 98207768],
            ["chr17", 94987271],
            ["chr18", 90702639],
            ["chr19", 61431566],
            ["chrX", 171031299],
            ["chrY", 91744698],
            ["chrM", 16299],
        ],
    }

    return defaults.get(assembly_id)


def calculate_cumulative_sizes(chromsizes: List[List]) -> List[List]:
    """
    Calculate cumulative chromosome sizes.
    """
    cumulative = []
    total = 0

    for chrom, size in chromsizes:
        cumulative.append([chrom, total])
        total += size

    return cumulative
