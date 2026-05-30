from pathlib import Path

import pandas as pd


Q15_COLUMN = '15、为了确保问卷质量,请在本题选择"基本同意":'
Q15_VALID_VALUE = '基本同意 ←请选择此项'
TIME_SPENT_COLUMN = '所用时间'
Q6_COLUMN = '6、 如果学院允许以 "实践成果 "替代传统学位论文 ,您最愿意选择以下哪种形式?(请选择最多3项并排序 ,1=最愿意，2=次选。3=第三选)'
MULTI_CHOICE_COLUMNS = [
	'3、您在实习/实践中是否产出过以下材料?（请根据实际产出选择，可多选，最多3项）',
	'7、 您选择上述类型的主要原因是:(最多选3项)',
	'8、 您认为以下哪些实践成果不适合作为学位论文的替代形式?(多选，最多选3个)',
	'11、您目前最担心的问题是:(最多选3项)',
	'12、您希望学院在制定"实践成果分类标准"时,应重点考虑哪些因素?(最多选3项)',
	'13、您希望学院提供哪些支持工具?(多选，最多选3个)',
]


def split_pipe_values(series: pd.Series) -> pd.Series:
	return series.fillna("").astype(str).str.split("┋")


def build_q6_ranked(df: pd.DataFrame) -> pd.DataFrame:
	ranked = df[["序号", Q6_COLUMN]].copy()
	parts = ranked[Q6_COLUMN].fillna("").astype(str).str.split("→", n=2, expand=True)
	ranked["Q6_第1选"] = parts[0].str.strip()
	ranked["Q6_第2选"] = parts[1].fillna("").str.strip()
	ranked["Q6_第3选"] = parts[2].fillna("").str.strip()
	return ranked


def build_multi_choice_binary(df: pd.DataFrame) -> pd.DataFrame:
	binary_frames = [df[["序号"]].copy()]
	for column in MULTI_CHOICE_COLUMNS:
		options = split_pipe_values(df[column]).apply(
			lambda items: [item.strip() for item in items if item and item.strip()]
		)
		exploded = options.explode()
		if exploded.dropna().empty:
			continue
		dummies = pd.crosstab(exploded.index, exploded)
		dummies = dummies.reindex(df.index, fill_value=0)
		dummies.columns = [f"{column}__{option}" for option in dummies.columns]
		binary_frames.append(dummies.reset_index(drop=True))
	return pd.concat(binary_frames, axis=1)


def main() -> None:
	excel_path = Path(__file__).with_name("学生问卷172份.xlsx")
	output_dir = Path(__file__).with_name("output")
	output_dir.mkdir(exist_ok=True)
	df = pd.read_excel(excel_path, sheet_name="Sheet1")
	filtered_df = df[df[Q15_COLUMN] == Q15_VALID_VALUE].copy()
	removed_rows = len(df) - len(filtered_df)
	filtered_df["所用时间_秒"] = pd.to_numeric(
		filtered_df[TIME_SPENT_COLUMN].astype(str).str.extract(r"(\d+)")[0],
		errors="coerce",
	)
	q6_ranked_df = build_q6_ranked(filtered_df)
	multi_choice_binary_df = build_multi_choice_binary(filtered_df)
	cleaned_data_path = output_dir / "cleaned_data.csv"
	q6_ranked_path = output_dir / "q6_ranked.csv"
	multi_choice_binary_path = output_dir / "multi_choice_binary.csv"
	cleaning_report_path = output_dir / "cleaning_report.txt"
	filtered_df.to_csv(cleaned_data_path, index=False, encoding="utf-8-sig")
	q6_ranked_df.to_csv(q6_ranked_path, index=False, encoding="utf-8-sig")
	multi_choice_binary_df.to_csv(multi_choice_binary_path, index=False, encoding="utf-8-sig")
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
	print("服务交付目标: 为后续数据质量检查与一致性校验提供数值型输入")
	print(f"原列名: {TIME_SPENT_COLUMN}")
	print("新增数值列: 所用时间_秒")
	print(f"成功转为数字的行数: {filtered_df['所用时间_秒'].notna().sum()}")
	print(f"转换失败的行数: {filtered_df['所用时间_秒'].isna().sum()}")
	print("转换后前5个值:")
	print(filtered_df["所用时间_秒"].head().tolist())
	print()
	print(f"{cleaned_data_path} 已保存")
	print(f"{q6_ranked_path} 已保存")
	print(f"{multi_choice_binary_path} 已保存")
	print(f"{cleaning_report_path} 已保存")


if __name__ == "__main__":
	main()