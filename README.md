# 🛒 Amazon Japan QA Automation Study
### Personal Practice Project for Learning Software Testing

---

## 📝 Project Overview (プロジェクト概要)

This is a **personal study project** to learn the basics of QA Automation. I chose **Amazon Japan (amazon.co.jp)** as my target to practice real-world testing scenarios and improve my automation skills using Python and Selenium.
> このプロジェクトは、QA自動化の基礎を学ぶための**個人学習プロジェクト**です。実務に近いテストシナリオを練習し、PythonとSeleniumを用いた自動化スキルを向上させるため、**Amazon Japan**をターゲットに選んでいます。

Through this project, I am focusing on writing organized code by practicing the **Page Object Model (POM)**, which is essential for professional QA engineering.
> プロのQAエンジニアに欠かせない「整理されたコード」を書く練習として、**Page Object Model (POM)** の採用に挑戦しています。

---

## 🚀 What I am Practicing (学習内容)

### 1. Web Automation Basics
I am learning how to interact with web elements and verify search results. I practiced implementing sorting logic (Price: Low to High) to ensure data accuracy.
> Web要素の操作や検索結果の検証方法を学んでいます。データの正確性を保証するため、「価格の低い順」のソートロジックの実装を練習しました。

### 2. Generating Test Evidence
To understand professional reporting, I am using `openpyxl` to automatically save test results into **Excel** files.
> 実務的な報告プロセスを理解するため、`openpyxl` を活用してテスト結果を **Excel** 形式で自動保存する機能を実装しています。

### 3. Improving Test Stability
I am learning how to use **WebDriverWait** to handle dynamic web pages and make my test scripts more reliable.
> 動的なページに対応し、テストの安定性を高めるために **WebDriverWait** の適切な使い方を学習しています。

---

## 🛠 Tech Stack (技術スタック)

- **Language:** Python 3.14
- **Automation:** Selenium WebDriver (Chrome)
- **Framework:** Pytest (Learning in progress)
- **Excel Library:** openpyxl
- **IDE:** PyCharm

---

## 🙋‍♂️ About Me (自己紹介)

I am an aspiring QA Engineer with a strong passion for software quality.
> ソフトウェアの品質向上に強い情熱を持っているQAエンジニア志望です。

<div align="center">
  <img src="images/lebanon_deployment.jpg" width="450" title="Lebanon Deployment">
  <br>
  <p><i>"Discipline and Precision: Experience as a UN Peacekeeper in Lebanon"</i></p>
  <p><b>「レバノン派兵を通じて学んだ『規律』と『エラーを許さない責任感』。<br>その精神を現在はQAエンジニアとして、ソフトウェアの品質管理に注いでいます。」</b></p>
</div>

<br>

- 📍 **Status:** Relocating to **Hachioji, Japan** on **January 29, 2026** for a Working Holiday.
  > **2026年1月29日より日本・八王子に居住予定** (ワーキングホリデー)
- 📖 **Studying:** Preparing for the **JSTQB Foundation Level** certification.
  > **JSTQB Foundation Level** の取得に向けて勉強中
- 🎯 **Goal:** To grow into a reliable QA Engineer in the Japanese IT industry.
  > 日本のIT現場で信頼されるQAエンジニアへの成長を目指しています

---

## 🏗 Project Structure (プロジェクト構造)

```text
.
├── pages/             # Page Object Classes (Elements & Actions)
├── tests/             # Test Scenarios
├── utilities/         # Helper functions (Excel, etc.)
├── reports/           # Test Evidence (Excel, Screenshots)
└── README.md          # Documentation