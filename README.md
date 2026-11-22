# 信号機検出（Faster R-CNN）

車載カメラの映像から信号機を検出し、信号機の状態（青・黄・赤・矢印）を画面右下に表示します。物体検出の代表的なモデルである Faster R-CNN を勉強したので、理解を深めるために PyTorch で実装し、自作のデータセットで学習させました。

<img src="./output_images/sample2.png" alt="動画に検出結果を重ねた様子" width="600">

デモ動画（約1分）：https://youtu.be/RZgY4dEtYw8

別動画：test_/detection_video_shortversion.mp4

## 特徴

- **Faster R-CNN** を torchvision で構築し、ファインチューニングしました。
- **6クラス**を検出します：青（Green）、黄（Yellow）、赤（Red）、右矢印（Right）、直進矢印（Forward）、左矢印（Left）。
- **手前の信号機だけを表示します**：信頼度 0.7 を超える検出結果のうち、ボックスの面積が最も大きいものを採用します。

  <img src="./output_images/sample.png" alt="検出結果の表示例" width="500">

## 使用技術

- PyTorch / torchvision（Faster R-CNN）
- OpenCV、ffmpeg-python（動画の入出力）
- CVAT（アノテーション）
- [review_object_detection_metrics](https://github.com/rafaelpadilla/review_object_detection_metrics)（AP・mAP の評価）

## リポジトリ構成

```
TrafficLightDetection/
├── main.py                          # テスト画像に対する検出結果を表示する
├── train/
│   ├── train.py                     # 学習スクリプト
│   ├── model.py                     # Faster R-CNNの定義
│   ├── TrafficLightDataset.py       # CVAT 形式のアノテーションを読むデータセット
│   └── early_stopping.py            # Early stopping とモデルの保存
├── test_/
│   ├── video_detection.py           # 動画に対して検出し、結果を重ねた動画を出力する
│   └── detection_video_shortversion.mp4  # 出力例
├── other/
│   ├── utils.py                     # アノテーションの読み込み、学習・評価ループ、描画
│   └── analyze_dataset.py           # データセットのクラス分布を集計する
├── create_detection_annotation.py   # 評価用に、検出結果をテキストで書き出す
├── PASCAL_VOC_Annotations/          # 評価用の正解データ（テスト画像31枚）
├── dets_annotation/                 # 評価用の検出結果
├── dets_annotation0.7/              # 評価用の検出結果（信頼度 0.7 以上のみ）
├── models/                          # 学習済みモデル（TorchScript、Git LFS）と学習曲線
├── output_images/                   # README 用の図（評価結果、データセットの分析）
└── classes.txt                      # クラスの一覧
```

## 動作環境

- Python 3


## データセット

学習データは YouTube の運転動画のスクリーンショットから集め、CVAT でアノテーションしました（CVAT for images 1.1 形式）。

- 学習：420枚
- テスト：31枚


データセットのクラス分布（`other/analyze_dataset.py` で集計）：

<img src="./output_images/train_analysis.png" alt="学習データのクラス分布" width="400">
<img src="./output_images/test_analysis.png" alt="テストデータのクラス分布" width="400">


## 学習結果

エポック 16 で early stopping しました。

<img src="./models/learning_plot_dataset2_b8_e200_lr0.005.png" alt="学習曲線" width="400">

## 評価

[review_object_detection_metrics](https://github.com/rafaelpadilla/review_object_detection_metrics) を使って、テスト画像31枚で AP と mAP を計算しました（IoU の閾値は 0.5）。

**すべての検出結果を使った場合**：青・黄・赤は高い精度で検出できています。矢印は、ほかと比べるとやや劣ります。

<img src="./output_images/AP_mAP/all_classes.png" alt="AP と mAP（すべての検出結果）" width="400">

**信頼度 0.7 以上の検出結果だけを使った場合**：デモ動画では閾値を 0.7 にしているので、こちらが実際の性能に近い値です。

<img src="./output_images/AP_mAP_0.75/all_classes.png" alt="AP と mAP（信頼度 0.7 以上）" width="400">

