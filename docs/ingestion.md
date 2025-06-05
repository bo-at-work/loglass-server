# HiGlass Server: Data Ingestion

This document outlines the methods for ingesting data into the HiGlass server to create tilesets.

## 1. Command-Line Ingestion (`manage.py ingest_tileset`)

The primary and most flexible method for ingesting local files is using the `manage.py ingest_tileset` script. This tool processes your data file, generates the necessary tiles, and registers the tileset with the HiGlass server.

**Basic Usage:**

```bash
python manage.py ingest_tileset \
    --filename /path/to/your/datafile.cool \
    --filetype cooler \
    --datatype matrix \
    --coordSystem hg19 \
    --uid my-cooler-tileset \
    --name "My Cooler Dataset" \
    --project-name "My Research Project"
```

**Key Parameters:**

*   `--filename`: (Required) Path to the local data file.
*   `--filetype`: (Required) Type of the input file. Examples: `cooler`, `bigwig`, `hitile`, `chromsizes-tsv`, `bedfile`, `beddb`, `fasta`.
*   `--datatype`: (Required) Nature of the data. Examples: `matrix`, `vector`, `gene-annotation`, `chromsizes`.
*   `--coordSystem`: (Required) Genome assembly or coordinate system (e.g., `hg19`, `mm10`).
*   `--uid` (optional): Specify a unique ID for the tileset. If not provided, one will be generated.
*   `--name` (optional): A human-readable name for the tileset.
*   `--project-name` (optional): Name of an existing project to associate this tileset with. The project will be created if it doesn't exist.
*   `--indexfile` (optional): Path to an index file if required by the filetype (e.g., for BAM files, this would be the `.bai` file).
*   `--no-upload` (optional): If specified, the file will not be copied to the server's media directory. Use if the file is already in a location accessible by the server.
*   `--assembly` (optional): Alias for `--coordSystem`.
*   Additional parameters may be available or required depending on the `filetype` (e.g., chromosome names/sizes for bed-like files if not using a `chromsizes-tsv` filetype).

Run `python manage.py ingest_tileset --help` for a full list of options.

## 2. API-Based Ingestion

While command-line ingestion is common for local files, the API also provides methods for creating tilesets:

*   **Direct File Upload:** `POST /api/v1/tilesets/`
    This endpoint allows for creating a tileset by directly uploading the `datafile` (and optionally `indexfile`) as part of a `multipart/form-data` request. See the [Tileset API Documentation](./tilesets_api.md#post-apiv1tilesets) for more details.

*   **Registering a Remote URL:** `POST /api/v1/register_url/`
    This endpoint allows registering a tileset from a publicly accessible URL. The server will then fetch and process the data from this URL. See the [Tileset API Documentation](./tilesets_api.md#44-apiv1register_url) for more details.

These API methods are useful for programmatic ingestion or when integrating HiGlass server with other systems that manage data remotely.
