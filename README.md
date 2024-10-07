
# 校準界面 (CalibraInterface)

## 概述

`CalibraInterface` 是一個基於 Python 的圖形化界面應用程式，用於管理和執行校準測試。該應用使用 `Tkinter` 框架，提供了簡單易用的兩個頁面界面，並且可以透過串口與外部設備進行通信。

## 主要功能

- **兩個頁面**：
  - **PageOne**：用於校準過程的配置或總覽。
  - **PageTwo**：處理測試過程中的某一特定部分。
- **串口通信**：應用程序可以透過串口與校準設備通信，適用於各種設備。
- **圖形界面**：基於 `Tkinter` 的圖形化界面，操作簡單直觀。

## 安裝需求

- Python 3.x
- 需要安裝 `pyserial` 庫進行串口通信：
  ```bash
  pip install pyserial
  ```

## 如何運行

1. 確保已安裝所需的庫。
2. 運行程式：
   ```bash
   python CalibraInterface.py
   ```
3. 程式將啟動，您可以開始與校準設備進行交互。

