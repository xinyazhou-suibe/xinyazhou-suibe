# 画图实现任务单

基于当前清洗产物整理。只列实现任务，不包含代码。

| 任务名 | 输入文件 | 输出文件 | 终端验收信号 | 失败时优先排查点 |
|---|---|---|---|---|
| 绘图前输入校验 | output/cleaned_data.csv；output/q6_ranked.csv；output/multi_choice_binary.csv；output/cleaning_report.txt | 无 | 终端打印 4 个输入文件读取成功；并打印有效问卷数、Q6 三列存在、多选宽表列数大于 0 | 先查文件路径是否正确；再查 CSV 编码是否按 utf-8-sig 读取；再查列名是否与清洗阶段一致 |
| Q1 单选题频率图 | output/cleaned_data.csv | output/desc_q1.png | 终端打印 Q1 非空样本数、各选项频数、图片已保存 | 先查 Q1 真实列名是否匹配；再查是否误用了原始表而不是 cleaned_data.csv；再查空值是否被当成类别 |
| Q2 单选题频率图 | output/cleaned_data.csv | output/desc_q2.png | 终端打印 Q2 非空样本数、各选项频数、图片已保存 | 先查 Q2 真实列名；再查类别值是否存在前后空格导致重复类别；再查图像保存路径 |
| Q4 单选题频率图 | output/cleaned_data.csv | output/desc_q4.png | 终端打印 Q4 非空样本数、各选项频数、图片已保存 | 先查超长列名是否完整匹配；再查中文字体显示；再查饼图标签是否截断 |
| Q5 单选题频率图 | output/cleaned_data.csv | output/desc_q5.png | 终端打印 Q5 非空样本数、各选项频数、图片已保存 | 先查 Q5 列名；再查频数统计是否只基于有效问卷；再查图片覆盖保存是否成功 |
| Q3 多选题选择次数/选择率图 | output/multi_choice_binary.csv；output/cleaning_report.txt | output/desc_q3.png | 终端打印 Q3 选项数、各选项选择次数、选择率分母、图片已保存 | 先查多选宽表中 Q3 对应列前缀是否完整；再查选择率分母是否用有效问卷总数；再查排序是否按次数或选择率统一 |
| Q7 多选题选择次数/选择率图 | output/multi_choice_binary.csv；output/cleaning_report.txt | output/desc_q7.png | 终端打印 Q7 选项数、各选项选择次数、选择率分母、图片已保存 | 先查 Q7 列前缀筛选规则；再查是否混入别题列；再查横向条形图标签是否完整 |
| Q8 多选题选择次数/选择率图 | output/multi_choice_binary.csv；output/cleaning_report.txt | output/desc_q8.png | 终端打印 Q8 选项数、各选项选择次数、选择率分母、图片已保存 | 先查 Q8 列筛选；再查选择次数是否按列求和；再查是否错误过滤掉全 0 列 |
| Q11 多选题选择次数/选择率图 | output/multi_choice_binary.csv；output/cleaning_report.txt | output/desc_q11.png | 终端打印 Q11 选项数、各选项选择次数、选择率分母、图片已保存 | 先查 Q11 列前缀；再查分母口径；再查图中排序和汇总表是否一致 |
| Q12 多选题选择次数/选择率图 | output/multi_choice_binary.csv；output/cleaning_report.txt | output/desc_q12.png | 终端打印 Q12 选项数、各选项选择次数、选择率分母、图片已保存 | 先查 Q12 列前缀；再查选项名中标点是否导致重复列；再查图片高度是否足够容纳长标签 |
| Q13 多选题选择次数/选择率图 | output/multi_choice_binary.csv；output/cleaning_report.txt | output/desc_q13.png | 终端打印 Q13 选项数、各选项选择次数、选择率分母、图片已保存 | 先查 Q13 列前缀；再查宽表列命名；再查保存时是否误覆盖其他题图片 |
| Q6 排序题加权偏好图 | output/q6_ranked.csv | output/desc_q6.png | 终端打印 Q6 候选类型数、3/2/1 加权规则、各类型总分、图片已保存 | 先查 第1选/第2选/第3选 三列是否存在；再查类别文本是否有空格差异导致重复类别；再查计分规则是否严格为 3/2/1 |
| Q9 李克特雷达图与箱线图 | output/cleaned_data.csv | output/desc_q9.png | 终端打印 10 个维度名称、各维度均值、图片已保存 | 先查 10 个 Q9 列是否齐全；再查数值范围是否仍在 1 到 5；再查是否采用一张复合图输出而不是拆成两张 |
| Q10 平均权重堆积条形图 | output/cleaned_data.csv | output/desc_q10.png | 终端打印 5 个主体平均权重、均值和、图片已保存 | 先查 5 个 Q10 列是否齐全；再查是否仅使用有效问卷；再查平均权重之和是否接近 100 |
| 图表输出总验收 | 上述全部输入文件 | output/desc_q1.png 至 output/desc_q13.png 中实际需要的文件 | 终端打印每张图已保存，并打印“全部图表任务完成”或等价汇总信息 | 先查 output 目录写入权限；再查中文字体和图像后端；再查文件命名是否严格按题号 |

## 建议执行顺序

1. 先做绘图前输入校验，因为它能一次暴露路径、编码、列名、分母口径问题。
2. 再做 Q1、Q2、Q4、Q5 单选题，因为输入最简单，最适合先验证画图流程。
3. 然后做 Q3、Q7、Q8、Q11、Q12、Q13，因为它们共享同一份 output/multi_choice_binary.csv。
4. 最后做 Q6、Q9、Q10，因为这三类题的图形逻辑更依赖列结构和统计口径。
