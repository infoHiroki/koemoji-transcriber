import flet as ft
from typing import TYPE_CHECKING, Callable, Tuple # Import Callable and Tuple

if TYPE_CHECKING:
    from ..core.config import AppConfig
    from flet import Page, FilePicker, Ref, Control # Import Ref and Control

# TODO: デバイス検出などの非UIロジックを core に移動する

def create_settings_tab(
    page: 'Page',
    config: 'AppConfig',
    file_picker: 'FilePicker',
    set_picker_action_callback: Callable[[str], None], # Callback to set action context
    detected_device_str: str # Add parameter for detected device
) -> Tuple[ft.Control, ft.Ref[ft.TextField]]: # Return Control and Ref
    """
    設定ビューのUIコントロールを作成し、コンテンツコントロールと出力フォルダテキストフィールドのRefを返します。
    detected_device_str: 実際に使用されているデバイス ("CPU" または "CUDA")。
    """
    # --- コントロール定義 (Use Ref) ---
    default_output_dir_textfield_ref = ft.Ref[ft.TextField]() # Create Ref

    default_output_dir_textfield = ft.TextField(
        ref=default_output_dir_textfield_ref, # Assign Ref
        label="デフォルト出力フォルダ",
        value=config.get("General", "default_output_dir", fallback=""), # Use config directly
        read_only=True,
        text_size=14, # Increase size
        expand=True,
    )

    # The select_default_output_dir function is removed.
    # Logic will be handled in main.py via handle_default_output_dir_picked

    select_default_output_dir_button = ft.IconButton(
        icon=ft.Icons.FOLDER_OPEN_OUTLINED, # Use ft.Icons (alternative)
        tooltip="デフォルト出力フォルダを選択",
        on_click=lambda _: (
            set_picker_action_callback('select_default_output'), # Set context before picking
            file_picker.get_directory_path(dialog_title="デフォルト出力フォルダを選択")
        )
    )

    default_language_dropdown = ft.Dropdown(
        label="デフォルト言語",
        value=config.get("General", "default_language", fallback="ja"),
        text_size=14, # Increase size
        options=[
            ft.dropdown.Option("ja", "日本語 (Japanese)"),
            ft.dropdown.Option("en", "英語 (English)"),
            ft.dropdown.Option("zh", "中国語 (Chinese)"),
            ft.dropdown.Option("ko", "韓国語 (Korean)"),
            # 必要に応じて他の言語を追加
        ],
        on_change=lambda e: config.set("General", "default_language", e.control.value) and config.save()
    )

    # --- モデルタブ ---
    model_path_textfield = ft.TextField(
        label="モデルパス (設定値)", # ラベル変更: 自動検出ではないため
        value=config.get('Model', 'model_path', fallback='N/A'), # 正しい取得方法に変更
        read_only=True,
        expand=True,
        text_size=14 # Increase size
    )
    # TODO: デバイス検出ロジックを core に移し、結果を表示する -> DONE (Passed via parameter)
    detected_device_textfield = ft.TextField(
        label="検出デバイス (自動)",
        value=detected_device_str, # Use the passed value
        read_only=True,
        text_size=14 # Increase size
    )
    # SRT/VTTチェックボックスは仕様変更により削除 (2025-04-05)

    # --- タブコンテンツの構築 (Card を使用) ---
    general_settings_card = ft.Card(
        content=ft.Container( # Add padding inside the card
            content=ft.Column(
                [
                    ft.Text("一般設定", style=ft.TextThemeStyle.TITLE_MEDIUM, size=16),
                    ft.Row(
                        [
                            default_output_dir_textfield,
                            select_default_output_dir_button,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    default_language_dropdown,
                ],
                spacing=10
            ),
            padding=15 # 内側の余白
        )
    )

    model_settings_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text("モデル設定", style=ft.TextThemeStyle.TITLE_MEDIUM, size=16),
                    model_path_textfield,
                    detected_device_textfield,
                ],
                spacing=10
            ),
            padding=15
        )
    )

    settings_content = ft.Column(
        [
            general_settings_card,
            model_settings_card,
            # output_settings_card, # Removed 2025-04-07
        ],
        spacing=10, # カード間のスペース
        scroll=ft.ScrollMode.AUTO, # コンテンツが多くなった場合に備えてスクロールを有効化
        width=600 # 中央のカラムに固定幅を設定
    )

    # --- Rowを使って中央揃えと幅制限を実現 ---
    settings_layout_row = ft.Row(
        [
            ft.Container(expand=True), # 左側のスペーサー
            settings_content,          # 中央のコンテンツカラム (幅600)
            ft.Container(expand=True), # 右側のスペーサー
        ],
        vertical_alignment=ft.CrossAxisAlignment.START # 上揃えにする
    )

    # Return the main layout Row and the Ref to the text field
    return settings_layout_row, default_output_dir_textfield_ref
