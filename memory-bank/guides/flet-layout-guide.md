# Fletの最新レイアウトガイド

## 目次
- [はじめに](#はじめに)
- [基本的なレイアウトコントロール](#基本的なレイアウトコントロール)
  - [Row](#row)
  - [Column](#column)
  - [Container](#container)
  - [Stack](#stack)
- [高度なレイアウトコントロール](#高度なレイアウトコントロール)
  - [ResponsiveRow](#responsiverow)
  - [GridView](#gridview)
  - [ListView](#listview)
  - [Tabs](#tabs)
  - [ExpansionPanel](#expansionpanel)
  - [ExpansionTile](#expansiontile)
- [レイアウトのプロパティ](#レイアウトのプロパティ)
  - [alignment](#alignment)
  - [expand](#expand)
  - [padding と margin](#padding-と-margin)
  - [spacing](#spacing)
- [レスポンシブデザイン](#レスポンシブデザイン)
- [レイアウトの例](#レイアウトの例)

## はじめに

Fletは、Pythonでクロスプラットフォームのアプリケーションを簡単に構築できるフレームワークです。このドキュメントでは、Fletの公式ドキュメントに基づいて、レイアウト関連のコントロールとプロパティについて説明します。

## 基本的なレイアウトコントロール

### Row

`Row`は子コントロールを水平方向に配置するコンテナコントロールです。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.Text("テキスト1"),
                ft.Text("テキスト2"),
                ft.Text("テキスト3"),
            ]
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: 子コントロールのリスト
- `alignment`: 水平方向の配置（`MainAxisAlignment.START`, `CENTER`, `END`, `SPACE_BETWEEN`, `SPACE_AROUND`, `SPACE_EVENLY`）
- `vertical_alignment`: 垂直方向の配置（`CrossAxisAlignment.START`, `CENTER`, `END`, `STRETCH`）
- `spacing`: 子コントロール間のスペース（デフォルトは10ピクセル）
- `wrap`: コントロールを折り返すかどうか（`True`または`False`）
- `scroll`: スクロール可能にするかどうか（`ScrollMode.AUTO`, `ADAPTIVE`, `ALWAYS`, `HIDDEN`）

### Column

`Column`は子コントロールを垂直方向に配置するコンテナコントロールです。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Column(
            controls=[
                ft.Text("テキスト1"),
                ft.Text("テキスト2"),
                ft.Text("テキスト3"),
            ]
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: 子コントロールのリスト
- `horizontal_alignment`: 水平方向の配置（`CrossAxisAlignment.START`, `CENTER`, `END`, `STRETCH`）
- `alignment`: 垂直方向の配置（`MainAxisAlignment.START`, `CENTER`, `END`, `SPACE_BETWEEN`, `SPACE_AROUND`, `SPACE_EVENLY`）
- `spacing`: 子コントロール間のスペース（デフォルトは10ピクセル）
- `wrap`: コントロールを折り返すかどうか（`True`または`False`）
- `scroll`: スクロール可能にするかどうか（`ScrollMode.AUTO`, `ADAPTIVE`, `ALWAYS`, `HIDDEN`）

### Container

`Container`は単一の子コントロールを装飾し、位置を調整するためのコントロールです。背景色、ボーダー、パディング、マージン、配置などをカスタマイズできます。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Container(
            content=ft.Text("コンテナ内のテキスト"),
            width=200,
            height=100,
            bgcolor=ft.colors.BLUE_100,
            border_radius=10,
            padding=10,
            margin=ft.margin.only(left=20, top=20),
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `content`: 単一の子コントロール
- `width`: 幅
- `height`: 高さ
- `bgcolor`: 背景色
- `border_radius`: 境界線の角の丸み
- `border`: 境界線
- `padding`: 内側のスペース
- `margin`: 外側のスペース
- `alignment`: 子コントロールの配置
- `expand`: コンテナを拡張するかどうか（`True`/`False`または数値）

### Stack

`Stack`は子コントロールを重ねて表示するコンテナコントロールです。リストの最初の要素が一番下に配置され、最後の要素が一番上に配置されます。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Stack(
            controls=[
                ft.Container(width=100, height=100, bgcolor=ft.colors.RED),
                ft.Container(width=80, height=80, bgcolor=ft.colors.BLUE, left=10, top=10),
                ft.Container(width=60, height=60, bgcolor=ft.colors.GREEN, left=20, top=20),
            ]
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: 子コントロールのリスト
- `width`: スタックの幅
- `height`: スタックの高さ

子コントロールのプロパティ:
- `left`: 左からの位置
- `top`: 上からの位置
- `right`: 右からの位置
- `bottom`: 下からの位置

## 高度なレイアウトコントロール

### ResponsiveRow

`ResponsiveRow`はBootstrapのグリッドレイアウトの考え方を取り入れたコントロールです。画面サイズに応じてレイアウトを調整します。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.ResponsiveRow(
            controls=[
                ft.TextField(label="名前", col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                ft.TextField(label="メール", col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                ft.TextField(label="電話", col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
                ft.TextField(label="住所", col={"xs": 12, "sm": 6, "md": 4, "lg": 3}),
            ]
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: 子コントロールのリスト
- `spacing`: 列間のスペース
- `run_spacing`: 行間のスペース

各子コントロールには`col`プロパティを設定して、異なる画面サイズでの列数を指定します:
- `xs`: エクストラスモール（〜600px）
- `sm`: スモール（600px〜960px）
- `md`: ミディアム（960px〜1280px）
- `lg`: ラージ（1280px〜1920px）
- `xl`: エクストララージ（1920px〜）

### GridView

`GridView`は、グリッド形式で子コントロールを表示するスクロール可能なコントロールです。数千のアイテムを扱う大きなリストに最適で、スムーズなスクロールを提供します。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=150,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            controls=[
                ft.Container(bgcolor=ft.colors.AMBER, border_radius=10),
                ft.Container(bgcolor=ft.colors.BLUE, border_radius=10),
                ft.Container(bgcolor=ft.colors.GREEN, border_radius=10),
                # ... 更に多くのコンテナ
            ],
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: 子コントロールのリスト
- `runs_count`: 行または列の数
- `max_extent`: 各アイテムの最大サイズ
- `spacing`: アイテム間の水平方向のスペース
- `run_spacing`: アイテム間の垂直方向のスペース
- `child_aspect_ratio`: 子アイテムのアスペクト比（幅/高さ）
- `padding`: グリッド全体のパディング

### ListView

`ListView`は、スクロール可能な線形リストを表示するコントロールです。大量のアイテム（数千）を扱う場合に、`Column`や`Row`よりも効率的です。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.ListView(
            expand=True,
            spacing=10,
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PERSON),
                    title=ft.Text(f"ユーザー {i}"),
                    subtitle=ft.Text(f"ユーザー {i} の説明"),
                )
                for i in range(1, 51)
            ],
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: 子コントロールのリスト
- `spacing`: アイテム間のスペース
- `padding`: リスト全体のパディング
- `divider_thickness`: 区切り線の太さ
- `auto_scroll`: 新しいアイテムが追加されたときに自動スクロールするかどうか

### Tabs

`Tabs`は、タブインターフェースを作成するためのコントロールです。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(
                    text="タブ1",
                    content=ft.Container(
                        content=ft.Text("タブ1の内容"),
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="タブ2",
                    content=ft.Container(
                        content=ft.Text("タブ2の内容"),
                        padding=10,
                    ),
                ),
                ft.Tab(
                    text="タブ3",
                    content=ft.Container(
                        content=ft.Text("タブ3の内容"),
                        padding=10,
                    ),
                ),
            ],
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `tabs`: `Tab`コントロールのリスト
- `selected_index`: 選択されているタブのインデックス
- `on_change`: タブが変更されたときに呼び出されるコールバック

### ExpansionPanel

`ExpansionPanel`は、折りたたみ可能なパネルを作成するためのコントロールです。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.ExpansionPanelList(
            controls=[
                ft.ExpansionPanel(
                    expanded=True,
                    header=ft.ListTile(title=ft.Text("パネル1")),
                    content=ft.Container(
                        content=ft.Text("パネル1の内容"),
                        padding=10,
                    ),
                ),
                ft.ExpansionPanel(
                    expanded=False,
                    header=ft.ListTile(title=ft.Text("パネル2")),
                    content=ft.Container(
                        content=ft.Text("パネル2の内容"),
                        padding=10,
                    ),
                ),
            ],
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `controls`: `ExpansionPanel`コントロールのリスト
- `expanded`: パネルが展開されているかどうか
- `header`: パネルのヘッダー部分
- `content`: パネルの内容部分

### ExpansionTile

`ExpansionTile`は、`ListTile`を拡張した展開可能なタイルコントロールです。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.ExpansionTile(
            title=ft.Text("展開可能なタイル"),
            subtitle=ft.Text("タップして展開"),
            controls=[
                ft.ListTile(title=ft.Text("アイテム1")),
                ft.ListTile(title=ft.Text("アイテム2")),
                ft.ListTile(title=ft.Text("アイテム3")),
            ],
        )
    )

ft.app(target=main)
```

主なプロパティ:
- `title`: タイルのタイトル
- `subtitle`: タイルのサブタイトル
- `controls`: 展開時に表示される子コントロールのリスト
- `initially_expanded`: 初期状態で展開されているかどうか

## レイアウトのプロパティ

### alignment

`alignment`プロパティは、コンテナ内の子コントロールの配置を制御します。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Container(
            content=ft.Text("中央揃え"),
            width=200,
            height=200,
            bgcolor=ft.colors.AMBER,
            alignment=ft.alignment.center,
        )
    )

ft.app(target=main)
```

利用可能な`alignment`値:
- `center`: 中央
- `center_left`: 左中央
- `center_right`: 右中央
- `top_center`: 上中央
- `top_left`: 左上
- `top_right`: 右上
- `bottom_center`: 下中央
- `bottom_left`: 左下
- `bottom_right`: 右下

### expand

`expand`プロパティは、コントロールが利用可能なスペースをどのように拡張するかを制御します。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text("展開なし"),
                    bgcolor=ft.colors.RED,
                    padding=10,
                ),
                ft.Container(
                    content=ft.Text("展開あり"),
                    bgcolor=ft.colors.GREEN,
                    padding=10,
                    expand=True,
                ),
                ft.Container(
                    content=ft.Text("展開なし"),
                    bgcolor=ft.colors.BLUE,
                    padding=10,
                ),
            ]
        )
    )

ft.app(target=main)
```

- `expand=True`: コントロールは利用可能なスペースを埋めるように拡張します
- `expand=1`、`expand=2`など: 複数のコントロールがある場合、拡張比率を指定します

### padding と margin

`padding`と`margin`プロパティは、コントロールの内部および外部のスペースを制御します。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Container(
            content=ft.Text("パディングとマージンの例"),
            bgcolor=ft.colors.AMBER,
            padding=ft.padding.all(20),
            margin=ft.margin.only(left=10, top=10, right=10, bottom=10),
        )
    )

ft.app(target=main)
```

パディングとマージンの指定方法:
- `all(値)`: すべての辺に同じ値を設定
- `only(left=値, top=値, right=値, bottom=値)`: 各辺に個別の値を設定
- `symmetric(vertical=値, horizontal=値)`: 垂直方向と水平方向に対称的な値を設定

### spacing

`spacing`プロパティは、`Row`や`Column`内の子コントロール間のスペースを制御します。デフォルト値は10バーチャルピクセルです。

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Column(
            controls=[
                ft.Text("アイテム1"),
                ft.Text("アイテム2"),
                ft.Text("アイテム3"),
            ],
            spacing=20,  # デフォルトの2倍のスペース
        )
    )

ft.app(target=main)
```

`spacing`は、`alignment`が`MainAxisAlignment.START`、`MainAxisAlignment.END`、または`MainAxisAlignment.CENTER`に設定されている場合にのみ適用されます。

## レスポンシブデザイン

Fletでは、`ResponsiveRow`コントロールや`page.on_resize`イベントを使用して、異なる画面サイズに対応するアプリケーションを作成できます。

```python
import flet as ft

def main(page: ft.Page):
    def on_resize(e):
        # 画面幅に基づいてレイアウトを変更
        if page.width < 600:
            # モバイルレイアウト
            row.visible = False
            column.visible = True
        else:
            # デスクトップレイアウト
            row.visible = True
            column.visible = False
        page.update()

    # モバイル用レイアウト
    column = ft.Column(
        controls=[
            ft.Container(content=ft.Text("ヘッダー"), bgcolor=ft.colors.BLUE, padding=10),
            ft.Container(content=ft.Text("コンテンツ"), bgcolor=ft.colors.GREEN, padding=10, expand=True),
            ft.Container(content=ft.Text("フッター"), bgcolor=ft.colors.BLUE, padding=10),
        ],
        visible=False,
        expand=True,
    )

    # デスクトップ用レイアウト
    row = ft.Row(
        controls=[
            ft.Container(content=ft.Text("サイドバー"), bgcolor=ft.colors.BLUE, padding=10, width=200),
            ft.VerticalDivider(),
            ft.Container(content=ft.Text("メインコンテンツ"), bgcolor=ft.colors.GREEN, padding=10, expand=True),
        ],
        visible=True,
        expand=True,
    )

    page.on_resize = on_resize
    page.add(row, column)
    # 初期表示の設定
    on_resize(None)

ft.app(target=main)
```

また、`ResponsiveRow`を使用した例:

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.ResponsiveRow(
            controls=[
                # xs（モバイル）: 全幅、sm（タブレット）以上: 半分の幅
                ft.Container(
                    content=ft.Text("カード1"),
                    bgcolor=ft.colors.AMBER,
                    padding=20,
                    col={"xs": 12, "sm": 6, "md": 4},
                ),
                ft.Container(
                    content=ft.Text("カード2"),
                    bgcolor=ft.colors.BLUE,
                    padding=20,
                    col={"xs": 12, "sm": 6, "md": 4},
                ),
                ft.Container(
                    content=ft.Text("カード3"),
                    bgcolor=ft.colors.GREEN,
                    padding=20,
                    col={"xs": 12, "sm": 6, "md": 4},
                ),
            ],
        )
    )

ft.app(target=main)
```

## レイアウトの例

### 基本的なアプリレイアウト

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Fletアプリの例"
    
    # アプリバー
    appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.MENU),
        leading_width=40,
        title=ft.Text("Fletアプリ"),
        center_title=False,
        bgcolor=ft.colors.BLUE,
        actions=[
            ft.IconButton(ft.icons.SEARCH),
            ft.IconButton(ft.icons.SETTINGS),
        ],
    )
    
    # サイドバー
    sidebar = ft.Container(
        content=ft.Column(
            controls=[
                ft.ListTile(
                    leading=ft.Icon(ft.icons.HOME),
                    title=ft.Text("ホーム"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.PERSON),
                    title=ft.Text("プロフィール"),
                ),
                ft.ListTile(
                    leading=ft.Icon(ft.icons.SETTINGS),
                    title=ft.Text("設定"),
                ),
            ]
        ),
        width=200,
        bgcolor=ft.colors.BLUE_50,
        padding=10,
    )
    
    # メインコンテンツ
    main_content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text("メインコンテンツ", size=20),
                ft.ElevatedButton(text="ボタン"),
            ],
            expand=True,
        ),
        expand=True,
        padding=20,
    )
    
    # レイアウト構築
    page.add(
        appbar,
        ft.Row(
            controls=[
                sidebar,
                ft.VerticalDivider(width=1),
                main_content,
            ],
            expand=True,
        ),
    )

ft.app(target=main)
```

### レスポンシブダッシュボードレイアウト

```python
import flet as ft

def main(page: ft.Page):
    page.title = "ダッシュボード例"
    
    # レスポンシブカードを作成する関数
    def create_card(title, value, color, progress):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(title, weight=ft.FontWeight.BOLD),
                    ft.Text(value, size=20),
                    ft.ProgressBar(value=progress, bgcolor=color),
                ],
                spacing=10,
            ),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            border=ft.border.all(1, ft.colors.GREY_300),
            col={"xs": 12, "sm": 6, "md": 4},
        )
    
    # ダッシュボードレイアウト
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("ダッシュボード", size=30, weight=ft.FontWeight.BOLD),
                    
                    # メトリックカード
                    ft.ResponsiveRow(
                        controls=[
                            create_card("売上", "¥1,234,567", ft.colors.BLUE_100, 0.7),
                            create_card("ユーザー", "45,678", ft.colors.GREEN_100, 0.5),
                            create_card("注文", "1,234", ft.colors.AMBER_100, 0.3),
                        ],
                        spacing=10,
                    ),
                    
                    # データテーブル
                    ft.Container(
                        content=ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("ID")),
                                ft.DataColumn(ft.Text("名前")),
                                ft.DataColumn(ft.Text("ステータス")),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("1")),
                                        ft.DataCell(ft.Text("山田太郎")),
                                        ft.DataCell(ft.Text("アクティブ")),
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("2")),
                                        ft.DataCell(ft.Text("佐藤花子")),
                                        ft.DataCell(ft.Text("休止中")),
                                    ],
                                ),
                            ],
                        ),
                        padding=20,
                        border_radius=10,
                        bgcolor=ft.colors.WHITE,
                        border=ft.border.all(1, ft.colors.GREY_300),
                    ),
                ],
                spacing=20,
            ),
            padding=20,
            bgcolor=ft.colors.GREY_100,
            expand=True,
        )
    )

ft.app(target=main)
```

これらの例を通じて、Fletを使ったレイアウトの基本的な概念と実装方法を示しました。ご自身のプロジェクトに合わせてカスタマイズしてください。
