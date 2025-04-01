#scripts/pipeline/processor.py
import pandas as pd
from .database import get_engine

def import_data(file_path):
    """Importing TSV into a database"""
    try:
        df = pd.read_csv(file_path, sep='\t')
        long_df = df.melt(
            id_vars="Ensembl_ID",
            var_name="SampleID",
            value_name="FPKM"
        )
        engine =get_engine()
        long_df.to_sql('expression', engine, index=False, if_exists='replace')
        return True
    except Exception as e:
        print(f"flase:{str(e)}")
        return False