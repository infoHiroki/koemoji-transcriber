基本設計概要

1. 技術スタック

言語: Python (3.9+)

GUI: Flet

文字起こし: FasterWhisper (CTranslate2バックエンド)

コア: PyTorch (CPU/GPU), logging, configparser

音声処理: ffmpeg (同梱)

パッケージング: PyInstaller

インストーラー: Inno Setup

(オプション): ffmpeg-python

2. ディレクトリ構造 (推奨)

whisper-desktop-transcriber/
├── src/                     # ソースコード (main.py, app/, assets/)
│   ├── app/
│   │   ├── ui/              # Flet UIコンポーネント
│   │   └── core/            # コアロジック (transcription, config, license)
│   └── utils/               # ヘルパー関数
├── models_source/           # 開発用モデルファイル (-> インストーラーへ)
├── build_scripts/           # ビルド設定 (requirements.txt, .spec, .iss)
├── ffmpeg_bin/              # 同梱するffmpeg実行ファイル (-> インストーラーへ)
├── dist/                    # PyInstaller出力先
├── release/                 # Inno Setup出力先 (最終インストーラー)
├── docs/                    # ドキュメント
├── tests/                   # (オプション) テストコード
├── .gitignore
├── README.md
└── LICENSE


3. 主要コンポーネント役割

src/app/ui/: Fletを用いた画面レイアウト、ウィジェット配置、ユーザー操作への応答定義。

src/app/core/transcription.py:

*   ffmpeg を利用した音声ファイルの読み込み・デコード。
*   GPU(CUDA)の利用可否判定と、デバイス(CPU/GPU)の自動選択。
*   FasterWhisperモデルのロードと管理（バンドルされたモデルを優先）。
*   文字起こし処理の実行と結果（プレーンテキスト、タイムスタンプ付きテキスト）の取得。
*   バックグラウンドスレッドでの処理実行とUIへの進捗/結果通知。

src/app/core/config.py: INI形式の設定ファイルの読み書き、デフォルト値の管理。

# src/app/core/license.py: 削除 (2025-04-07)

src/app/core/processing.py: バックグラウンドでの文字起こし処理の実行、進捗管理、UIへの結果通知。

src/app/handlers.py: UIイベント（ボタンクリック、ファイル選択など）への応答、対応する処理の呼び出し。

main.py: アプリケーション起動、Fletの初期化、UIビューの組み立て、各コンポーネントとハンドラの接続、依存関係の注入。

PyInstaller (build_app.spec): Pythonコード、依存ライブラリ、ffmpeg、モデルファイル（またはロード用設定）、アセットを単一実行可能ファイル（またはフォルダ）にパッケージング。

Inno Setup (create_installer.iss): PyInstallerで生成されたアプリ一式、モデルファイル、ffmpeg、その他必要なファイル（ライセンス文書等）を同梱し、Windowsインストーラーを作成。インストール時のファイル配置、ショートカット作成、レジストリ/設定ファイルの初期設定（オプション）を定義。

4. データフロー概要 (文字起こし処理)

ユーザーがファイルリストに音声ファイルを追加。

ユーザーが「処理開始」ボタンをクリック (`handlers.py` がイベントを処理)。

`handlers.py` が `processing.py` の処理開始関数を呼び出す。

`processing.py` がバックグラウンドスレッドを開始。

バックグラウンドスレッド (`processing.py` 内):
a. UIに進捗「モデル読込中」を通知 (`file_list_view.py` の `update_file_status` を使用)。
b. `transcription.py` の `_load_model` を呼び出し (必要であれば)。
c. UIに進捗「処理中」を通知。
d. `transcription.py` の `transcribe_audio` を呼び出し (内部でffmpegを使用)。
e. 結果（プレーンテキスト、タイムスタンプ付きテキスト）を受け取る。
f. **プレーンテキスト結果を、設定された出力先フォルダに `.txt` ファイルとして自動保存。**
g. UIに結果（プレーンテキスト、タイムスタンプ付きテキスト）と進捗「完了」を通知 (`file_list_view.py` の `update_file_status`、`result_view.py` の `update_dropdown_options`、`handlers.py` の `handle_file_selection` を使用)。
h. エラー発生時はUIに「エラー」と概要を通知、詳細をログファイルに記録。

UIスレッド (`file_list_view.py`, `main_view.py`) が通知を受け取り、表示を更新。ユーザーは結果表示ビューからタイムスタンプ付きテキストを手動でダウンロード可能 (`handlers.py` がイベントを処理)。

# 5. ライセンスに関する注意点 - 削除 (2025-04-07)
