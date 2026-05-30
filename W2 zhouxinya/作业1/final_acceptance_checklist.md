# 交付前最终验收清单

## 1) 文件完整性

1. 清洗输出文件存在  
通过标准：以下 4 个文件都存在，且能正常打开读取。  
- output/cleaned_data.csv  
- output/q6_ranked.csv  
- output/multi_choice_binary.csv  
- output/cleaning_report.txt

2. 图表文件存在且题号完整  
通过标准：以下图表文件都存在，文件名与题号一一对应，没有缺号、错号、重名覆盖。  
- output/desc_q1.png  
- output/desc_q2.png  
- output/desc_q3.png  
- output/desc_q4.png  
- output/desc_q5.png  
- output/desc_q6.png  
- output/desc_q7.png  
- output/desc_q8.png  
- output/desc_q9.png  
- output/desc_q10.png  
- output/desc_q11.png  
- output/desc_q12.png  
- output/desc_q13.png

3. 汇总表文件存在  
通过标准：最终应存在 output/descriptive_summary.csv，且不是空文件。  
当前状态：这一步还没做，如果要正式交付，这个文件必须补上。

4. 脚本可重复运行  
通过标准：重新运行 module1_data_cleaning.py 和 module2_descriptive.py 后，不报错、不要求人工输入、不会中断已有输出流程。

## 2) 图表质量（是否乱码、是否可读）

1. 中文不乱码  
通过标准：所有 PNG 中的标题、坐标轴、图例、标签都能正常显示中文，不出现方框、问号、缺字、重叠成不可读文本。

2. 长标签可读  
通过标准：多选题和 Q6 中较长的选项名称没有被严重截断；即使换行或倾斜，也仍能辨认完整含义。重点检查：  
- output/desc_q3.png  
- output/desc_q7.png  
- output/desc_q8.png  
- output/desc_q11.png  
- output/desc_q12.png  
- output/desc_q13.png  
- output/desc_q6.png

3. 单选题双图可读  
通过标准：Q1、Q2、Q4、Q5 的条形图和饼图都能清楚看出类别差异；饼图标签没有相互遮挡到无法辨认。重点检查：  
- output/desc_q1.png  
- output/desc_q2.png  
- output/desc_q4.png  
- output/desc_q5.png

4. 多选题排序正确  
通过标准：横向条形图按选择次数从高到低或从低到高排序，且排序规则与终端打印一致；图上的数值标注与条形长度一致。

5. Q9 复合图可读  
通过标准：output/desc_q9.png 中雷达图 10 个维度标签能辨认，箱线图 10 个维度名称不重叠到完全不可读，纵轴范围能看出 1 到 5 分分布。

6. Q10 堆积条形图可读  
通过标准：output/desc_q10.png 中 5 个主体颜色区分清楚，图例完整，条内百分比标注没有重叠，整体一眼能看出总和约为 100%。

7. 图片分辨率足够  
通过标准：在常见屏幕查看比例下，无需过度放大即可识别主要标签和数值；图片不是明显模糊或过小。

## 3) 数据一致性（样本数、异常数、汇总表字段）

1. 有效样本口径一致  
通过标准：所有统计与作图统一使用 Q15 过滤后的有效问卷。当前已验证有效问卷数应为 160；终端、日志、图表口径必须一致。以 output/cleaning_report.txt 为准。

2. 无效问卷定义一致  
通过标准：无效问卷只由 Q15 未选“基本同意 ←请选择此项”判定，不混入其他临时过滤规则；output/cleaning_report.txt 中剔除原因与实现一致。

3. 多选题分母一致  
通过标准：Q3、Q7、Q8、Q11、Q12、Q13 的选择率分母全部为有效问卷总数 160，而不是各题非空人数；终端打印的选择率与图中标注一致。

4. 多选题样本筛选一致  
通过标准：多选宽表统计前，已经用 cleaned_data.csv 的 序号 对 multi_choice_binary.csv 做有效样本筛选；不会把无效问卷混入多选统计。

5. Q6 计分规则一致  
通过标准：Q6 严格按 第1选=3 分、第2选=2 分、第3选=1 分计算；终端打印得分表与 output/desc_q6.png 排序一致；候选类型数为 9。

6. Q9 数值范围合理  
通过标准：Q9 各维度值都应落在 1 到 5 之间；均值也应全部落在 1 到 5 之间；雷达图和箱线图的维度数均为 10。

7. Q10 权重和一致  
通过标准：Q10 五个主体的平均权重之和应接近 100；当前终端验证结果是 100.00。若后续重跑后偏离明显，必须先排查原始权重列读取或类型问题。

8. 清洗后主表行数一致  
通过标准：output/cleaned_data.csv 的数据行数应与有效问卷数一致；当前应为 160 行数据。

9. Q6 解析表行数一致  
通过标准：output/q6_ranked.csv 的数据行数应与有效问卷数一致；当前应为 160 行数据，且包含 Q6_第1选、Q6_第2选、Q6_第3选 三列。

10. 汇总表字段完整  
通过标准：output/descriptive_summary.csv 至少包含以下字段，且字段命名全表统一：  
- 题号  
- 题型  
- 指标名称  
- 选项或维度  
- 统计值  
可选补充字段：样本数、选择率、排序值、备注

11. 汇总表内容覆盖完整  
通过标准：output/descriptive_summary.csv 至少覆盖：  
- Q1、Q2、Q4、Q5 的频数或占比  
- Q3、Q7、Q8、Q11、Q12、Q13 的选择次数和选择率  
- Q6 的加权偏好得分  
- Q9 的维度均值  
- Q10 的平均权重

12. 异常项有记录  
通过标准：如果存在“其他(请注明)”这类低频项、空值项、特殊文本项，不要求现在清洗掉，但要在终端或汇总表中能看出来，没有被静默丢失。
