# CN-maritime-sim

# コードの概要
東京大学・稗方研究室で行なった「国際海運カーボンニュートラルFeebate評価シミュレーションシステム」の再現実装

# 1, ディレクトリ構成
```text
your_project/
├── README.md
├── requirements.txt
├── .gitignore
└── src/
    ├── utils.py
    ├── prediction.py
    ├── agent.py
    ├── env.py
    ├── simulation.py     # CLI 引数でモデルを選択できるよう拡張
    └── models/
        ├── __init__.py   # モデル名 ↔ クラスを紐付けるファクトリ
        ├── base_model.py           # 何もせず base をそのまま使うモデル
        ├── rd_model.py             # R&D.py 相当
        ├── rd_transition_model.py  # R&D_with_Type_Transition.py 相当
        ├── rd_no_feebate_model.py  # R&D_without_Feebate.py 相当
        └── decreasing_feebate_model.py  # decreasing_feebate.py 相当
```
その他のコードは実験で用いたコードになります。

# 参考文献
```text
- 野々村 一歩, 稗方 和夫, 西野 成昭, 中島 拓也.  
  国際海運のカーボンニュートラルに向けたFeebateの評価のためのシミュレーションシステムの開発.  
  *日本船舶海洋工学会論文集* **39**, 87–99 (2024).  
  DOI: [10.2534/jjasnaoe.39.87](https://doi.org/10.2534/jjasnaoe.39.87) :contentReference[oaicite:0]{index=0}
```


