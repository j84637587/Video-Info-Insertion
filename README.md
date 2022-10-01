# Video-Info-Insertion
此專案目的在將csv中依照指定之時間資料嵌入影片當中。

## 需求
- Python >= 3.9

## 使用方式

1. 將 `example.csv` 修改或置換成想要的資料。
> 注意: 第一列必須為時間值(time)
2. 修改 `main.py` 中輸入影片位置，預設 `example.mp4`。
3. 開始執行嵌入，執行指令 ``` python3 main.py ``` ，並耐心等待。
> 注意: 根據設備性能與影片畫面數量可能需要大量時間。
4. 執行完成後結果會輸出於 `result.mp4`

## DEMO

以 `example.mp4` 為範例之產生[結果影片](https://youtu.be/8FL0JCCNaeY)。
