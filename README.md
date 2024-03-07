# 日本語の事前学習コーパスの作成 

このレポジトリは日本語の事前学習コーパスを作ることを目的としています.

※このスクリプトはGENIAC(松尾研究室)の活動で開発が進められています.

## [mC4のクリーニング](mc4s)
- mc4をクリーニングし､機械学習で商用サイトなどをフィルタリングし､textを出力します
- もとのサイズの20%くらいまでクリーニングできます(推定値)
- 並列化に対応していないコードなので注意
- 他のdatasetでも清掃可能です｡


## [CommonCrawlのWarcファイルからのコーパス構築](warc)
- CommonCrawlからWARCファイルをダウンロード
- 日本語のページを抜き出し､クリーニング､ゴミ記事の削除､jsonlを生成
- までやるコードです

## 予定

- 3/2 Streamlitを使い, アプリ上からコーパス構築を進められるツールの作成

- 3/3 コードの並列化に対応

- 3/5 大規模データ加工に秀でたAmazon EMRを使用し, 分散でデータの加工を実行するコードの追加

## TODO
- クリーニング精度
- 記事の分割精度
- ほか