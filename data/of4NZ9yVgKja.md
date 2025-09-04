# Publication Description

![wordcloud.png](wordcloud.png)--DIVIDER--# Foundational Models in Timeseries Forecasting: A Benchmarking Study

## Abstract

This ongoing project at Ready Tensor features a comprehensive benchmarking analysis of foundational time series models, starting with the **Chronos** family from **Amazon** Science and **MOIRAI** by **Salesforce**. Our study offers a detailed comparison of foundational forecasting models against 23 other leading models from our extensive database, covering neural networks, machine learning, statistical methods, and naive approaches. The evaluation criteria include performance measured by RMSSE across 24 datasets, execution durations, memory usage, hyperparameter sensitivity, and the comparative sizes of Docker images for deployment. By integrating these foundational models, our project aims to uncover their unique advantages in zero-shot learning, generalization across diverse dataset frequencies, and operational efficiencies against the backdrop of traditional and contemporary forecasting techniques.

## Introduction

Recent emergence of foundational models like Chronos, MOIRAI, Moment, and TimesFM introduces a new paradigm in forecasting, promising improved accuracy and generalization capabilities. Ready Tensor's project evaluates these models against traditional forecasting methods to understand their effectiveness and operational efficiency.

This project incorporates performance comparisons using the RMSSE metric, execution time, and memory usage. We also perform sensitivity analysis on model hyperparameters. As an additional criterion for consideration for deployment, we report the sizes of dockerized images for each model in this project. This approach helps identify the most efficient and accurate models for practical deployment in diverse settings. By focusing on foundational models, we aim to provide insights into their role in simplifying forecasting pipelines and enhancing predictive accuracy.


## Architectural Overview and Model Sizes

For detailed architectural insights and methodologies behind the Chronos and Moirai models, readers are directed to their respective publications:

