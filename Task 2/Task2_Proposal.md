# Project Proposal: Customer Lifetime Value Calculation Script with CRM Integration and Visualization

## Introduction
This project aims to develop a Python-based script that calculates the Customer Lifetime Value (CLV) by accessing customer data from a SQL-based CRM system and generates insightful visualizations. 

## Objectives
- **Develop a CLV calculation script** that fetches and processes transaction data from a SQL CRM database.
- **Integrate visualization tools** to represent the data in an accessible format.
- **Compare iterative and recursive programming approaches** to implementing the CLV calculation.

## Scope
The project will focus on:
1. Designing and implementing the CLV calculation in both iterative and recursive forms.
2. Integrating with a SQL-based CRM system to fetch necessary data.
3. Generating visualizations to represent CLV data effectively.

## Methodology
### Customer Life Time Value (CLV)
CLV is forward-looking approach that allows estimation of value and profitability of customers. CLV equals the net present value of all futures streams of profits that a customer generates over the life of the relationship with the company. See the bottom of this document for a detailed derivation of CLV.

#### CLV Formula:
The Customer Lifetime Value (CLV) is calculated as:

$$ CLV = M \times \frac{r}{1 + d - r} $$

#### Variables Description:
- **\( M \)**: **Margin per Customer**. This is calculated as \( \text{Price} - \text{Unit Variable Cost} \). For your example, this would be $350. This represents the profit from each purchase, assuming the cost to provide the product or service is subtracted from the price at which it's sold.

- **\( r \)**: **Retention Rate**. This is the probability that a customer will return to make another purchase in the next period. In your example, this rate is 0.9 (or 90%), indicating a high likelihood that a customer will continue to buy annually.

- **\( d \)**: **Discount Rate**. This rate is used to discount the value of future cash flows to present value. It reflects the time value of money, indicating how much future revenues are worth today. The choice of \( d \) depends on the cost of capital or an estimated rate that reflects the firm's opportunity cost of capital.

### Function Design
- The script will calculate CLV using both an iterative and a recursive method to evaluate the benefits of each approach.

### System Integration
- Connect to a SQL-based CRM system to retrieve customer transaction data.

### Visualization
- Develop graphical representations of the data using Matplotlib or Seaborn.

## Performance Metrics
- Execution time
- Memory usage
- Computational complexity

## Expected Deliverables
- **Code**: Python scripts for both versions of the CLV calculation.
- **Documentation**: Comprehensive comments within the scripts explaining the functionality.
- **Test Cases**: Examples and results demonstrating the correctness of both script versions.
- **Performance Analysis**: Evaluation and comparison of the iterative and recursive implementations.
- **Project Report**: A detailed report discussing the methodology, results, and insights from the project.
- **Presentation**: Slides summarizing the project, its outcomes, and strategic recommendations.

## CLV Derivation
Let's consider a consumer who buys a snowboard every year:

**Let:**
- $M = Price - Unit Variable Cost = $350

**Then CLV is**
$M_1 + $M_2 + ... = $350 + $350 + ...

But the value of future purchases are not the same value as the present purchases, hence, we discount the earnings by:
$$\frac{\$ M_1}{(1+d)^1} + \frac{\$ M_2}{(1+d)^2} + \frac{\$ M_3}{(1+d)^3} + \ldots$$
Where $d$ is the discount rate chosen by the firm. Additionally, loyalty will diminish overtime, so we can account for the probability that a consumer will still be a consumer in time period $t$ by doing the following:

$$\frac{\$ M_1 * p_1}{(1+d)^1} + \frac{\$ M_2 * p_2}{(1+d)^2} + \frac{\$ M_3 * p_3}{(1+d)^3} + \ldots$$

where $p$ is the probability that a consumer will buy in a given time period (which in turn is derived from retention rate, $r$). Let's assume that there is a $0.9$ probability that a consumer will make a purchase in time period $t$, given that he bought in $t-1$. Thus, we can derive the probabilities by:

$$p(1) = r(1) = 0.90$$
$$p(2) = r(1)*r(2) = 0.9^2$$
$$p(3) = r(1)*r(2)*r(3) = 0.9^3$$

Therefore, **Standard CLV** can be written as:
$$\frac{\$ M_1 * r^1}{(1+d)^1} + \frac{\$ M_2 * r^2}{(1+d)^2} + \frac{\$ M_3 * r^3}{(1+d)^3} + \ldots$$
or

$$\text{CLV} = \sum_{t=1} ^\infty \frac{\$ M_t r^t}{(1+d)^t} = \$M * \frac{r}{1+d-r}$$