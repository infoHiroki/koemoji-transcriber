# Whisper Desktop Transcriber (Batch Edition)

会議などの複数の音声データを、高精度な文字起こしモデル (Whisper large) を使用して、ローカル環境 (オフライン) で安全かつ効率的に一括でテキスト化できる Windows デスクトップアプリケーションです。

## 主な機能

*   **オフライン動作:** インターネット接続不要で、ローカルPC上で文字起こしが完結します。
*   **高精度:** [FasterWhisper](https://github.com/guillaumekln/faster-whisper) 実装の Whisper large モデルにより、高精度な文字起こしを実現します。
*   **一括処理:** 複数の音声ファイルをリストに追加し、まとめて処理できます。
*   **ファイル形式:** TXT, SRT, VTT形式での出力に対応しています（設定で選択可能）。
*   **シンプルなUI:** [Flet](https://flet.dev/) を使用した直感的なユーザーインターフェース (`NavigationRail` ベース)。
*   **設定:** 文字起こし言語、モデルサイズ（現状 large 固定）、出力形式などを設定画面で変更できます。

## 使い方 (開発環境)

1.  **リポジトリのクローン:**
    ```bash
    git clone <リポジトリURL>
    cd whisper-desktop-transcriber
    ```
2.  **依存関係のインストール:**
    ```bash
    pip install -r build_scripts/requirements.txt
    # 必要に応じて PyTorch (CPU/GPU) を別途インストールしてください
    # https://pytorch.org/
    ```
3.  **FFmpegの準備:**
    FFmpeg がシステムにインストールされているか、`ffmpeg_bin` ディレクトリ内の実行ファイルが利用可能であることを確認してください。
4.  **アプリケーションの起動:**
    ```bash
    python src/main.py
    ```
5.  **基本操作:**
    *   左側のナビゲーションレールで「ファイル処理」「結果表示」「設定」ビューを切り替えます。
    *   **ファイル処理ビュー:**
        *   「音声ファイルを追加」ボタンで文字起こししたいファイルを選択します。
        *   リストに追加されたファイルの処理ステータスを確認できます。
        *   「処理開始」ボタンでリスト内のファイルの文字起こしを開始します。
        *   「全てクリア」ボタンでリストを空にします。
    *   **結果表示ビュー:**
        *   処理が完了したファイルの文字起こし結果が表示されます。
        *   「全件保存」ボタンで、設定で指定したフォルダに全ての処理結果を保存します。
    *   **設定ビュー:**
        *   文字起こし言語、モデル、出力形式、保存先フォルダなどを設定します。
        *   設定は自動的に保存されます。

## 開発者向け情報

*   主要な依存関係は `build_scripts/requirements.txt` を参照してください。
*   ビルド設定は `build_scripts/build_app.spec` (PyInstaller) および `build_scripts/create_installer.iss` (Inno Setup) を参照してください。

## 安定版

*   現在の最新安定版は Git タグ `stable-v0.3` です。

## インストール

### 配布物

- `release/Koemoji_Setup_1.0.0.exe`
- `release/Koemoji_Setup_1.0.0-1.bin`
- `release/Koemoji_Setup_1.0.0-2.bin`

### インストール手順

1. `release/Koemoji_Setup_1.0.0.exe` をダブルクリック
2. セットアップウィザードに従い「次へ」「インストール」を選択
3. 完了後、スタートメニューやデスクトップのショートカットから起動可能

### アンインストール方法

- Windowsの「設定」→「アプリと機能」から「Koemoji」を選び「アンインストール」

### 注意点

- 2GB超のため複数の`.bin`ファイルが生成されています。**exeと同じ `release/` フォルダに全て置いてください**
- インストーラーは多言語対応、ショートカット作成、アンインストーラー付きです

## ライセンス

このソフトウェアのソースコードは MIT License の下で提供されます。ライセンスの詳細は、プロジェクトルートにある `LICENSE` ファイルをご覧ください。

(参考: MITライセンスは、著作権表示とライセンス条文を含めることを条件に、商用利用、改変、再配布などを自由に行うことを認める、非常に寛容なオープンソースライセンスです。)
