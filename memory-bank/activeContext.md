# アクティブコンテキスト (2025-04-07 v1)

## 現在のフォーカス

PyInstallerでのビルド時にNumPyのDLL読み込みエラーが解決せず、ビルド作業を一旦中断。安定版 `stable-v0.8` までの機能実装は完了。

## 次のステップ (優先順位順)

---

### 今後の推奨作業

- Google Drive等に`release/for-distribution/`内の重要ファイルをアップロード
- 共有リンクを`README.md`に追記
- 新しいクリーンなGitリポジトリに必要ファイルだけをpush
- GitHubのReleasesページに案内を掲載
- 社内・関係者にリリース案内
- 旧リポジトリや大容量ファイルのバックアップ
- 今後の改善・開発計画の策定

---
1.  **TODO:** 包括的な機能テストを実施。
    *   [x] アプリケーションが正常に起動し、動作するか。
    *   [x] ファイル追加、処理開始、完了までの流れ。
    *   [x] TXTファイルの自動保存（結合された内容）が正しく行われるか。
    *   [x] 結果表示エリア（上下分割）が正しく表示・更新されるか（完了時自動表示、ファイル選択による切り替え）。
    *   [x] 各結果エリア横のコピーボタンが期待通り動作するか。
    *   [x] 「全てクリア」ボタンが機能するか。
    *   [x] 設定タブの各設定が反映されるか (**検出デバイス表示、出力設定削除後の確認含む**)。(ユーザーテストOK 2025-04-07)
    *   [-] ライセンス認証ダイアログの表示・認証プロセス (**機能廃止 2025-04-07**)。
    *   [-] エラーハンドリング (**一旦見送り 2025-04-07**)。
    *   [-] ファイルリスト選択時の視覚的フィードバック強化、ホバー時のカーソル変更の実装状況確認 (**一旦見送り 2025-04-07**)。
    *   [x] ウィンドウアイコン設定 (`main.py`)。
    *   [x] 非推奨アイコン (`ft.icons` -> `ft.Icons`) 置換 (`main.py`, `settings_tab.py`)。
    *   [x] 起動時の黒画面対策としてローディング画面表示とバックグラウンド初期化を実装 (`main.py`)。(安定版 `stable-v0.8` 作成)
2.  [-] UIの最終調整（**一旦完了 2025-04-07**）。
3.  [-] キャンセル機能の実装（**実装見送り 2025-04-07**）。
4.  [-] ライセンス機能 (`license.py`) の実装・テスト（**機能廃止 2025-04-07**）。
5.  [x] **ビルド実行 (PyInstaller, Inno Setup) (2025-04-08 解決済み)**
    *   Inno Setupスクリプトを修正し、GUIDとPublisher名を更新。
    *   2GB超の大容量対応のため`DiskSpanning=yes`を設定。
    *   `ISCC.exe`でビルドし、`build_scripts/Output/`に分割インストーラーが生成された。
    *   出力ファイル名に`; Changed output name`が混入しているため、次回はコメント削除推奨。
    *   多言語対応、ショートカット作成、アンインストーラー付きのWindowsインストーラーが完成。

## 最近の決定事項・学び

---

### 重要な履歴・決定事項・工夫点まとめ

- **PyInstallerのNumPy DLL問題**  
  → 仮想環境を再作成し、依存関係を再インストールして解決

- **Fletのhiddenimports問題**  
  → `.spec`ファイルに`flet_core`, `flet_runtime`, `flet_desktop`を追加

- **Inno Setupの2GB超対応**  
  → `DiskSpanning=yes`で分割インストーラを生成

- **GitHubの2GB制限問題**  
  → pushできず、大容量ファイルはGit管理対象外に決定

- **履歴削除 (`git filter-repo`) を実施**  
  → それでもpush不可のため、新リポジトリでクリーンスタートを決定

- **大容量ファイルはGoogle Drive等で配布**

- **UI/UX改善**  
  → タブ統合、上下分割ビュー、コピー・保存機能の強化

- **ライセンス認証機能は廃止し、MITライセンスに統一**

- **旧リポジトリはバックアップとして保持**

- **新リポジトリは履歴なしのクリーンスタート**

