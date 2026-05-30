from pathlib import Path
import re
from typing import Optional


import matplotlib
import pandas as pd


matplotlib.use("Agg")

import matplotlib.pyplot as plt


Q6_REQUIRED_COLUMNS = ["Q6_第1选", "Q6_第2选", "Q6_第3选"]
Q1_COLUMN = "1、 您的年级:"
Q2_COLUMN = "2、您是否有企业实习或实践项目经历?"
Q4_COLUMN = "4、您是否了解2025年1月1日实施的《中华人民共和国学位法》关于“硕士专业学位研究生可以通过‘规定的实践成果’代替传统学位论文来申请学位”的政策？"
Q5_COLUMN = "5、 您是否清楚本校MIB对实践成果的具体要求和标准?"
Q9_COLUMNS = [
	'9、您认为评价一份"高质量"实践成果,以下维度的重要性如何?(请在每项后打分,5=非常重要,1=不重要)—问题导向性:针对真实商业问题,问题界定清晰',
	"9、数据支撑度:基于充分的一手或二手数据分析",
	"9、理论应用性:恰当运用国际商务相关理论",
	"9、创新性:在分析视角或解决方案上有创新",
	"9、实践价值:对企业决策或行业发展有参考价值",
	"9、工作量:体现足够的研究和实践工作投入",
	"9、规范性:格式、逻辑、语言表达符合专业规范",
	"9、真实性:基于真实企业/项目,非虚构或纸上谈兵",
	"9、可操作性:提出的方案具备实际可行性",
	"9、团队协作能力:体现跨部门/跨文化协作能力",
]
Q9_SHORT_LABELS = [
	"问题导向性",
	"数据支撑度",
	"理论应用性",
	"创新性",
	"实践价值",
	"工作量",
	"规范性",
	"真实性",
	"可操作性",
	"团队协作",
]
Q10_COLUMNS = [
	"10、如果您的实践成果由多方评价,您认为以下主体的评价各应占多少权重?(总和=100%)—校内学术导师",
	"10、校外企业导师",
	"10、学院专家评审组",
	"10、企业客户/受益方",
	"10、学生自评",
]
Q10_SHORT_LABELS = ["校内学术导师", "校外企业导师", "学院专家评审组", "企业客户/受益方", "学生自评"]
RESPONDENT_ID_COLUMN = "序号"
Q3_PREFIX = "3、您在实习/实践中是否产出过以下材料?（请根据实际产出选择，可多选，最多3项）__"
Q7_PREFIX = "7、 您选择上述类型的主要原因是:(最多选3项)__"
Q8_PREFIX = "8、 您认为以下哪些实践成果不适合作为学位论文的替代形式?(多选，最多选3个)__"
Q11_PREFIX = "11、您目前最担心的问题是:(最多选3项)__"
Q12_PREFIX = "12、您希望学院在制定\"实践成果分类标准\"时,应重点考虑哪些因素?(最多选3项)__"
Q13_PREFIX = "13、您希望学院提供哪些支持工具?(多选，最多选3个)__"


def configure_matplotlib_fonts() -> None:
	plt.rcParams["font.sans-serif"] = [
		"Microsoft YaHei",
		"SimHei",
		"Noto Sans CJK SC",
		"SimSun",
		"Arial Unicode MS",
		"DejaVu Sans",
	]
	plt.rcParams["axes.unicode_minus"] = False


def extract_effective_count(report_text: str) -> Optional[int]:
	match = re.search(r"有效行数:\s*(\d+)", report_text)
	if match is None:
		return None
	return int(match.group(1))


def plot_single_choice_distribution(series: pd.Series, title: str, output_path: Path) -> pd.Series:
	counts = series.dropna().astype(str).value_counts()
	fig, axes = plt.subplots(1, 2, figsize=(12, 5))

	counts.sort_values(ascending=False).plot(kind="bar", ax=axes[0], color="#4C78A8")
	axes[0].set_title(f"{title} 频数")
	axes[0].set_xlabel("选项")
	axes[0].set_ylabel("频数")
	axes[0].tick_params(axis="x", rotation=15)

	axes[1].pie(counts.values, labels=counts.index.tolist(), autopct="%1.1f%%", startangle=90)
	axes[1].set_title(f"{title} 占比")

	fig.tight_layout()
	fig.savefig(output_path, dpi=200, bbox_inches="tight")
	plt.close(fig)
	return counts


