from pathlib import Path

import pandas as pd


def main() -> None:
	excel_path = Path(__file__).with_name("学生问卷172份.xlsx")
	df = pd.read_excel(excel_path, sheet_name="Sheet1")

	print("1) 数据行列数")
	print(df.shape)
	print()

	print("2) 列名清单")
	print(df.columns.tolist())
	print()

	print("3) 前5行预览")
	print(df.head())
	print()

	print("4) 每列的数据类型")
	print(df.dtypes)


if __name__ == "__main__":
	main()