- **社内ナレッジ`docs/internal_knowledge.md`に詳細を記録済み**

---

*   **PyInstallerビルド問題の解決 (2025-04-08):**
    *   当初、ビルド後の実行ファイルで NumPy の `ImportError: DLL load failed while importing _multiarray_umath` が発生。
    *   `.spec` ファイルへのバイナリ/データ収集の明示的追加、カスタムフック (`hook-numpy.py`) の作成などを試したが解決せず。
    *   ビルドログの警告 (`Foreign Python environment's site-packages...`) に着目し、仮想環境 (`.venv`) を再作成。
    *   再作成した仮想環境をアクティベートし、依存関係 (`requirements.txt`) と PyInstaller を再インストール。
    *   これにより NumPy エラーは解消されたが、新たに Flet の `ModuleNotFoundError: No module named 'flet_desktop'` が発生し、アプリが起動ループに陥る。
    *   Flet のエラーメッセージとドキュメントに基づき、仮想環境に `pip install "flet[all]==0.27.6" --upgrade` を実行してデスクトップ用コンポーネントを含む完全版をインストール。
    *   `.spec` ファイルの `hiddenimports` に `flet_core`, `flet_runtime`, `flet_desktop` を追加。
    *   上記手順により、最終的にビルド・実行時エラーが解消された。
    *   **学び:** PyInstaller で複雑な依存関係を持つライブラリ (NumPy, PyTorch, Flet) を扱う際は、クリーンな仮想環境を使い、その環境を**アクティベートした状態**で PyInstaller を実行することが極めて重要。また、GUIフレームワークによっては `pip install framework[all]` のような完全版のインストールが必要な場合がある。`.spec` の `hiddenimports` も適切に設定する必要がある。

*   **タブ統合完了 (2025-04-06):**
    *   ファイル処理タブと結果表示タブを統合し、新しいメインビュー (`src/app/ui/main_view.py`) を作成。
    *   `main.py`, `handlers.py`, `processing.py` を修正し、新しいビュー構造に対応。
    *   不要になった `file_processing_tab.py`, `result_view.py` を削除。
    *   処理完了時に、選択中のファイルであれば結果が自動表示されるように修正。
    *   変更を `feature/tab-integration` ブランチにコミット (`807ada6`, `4a4d12d`)。
*   **タブ統合後のエラー修正 (2025-04-06):**
    *   タブ統合後に発生した起動エラー (`ModuleNotFoundError`, `ImportError`, `NameError`) を修正。原因は、削除されたモジュール (`result_view`) のインポートや関数の呼び出し、引数の不整合が残っていたため。`main.py`, `handlers.py`, `main_view.py` の関連箇所を修正して解決。
*   **初期テストと次の仕様決定 (2025-04-06):**
    *   タブ統合後の初期テストを実施。起動、ファイル追加、処理、自動保存は正常。
    *   ファイル選択による結果表示切り替えが機能しない問題を確認 (`NameError: name 'e' is not defined` が発生していたが、これは `handlers.py` の修正で解消済み。ただし、意図した表示更新は行われていない)。
    *   レイアウトを左右分割から上下分割に変更。
    *   **次の仕様(明確化):** 結果表示エリアは常時表示。処理完了時に該当ファイルの結果を自動表示。ユーザーはファイルリスト選択で表示結果を手動切り替え可能。コピーボタンは各テキストエリアの横（ヘッダー行）。
*   **ビルドエラー調査 (2025-04-07):**
    *   PyInstallerビルド時に `ImportError: DLL load failed while importing _multiarray_umath` が発生。
    *   `build_app.spec` に `pathex` で `.venv/Lib/site-packages` を追加。
    *   `build_app.spec` に `hookspath` でPyInstaller標準フックパスを追加。
    *   `build_app.spec` で `collect_dynamic_libs('numpy')` や `collect_data_files('numpy')` を試行するも `ValueError` が発生。
    *   `pip uninstall/install` で `numpy`, `torch` を再インストール。
    *   上記対策でも解決せず、ビルド作業を一旦中断。
