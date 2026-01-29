import pytest
from src.heady_project.archive import HeadyArchive
from src.heady_project.economy import mint_coin

def test_mint_coin():
    tx_id = mint_coin(100, "TestCoin")
    assert tx_id is not None
    assert "tx_mint_100_TestCoin" in tx_id

def test_mint_coin_invalid():
    tx_id = mint_coin(0, "TestCoin")
    assert tx_id is None

def test_archive_preserve():
    data = {"key": "value"}
    result = HeadyArchive.preserve(data, "test_dest")
    assert result is True
