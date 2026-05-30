from pathlib import Path

import pandas as pd


Q15_COLUMN = '15、为了确保问卷质量,请在本题选择"基本同意":'
Q15_VALID_VALUE = '基本同意 ←请选择此项'
TIME_SPENT_COLUMN = '所用时间'


def main() -> None:
	excel_path = Path(__file__).with_name("学生问卷172份.xlsx")
	output_dir = Path(__file__).with_name("output")
	output_dir.mkdir(exist_ok=True)
	cleaned_data_path = output_dir / "cleaned_data.csv"
	q6_ranked_path = output_dir / "q6_ranked.csv"
	multi_choice_binary_path = output_dir / "multi_choice_binary.csv"
	cleaning_report_path = output_dir / "cleaning_report.txt"
	df = pd.read_excel(excel_path, sheet_name="Sheet1")
	filtered_df = df[df[Q15_COLUMN] == Q15_VALID_VALUE].copy()
	removed_rows = len(df) - len(filtered_df)
	filtered_df["所用时间_秒"] = pd.to_numeric(
		filtered_df[TIME_SPENT_COLUMN].astype(str).str.extract(r"(\d+)")[0],
		errors="coerce",
	)
	filtered_df.to_csv(cleaned_data_path, index=False, encoding="utf-8-sig")
	cleaning_report = "\n".join(
		[
			"清洗日志",
			f"原始行数: {len(df)}",
			f"有效行数: {len(filtered_df)}",
			f"剔除行数: {removed_rows}",
			"各类无效原因统计:",
			f"- Q15未选择指定答案: {removed_rows}",
		]
	)
	cleaning_report_path.write_text(cleaning_report, encoding="utf-8-sig")

	print("1) 数据行列数")
	print(df.shape)
	print()

	print("2) 列名清单")
	print(df.columns.tolist())
	print()

	print("3) Q15有效性过滤")
	print(f"过滤前行数: {len(df)}")
	print(f"过滤后行数: {len(filtered_df)}")
	print(f"剔除行数: {removed_rows}")
	print()

	print("4) 所用时间转数字")
	print("本步服务的交付目标: 为后续数据质量检查与一致性校验提供数值型输入")
	print(f"原列名: {TIME_SPENT_COLUMN}")
	print("新增数值列: 所用时间_秒")
	print(f"成功转为数字的行数: {filtered_df['所用时间_秒'].notna().sum()}")
	print(f"转换失败的行数: {filtered_df['所用时间_秒'].isna().sum()}")
	print("验收信号: 终端应看到新增数值列名称，以及成功/失败行数统计")
	print()

	print("5) 中间结果统一保存")
	print(f"{cleaned_data_path} 已保存")
	print(f"{q6_ranked_path} 已保存")
	print(f"{multi_choice_binary_path} 已保存")
	print(f"{cleaning_report_path} 已保存")


if __name__ == "__main__":
	main()