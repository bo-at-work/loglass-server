from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import TilesetInfoCooler, TilesetPublic
from app.services.tileset_repository import StubTilesetRepository


@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)


@pytest.fixture
def mock_repository():
    """Mock repository fixture"""
    return AsyncMock(spec=StubTilesetRepository)


@pytest.fixture
def sample_tileset():
    """Sample tileset fixture"""
    return TilesetPublic(
        uuid="test_hg19_chromsizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        name="Test Human (hg19) Chromosome Sizes",
        coordSystem="hg19",
        owner="test_user",
        description="Test chromosome sizes for hg19",
    )


@pytest.fixture
def sample_tileset_info():
    """Sample tileset info fixture"""
    return TilesetInfoCooler(
        name="Test Human (hg19) Chromosome Sizes",
        filetype="chromsizes-tsv",
        datatype="chromsizes",
        coordSystem="hg19",
        min_pos=[1],
        max_pos=[249250621],
        max_zoom=0,
        tile_size=1,
        chromsizes=[
            ["chr1", 249250621],
            ["chr2", 243199373],
            ["chr3", 198022430],
            ["chrX", 155270560],
            ["chrY", 59373566],
        ],
    )


class TestChromSizesEndpoint:
    """Tests for the /api/v1/chrom-sizes/ endpoint"""

    def test_get_chrom_sizes_with_tileset_uuid(self, client, monkeypatch, sample_tileset, sample_tileset_info):
        """Test getting chromosome sizes using a tileset UUID"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = sample_tileset
        mock_repo.get_tileset_info.return_value = sample_tileset_info

        # Override the dependency
        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=test_hg19_chromsizes")

            assert response.status_code == 200
            data = response.json()
            assert "chromsizes" in data
            assert len(data["chromsizes"]) == 5
            assert data["chromsizes"][0] == ["chr1", 249250621]
            assert data["chromsizes"][1] == ["chr2", 243199373]

            mock_repo.get_tileset_by_uuid.assert_called_once_with("test_hg19_chromsizes")
            mock_repo.get_tileset_info.assert_called_once_with("test_hg19_chromsizes")
        finally:
            # Clean up
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_with_assembly_name(self, client, monkeypatch, sample_tileset, sample_tileset_info):
        """Test getting chromosome sizes using assembly name"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = None
        mock_repo.get_tilesets_by_coord_system.return_value = [sample_tileset]
        mock_repo.get_tileset_info.return_value = sample_tileset_info

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=hg19")

            assert response.status_code == 200
            data = response.json()
            assert "chromsizes" in data
            assert len(data["chromsizes"]) == 5

            mock_repo.get_tileset_by_uuid.assert_called_once_with("hg19")
            mock_repo.get_tilesets_by_coord_system.assert_called_once_with("hg19")
            mock_repo.get_tileset_info.assert_called_once_with("test_hg19_chromsizes")
        finally:
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_with_default_assembly(self, client, monkeypatch):
        """Test getting chromosome sizes using built-in default assembly"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = None
        mock_repo.get_tilesets_by_coord_system.return_value = []

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=hg19")

            assert response.status_code == 200
            data = response.json()
            assert "chromsizes" in data
            assert len(data["chromsizes"]) == 25  # hg19 has 25 chromosomes
            assert data["chromsizes"][0] == ["chr1", 249250621]
            assert data["chromsizes"][-1] == ["chrM", 16569]
        finally:
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_tsv_format(self, client, monkeypatch):
        """Test getting chromosome sizes in TSV format"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = None
        mock_repo.get_tilesets_by_coord_system.return_value = []

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=hg19&type=tsv")

            assert response.status_code == 200
            assert response.headers["content-type"] == "text/tab-separated-values; charset=utf-8"

            lines = response.text.strip().split("\n")
            assert len(lines) == 25
            assert lines[0] == "chr1\t249250621"
            assert lines[1] == "chr2\t243199373"
        finally:
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_cumulative(self, client, monkeypatch):
        """Test getting cumulative chromosome sizes"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = None
        mock_repo.get_tilesets_by_coord_system.return_value = []

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=hg19&cum=1")

            assert response.status_code == 200
            data = response.json()
            assert "chromsizes" in data

            # First chromosome should start at 0
            assert data["chromsizes"][0] == ["chr1", 0]
            # Second chromosome should start at the size of chr1
            assert data["chromsizes"][1] == ["chr2", 249250621]
            # Third chromosome should start at chr1 + chr2 sizes
            assert data["chromsizes"][2] == ["chr3", 249250621 + 243199373]
        finally:
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_not_found(self, client, monkeypatch):
        """Test 404 when assembly/tileset not found"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = None
        mock_repo.get_tilesets_by_coord_system.return_value = []

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=unknown_assembly")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "No chromosome sizes found for assembly: unknown_assembly" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_tileset_without_chromsizes(self, client, monkeypatch, sample_tileset):
        """Test 404 when tileset exists but has no chromsizes"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = sample_tileset
        mock_repo.get_tileset_info.return_value = None

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=test_hg19_chromsizes")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "No chromosome sizes available for this tileset" in data["detail"]
        finally:
            app.dependency_overrides.clear()

    def test_get_chrom_sizes_with_empty_chromsizes(self, client, monkeypatch, sample_tileset):
        """Test 404 when tileset exists but has empty chromsizes"""
        mock_repo = AsyncMock()
        mock_repo.get_tileset_by_uuid.return_value = sample_tileset

        empty_tileset_info = TilesetInfoCooler(
            name="Empty chromsizes",
            filetype="chromsizes-tsv",
            datatype="chromsizes",
            coordSystem="test",
            min_pos=[1],
            max_pos=[1000],
            max_zoom=0,
            tile_size=1,
            chromsizes=[],  # Empty chromsizes
        )
        mock_repo.get_tileset_info.return_value = empty_tileset_info

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/chrom-sizes/?id=test_hg19_chromsizes")

            assert response.status_code == 404
            data = response.json()
            assert "detail" in data
            assert "No chromosome sizes available for this tileset" in data["detail"]
        finally:
            app.dependency_overrides.clear()


class TestAvailableChromSizesEndpoint:
    """Tests for the /api/v1/available-chrom-sizes/ endpoint"""

    def test_get_available_chrom_sizes_success(self, client, monkeypatch):
        """Test successfully getting available chromosome size datasets"""
        sample_tilesets = [
            TilesetPublic(
                uuid="hg19_chromsizes",
                filetype="chromsizes-tsv",
                datatype="chromsizes",
                name="Human (hg19) Chromosome Sizes",
                coordSystem="hg19",
                owner="admin",
            ),
            TilesetPublic(
                uuid="hg38_chromsizes",
                filetype="chromsizes-tsv",
                datatype="chromsizes",
                name="Human (hg38) Chromosome Sizes",
                coordSystem="hg38",
                owner="admin",
            ),
        ]

        mock_repo = AsyncMock()
        mock_repo.list_tilesets.return_value = (sample_tilesets, 2)

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/available-chrom-sizes/")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 2
            assert data["next"] is None
            assert data["previous"] is None
            assert len(data["results"]) == 2
            assert data["results"][0]["uuid"] == "hg19_chromsizes"
            assert data["results"][0]["datatype"] == "chromsizes"
            assert data["results"][1]["uuid"] == "hg38_chromsizes"

            mock_repo.list_tilesets.assert_called_once_with(datatype=["chromsizes"], page=1, page_size=10)
        finally:
            app.dependency_overrides.clear()

    def test_get_available_chrom_sizes_with_pagination(self, client, monkeypatch):
        """Test getting available chromosome sizes with pagination parameters"""
        mock_repo = AsyncMock()
        mock_repo.list_tilesets.return_value = ([], 0)

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/available-chrom-sizes/?page=2&page_size=5")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 0
            assert len(data["results"]) == 0

            mock_repo.list_tilesets.assert_called_once_with(datatype=["chromsizes"], page=2, page_size=5)
        finally:
            app.dependency_overrides.clear()

    def test_get_available_chrom_sizes_empty_result(self, client, monkeypatch):
        """Test getting available chromosome sizes when no datasets exist"""
        mock_repo = AsyncMock()
        mock_repo.list_tilesets.return_value = ([], 0)

        from app.routers import chromsizes

        app.dependency_overrides[chromsizes.get_repository] = lambda: mock_repo

        try:
            response = client.get("/api/v1/available-chrom-sizes/")

            assert response.status_code == 200
            data = response.json()
            assert data["count"] == 0
            assert data["results"] == []
        finally:
            app.dependency_overrides.clear()


class TestHelperFunctions:
    """Tests for helper functions in the chromsizes module"""

    def test_get_default_chromsizes_hg19(self):
        """Test getting default chromsizes for hg19"""
        from app.routers.chromsizes import get_default_chromsizes

        result = get_default_chromsizes("hg19")
        assert result is not None
        assert len(result) == 25
        assert result[0] == ["chr1", 249250621]
        assert result[-1] == ["chrM", 16569]

    def test_get_default_chromsizes_hg38(self):
        """Test getting default chromsizes for hg38"""
        from app.routers.chromsizes import get_default_chromsizes

        result = get_default_chromsizes("hg38")
        assert result is not None
        assert len(result) == 25
        assert result[0] == ["chr1", 248956422]
        assert result[-1] == ["chrM", 16569]

    def test_get_default_chromsizes_mm10(self):
        """Test getting default chromsizes for mm10"""
        from app.routers.chromsizes import get_default_chromsizes

        result = get_default_chromsizes("mm10")
        assert result is not None
        assert len(result) == 22
        assert result[0] == ["chr1", 195471971]
        assert result[-1] == ["chrM", 16299]

    def test_get_default_chromsizes_unknown(self):
        """Test getting default chromsizes for unknown assembly"""
        from app.routers.chromsizes import get_default_chromsizes

        result = get_default_chromsizes("unknown_assembly")
        assert result is None

    def test_calculate_cumulative_sizes(self):
        """Test calculating cumulative chromosome sizes"""
        from app.routers.chromsizes import calculate_cumulative_sizes

        input_chromsizes = [
            ["chr1", 100],
            ["chr2", 200],
            ["chr3", 150],
        ]

        result = calculate_cumulative_sizes(input_chromsizes)

        expected = [
            ["chr1", 0],
            ["chr2", 100],
            ["chr3", 300],
        ]

        assert result == expected

    def test_calculate_cumulative_sizes_empty(self):
        """Test calculating cumulative sizes with empty input"""
        from app.routers.chromsizes import calculate_cumulative_sizes

        result = calculate_cumulative_sizes([])
        assert result == []

    def test_calculate_cumulative_sizes_single_chromosome(self):
        """Test calculating cumulative sizes with single chromosome"""
        from app.routers.chromsizes import calculate_cumulative_sizes

        input_chromsizes = [["chr1", 1000]]
        result = calculate_cumulative_sizes(input_chromsizes)

        assert result == [["chr1", 0]]


class TestParameterValidation:
    """Tests for parameter validation"""

    def test_chrom_sizes_missing_id_parameter(self, client):
        """Test that id parameter is required"""
        response = client.get("/api/v1/chrom-sizes/")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data
        assert any("id" in str(error) for error in data["detail"])

    def test_available_chrom_sizes_invalid_page(self, client):
        """Test validation of page parameter"""
        response = client.get("/api/v1/available-chrom-sizes/?page=0")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    def test_available_chrom_sizes_invalid_page_size(self, client):
        """Test validation of page_size parameter"""
        response = client.get("/api/v1/available-chrom-sizes/?page_size=101")

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data


# Integration tests using the actual repository (not mocked)
class TestIntegration:
    """Integration tests using the actual stub repository"""

    def test_chrom_sizes_integration_with_real_repo(self, client):
        """Test chromosome sizes endpoint with real repository"""
        # This tests with the actual stub data
        response = client.get("/api/v1/chrom-sizes/?id=hg19_chromsizes")

        assert response.status_code == 200
        data = response.json()
        assert "chromsizes" in data
        assert len(data["chromsizes"]) > 0
        # Check that we get the actual hg19 chromosome data
        assert data["chromsizes"][0][0] == "chr1"
        assert isinstance(data["chromsizes"][0][1], int)

    def test_available_chrom_sizes_integration(self, client):
        """Test available chromosome sizes endpoint with real repository"""
        response = client.get("/api/v1/available-chrom-sizes/")

        assert response.status_code == 200
        data = response.json()
        assert data["count"] >= 0
        assert "results" in data

        # If there are results, they should be chromsizes tilesets
        for tileset in data["results"]:
            assert tileset["datatype"] == "chromsizes"
