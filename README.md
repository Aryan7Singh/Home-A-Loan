# Home-A-Loan

# Short, sharp, and on point description of project

Home A Loan is a powerful, data-centric model that financial institutions can leverage to determine whether people are at risk of defaulting on their loans.

# The problem it solves

The absence of a credit history can indicate different things, like being young or preferring cash transactions. Without traditional data, people with little to no credit history are likely to be denied loans. It is essential for finance providers to accurately assess who can repay a loan and who can't, making data crucial. By using data science to improve predictions of repayment capabilities, loans could be more accessible to those who could benefit the most from them.

Currently, financial institutions use models called scorecards to predict loan risk. Since clients’ behavior changes constantly, every scorecard must be regularly updated, a time-consuming and tedious process. This often means loan providers struggle to identify potential issues until the first due dates of loans are visible.

This is where Home A Loan steps in. Home A Loan is a data-driven model designed to assess the risk of default for clients. We started with a dataset consisting of 1.5 million data points, encompassing 220 features detailing historic loan outcomes. From this dataset, we employed LightGBM, a powerful machine-learning model, to extract six of the most influential features. This process allowed us to focus our analysis on the most critical factors driving loan outcomes.

To ensure our models’ predictive power, we developed three distinct models: LightGBM, XGBoost, and logistic regression. Both LightGBM and XGBoost (0.739 5-Fold Stratified Validation AoC) are robust decision tree models renowned for their accuracy, while logistic regression (0.691 AoC) provides a baseline for comparison. With these models, we can assess the likelihood of a person defaulting on their loan, enabling informed decision-making in seconds. 

We envision financial institutions leveraging our models to broaden their acceptance of loan applications, potentially transforming the lives of individuals historically denied due to limited credit history. Our approach ensures deserving clients are not overlooked.

# Challenges we ran into

Throughout our project, we encountered several challenges that required innovative solutions:

Identifying significant features that also add value (feature selection): We grappled with the task of pinpointing features that were not only intriguing but also influential in our model's predictive accuracy. To solve this issue, we implemented a large-scale LightGBM model that analyzed 220 features over 1.5 million data points and extracted 6 of the most influential features.

Managing missing values in the dataset: Dealing with missing data posed an interesting hurdle, especially since the dataset was so large. For logistic regression, we adopted imputation and normalization techniques, while for tree models, we preserved the missing values as these models inherently handle such data.

Handling a vast dataset efficiently: To overcome the problem of handling a large dataset, we explored cutting-edge libraries and technologies, such as polars, renowned for their ability to streamline computational workflows. As we navigated through this process, we uncovered novel optimization techniques, such as data streaming and parallel processing, which not only preserved memory but also substantially enhanced the efficiency of our models' computations. This facilitated the seamless processing of large datasets but also equipped us with invaluable insights into maximizing computational efficiency in data-intensive tasks.

Getting real-time predictions: One of the biggest challenges we ran into was the connection between the frontend and the model. Specifically, we had to asynchronously sync user data with the model; this required building Javascript infrastructure that incorporated action events to detect user input. 

Overall, we experienced many challenges relating to the model, frontend, and backend. However, as we grappled with these various problems, we learned techniques and concepts from data engineering to memory optimization to software architecture.
