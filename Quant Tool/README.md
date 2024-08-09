# zx_quant_tool

本人致力于构建一个开源的量化交易工具箱，旨在为量化交易者提供便捷的量化交易工具。欢迎大家一起共同开发，共同使用。目前工具包还在开发过程中，后续随着量化项目的进行，工具包会不断地完善更新，敬请期待。   
## 1.量化工具整体架构
#### a.数据获取模块
    主要从mysql数据库，本地存储数据中获取数据
#### b.数据预处理板块
    主要包括异常值处理、中性化、标准化、去极值、缺失值处理等操作。
#### c.净值拟合模块
    根据持仓股票标的，合成日度净值波动曲线
#### d.历史情景回测模块
    即在固定时间换仓，持有的股票数量固定，权重已知，完全知道历史持仓数据
#### e.事件驱动回测模块
    持有股票数量随着事件的发生而变化，持有的股票数量和股票标的在不同事时间点回测，最终数据都不一样。
#### f.策略评估模块
    评估策略的收益、风险、波动率、夏普比率、最大回撤、超额收益等指标。
#### g.因子测试模块
    RankIC、累计RankIC、IR等方法
#### h.因子库模块
    总结一些常用因子的计算方法