# scripts/pipeline/core.py
from .database import get_engine
from .processor import import_data
from .analysis import analysis_pipeline

def main():
    #load raw data
    raw_data_path ="/Users/linhao/tcga_sql_demo/data/raw/TCGA-ACC.htseq_fpkm.tsv"
    import_success = import_data(raw_data_path)

    if not import_success:
        return
    
    #analysis process
    analysis_result = analysis_pipeline()

    if analysis_result['status'] =='success':
        print(f"""
        分析レポート:
        - 元の次元数: {analysis_result['original_shape']}
        - 最終的な次元数: {analysis_result['final_shape']}
        - 削除された遺伝子数: {analysis_result['removed_genes']}
        - 削除されたサンプル数: {analysis_result['removed_samples']}
        """)
    else:
        print(f"失敗:{analysis_result['message']}")
if __name__ == "__main__":
    main()