*   **起動処理改善と安定化 (2025-04-07):**
    *   起動時のモデル読み込み中にローディング画面（プログレスリングとテキスト）を表示するように `main.py` を修正。
    *   モデル読み込みとメインUI構築をバックグラウンドスレッド (`initialize_app_background`) で実行するように変更。
    *   初期化完了後、メインスレッドでUIをローディング画面からメイン画面に切り替える処理を追加。
    *   `page.run_thread_safe` の誤用を修正し、Fletの内部機構によるスレッドセーフなUI更新に修正。
    *   上記変更をコミット (`6289df7`)。
    *   安定版タグ `stable-v0.8` を作成。
*   **アイコン設定と更新 (2025-04-07):**
    *   `main.py` にウィンドウアイコン (`src/assets/koemoji-infinity-logo-256x256.ico`) を設定。
    *   `main.py` と `settings_tab.py` 内の非推奨 `ft.icons` を推奨される `ft.Icons` に置換。
*   **ライセンス認証廃止 (2025-04-07):**
    *   商用ライセンスモデルを取りやめ、完全にMITライセンスのフリーソフトウェアとすることを決定。
    *   ライセンスチェック、ダイアログ表示、キー検証・保存に関連するコードを `main.py`, `handlers.py` から削除。
    *   `src/app/core/license.py` ファイルを削除。
    *   関連ドキュメント (`projectBrief.md`, `systemPatterns.md`, `README.md`) を更新。
*   **コードリセット (2025-04-07):** ライセンス認証ダイアログの表示問題デバッグのため加えた変更 (`main.py`, `handlers.py`) を破棄し、`git reset --hard stable-v0.7` を実行して安定版の状態に戻した。
*   **設定タブ調整と安定化 (stable-v0.7 時点) (2025-04-07):**
    *   設定タブに検出デバイス（CPU/CUDA）を表示する機能を追加 (`main.py`, `settings_tab.py`)。
    *   設定タブから不要な「出力設定」セクション（TXT保存チェックボックス）を削除 (`settings_tab.py`)。
    *   設定ファイル (`config.py`) のデフォルト値から `[Output]` セクションを削除。
    *   上記変更を含むコミット (`e59c3be`) に安定版タグ `stable-v0.7` を作成済み。
*   **レイアウト調整とエラー修正 (stable-v0.6 時点) (2025-04-07):**
    *   上下分割レイアウトでファイルリストが増えると結果表示エリアに被る問題を修正 (`file_list_view.py`, `main.py` の構造変更と `expand` 設定調整)。
    *   コピーボタンが機能しない `TypeError` を修正 (`handlers.py` のコールバック関数定義に引数を追加)。
    *   「全てクリア」ボタンが機能しない問題を修正 (`main.py` の `on_click` 設定を修正)。
    *   プレーンテキスト表示でセグメント間に不要な空行が入る問題を修正 (`transcription.py` の改行処理を変更)。
    *   修正後の安定版タグ `stable-v0.6` を作成。
*   **エラー修正と安定化 (2025-04-06):**
    *   起動時に `TypeError: create_file_processing_tab() got an unexpected keyword argument 'cancel_processing_callback'` が発生する問題を修正 (`main.py` の呼び出し箇所から不要な引数を削除)。
    *   修正後の安定版タグ `stable-v0.5` を作成。
*   **結果表示仕様変更 (2025-04-05):**
    *   結果表示ビューのレイアウトをアコーディオン形式から上下分割（上:プレーンテキスト、下:タイムスタンプ付き）に変更。
    *   「タイムスタンプ付きテキストをダウンロード」ボタンを削除。
    *   自動保存される `.txt` ファイルに、プレーンテキストとタイムスタンプ付きテキストの両方を含めるように変更。
    *   結果表示ビューのコピーボタンを、プレーンテキスト用とタイムスタンプ付きテキスト用に分離。
*   **UI/UX改善方針決定 (2025-04-06):**
    *   ファイル処理タブと結果表示タブを統合し、1画面でファイルリストと結果を確認できるようにする。
    *   文字起こし完了時に、そのファイルの結果を結果表示エリアに自動的に表示する。
    *   ファイルリスト選択時の視覚的フィードバック強化、ガイドテキスト表示、ホバー時のカーソル変更を行う。

