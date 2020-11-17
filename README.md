> 项目网址：http://zomboost.dcts.top/

## 一、前言

近年来，依法处置“僵尸企业”已经成为“深化重点领域改革，加快完善市场机制”的关键。2020年作为治理“僵尸企业”的收官之年，各监管部门亟需一种行之有效的“僵尸企业”识别方案。

本项目将对企业多维度数据进行可视化分析，构建企业全息画像。通过机器学习技术对数据进行建模，实现对僵尸企业的精准识别，并搭建识别平台，为用户提供线上的僵尸企业自动识别服务。



## 二、项目创新

1. **准确率高**。在对数据建模时，基于推荐系统中的特征组合方法DeepFM，结合相关企业的业务特征进行“类DeepFM特征组合”，捕获企业基本特征和组合特征，提高模型的泛化能力，将模型的识别准确率提升到99.99%。

2. **模型优越**。采用对于类别特征有较好识别能力的Catboost集成学习模型对数据集进行训练，在各种评估指标下均优于同类模型。

3. **结果直观**。使用数据可视化技术，对数据特征及识别结果进行直观呈现。

4. **交互性强**。交互式的可视化图表更便于浏览，可根据需求进行个性化数据查询、筛选，区域缩放、拖拽等操作。



## 三、功能简介

在浏览器中输入网址 <http://zomboost.dcts.top/> 进入图1所示项目首页。

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE1%20%E9%A1%B9%E7%9B%AE%E9%A6%96%E9%A1%B5.png)

<p style="text-align:center;">图1 项目首页</p>

如图2所示，项目提供僵尸企业智能识别平台，并使用可视化技术展示数据的分布与关联性。此外还根据可视化结果定性识别僵尸企业，构建企业画像。最后将模型训练结果可视化，横向对比十余个常用模型，多指标综合评估模型性能。

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE2%20%E5%8A%9F%E8%83%BD%E7%AE%80%E4%BB%8B.png)

<p style="text-align:center;">图2 功能简介</p>



## 四、实现方案

**1、** **数据预处理**

本项目使用验证集作为模型的训练数据，完成包括年份融合、缺失值填充等单表处理以及多表融合操作。

**2、** **数据建模**

首先，如图3、4所示，对经过预处理的数据采用基于DeepFM思想的特征工程，挖掘与“是否为僵尸企业”有关的高阶特征。

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE3%20DeepFM%E6%A8%A1%E5%9E%8B%E7%BB%93%E6%9E%84%E5%9B%BE.png)

<p style="text-align:center;">图3 DeepFM模型结构图</p>

其次，**选用CatBoost模型**，通过十折交叉验证和混淆矩阵综合评估模型的表现后，对验证集提供的所有数据集进行训练，并保存训练好的模型。此外，从准确率、精准率、召回率、AUC、F1-score多指标对比与其他经典模型之间的差异，并可视化对比结果。

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE4%20%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86%E5%8F%8A%E5%BB%BA%E6%A8%A1%E6%B5%81%E7%A8%8B.png)

<p style="text-align:center;">图4 数据预处理及建模流程</p>


**3、** **数据可视化**

可视化不是一个独立的过程，它穿插在数据预处理和建模之间。

**数据分布可视化**（图5）及**关联性探索**（图6）用一种直观的方式分析数据集特点，分别为数据预处理和特征组合提供依据。

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE5%20%E6%95%B0%E6%8D%AE%E5%8F%AF%E8%A7%86%E5%8C%96%E9%A1%B5%E9%9D%A2.png)

<p style="text-align:center;">图5 数据可视化页面</p>

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE6%20%E6%95%B0%E6%8D%AE%E5%85%B3%E8%81%94%E6%80%A7%E6%8E%A2%E7%B4%A2%E9%A1%B5%E9%9D%A2.png)

<p style="text-align:center;">图6 数据关联性探索页面</p>

**僵尸企业画像**（图7）通过输入企业ID，构建企业画像，并回答了如下两个问题：该企业是否是僵尸企业？在数据分布上如何做出上述判断？

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE7%20%E5%83%B5%E5%B0%B8%E4%BC%81%E4%B8%9A%E7%94%BB%E5%83%8F.png)

<p style="text-align:center;">图7 僵尸企业画像</p>

**模型训练可视化**（图8）的目的其一，是直观展示分类模型自动挑选的若干个与“是否是僵尸企业”强相关的特征，其二，是将本项目模型与其他模型进行对比，并将对比结果可视化。

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/%E5%9B%BE8%20%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83%E5%8F%AF%E8%A7%86%E5%8C%96%E9%A1%B5%E9%9D%A2.png)

<p style="text-align:center;">图8 模型训练可视化页面</p>




## 五、开发工具与技术

1、可视化及网页开发技术

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/5.1%E5%8F%AF%E8%A7%86%E5%8C%96%E5%8F%8A%E7%BD%91%E9%A1%B5%E5%BC%80%E5%8F%91%E6%8A%80%E6%9C%AF.png)



2、数据建模工具

![image](https://github.com/WolfMy/ZombieCompany/blob/master/image/5.2%E6%95%B0%E6%8D%AE%E5%BB%BA%E6%A8%A1%E5%B7%A5%E5%85%B7.png)





## 六、应用对象

1. 作为**市场监督局和工商管理局**等政府机构的僵尸企业智能识别平台，对僵尸企业进行客观、精确、快速的识别；
2. 帮助**企业管理者**评估企业当前经营状况，辅助企业进行资源优化、经营调整等。




## 七、结束语

在信息共享的大数据时代，人工智能计算作为时代下的产物，为人类认识世界插上了新的翅膀。本项目团队脱离传统识别标准的束缚，紧跟大数据与人工智能时代的潮流，使用机器学习技术，构建了一个客观公正且高精确度的“僵尸企业”识别模型，对于破解僵尸企业难题、加快清理和处置“僵尸企业”的步伐、推进供给侧改革具有重要意义。

## 如何使用
1. 安装Mysql并建立数据库，做好FLask与数据库的迁移与升级:flask db init,flask db migrate...
2. 使用gunicorn启动flask服务，调整自己部署的服务器ip
3. 修改vue生产环境的api接口地址，并将vue打包: npm run build...
4. 配置nginx，监听80端口，部署vue静态页面
