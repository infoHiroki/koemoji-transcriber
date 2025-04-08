# 開発進捗ログ

## 2025-04-03

*   [x] プロジェクト初期セットアップ
    *   [x] ディレクトリ構造作成 (`src`, `docs`, `build_scripts` 等)
    *   [x] 基本ファイル作成 (`.gitignore`, `README.md`, `LICENSE`)
    *   [x] プレースホルダーPythonファイル作成 (`main.py`, UIコンポーネント, Coreロジック)
    *   [x] 依存関係ファイル作成 (`build_scripts/requirements.txt`)
    *   [x] ビルドスクリプト雛形作成 (`build_scripts/build_app.spec`, `build_scripts/create_installer.iss`)
    *   [x] Gitリポジトリ初期化とコミット
*   [x] 基本UIレイアウト実装とファイル選択機能
    *   [x] `main.py`: 左ペイン（ファイルリスト）と右ペイン（結果表示）の基本レイアウト作成
    *   [x] `main.py`: ファイル選択ボタンと `FilePicker` の追加
    *   [x] `file_list_view.py`: `ListView` を使用したファイル表示コンポーネント実装
    *   [x] `main.py`: 選択されたファイルをリストビューに追加するロジック実装
*   [x] 文字起こし処理の開始と進捗表示 (基本)
    *   [x] `main.py`: 「処理開始」ボタンとプログレスリングを追加
    *   [x] `main.py`: ボタンクリックでバックグラウンドスレッドを開始するロジック実装
    *   [x] `main.py`: スレッド内で `TranscriptionService` を呼び出し（現在はシミュレーション）
    *   [x] `file_list_view.py`: ファイルステータス更新メソッド (`update_status`) を追加
    *   [x] `main.py`: スレッド内でファイルステータスを「処理中」「完了」「エラー」に更新
*   [x] 結果表示エリアへの反映 (基本)
    *   [x] `file_list_view.py`: アイテム選択コールバックと選択状態管理を追加 (`FileItem`, `FileListView`)
    *   [x] `file_list_view.py`: `FileItem` に結果保持用の属性を追加
    *   [x] `result_view.py`: 結果表示用メソッド (`update_results`, `clear_results`) を追加
    *   [x] `main.py`: `FileListView` と `ResultView` を連携させ、選択アイテムの結果を表示
    *   [x] `main.py`: バックグラウンド処理で結果を `FileItem` に保存
*   [x] 実際の文字起こし実装 (`TranscriptionService`)
    *   [x] `transcription.py`: `faster_whisper` と `torch` をインポート
    *   [x] `transcription.py`: `AppConfig` を利用してモデルパスやデバイス設定を読み込み
    *   [x] `transcription.py`: デバイス(CPU/GPU)自動検出とモデルロード処理を実装 (`_detect_device`, `_load_model`)
    *   [x] `transcription.py`: `transcribe_audio` メソッドで実際に `model.transcribe` を呼び出し、結果を整形
    *   [x] `main.py`: `TranscriptionService` 初期化時に `AppConfig` を渡すように修正
*   [x] 出力機能の実装 (初期: 手動保存、複数形式対応)
    *   [x] `main.py`: 「Save Selected Result」ボタンを追加 (後に削除)
    *   [x] `main.py`: 結果保存ロジック (`save_selected_result`) を実装 (TXT/SRT/VTT対応) (後に変更)
    *   [x] `main.py`: ボタンイベントと保存ロジックを接続 (後に削除)
    *   [x] `main.py`: 「Save All Completed Results」ボタンと `DirectoryPicker` を再実装 (後に削除)
*   [x] エラー修正とリファクタリング
    *   [x] `UserControl` / `run_thread_safe` / `update_async` に関するエラー修正
    *   [x] モデルパスのデフォルト値修正
    *   [x] 非推奨API (icons/colors) の修正
    *   [x] UIコンポーネントを関数ベースにリファクタリング
