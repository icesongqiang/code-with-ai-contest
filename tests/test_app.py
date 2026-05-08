import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import load_data, get_color, DATA_PATH


class TestDataLoading:
    def test_load_data_returns_dataframe(self):
        df = load_data()
        assert isinstance(df, pd.DataFrame)

    def test_load_data_has_required_columns(self):
        df = load_data()
        required_cols = ['Latitude', 'Longitude', 'Band', 'RSRP_dBm', 'TerminalType', 'Download_Mbps']
        for col in required_cols:
            assert col in df.columns, f"Missing column: {col}"

    def test_load_data_not_empty(self):
        df = load_data()
        assert len(df) > 0


class TestColorMapping:
    def test_strong_signal_green(self):
        assert get_color(-80) == [0, 255, 0]
        assert get_color(-89) == [0, 255, 0]

    def test_medium_signal_yellow(self):
        assert get_color(-100) == [255, 255, 0]
        assert get_color(-105) == [255, 255, 0]

    def test_weak_signal_red(self):
        assert get_color(-115) == [255, 0, 0]
        assert get_color(-120) == [255, 0, 0]


class TestDataFiltering:
    def test_rsrp_thresholds(self):
        df = load_data()
        rsrp_min, rsrp_max = df['RSRP_dBm'].min(), df['RSRP_dBm'].max()
        assert rsrp_min < rsrp_max
        assert rsrp_min < -70
        assert rsrp_max > -120