*   **リファクタリング実施 (2025-04-05):** `main.py` が肥大化してきたため、保守性向上の目的でリファクタリングを実施。
    *   イベントハンドラ関数群 (`handle_file_selection`, `handle_copy_results`, `activate_license` など) を `src/app/handlers.py` に移動。
    *   バックグラウンドでの文字起こし処理ループ (`run_transcription_thread`) と処理開始関数 (`start_processing`) を `src/app/core/processing.py` に移動。
    *   `main.py` はUIの組み立て、各モジュールの初期化と依存関係の注入 (`setup_handlers`, `setup_processing`) を行う役割に整理された。
*   UIをタブ形式 (`ft.Tabs`) に変更。設定機能はダイアログではなくタブ内に統合。(2025-04-04)
*   `FilePicker` の `get_directory_path` は、`pick_files` と異なり、呼び出し時に `on_result` パラメータで直接コールバックを指定する必要があることが判明。共通の `on_result` ハンドラではディレクトリ選択イベントを捕捉できなかった。
*   設定ダイアログの表示に `page.show_dialog()` を使用するアプローチも試したが、根本的な解決には至らなかった（ライセンスダイアログとの競合可能性）。タブ化によりこの問題を回避。
*   タブUIへのリファクタリングにより、「音声ファイルを追加」ボタンが正常に機能するようになったことを確認 (2025-04-04)。他のボタン（処理開始など）も動作している模様。
*   ボタンベースUIのデバッグ（特にフォルダ選択、設定ダイアログ）が難航したため、タブUIへの変更を決定 (2025-04-04)。
*   Gitコミット時のコマンド連結は、現在のシェル環境 (PowerShell) では `;` を使用する必要がある。
*   **解決済み (FilePicker):** `FilePicker` の結果処理を中央ハンドラ (`handle_picker_result`) に集約し、アクションコンテキスト (`_current_picker_action`) を使用することで、ファイル選択とディレクトリ選択の両方が正しく機能するようになった (2025-04-04)。`get_directory_path` 呼び出し時に `on_result` を渡さないように修正。
*   **解決済み (AppConfig):** `AppConfig` クラスのメソッド呼び出しに関するエラー (`get_model_path`, `save`) を修正 (2025-04-04)。
*   **ファイル分割完了:** `main.py` から設定タブ関連のコードを `src/app/ui/settings_tab.py` に分離するリファクタリングを実施 (2025-04-04)。`main.py` はよりシンプルになった。
*   **UI調整:** ファイルリストの文字サイズ、クリアボタンの表示方法、区切り線を調整した (2025-04-04)。
*   **レイアウト課題:**
    *   `ft.Container` や `ft.Column` を使ったタブ全体の左右パディング設定が期待通りに機能しなかった。`Tab` の `content` に直接 `Container` を設定する方法も試したが失敗。Fletのレイアウトシステム、特に `Tabs` との組み合わせについて、さらに調査が必要かもしれない。当面はパディングなしで進める。
    *   `page.window_width` および `page.window_min_width` による初期ウィンドウ幅の設定が、現在の環境では期待通りに反映されなかったため、最終的に元の設定に戻した。