*   [x] **設定画面、ライセンス機能、UI改善の実装**
    *   [x] 設定画面の実装
        *   [x] `main.py`: 設定ボタンと設定ダイアログ (`AlertDialog`, `Tabs`) の追加
        *   [x] `main.py`: 一般タブ (デフォルト出力フォルダ選択、デフォルト言語選択) の実装
        *   [x] `main.py`: モデルタブ (モデルパス、検出デバイス表示) の実装
        *   [x] `main.py`: 出力タブ (TXT/SRT/VTT 保存有効化) の実装 (後に削除)
        *   [x] `main.py`: 設定値の読み込み・保存ロジック (`AppConfig`連携) の実装
    *   [x] ライセンス機能の実装 (MVP)
        *   [x] `license.py`: ライセンス検証、ハードウェアID取得、キー保存/読込関数の作成
        *   [x] `license.py`: `SECRET_SALT` の設定 (`KoemojiSecretSaltForLicense2025!`)
        *   [x] `main.py`: 起動時のライセンスチェックとアクティベーションダイアログ表示
                        *   [x] `main.py`: アクティベーションロジックの実装
                        *   [x] `kihonnsekkeigaiyou.md`: `SECRET_SALT` の記録
    *   [x] その他UI改善
                        *   [x] `file_list_view.py`: 各ファイル項目に言語選択ドロップダウンを追加
                        *   [x] `file_list_view.py`: 各ファイル項目に処理時間表示を追加
        *   [x] `main.py`: 文字起こし処理でファイルごとの言語設定を使用
                        *   [x] `main.py`: 文字起こし完了時に処理時間を計算・表示
                        *   [x] `file_list_view.py`: 「全ファイル削除」ボタンを追加
    *   [x] UI調整
        *   [x] `main.py`: アプリケーションテーマをライトモードに設定
        *   [x] `main.py`: UI要素（ボタン、ラベル、ダイアログ等）を日本語化
*   [x] **パッケージング準備**
    *   [x] `build_app.spec`: モデル、ffmpeg、アセット、隠しインポート等の設定更新
    *   [x] `create_installer.iss`: アプリ名、バージョン、発行元、パス等の設定更新

## 2025-04-04

*   [x] **UIリファクタリング (タブ形式へ変更 & ファイル分割)**
    *   [x] ボタン応答性・ダイアログ表示の問題解決のため、メインUI構造を変更
    *   [x] メインレイアウトを `ft.Tabs` に変更 (`ファイル処理`, `結果表示`, `設定` タブ)
    *   [x] 設定ダイアログを廃止し、「設定」タブに機能を統合
    *   [x] `FilePicker` のフォルダ選択 (`get_directory_path`) のコールバック処理を修正
    *   [x] 「音声ファイルを追加」ボタンの動作を修正・確認
    *   [x] `main.py` から設定タブ関連のコードを `src/app/ui/settings_tab.py` に分離 (2025-04-04)
*   [x] **UI調整と安定化**
    *   [x] ファイルリストの文字サイズ拡大、クリアボタンの表示調整 (`file_list_view.py`)
    *   [x] 不要な区切り線の削除 (`main.py`)
    *   [x] 設定タブのUI改善 (`ft.Card` 使用、幅調整) (`settings_tab.py`)
    *   [x] ファイル処理タブのリファクタリング (`src/app/ui/file_processing_tab.py`) とUI改善 (`ft.Card` 使用、幅調整)
    *   [x] ファイルリストが空の場合にカードを非表示にする機能 (`main.py`, `file_list_view.py`)
    *   [x] 安定版タグ作成 (`stable-v0.1`, `stable-v0.2`)
*   [x] **UIナビゲーション変更 (NavigationRail)**
    *   [x] メインナビゲーションを `ft.Tabs` から `ft.NavigationRail` に変更 (`main.py`)
    *   [x] ビュー切り替えロジックの実装
    *   [x] 関連するエラー修正 (UnboundLocalError, 非推奨API)
    *   [x] 安定版タグ作成 (`stable-v0.3`)
*   [x] **ドキュメント整備**
    *   [x] `README.md` を更新 (機能、使い方、開発者情報、ライセンス補足) (`2296037`, `a21a612`)
*   [x] **パッケージング準備完了**
    *   [x] `models_source/` に large-v3 モデルファイルを配置
    *   [x] `ffmpeg_bin/` に `ffmpeg.exe` を配置
    *   [x] `build_app.spec` を修正し、モデルとffmpegがバンドルに含まれるように設定 (`b06f7cf`)
    *   [x] `create_installer.iss` を修正し、`LICENSE` と `README.md` がインストール先にコピーされるように設定 (`ec21563`)
    *   [x] `src/app/core/transcription.py` を修正し、バンドルされたモデルパスを優先的に使用するように変更 (`083cd03`)
    *   [x] `LICENSE` ファイル (MIT) を作成 (`a21a612`)

