import pandas as pd
from sqlalchemy import create_engine

#　読み込む
df = pd.read_csv('/Users/linhao/tcga_sql_demo/data/TCGA-ACC.htseq_fpkm.tsv', sep='\t')

#　long形式へ変換
long_df = df.melt(
    id_vars="Ensembl_ID",
    var_name="SampleID",
    value_name="FPKM"
)

#SQLiteデータベース接続

engine = create_engine('sqlite:////Users/linhao/tcga_sql_demo/database/tcga_acc')
long_df.to_sql('expression', engine, index=False, if_exists='replace')

print("success")