*   **エラー修正:** `page.window_center()` は存在しないため削除 (2025-04-04)。
*   **パッケージング準備完了:** モデルファイル (large-v3) と ffmpeg.exe をプロジェクト内に配置し、`build_app.spec` と `create_installer.iss` を更新して、これらが正しくバンドル・インストールされるように設定した (2025-04-05)。
*   **バンドル対応:** `transcription.py` を修正し、PyInstallerでバンドルされた環境で実行された場合に、同梱されたモデルパス (`models/large-v3`) を自動的に使用するようにした (2025-04-05)。
*   **ライセンスファイル:** プロジェクトルートに MIT License で `LICENSE` ファイルを作成した。`README.md` にもライセンスに関する補足説明を追加した (2025-04-05)。
*   **結果保存仕様変更 (2025-04-05):** 手動保存からTXT自動保存 + タイムスタンプ手動ダウンロードに変更。SRT/VTTサポートは削除。
*   **結果表示仕様変更 (2025-04-05):** 単一表示からアコーディオン形式での複数結果表示に変更。
*   **ロールバック実施:** 設定タブの幅調整 (`9daea95`) および関連するエラー修正 (`91505f6`) 後に `ModuleNotFoundError` が解消されなかったため、プロジェクト全体を安定動作していたコミット `f6407a9` (アプリケーション全体の文字サイズ調整完了時点) に `git reset --hard` でロールバック (2025-04-04)。
*   **安定版タグ作成:** ロールバック先のコミット `f6407a9` に `stable-v0.1` というGitタグを作成 (2025-04-04)。
*   **UI改善 (設定タブ):** 設定タブの各セクション（一般、モデル、出力）を `ft.Card` を使用してグループ化。カード内にパディングを追加し、カード間のスペースを調整 (`settings_tab.py`) (2025-04-05)。
*   **エラー修正 (設定タブ幅):** `ft.Container` に存在しない `max_width` 引数を使用していたため `TypeError` が発生。修正のため、中央の `ft.Column` (`settings_content`) に `width=600` を設定し、それを `ft.Row` 内で左右の `ft.Container(expand=True)` で挟む方式に変更して幅制限と中央揃えを実現 (`settings_tab.py`) (2025-04-05)。
*   **安定版タグ作成 (v0.2):** 設定タブのUI改善とエラー修正が完了したコミット `c870f5a` に `stable-v0.2` というGitタグを作成 (2025-04-05)。
*   **リファクタリング (ファイル処理タブ):** ファイル処理タブのUI構築ロジックを `main.py` から `src/app/ui/file_processing_tab.py` に分離 (2025-04-05)。
*   **UI改善 (ファイル処理タブ):** ファイル処理タブのUI要素（アクションボタン、ファイルリスト、保存ボタン）をそれぞれ `ft.Card` でグループ化 (`file_processing_tab.py`) (2025-04-05)。
*   **UI改善 (ファイル処理タブ幅):** ファイル処理タブのコンテンツ全体を `ft.Row` でラップし、中央のカラムに `width=800` を設定、左右に `expand=True` の `ft.Container` を配置して幅制限と中央揃えを実現 (`main.py`) (2025-04-05)。
*   **エラー修正 (Import):** リファクタリング中に `main.py` で `file_list_view_control` を直接インポートしようとして `ImportError` が発生したため修正。`create_file_list_view` を呼び出してコントロールを取得するように変更 (2025-04-05)。
*   **UI改善 (ファイルリストカード):** ファイルリストが空の場合に、ファイルリストを含むカード (`file_list_card`) を非表示にするように実装。`file_list_view` モジュールに状態変更通知コールバックを追加し、`main.py` でカードの `visible` プロパティを制御 (2025-04-05)。
*   **エラー修正 (ファイルリストマージン):** `ft.Row` に存在しない `margin` 引数を使用していたため `TypeError` が発生。修正のため、「すべてクリア」ボタンを含む `ft.Row` を `ft.Container` でラップし、そのコンテナに上マージンを設定 (`file_list_view.py`) (2025-04-05)。
*   **UI調整 (タブ):** タブ自体（ファイル処理、結果表示、設定）を中央揃えにするため、`ft.Tabs` に `tab_alignment=ft.TabAlignment.CENTER` を設定 (`main.py`) (2025-04-05)。
*   **UIナビゲーション変更:** ユーザーの提案に基づき、メインナビゲーションを `ft.Tabs` から `ft.NavigationRail` に変更 (2025-04-05)。これにより、左側に縦型のナビゲーションが表示されるようになった。
*   **ビューコンテンツの分離:** `create_settings_tab` のようなビュー構築関数は、コンテナ（例: `ft.Tab`）ではなく、表示するコンテンツコントロール自体を返すように修正する必要がある。
*   **関数定義順序:** Fletアプリケーション内で関数（特にコールバックとして渡すもの）を使用する場合、呼び出し箇所よりも前で定義する必要がある。
*   **非推奨API:** Fletのバージョンアップに伴い非推奨となったAPI (`ft.icons`, `ft.colors`) は、推奨される新しいAPI (`ft.Icons`, `ft.Colors`) に置き換える必要がある。
