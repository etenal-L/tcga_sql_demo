#scripts/pipeline/analysis.py
import pandas as pd
import numpy as np
from sqlalchemy import text
from .database import get_engine

def load_processed_data():
    """"load data"""
    engine = get_engine()
    return pd.read_sql_table('processed_expression', engine, index_col='SampleID')

def preprocess_data(df):
    
    #change to matrix
    data = df.astype(np.float64)

    #Remove low-variance genes
    gene_std =data.std(axis=0)
    filtered_genes = gene_std[gene_std > 0.1].index
    data = data[filtered_genes]

    return data

def quality_control(data, gene_missing_thresh=0.1, sample_missing_thresh=0.1):
    """Quality control (similar to WGCNA's goodSamplesGenes function)
    Returns:
    - Cleaned data
    - List of removed genes
    - List of removed samples"""

    #check gene dimension
    gene_missing =data.isnull().mean(axis=0) > gene_missing_thresh
    bad_genes = gene_missing[gene_missing].index.tolist()

    #check samples dimension
    sample_missing = data.isnull().mean(axis=1) > sample_missing_thresh
    bad_samples =sample_missing[sample_missing].index.tolist()

    cleaned = data.loc[~sample_missing, ~gene_missing]

    #print report    
    if bad_genes:
        print(f"Removed genes ({len(bad_genes)}): {', '.join(bad_genes[:3])}...")
    if bad_samples:
        print(f"Removed samples ({len(bad_samples)}): {', '.join(bad_samples[:3])}...")

    return cleaned, bad_genes, bad_samples
def analysis_pipeline():
    """"whole analysis process"""
    try:
        #load data from database
        raw_df = load_processed_data()

        #preprocess
        processed_data =preprocess_data(raw_df)

        #quality check
        final_data, bad_genes, bad_samples = quality_control(processed_data)

        #save result
        final_data.to_sql('cleaned_expression', get_engine(), if_exists='replace')

        return{
            "status": "success",
            "original_shape": raw_df.shape,
            "final_shape": final_data.shape,
            "removed_genes": len(bad_genes),
            "removed_samples": len(bad_samples)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
