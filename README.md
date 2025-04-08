# Koemoji Transcriber (Whisper Desktop Batch Edition)

会議や講演など複数の音声ファイルを、高精度なWhisper largeモデルで**完全オフライン**かつ**安全・効率的**に一括文字起こしできるWindowsデスクトップアプリです。

---

## 主な特徴

- **完全オフライン動作**：インターネット接続不要。機密データも安心。
- **高精度**：[FasterWhisper](https://github.com/guillaumekln/faster-whisper)実装のWhisper largeモデルを使用。
- **一括処理**：複数ファイルをまとめて高速に文字起こし。
- **自動保存**：文字起こし完了時に**プレーンテキスト(.txt)**を自動保存。
- **タイムスタンプ付き結果の閲覧・コピー**：アプリ内で確認・コピー可能。
- **シンプルなUI**：[Flet](https://flet.dev/)製の直感的なインターフェース。
- **MITライセンス**：商用・個人利用ともに無料。

---

## 使い方

### 1. 音声ファイルの追加
- 「ファイル追加」ボタンで複数の音声ファイルを選択。

### 2. 一括文字起こし開始
- 「処理開始」ボタンで全ファイルの文字起こしを実行。
- 進捗状況はリストで確認可能。

### 3. 結果の確認・コピー
- 完了したファイルを選択すると、  
  - **プレーンテキスト**  
  - **タイムスタンプ付きテキスト**  
  がアプリ内に表示されます。
- 各テキストは**コピー**可能。

### 4. 自動保存
- プレーンテキストは自動で`.txt`ファイルとして保存されます。

---

## インストール方法

### 配布リンク

[最新版インストーラーのダウンロードはこちら](https://e.pcloud.link/publink/show?code=kZlwxdZQhuRmYUWvTjj6GAPsVIrSJgcDrtV)

### 配布物

- `release/Koemoji_Setup_1.0.0.exe`
- `release/Koemoji_Setup_1.0.0-1.bin`
- `release/Koemoji_Setup_1.0.0-2.bin`

### 手順

1. `Koemoji_Setup_1.0.0.exe`をダブルクリック
2. ウィザードに従いインストール
3. スタートメニューやデスクトップのショートカットから起動

### 注意

- `.exe`と`.bin`は**同じフォルダ**に置いてください
- 多言語対応、アンインストーラー付き

---

## 開発者向け

- Python 3.9+
- 依存関係は `requirements.txt` 参照
- FasterWhisper, PyTorch, CTranslate2, Fletを使用
- ビルドはPyInstaller、インストーラーはInno Setupで作成
- 詳細は`memory-bank/`内のドキュメント参照

---

## 最新安定版

`v1.0`

---

## ライセンス

MIT License  
詳細は`LICENSE`ファイル参照。

---