- **Chronos** paper: [Chronos: Learning the Language of Time Series](https://arxiv.org/pdf/2403.07815)
- **Moirai** paper: [Unified Training of Universal Time Series Forecasting Transformers](https://arxiv.org/pdf/2402.02592)

The model sizes, quantified in terms of the number of trainable parameters, vary significantly across different configurations, impacting both their performance and computational demands:

- **Chronos Sizes**:
  - `chronos-t5-tiny`: 8 million parameters
  - `chronos-t5-mini`: 20 million parameters
  - `chronos-t5-small`: 46 million parameters
  - `chronos-t5-base`: 200 million parameters
  - `chronos-t5-large`: 710 million parameters
- **Moirai Sizes**:
  - `moirai-R-small`: 14 million parameters
  - `moirai-R-base`: 91 million parameters
  - `moirai-R-large`: 311 million parameters

Understanding the scale of these models is crucial for users to anticipate the resource needs and potential deployment scenarios, balancing the trade-offs between computational efficiency and forecasting accuracy.

## Forecast Accuracy

Our analysis, represented through a heatmap chart, compares the RMSSE performance of 5 Chronos models and 3 Moirai models against 23 other leading forecasting models across 24 datasets. Refer to the page for project [Ready Tensor Forecasting Benchmark](https://app.readytensor.ai/projects/EeNv3K1byb1V20OLZbBOd) for a description of the datasets, evaluation method, and metrics used in this analysis.

Models can be compared on a number of metrics, including RMSE, RMSSE, MAE, MASE, sMAPE, WAPE, and R-squared.

For this analysis, we focus on RMSSE, a scaled version of RMSE that compares a model's performance to a naive baseline. Note that lower RMSSE scores indicate better forecasting performance.

The following heatmap displays the average RMSSE scores for each model, grouped by dataset frequency. The results are filtered to 31 models for brevity, including the five Chronos models and 3 Moirai models which are at the bottom of the chart.

![Forecasting Models RMSSE Heatmap](https://github.com/readytensor/rt_forecasting_foundational_models/blob/main/outputs/moirai/moirai_forecasting_models_heatmap.png?raw=true)

**Key Findings:**

- The analysis reveals consistently strong performance for the Chronos models across different time frequencies. This demonstrates the Chronos models' adeptness at handling diverse forecasting scenarios without prior training on those specific datasets.
- The Chronos-T5-Large model emerges as a standout, demonstrating exceptional forecasting accuracy. This places it on par with the best of traditional machine-learning and neural network models.
- The Moirai models have been integrated into this benchmark. The Moirai base and large models each achieved an average RMSSE score of 0.80, indicating solid performance though not surpassing the top models like Chronos-T5-Large. The Moirai small model scored a 0.89, reflecting challenges in robustness or generalization compared to its larger counterparts.
- A performance gradient is observed among the foundational models, with larger models generally performing better, a trend also seen within the Chronos and Moirai families.

These results underscore the promising potential of foundational models in forecasting, aligning with trends seen in other domains like natural language processing. The insights from the Chronos and Moirai models affirm the evolving landscape where large, pretrained models increasingly define the frontiers of accuracy and applicability in forecasting tasks.


:::alert{type=info}
**Note on Forecast Length**: The Chronos documentation indicates that the current Chronos checkpoints (03/24/2024 at the time of this writing) work best with prediction_length <= 64. In our benchmark, 5 out of 24 datasets exceed the threshold.
:::

### Potential Train-Test Leakage
When evaluating foundational models such as Chronos and Moirai, it's essential to consider the possibility of train-test leakage. This issue arises if benchmarking datasets, like samples from the M4 competition, have also been used during the development of these models. Such overlap could result in models being indirectly 'trained' on data that is later used for their evaluation.

Addressing this challenge is complex. As we continue to incorporate more foundational models into our analysis, finding a large enough benchmark untouched by any model becomes increasingly challenging. However, the results of our evaluations are still valuable for understanding the relative performance of these models and offer insights into their effectiveness across diverse datasets. Users should remain mindful of this potential bias when interpreting results and making decisions based on these evaluations.



## Execution Durations and Memory Usage

Our analysis extends to the execution durations (training and prediction) and memory usage (CPU and GPU) of the Chronos models compared with other models. We particularly focused on the **Air Quality 2018** dataset, the largest among the 24 datasets in our benchmark, to underscore the differences in execution time and resource utilization more distinctly.

### Benchmarking Infrastructure

The study utilized two types of machines from the AWS platform based on the requirement for GPU acceleration:

- For models not requiring GPU acceleration, `c6a.4xlarge` instances were used, featuring 16 vCPUs, 32.0 GiB memory, with AMD EPYC 7R13 processors.
- Models requiring GPU acceleration were run on `g5.2xlarge` instances, equipped with 8 vCPUs, 32.0 GiB memory, 24.0 GiB video memory, powered by AMD EPYC 7R32 processors, and utilizing NVIDIA A10G GPUs.

### Tracking Methodology

Ideally, the training and prediction tasks would be executed multiple times (3 or 5 times) to report the minimum observed values for durations and memory usage. However, to manage compute costs, metrics from a single run are reported in this study.

The reported CPU memory usage primarily tracks Python memory through `tracemalloc`, which may not fully represent the total memory footprint. Specifically, this tracking does not include memory consumed by underlying processes, such as those executed in C/C++ by imported modules. Consequently, the actual CPU memory utilization could be higher than what is reported.

It should be noted upfront that observed differences in execution times and memory requirements may not solely reflect the computational demands of the forecasting models themselves but also the preprocessing overhead introduced by their respective libraries. Models leveraging libraries like MLForecast, NeuralForecast, Skforecast, GluonTS and Darts incorporate distinct preprocessing steps, which could significantly impact overall execution times and memory usage.

### Execution Time and Memory Usage Comparison

See the following chart for a comparison of the prediction times and memory usage of the Chronos and Moirai models against other models:

![Execution Times and Memory Usage by Forecasting Models](https://github.com/readytensor/rt_forecasting_foundational_models/blob/main/outputs/moirai/moirai_model_exec_durations_and_memory.png?raw=true)

Key observations from the data include:

- **Training Times:** Both the Chronos and Moirai models, as zero-shot learners, do not require training, leading to zero training time and memory usage.
- **Prediction Times:** The Chronos-T5-Large model's inference time is significantly longer than all other models, including Moirai, with a prediction time of 51.7 seconds for the Air Quality dataset. In contrast, the Moirai Large model takes 27.8 seconds, performing faster than Chronos but slower compared to traditional methods.
- **CPU Memory Usage:** The Base and Large Moirai models exhibit higher CPU memory requirements than the Chronos models during prediction.
- **GPU Memory Usage:** There is a notable difference in GPU memory consumption between the models. The Chronos-T5-Large model consumes a substantial 13.8 GB, while the Moirai Large model uses significantly less, with only 2.4 GB required. This reflects Moirai's more efficient use of GPU resources during prediction tasks.

These metrics highlight the operational demands and efficiencies of foundational models, with Moirai models presenting a lower resource footprint at inference compared to Chronos. This section underscores the need to balance the advanced predictive capabilities of such models against their computational resource requirements, especially in GPU-intensive environments.

## Hyperparameter Impact Analysis

### Chronos-T5-Large Model

We conducted an analysis of how changes in hyperparameters affect the forecasting accuracy of the Chronos-T5-Large model. This analysis focused on four key hyperparameters: `num_samples`, `top_p`, `top_k`, and `temperature`. The default values for these hyperparameters for the Chronos models are `num_samples=20`, `top_p=1.0`, `top_k=50`, and `temperature=1.0`. To isolate the impact of each hyperparameter, we varied them individually while keeping the others at their default values. The analysis was performed across all 24 datasets to observe the changes in RMSSE values.

See the following charts for the impact of each hyperparameter on the Chronos-T5-Large model's performance:

![Hyperparameter Impact Analysis](https://github.com/readytensor/rt_forecasting_foundational_models/blob/main/outputs/chronos/chronos_hyperparameter_impacts.png?raw=true)

**Key findings:**

- **`num_samples`:** Results observed in the chart above suggests that increasing the `num_samples` enhances the model's accuracy. We observe the best RMSSE value at num_samples = 30. However, this improvement comes at the cost of increased GPU memory consumption (not displayed in chart). The physical limitation of GPU memory capped our experimentation at 30 samples (which consumed ~20GB VRAM).
- **`top_k`:** The performance improvement with an increase in `top_k` values is evident, indicating a positive correlation between `top_k` and forecasting accuracy. However, a plateau effect is observed beyond `top_k` = 100, suggesting diminishing returns with further increases.
- **`top_p`: amd `temperature`** These two hyperparameters showed mixed impacts on RMSSE values, without a clear directional trend. This suggests that the influence of `top_p` and `temperature` on model performance might be more complex, requiring further exploration to fully understand their effects.

**Note on `temperature`:**
During our investigation, we experimented with values of `temperature` higher than 1.0. However, these adjustments led to significantly worse performance outcomes, signaling that the model becomes more volatile with increased `temperature` values. This finding emphasizes the delicate balance required in tuning `temperature` to enhance model stability and accuracy.

### Moirai-Large Model

We conducted an analysis to examine how changes in hyperparameters during inference affect the forecasting accuracy of the Moirai-Large model. This analysis focused on two key hyperparameters: `num_samples` and `context_length`. The default settings for these hyperparameters in Moirai models are `num_samples=100` and `context_length=1000`. To isolate the impact of each hyperparameter, we varied them individually while keeping the others at their default values. The analysis spanned all 24 datasets to observe variations in RMSSE values.

See the following charts for the impact of each hyperparameter on the Moirai-Large model's performance:

![Hyperparameter Impact Analysis for Moirai-Large](https://github.com/readytensor/rt_forecasting_foundational_models/blob/main/outputs/moirai/moirai_hyperparameter_impacts.png?raw=true)

**Key findings:**

- **`num_samples`:** Moirai-Large model sensitivity to `num_samples` is evident at lower counts, with performance improving from an RMSSE of 0.88 at 10 samples to 0.83 at 20, stabilizing at 0.80 from 50 samples onward. Higher sample counts are advisable for optimal accuracy.
- **`context_length`:** Moirai-Large's performance is also sensitive to `context_length`. RMSSE improves from 0.92 at 50 to 0.82 at 100, stabilizing at 0.80 for lengths of 500 and beyond. While the authors recommend a minimum of 1000 for most scenarios, dataset frequency should guide the optimal setting: shorter lengths may suffice for low frequency data, while high frequency data typically benefits from longer lengths.

:::alert{type=important}
**Note on `patch_size`:**
`patch_size` is a critical third hyperparameter for the Moirai-Large model. We used the default 'auto' setting for our analysis. While attempting to explore different `patch_size` settings, our internal tests showed high variance and did not reveal clear trends, making the results inconclusive. The model authors suggest adjusting `patch_size` according to data frequency—opting for shorter patch sizes for lower frequency data and larger ones for higher frequency data. Given the sensitivity and complexity associated with this hyperparameter, we strongly recommend users to carefully calibrate `patch_size` based on the specific characteristics and frequency of their datasets to optimize forecasting accuracy.
:::

## Docker Image Sizes Across Forecasting Models

In our study, all models are containerized using Docker to facilitate cross-platform deployment and reproducibility. The Docker images represents the model, its dependencies, and the necessary libraries for deployment. In this section, we review the image sizes across 31 models as a final consideration of model comparisons. The image sizes provide insights into the resource footprint of each model, which is crucial for deployment in resource-constrained environments.

See the following chart for a comparison of Docker image sizes across the 31 forecasting models:

![Model Image Sizes](https://github.com/readytensor/rt_forecasting_foundational_models/blob/main/outputs/moirai/moirai_docker_image_sizes.png?raw=true)

The following are the key takeaways from the Docker image size review:

- **Chronos models' image sizes:** The Chronos models are notably the largest in image size, with sizes ranging from 15.96 GB for the Chronos-T5-Tiny to 18.76 GB for the Chronos-T5-Large model. This indicates a significant resource footprint, attributed to the comprehensive libraries and dependencies these advanced models necessitate. Note that these images include the pretrained model weights, ensuring everything required for making predictions is self-contained within the image.
- **Moirai models' image sizes:** The Moirai models have smaller Docker images than the Chronos models, with sizes ranging from 11.42 GB for the Moirai Small, 12.11 GB for the Moirai Base, to 13.87 GB for the Moirai Large model. These sizes are smaller than those of the Chronos models but still larger than most other models, reflecting a moderate to high resource footprint.
- **Comparison with other models:** The smallest image sizes belong to models like the Extra Trees and Random Forest Forecasting Models in Scikit-Learn, which are among the top performers in forecasting accuracy. These models demonstrate an efficient use of resources without compromising on performance.
- **Naive models' image sizes:** Despite their simplicity, naive models using the Darts library do not yield the smallest Docker images. The choice of Darts, which supports a wide array of forecasting algorithms, introduces a considerable set of dependencies. This decision, prioritizing convenience and functionality, impacts the overall image size.

The analysis of Docker image sizes underscores the operational considerations that accompany the adoption of advanced models like Chronos and Moirai. While these models offer superior forecasting accuracy even on unseen datasets, they demand substantial computational resources for deployment.

## Project Summary

This comprehensive benchmarking project by Ready Tensor delivers critical insights into the performance, operational efficiency, and deployment considerations of 31 forecasting models, including the foundational Chronos and Moirai families. Our findings highlight the superior accuracy of Chronos models and the commendable performance of Moirai models, although both come with considerable resource demands, particularly in terms of GPU memory and Docker image sizes.

Our sensitivity analysis underscores the necessity of carefully tuning inference hyperparameters for both Chronos and Moirai models to optimize their forecasting accuracy. Each model family responds differently to hyperparameter settings, emphasizing the importance of a tailored approach to maximize performance and efficiency.

As we continue to explore the frontier of forecasting with foundational models, this project remains a work-in-progress. We are consistently incorporating new foundational models and updating our analyses to extend our understanding of these advanced tools in forecasting. This ongoing effort reflects Ready Tensor’s commitment to advancing the state of the art in AI forecasting, aiming to balance cutting-edge accuracy with practical deployment considerations.