def plot_multi_choice_distribution(
	binary_df: pd.DataFrame,
	prefix: str,
	title: str,
	output_path: Path,
	denominator: int,
) -> pd.DataFrame:
	selected_columns = [column for column in binary_df.columns if column.startswith(prefix)]
	counts = binary_df[selected_columns].sum().sort_values(ascending=True)
	labels = [column.replace(prefix, "", 1) for column in counts.index]
	rates = counts / denominator
	plot_df = pd.DataFrame({"选项": labels, "选择次数": counts.values, "选择率": rates.values})

	fig, ax = plt.subplots(figsize=(12, 6))
	ax.barh(plot_df["选项"], plot_df["选择次数"], color="#59A14F")
	ax.set_title(title)
	ax.set_xlabel("选择次数")
	ax.set_ylabel("选项")

	for index, row in plot_df.iterrows():
		ax.text(row["选择次数"] + 0.5, index, f"{int(row['选择次数'])} ({row['选择率']:.1%})", va="center")

	fig.tight_layout()
	fig.savefig(output_path, dpi=200, bbox_inches="tight")
	plt.close(fig)
	return plot_df.sort_values("选择次数", ascending=False).reset_index(drop=True)


def plot_q6_weighted_scores(q6_df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
	weights = {"Q6_第1选": 3, "Q6_第2选": 2, "Q6_第3选": 1}
	score_frames = []
	for column, weight in weights.items():
		series = q6_df[column].dropna().astype(str).str.strip()
		series = series[series != ""]
		weighted = series.value_counts().mul(weight)
		score_frames.append(weighted)

	total_scores = pd.concat(score_frames, axis=1).fillna(0).sum(axis=1).sort_values(ascending=False)
	plot_df = pd.DataFrame({"成果类型": total_scores.index, "加权偏好得分": total_scores.values})

	fig, ax = plt.subplots(figsize=(12, 6))
	ax.bar(plot_df["成果类型"], plot_df["加权偏好得分"], color="#E15759")
	ax.set_title("Q6 实践成果类型加权偏好得分排名")
	ax.set_xlabel("成果类型")
	ax.set_ylabel("加权偏好得分")
	ax.tick_params(axis="x", rotation=25)

	for index, value in enumerate(plot_df["加权偏好得分"]):
		ax.text(index, value + 0.5, f"{int(value)}", ha="center", va="bottom")

	fig.tight_layout()
	fig.savefig(output_path, dpi=200, bbox_inches="tight")
	plt.close(fig)
	return plot_df


def plot_q9_likert_summary(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
	q9_df = df[Q9_COLUMNS].copy()
	means = q9_df.mean().sort_values(ascending=False)
	mean_labels = [Q9_SHORT_LABELS[Q9_COLUMNS.index(column)] for column in means.index]
	mean_values = means.tolist()

	angles = [index / float(len(mean_values)) * 2 * 3.141592653589793 for index in range(len(mean_values))]
	angles += angles[:1]
	radar_values = mean_values + mean_values[:1]

	fig = plt.figure(figsize=(14, 6))
	radar_ax = fig.add_subplot(1, 2, 1, polar=True)
	box_ax = fig.add_subplot(1, 2, 2)

	radar_ax.plot(angles, radar_values, color="#F28E2B", linewidth=2)
	radar_ax.fill(angles, radar_values, color="#F28E2B", alpha=0.25)
	radar_ax.set_xticks(angles[:-1])
	radar_ax.set_xticklabels(mean_labels)
	radar_ax.set_ylim(0, 5)
	radar_ax.set_title("Q9 均值排名雷达图")

	boxplot_data = [q9_df[column].dropna().tolist() for column in Q9_COLUMNS]
	box_ax.boxplot(boxplot_data, tick_labels=Q9_SHORT_LABELS, patch_artist=True)
	box_ax.set_title("Q9 各维度得分箱线图")
	box_ax.set_ylabel("得分")
	box_ax.set_ylim(0.5, 5.5)
	box_ax.tick_params(axis="x", rotation=25)

	fig.tight_layout()
	fig.savefig(output_path, dpi=200, bbox_inches="tight")
	plt.close(fig)

	return pd.DataFrame({"维度": mean_labels, "均值": mean_values})


def plot_q10_weight_distribution(df: pd.DataFrame, output_path: Path) -> pd.DataFrame:
	q10_df = df[Q10_COLUMNS].copy()
	mean_weights = q10_df.mean()
	plot_df = pd.DataFrame({"评价主体": Q10_SHORT_LABELS, "平均权重": mean_weights.values})

	colors = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2"]
	fig, ax = plt.subplots(figsize=(12, 3))
	left = 0.0
	for index, row in plot_df.iterrows():
		ax.barh(["平均权重分配"], [row["平均权重"]], left=left, color=colors[index], label=row["评价主体"])
		ax.text(left + row["平均权重"] / 2, 0, f"{row['平均权重']:.1f}%", ha="center", va="center", color="white")
		left += row["平均权重"]

	ax.set_xlim(0, 100)
	ax.set_xlabel("平均权重(%)")
	ax.set_title("Q10 平均权重分配")
	ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=3)

	fig.tight_layout()
	fig.savefig(output_path, dpi=200, bbox_inches="tight")
	plt.close(fig)
	return plot_df


def build_single_choice_summary(question_code: str, counts: pd.Series) -> pd.DataFrame:
	total = int(counts.sum())
	summary_df = counts.rename_axis("选项或维度").reset_index(name="统计值")
	summary_df["题号"] = question_code
	summary_df["题型"] = "单选题"
	summary_df["指标名称"] = "频数"
	summary_df["样本数"] = total
	summary_df["选择率"] = summary_df["统计值"] / total if total else 0.0
	summary_df["排序值"] = summary_df["统计值"]
	summary_df["备注"] = "基于非空作答样本"
	return summary_df[["题号", "题型", "指标名称", "选项或维度", "统计值", "样本数", "选择率", "排序值", "备注"]]


def build_multi_choice_summary(question_code: str, summary_df: pd.DataFrame, denominator: int) -> pd.DataFrame:
	result_df = summary_df.copy()
	result_df["题号"] = question_code
	result_df["题型"] = "多选题"
	result_df["指标名称"] = "选择次数"
	result_df["样本数"] = denominator
	result_df["排序值"] = result_df["选择次数"]
	result_df["备注"] = "选择率分母为有效问卷数"
	result_df = result_df.rename(columns={"选项": "选项或维度", "选择次数": "统计值"})
	return result_df[["题号", "题型", "指标名称", "选项或维度", "统计值", "样本数", "选择率", "排序值", "备注"]]


def build_q6_summary(summary_df: pd.DataFrame, respondent_count: int) -> pd.DataFrame:
	result_df = summary_df.copy()
	result_df["题号"] = "Q6"
	result_df["题型"] = "排序题"
	result_df["指标名称"] = "加权偏好得分"
	result_df["样本数"] = respondent_count
	result_df["选择率"] = pd.NA
	result_df["排序值"] = result_df["加权偏好得分"]
	result_df["备注"] = "第1选=3分, 第2选=2分, 第3选=1分"
	result_df = result_df.rename(columns={"成果类型": "选项或维度", "加权偏好得分": "统计值"})
	return result_df[["题号", "题型", "指标名称", "选项或维度", "统计值", "样本数", "选择率", "排序值", "备注"]]


def build_q9_summary(summary_df: pd.DataFrame, respondent_count: int) -> pd.DataFrame:
	result_df = summary_df.copy()
	result_df["题号"] = "Q9"
	result_df["题型"] = "李克特量表"
	result_df["指标名称"] = "均值"
	result_df["样本数"] = respondent_count
	result_df["选择率"] = pd.NA
	result_df["排序值"] = result_df["均值"]
	result_df["备注"] = "量表范围1到5"
	result_df = result_df.rename(columns={"维度": "选项或维度", "均值": "统计值"})
	return result_df[["题号", "题型", "指标名称", "选项或维度", "统计值", "样本数", "选择率", "排序值", "备注"]]


def build_q10_summary(summary_df: pd.DataFrame, respondent_count: int) -> pd.DataFrame:
	result_df = summary_df.copy()
	result_df["题号"] = "Q10"
	result_df["题型"] = "权重分配题"
	result_df["指标名称"] = "平均权重"
	result_df["样本数"] = respondent_count
	result_df["选择率"] = pd.NA
	result_df["排序值"] = result_df["平均权重"]
	result_df["备注"] = "单位为百分比"
	result_df = result_df.rename(columns={"评价主体": "选项或维度", "平均权重": "统计值"})
	return result_df[["题号", "题型", "指标名称", "选项或维度", "统计值", "样本数", "选择率", "排序值", "备注"]]


def build_descriptive_summary(
	q1_counts: pd.Series,
	q2_counts: pd.Series,
	q4_counts: pd.Series,
	q5_counts: pd.Series,
	q3_summary: pd.DataFrame,
	q7_summary: pd.DataFrame,
	q8_summary: pd.DataFrame,
	q11_summary: pd.DataFrame,
	q12_summary: pd.DataFrame,
	q13_summary: pd.DataFrame,
	q6_summary: pd.DataFrame,
	q9_summary: pd.DataFrame,
	q10_summary: pd.DataFrame,
	valid_count: int,
) -> pd.DataFrame:
	summary_frames = [
		build_single_choice_summary("Q1", q1_counts),
		build_single_choice_summary("Q2", q2_counts),
		build_single_choice_summary("Q4", q4_counts),
		build_single_choice_summary("Q5", q5_counts),
		build_multi_choice_summary("Q3", q3_summary, valid_count),
		build_multi_choice_summary("Q7", q7_summary, valid_count),
		build_multi_choice_summary("Q8", q8_summary, valid_count),
		build_multi_choice_summary("Q11", q11_summary, valid_count),
		build_multi_choice_summary("Q12", q12_summary, valid_count),
		build_multi_choice_summary("Q13", q13_summary, valid_count),
		build_q6_summary(q6_summary, valid_count),
		build_q9_summary(q9_summary, valid_count),
		build_q10_summary(q10_summary, valid_count),
	]
	return pd.concat(summary_frames, ignore_index=True)


def main() -> None:
	configure_matplotlib_fonts()

	base_dir = Path(__file__).resolve().parent
	output_dir = base_dir / "output"
	cleaned_data_path = output_dir / "cleaned_data.csv"
	q6_ranked_path = output_dir / "q6_ranked.csv"
	multi_choice_binary_path = output_dir / "multi_choice_binary.csv"
	cleaning_report_path = output_dir / "cleaning_report.txt"
	q1_output_path = output_dir / "desc_q1.png"
	q2_output_path = output_dir / "desc_q2.png"
	q4_output_path = output_dir / "desc_q4.png"
	q5_output_path = output_dir / "desc_q5.png"
	q3_output_path = output_dir / "desc_q3.png"
	q7_output_path = output_dir / "desc_q7.png"
	q8_output_path = output_dir / "desc_q8.png"
	q11_output_path = output_dir / "desc_q11.png"
	q12_output_path = output_dir / "desc_q12.png"
	q13_output_path = output_dir / "desc_q13.png"
	q6_output_path = output_dir / "desc_q6.png"
	q9_output_path = output_dir / "desc_q9.png"
	q10_output_path = output_dir / "desc_q10.png"
	descriptive_summary_path = output_dir / "descriptive_summary.csv"

	cleaned_df = pd.read_csv(cleaned_data_path, encoding="utf-8-sig")
	q6_ranked_df = pd.read_csv(q6_ranked_path, encoding="utf-8-sig")
	multi_choice_binary_df = pd.read_csv(multi_choice_binary_path, encoding="utf-8-sig")
	cleaning_report_text = cleaning_report_path.read_text(encoding="utf-8-sig")
	valid_count = extract_effective_count(cleaning_report_text)
	valid_ids = set(cleaned_df[RESPONDENT_ID_COLUMN].tolist())
	valid_multi_choice_df = multi_choice_binary_df[
		multi_choice_binary_df[RESPONDENT_ID_COLUMN].isin(valid_ids)
	].copy()

	missing_q6_columns = [column for column in Q6_REQUIRED_COLUMNS if column not in q6_ranked_df.columns]

	print("1) 绘图前输入校验")
	print(f"本步输入: {cleaned_data_path}, {q6_ranked_path}, {multi_choice_binary_path}, {cleaning_report_path}")
	print("本步输出文件: 无")
	print("终端验收信号: 应看到4个输入文件读取成功、有效问卷数、Q6三列存在、多选宽表列数大于0")
	print()

	print("输入文件读取结果")
	print(f"- {cleaned_data_path} 读取成功, 行列数: {cleaned_df.shape}")
	print(f"- {q6_ranked_path} 读取成功, 行列数: {q6_ranked_df.shape}")
	print(f"- {multi_choice_binary_path} 读取成功, 行列数: {multi_choice_binary_df.shape}")
	print(f"- {cleaning_report_path} 读取成功")
	print()

	print("关键校验结果")
	print(f"- 有效问卷数: {valid_count if valid_count is not None else '未从日志中解析到'}")
	if missing_q6_columns:
		print(f"- Q6缺失列: {missing_q6_columns}")
	else:
		print(f"- Q6三列存在: {Q6_REQUIRED_COLUMNS}")
	print(f"- 多选宽表列数: {multi_choice_binary_df.shape[1]}")
	print()

	q1_counts = plot_single_choice_distribution(cleaned_df[Q1_COLUMN], "Q1 年级分布", q1_output_path)
	q2_counts = plot_single_choice_distribution(cleaned_df[Q2_COLUMN], "Q2 实习经历分布", q2_output_path)
	q4_counts = plot_single_choice_distribution(cleaned_df[Q4_COLUMN], "Q4 政策了解程度分布", q4_output_path)
	q5_counts = plot_single_choice_distribution(cleaned_df[Q5_COLUMN], "Q5 校内要求清楚程度分布", q5_output_path)
	q3_summary = plot_multi_choice_distribution(
		valid_multi_choice_df,
		Q3_PREFIX,
		"Q3 实践产出材料选择情况",
		q3_output_path,
		valid_count if valid_count is not None else len(cleaned_df),
	)
	q7_summary = plot_multi_choice_distribution(
		valid_multi_choice_df,
		Q7_PREFIX,
		"Q7 选择原因分布",
		q7_output_path,
		valid_count if valid_count is not None else len(cleaned_df),
	)
	q8_summary = plot_multi_choice_distribution(
		valid_multi_choice_df,
		Q8_PREFIX,
		"Q8 不适合作为替代形式的成果类型",
		q8_output_path,
		valid_count if valid_count is not None else len(cleaned_df),
	)
	q11_summary = plot_multi_choice_distribution(
		valid_multi_choice_df,
		Q11_PREFIX,
		"Q11 当前最担心的问题",
		q11_output_path,
		valid_count if valid_count is not None else len(cleaned_df),
	)
	q12_summary = plot_multi_choice_distribution(
		valid_multi_choice_df,
		Q12_PREFIX,
		"Q12 实践成果分类标准重点考虑因素",
		q12_output_path,
		valid_count if valid_count is not None else len(cleaned_df),
	)
	q13_summary = plot_multi_choice_distribution(
		valid_multi_choice_df,
		Q13_PREFIX,
		"Q13 希望学院提供的支持工具",
		q13_output_path,
		valid_count if valid_count is not None else len(cleaned_df),
	)
	q6_summary = plot_q6_weighted_scores(q6_ranked_df, q6_output_path)
	q9_summary = plot_q9_likert_summary(cleaned_df, q9_output_path)
	q10_summary = plot_q10_weight_distribution(cleaned_df, q10_output_path)
	summary_denominator = valid_count if valid_count is not None else len(cleaned_df)
	descriptive_summary_df = build_descriptive_summary(
		q1_counts,
		q2_counts,
		q4_counts,
		q5_counts,
		q3_summary,
		q7_summary,
		q8_summary,
		q11_summary,
		q12_summary,
		q13_summary,
		q6_summary,
		q9_summary,
		q10_summary,
		summary_denominator,
	)
	descriptive_summary_df.to_csv(descriptive_summary_path, index=False, encoding="utf-8-sig")

	print("2) Q1 单选题频率图")
	print(f"本步输入: {cleaned_data_path}")
	print(f"本步输出文件: {q1_output_path}")
	print("终端验收信号: 应看到Q1非空样本数、各选项频数、图片已保存")
	print(f"Q1非空样本数: {int(q1_counts.sum())}")
	print("Q1各选项频数:")
	print(q1_counts.to_string())
	print(f"{q1_output_path} 已保存")
	print()

	print("3) Q2 单选题频率图")
	print(f"本步输入: {cleaned_data_path}")
	print(f"本步输出文件: {q2_output_path}")
	print("终端验收信号: 应看到Q2非空样本数、各选项频数、图片已保存")
	print(f"Q2非空样本数: {int(q2_counts.sum())}")
	print("Q2各选项频数:")
	print(q2_counts.to_string())
	print(f"{q2_output_path} 已保存")
	print()

	print("4) Q4 单选题频率图")
	print(f"本步输入: {cleaned_data_path}")
	print(f"本步输出文件: {q4_output_path}")
	print("终端验收信号: 应看到Q4非空样本数、各选项频数、图片已保存")
	print(f"Q4非空样本数: {int(q4_counts.sum())}")
	print("Q4各选项频数:")
	print(q4_counts.to_string())
	print(f"{q4_output_path} 已保存")
	print()

	print("5) Q5 单选题频率图")
	print(f"本步输入: {cleaned_data_path}")
	print(f"本步输出文件: {q5_output_path}")
	print("终端验收信号: 应看到Q5非空样本数、各选项频数、图片已保存")
	print(f"Q5非空样本数: {int(q5_counts.sum())}")
	print("Q5各选项频数:")
	print(q5_counts.to_string())
	print(f"{q5_output_path} 已保存")
	print()

	print("6) Q3 多选题选择次数/选择率图")
	print(f"本步输入: {multi_choice_binary_path}, {cleaned_data_path}, {cleaning_report_path}")
	print(f"本步输出文件: {q3_output_path}")
	print("终端验收信号: 应看到Q3选项数、各选项选择次数、选择率分母、图片已保存")
	print(f"Q3选项数: {len(q3_summary)}")
	print(f"选择率分母: {valid_count if valid_count is not None else len(cleaned_df)}")
	print("Q3各选项选择次数与选择率:")
	print(q3_summary.to_string(index=False))
	print(f"{q3_output_path} 已保存")
	print()

	print("7) Q7 多选题选择次数/选择率图")
	print(f"本步输入: {multi_choice_binary_path}, {cleaned_data_path}, {cleaning_report_path}")
	print(f"本步输出文件: {q7_output_path}")
	print("终端验收信号: 应看到Q7选项数、各选项选择次数、选择率分母、图片已保存")
	print(f"Q7选项数: {len(q7_summary)}")
	print(f"选择率分母: {valid_count if valid_count is not None else len(cleaned_df)}")
	print("Q7各选项选择次数与选择率:")
	print(q7_summary.to_string(index=False))
	print(f"{q7_output_path} 已保存")
	print()

	print("8) Q8 多选题选择次数/选择率图")
	print(f"本步输入: {multi_choice_binary_path}, {cleaned_data_path}, {cleaning_report_path}")
	print(f"本步输出文件: {q8_output_path}")
	print("终端验收信号: 应看到Q8选项数、各选项选择次数、选择率分母、图片已保存")
	print(f"Q8选项数: {len(q8_summary)}")
	print(f"选择率分母: {valid_count if valid_count is not None else len(cleaned_df)}")
	print("Q8各选项选择次数与选择率:")
	print(q8_summary.to_string(index=False))
	print(f"{q8_output_path} 已保存")
	print()

	print("9) Q11 多选题选择次数/选择率图")
	print(f"本步输入: {multi_choice_binary_path}, {cleaned_data_path}, {cleaning_report_path}")
	print(f"本步输出文件: {q11_output_path}")
	print("终端验收信号: 应看到Q11选项数、各选项选择次数、选择率分母、图片已保存")
	print(f"Q11选项数: {len(q11_summary)}")
	print(f"选择率分母: {valid_count if valid_count is not None else len(cleaned_df)}")
	print("Q11各选项选择次数与选择率:")
	print(q11_summary.to_string(index=False))
	print(f"{q11_output_path} 已保存")
	print()

	print("10) Q12 多选题选择次数/选择率图")
	print(f"本步输入: {multi_choice_binary_path}, {cleaned_data_path}, {cleaning_report_path}")
	print(f"本步输出文件: {q12_output_path}")
	print("终端验收信号: 应看到Q12选项数、各选项选择次数、选择率分母、图片已保存")
	print(f"Q12选项数: {len(q12_summary)}")
	print(f"选择率分母: {valid_count if valid_count is not None else len(cleaned_df)}")
	print("Q12各选项选择次数与选择率:")
	print(q12_summary.to_string(index=False))
	print(f"{q12_output_path} 已保存")
	print()

	print("11) Q13 多选题选择次数/选择率图")
	print(f"本步输入: {multi_choice_binary_path}, {cleaned_data_path}, {cleaning_report_path}")
	print(f"本步输出文件: {q13_output_path}")
	print("终端验收信号: 应看到Q13选项数、各选项选择次数、选择率分母、图片已保存")
	print(f"Q13选项数: {len(q13_summary)}")
	print(f"选择率分母: {valid_count if valid_count is not None else len(cleaned_df)}")
	print("Q13各选项选择次数与选择率:")
	print(q13_summary.to_string(index=False))
	print(f"{q13_output_path} 已保存")
	print()

	print("12) Q6 排序题加权偏好图")
	print(f"本步输入: {q6_ranked_path}")
	print(f"本步输出文件: {q6_output_path}")
	print("终端验收信号: 应看到Q6候选类型数、3/2/1加权规则、各类型总分、图片已保存")
	print("Q6加权规则: 第1选=3分, 第2选=2分, 第3选=1分")
	print(f"Q6候选类型数: {len(q6_summary)}")
	print("Q6各类型加权偏好得分:")
	print(q6_summary.to_string(index=False))
	print(f"{q6_output_path} 已保存")
	print()

	print("13) Q9 李克特量表均值与分布图")
	print(f"本步输入: {cleaned_data_path}")
	print(f"本步输出文件: {q9_output_path}")
	print("终端验收信号: 应看到Q9维度数、各维度均值、图片已保存")
	print(f"Q9维度数: {len(q9_summary)}")
	print("Q9各维度均值:")
	print(q9_summary.to_string(index=False))
	print(f"{q9_output_path} 已保存")
	print()

	print("14) Q10 平均权重堆积条形图")
	print(f"本步输入: {cleaned_data_path}")
	print(f"本步输出文件: {q10_output_path}")
	print("终端验收信号: 应看到Q10主体数、各主体平均权重、均值和、图片已保存")
	print(f"Q10主体数: {len(q10_summary)}")
	print(f"Q10平均权重之和: {q10_summary['平均权重'].sum():.2f}")
	print("Q10各主体平均权重:")
	print(q10_summary.to_string(index=False))
	print(f"{q10_output_path} 已保存")
	print()

	print("15) descriptive_summary 汇总表导出")
	print(f"本步输入: 各题已生成的统计结果")
	print(f"本步输出文件: {descriptive_summary_path}")
	print("终端验收信号: 应看到汇总表行数、覆盖题号、文件已保存")
	print(f"汇总表行数: {len(descriptive_summary_df)}")
	print(f"覆盖题号: {', '.join(descriptive_summary_df['题号'].drop_duplicates().tolist())}")
	print(f"{descriptive_summary_path} 已保存")
	print()
	print("全部图表与汇总表任务完成")


if __name__ == "__main__":
	main()