## 2025-04-05

*   [x] **仕様変更: 結果保存と表示**
    *   [x] 結果保存をTXT自動保存のみに変更。SRT/VTT出力、手動保存ボタン、関連設定項目を削除する方針を決定。
    *   [x] 結果表示をアコーディオン形式に変更し、プレーンテキストとタイムスタンプ付きテキストの両方を表示。タイムスタンプ付きテキストの手動ダウンロード機能を追加する方針を決定。
*   [x] **仕様変更の実装完了 (2025-04-05)**
    *   [x] `settings_tab.py`: SRT/VTT出力形式チェックボックスを削除。
    *   [x] `transcription.py`: 戻り値が要件を満たしていることを確認。
    *   [x] `main.py`: 文字起こし完了時にプレーンテキストの `.txt` を自動保存するロジックを実装。
    *   [x] `result_view.py`: 結果表示をアコーディオン形式 (`ExpansionPanelList`) に変更。
    *   [x] `result_view.py`: アコーディオン内にプレーンテキストとタイムスタンプ付きテキストを表示。
    *   [x] `result_view.py`: アコーディオン内に「タイムスタンプ付きテキストをダウンロード」ボタンを追加。
    *   [x] `main.py`: タイムスタンプ付きテキストのダウンロード処理 (`handle_download_timestamps`, `on_save_timestamp_file_picked`) を実装。
    *   [x] `file_processing_tab.py`: 既存の手動保存ボタン (`save_selected`, `save_all`) と関連カードを削除。
    *   [x] `main.py`: 上記ボタン削除に伴うコールバックとRefの削除、`create_result_view` と `create_file_processing_tab` の呼び出しを更新。
    *   [x] `main.py`: コピーボタンのロジック (`handle_copy_results`) は構造的に問題ないと判断（テストで確認）。
*   [x] **リファクタリング (2025-04-05):**
    *   [x] `main.py` を分割し、イベントハンドラを `src/app/handlers.py` に、バックグラウンド処理ロジックを `src/app/core/processing.py` に分離。
    *   [x] リファクタリングに伴う起動時エラー (`Event loop is closed`, `TypeError`) を修正。
*   [ ] **次のステップ (優先順位順):**
    *   [ ] **テスト:**
        *   [ ] 包括的な機能テストを実施（リファクタリング完了後）。
            *   [ ] リファクタリング後のアプリケーションが正常に起動し、動作するか。
            *   [ ] ファイル追加、処理開始、完了までの流れ。
            *   [ ] TXTファイルの自動保存が正しく行われるか（デフォルトフォルダ、設定変更後）。
            *   [ ] 結果表示ビュー（アコーディオン）が正しく表示・更新されるか。
            *   [ ] タイムスタンプ付きテキストのダウンロード機能が動作するか。
            *   [ ] コピーボタンが期待通り動作するか。
            *   [ ] 設定タブの各設定が反映されるか（言語、出力フォルダ）。
            *   [ ] ライセンス認証ダイアログの表示・認証プロセス（テストキー使用）。
            *   [ ] エラーハンドリング（不正なファイル、処理中断など）。
    *   [x] **UI調整 (2025-04-05):**
        *   [x] 完了済みファイルドロップダウンの幅を調整 (`width=300` に設定後、`expand=True` に変更、最終的に `Container` でラップしてパディング追加)。
    *   [x] **仕様変更: 結果表示・保存 (2025-04-05):**
        *   [x] 自動保存TXTにタイムスタンプ付きテキストも結合して保存するように変更 (`processing.py`)。
        *   [x] 結果表示ビューから「タイムスタンプ付きテキストをダウンロード」ボタンを削除 (`result_view.py`)。
        *   [x] 結果表示ビューのコピーボタンをプレーンテキスト用とタイムスタンプ付きテキスト用に分離 (`result_view.py`, `handlers.py`, `main.py`)。
