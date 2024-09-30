# VSS-Lib: 車両信号仕様ライブラリ

[日本語](./lang/jp/README.md), [简体中文](./lang/zh/README.md), [한국어](./lang/ko/README.md), [Português](./lang/pt_BR/README.md), [Français](./lang/fr/README.md), [Italiano](./lang/it/README.md), [Español](./lang/es/README.md), [עִברִית](./lang/he/README.md), [English](https://github.com/autosd-vss-mw/vss-lib/)

[COVESA (Connected Vehicle Systems Alliance)](https://covesa.global/) と [その仕様](https://covesa.github.io/vehicle_signal_specification/) に基づいたPythonライブラリです。

VSS-Libは、車両信号仕様（VSS）に従って車両信号と対話するために設計されたミドルウェアPythonライブラリおよびD-Busサービスと見なされます。ベンダー固有のモデルをサポートしており、ランダムまたはリアルタイムのハードウェア信号をD-Busインターフェースに送信できます。また、このライブラリは、電子ベンダーを車両モデルに接続することも可能です。ご注意ください。ここで提供されているVSSデータは、あくまで例であり、ベンダーやサプライヤーから提供された実際のデータではありません。

# 目次

1. [VSS-Lib: 車両信号仕様ライブラリ](#vss-lib-車両信号仕様ライブラリ)
2. [特徴](#特徴)
3. [VSS-Libの利点](#vss-libの利点)
4. [要件](#要件)
5. [インストール](#インストール)
   - [ステップ1: リポジトリをクローンする](#ステップ1-リポジトリをクローンする)
   - [ステップ2: Python依存関係をインストールする](#ステップ2-python依存関係をインストールする)
   - [ステップ3: ライブラリをインストールする](#ステップ3-ライブラリをインストールする)
   - [ステップ4: Systemdサービスをインストールする](#ステップ4-systemdサービスをインストールする)
   - [ステップ5: VSSパスを設定する](#ステップ5-vssパスを設定する)
6. [D-Busインターフェース上で信号を監視する](#d-busインターフェース上で信号を監視する)
7. [ハードウェア信号を送信する](#ハードウェア信号を送信する)
8. [アンインストール](#アンインストール)
9. [Makefile](#makefile)
10. [貢献](#貢献)
11. [ライセンス](#ライセンス)

## 特徴

- QM、ASIL、またはUserPreferenceに基づいてランダムな車両信号を発信。
- ベアメタルデバイスからリアルタイムのハードウェア信号を処理。
- シミュレーションのために電子ベンダーを車両モデルに接続可能。
- D-Busで車両信号データを監視。

## VSS-Libの利点

### 1. **標準化と相互運用性**
   - **VSS-Lib**は、異なるベンダー間で車両信号を定義および管理するための標準化されたフレームワークを提供し、エコシステム内でのデータの共有、解釈、交換を容易にします。
   - 標準化されたアプローチにより、ベンダーは他のシステムとの連携を円滑に進めることができます。

### 2. **時間とコストの効率化**
   - 車両信号を処理するための独自ソフトウェアの開発は、コストがかかり、時間がかかります。**VSS-Lib**を使用することで、ベンダーは既存のソリューションを活用し、自社製品の他のコア部分に集中することができます。
   - **VSS-Lib**は、信号管理のための事前構築された機能を提供しており、ベンダーが一から開発する必要を減らします。

### 3. **業界動向に準拠**
   - **VSS-Lib**は、**COVESA VSS**のような業界の取り組みに準拠しており、ベンダーが業界標準に沿った運営を行えるようサポートします。
   - ベンダーは、データ共有や信号管理に関する規制要件が増加する中で、**VSS-Lib**を活用して準拠を維持できます。

### 4. **モジュール性と拡張性**
   - **VSS-Lib**はモジュール化されており、ベンダーは自社のニーズに応じてカスタマイズおよび拡張できます。
   - ベンダーは、自社固有の信号、プロトコル、データ構造を簡単に接続でき、標準化された構造の恩恵を受けられます。

### 5. **ベンダー間の協力が容易に**
   - 異なる電子機器や自動車のベンダーが協力する際、**VSS-Lib**を使用することで、複数のサプライヤーからの電子機器を統合する際の協力がスムーズになります。

### 6. **将来を見据えた設計**
   - **VSS-Lib**は、技術や規制の将来的な変化に対応できるように設計されています。ベンダーは、信号規格や要件の変化に対応するために**VSS-Lib**コミュニティに依存できます。

### 7. **オープンソースコミュニティとサポート**
   - **VSS-Lib**は、絶え間ない開発、改善、コミュニティのサポートを受けており、バグ修正や機能強化が迅速に行われます。

### 8. **業界全体での互換性**
   - **VSS-Lib**は、自動車、航空宇宙、医療機器、ドローンなど、さまざまな業界に適応できる統一構造を提供します。

### 9. **ハードウェアイノベーションに集中**
   - ベンダーは、カスタムソフトウェアを開発することなく、ハードウェアの開発や製品機能の向上に集中でき、**VSS-Lib**を共通の通信層として活用できます。

### 10. **干渉のない統合**
   - **箱から出してすぐに**、実際のデータに基づく干渉のないテストを実行し、ベンダーの仕様に基づく日々のテストが可能です。

その他にも多数の利点があります...

## 要件

- Python 3.10+
- D-Busとの連携のための`pydbus`
- `pyyaml`
- `toml`
- `invoke`
- D-Busサービス管理用のSystemd

## インストール

### ステップ1: リポジトリをクローン

```bash
git clone https://github.com/your-username/vss-lib.git
cd vss-lib
```

### ステップ2: Pythonの依存関係をインストール

Python 3.10+がインストールされていることを確認してください。依存関係を管理するために仮想環境を作成できます：

```bash
python3 -m venv venv
source venv/bin/activate
```

### ステップ3: ライブラリをインストール

ライブラリとVSS D-Busデモサービスをインストールします：

```bash
sudo pip install .
sudo systemctl daemon-reload
sudo systemctl enable vss-dbus.service
sudo systemctl start vss-dbus.service
sudo journalctl -u vss-dbus.service -f # デプロイの監視
sudo dbus-monitor --system "interface=com.vss_lib.VehicleSignals" # 送信されているすべての信号を確認
```

FedoraやCentOSの上で車両メーカーのベンダーやパートナーがVehicle Signal Specification (VSS) プロトコルで「通信」する様子を監視します：

```bash
sudo dbus-monitor --system "interface=com.vss_lib.VehicleSignals"

signal time=1725863086.478979 sender=:1.9701 -> destination=(null destination) serial=184 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Electronics.Bosch.ParkingSensorStatus.max"
   double 1.88863
signal time=1725863088.478907 sender=:1.9701 -> destination=(null destination) serial=185 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Speed.min"
   double 49.5526
signal time=1725863090.479247 sender=:1.9701 -> destination=(null destination) serial=186 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "BrakeFluidLevel.datatype"
   double 48.5111
signal time=1725863092.480390 sender=:1.9701 -> destination=(null destination) serial=187 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Electronics.Renesas.NavigationAccuracy.datatype"
   double 11.383
signal time=1725863094.479111 sender=:1.9701 -> destination=(null destination) serial=188 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Speed.unit"
   double 47.296
signal time=1725863096.479761 sender=:1.9701 -> destination=(null destination) serial=189 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=SignalEmitted
   string "Electronics.Renesas.NavigationAccuracy.unit"
   double 6.26474
```

(別のターミナルで、ASILとQM信号をVSS D-Busマネージャーデモに送信しているコンテナを確認します):

```bash
vss-lib (main) $ sudo podman ps
[sudo] password for douglas:
CONTAINER ID  IMAGE                                COMMAND               CREATED             STATUS             PORTS       NAMES
9a5937f3a82f                                       /sbin/init            54 minutes ago      Up 54 minutes                  qm
b5659436d457  localhost/toyota_vss_image:latest    sh -c /usr/lib/py...  About a minute ago  Up About a minute              toyota_vss_container
e62bf9a0e121  localhost/bmw_vss_image:latest       sh -c /usr/lib/py...  About a minute ago  Up About a minute              bmw_vss_container
866ad65b24b9  localhost/ford_vss_image:latest      sh -c /usr/lib/py...  About a minute ago  Up About a minute              ford_vss_container
387283dc83e8  localhost/honda_vss_image:latest     sh -c /usr/lib/py...  About a minute ago  Up About a minute              honda_vss_container
1e7cbb90f017  localhost/jaguar_vss_image:latest    sh -c /usr/lib/py...  About a minute ago  Up About a minute              jaguar_vss_container
212b103ffd6a  localhost/mercedes_vss_image:latest  sh -c /usr/lib/py...  About a minute ago  Up About a minute              mercedes_vss_container
161f79e61eb7  localhost/volvo_vss_image:latest     sh -c /usr/lib/py...  About a minute ago  Up About a minute              volvo_vss_container
```

### ステップ4: Systemdサービスをインストール

D-Busサービスを有効にして起動するために、以下の手順を実行します：

1. systemdサービスファイルを適切なディレクトリにコピーします：

```bash
sudo cp systemd/vss-dbus.service /etc/systemd/system/
```

2. systemdデーモンをリロードします：

```bash
sudo systemctl daemon-reload
```

3. 起動時にD-Busサービスが開始するように設定します：

```bash
sudo systemctl enable vss-dbus.service
```

4. サービスを開始します：

```bash
sudo systemctl start vss-dbus.service
```

5. サービスの状態を確認します：

```bash
sudo systemctl status vss-dbus.service
```

### ステップ5: VSSパスの設定

ベンダー固有のVSSファイルへのパスが設定されていることを確認してください。設定ファイルは`/etc/vss/vss.config`です。

設定例：

```ini
[global]
vspec_path=/usr/share/vss-lib/

[vehicle_toyota]
vspec_file=${vspec_path}toyota.vspec

[vehicle_bmw]
vspec_file=${vspec_path}bmw.vspec
```

## D-Busインターフェースで信号を監視

D-Busサービスが起動している場合、`dbus-monitor`を使用して、VSS D-Busサービスによって送信されるランダム信号をリアルタイムで監視できます。

以下のコマンドを実行します：

```bash
dbus-monitor "interface=com.vss_lib.VehicleSignals"
```

次のように、送信されたランダムな信号が表示されるはずです：

```bash
signal sender=:1.102 -> dest=(null destination) serial=44 path=/com/vss_lib/VehicleSignals; interface=com.vss_lib.VehicleSignals; member=EmitHardwareSignal
   string "Speed"
   double 80.0
```

## ハードウェア信号の送信

Pythonスクリプトからハードウェア信号を送信したい場合、このプロジェクトに含まれているD-Busクライアントを使用できます：

```python
from pydbus import SystemBus

def send_hardware_signal(signal_name, value):
    bus = SystemBus()
    vss_service = bus.get("com.vss_lib.VehicleSignals")
    vss_service.EmitHardwareSignal(signal_name, value)

# 例: スピード信号を80で送信
send_hardware_signal("Speed", 80)
```

## アンインストール

D-Busサービスを停止して無効化するには：

```bash
sudo systemctl stop vss-dbus.service
sudo systemctl disable vss-dbus.service
```

ライブラリをアンインストールしてクリーンアップするには：

```bash
pip uninstall vss-lib
sudo rm /etc/systemd/system/vss-dbus.service
sudo rm /etc/vss/vss.config
```

## Makefile

```bash
$ make help
利用可能なコマンド:
  make                    - Pythonパッケージをインストールする 'make python' のエイリアス
  make python             - 'sudo pip install .' を使ってPythonパッケージをインストール
  make python_uninstall   - 'sudo pip uninstall vss_lib' を使ってPythonパッケージをアンインストール
  make cpython            - PythonファイルをCython（.pyx）に変換し、C拡張機能をビルド
  make cpython_uninstall  - Cythonで生成されたファイルとビルドアーティファクトを削除
  make help               - このヘルプメッセージを表示し、各ターゲットを説明
```

## 貢献

このプロジェクトに貢献したい場合は、イシューを作成するか、プルリクエストを送信してください。

## ライセンス

このプロジェクトはApache License 2.0の下でライセンスされています。詳細については[LICENSE](LICENSE)ファイルを参照してください。