*   [x] **エラー修正と安定化 (2025-04-06):**
    *   [x] 起動時に `TypeError: create_file_processing_tab() got an unexpected keyword argument 'cancel_processing_callback'` が発生する問題を修正 (`main.py` の呼び出し箇所から不要な引数を削除)。
    *   [x] 修正後の安定版タグ `stable-v0.5` を作成。
*   [x] **UI統合 (2025-04-06):**
    *   [x] ファイル処理タブと結果表示タブを統合し、新しいメインビュー (`src/app/ui/main_view.py`) を作成。
    *   [x] `main.py`, `handlers.py`, `processing.py` を修正し、新しいビュー構造に対応。
    *   [x] 不要になった `file_processing_tab.py`, `result_view.py` を削除。
    *   [x] 処理完了時に、選択中のファイルであれば結果が自動表示されるように修正。
    *   [x] タブ統合後に発生した起動エラー (`ModuleNotFoundError`, `ImportError`, `NameError`) を修正 (`main.py`, `handlers.py` の不要なインポートや関数呼び出し、引数の不整合を修正)。
    *   [x] レイアウトを左右分割から上下分割に変更 (`main_view.py`)。
    *   [x] 初期テストを実施。起動、ファイル追加、処理、自動保存は正常。ファイル選択による結果表示切り替えは機能しない。
    *   [x] **仕様変更決定:** 結果表示エリアは常時表示。完了時に自動表示し、ファイル選択でも表示切り替え可能とする。
    *   [x] レイアウト崩れ（ファイルリスト増加で結果エリアに被る）を修正 (`file_list_view.py`, `main.py` の構造変更と `expand` 設定調整)。
    *   [x] コピーボタンが機能しない `TypeError` を修正 (`handlers.py` のコールバック関数定義に引数を追加)。
    *   [x] 「全てクリア」ボタンが機能しない問題を修正 (`main.py` の `on_click` 設定を修正)。
    *   [x] プレーンテキスト表示でセグメント間に不要な空行が入る問題を修正 (`transcription.py` の改行処理を変更)。
    *   [x] 修正後の安定版タグ `stable-v0.6` を作成。
    *   [ ] (TODO) ファイルリスト選択時の視覚的フィードバック強化、ガイドテキスト表示、ホバー時のカーソル変更を実装。
    *   [x] 変更を `feature/tab-integration` ブランチにコミット (`807ada6`, `4a4d12d`, `558443a`, `62f2fe1`, `14617cd`, `2c72423`)。
*   [x] **PyInstallerビルド問題解決 (2025-04-08):**
    *   [x] NumPyのDLLロードエラー、FletのModuleNotFoundErrorを解決。
    *   [x] 仮想環境再構築、`flet[all]`インストール、`.spec`ファイル修正（Flet隠しインポート追加）を実施。
    *   [x] 最終的なビルドが成功し、実行ファイルが正常に起動することを確認。
    *   [ ] **その他:**
        *   [ ] UIの最終調整（テスト結果に基づき必要に応じて）。
        *   [ ] ライセンス機能 (`license.py`) の実装・テスト（必要に応じて、現状はMVP）。
        *   [x] ビルド実行 (PyInstaller, Inno Setup) - **PyInstallerビルドは完了。Inno Setupは未実施。**

## 2025-04-08

*   [x] **Windowsインストーラー作成 (Inno Setup) 完了**
    *   `build_scripts/create_installer.iss`を修正し、GUIDとPublisher名を更新。
    *   コメントがファイル名に混入しないよう整理。
    *   2GB超の大容量対応のため`DiskSpanning=yes`と`SlicesPerDisk=1`を追加。
    *   `ISCC.exe`でビルドし、`build_scripts/Output/`に分割インストーラーが生成された。
    *   出力ファイル例：
        *   `Koemoji_Setup_1.0.0 ; Changed output name.exe`
        *   `Koemoji_Setup_1.0.0 ; Changed output name-1.bin`
        *   `Koemoji_Setup_1.0.0 ; Changed output name-2.bin`
    *   **注意:** ファイル名に`; Changed output name`が含まれているのはコメントが混入したため。次回はコメント削除推奨。
    *   インストーラーは多言語対応、ショートカット作成、アンインストーラー付き。
    *   これにより、ユーザーは簡単にセットアップ・アンインストール可能となった。
