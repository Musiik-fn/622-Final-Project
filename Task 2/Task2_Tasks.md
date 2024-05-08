# Task 2 Tasks


### Variables and Calculations

1. **Profit Per Order**:
   This is calculated as the average net profit for each transaction.

   \[
   \text{Profit Per Order} = \frac{\text{Total Profit from a Customer}}{\text{Total Number of Orders by the Customer}}
   \]

2. **Average Order Frequency**:
   This represents the average number of orders a customer places per year. It's calculated by dividing the total number of orders by the lifespan of the customer in years.

   \[
   \text{Average Order Frequency} = \frac{\text{Total Number of Orders by the Customer}}{\text{Customer's Lifespan in Years}}
   \]

   To convert the customer's lifespan from days to years:

   \[
   \text{Customer's Lifespan in Years} = \frac{\text{Customer's Lifespan in Days}}{365}
   \]

3. **Average Lifespan in Years**:
   This is the average duration that a customer continues to buy from the business. It is calculated directly by converting the average lifespan from days to years.

   \[
   \text{Average Lifespan in Years} = \frac{\text{Mean Lifespan Days}}{365}
   \]

### Customer Lifetime Value (CLV)
Combining the above elements, the CLV for a customer can be calculated as:

   \[
   \text{CLV} = \text{Average Profit Per Order} \times \text{Average Order Frequency} \times \text{Average Lifespan in Years}
   \]

Where:
- **Average Profit Per Order** is the average net profit each order contributes.
- **Average Order Frequency** is how often a customer places an order in a year.
- **Average Lifespan in Years** is the average number of years a customer continues to engage with the business.


   \[
   \text{CLV} = \text{Mean Profit Per Order} \times \left( \frac{\text{Mean Order Amount}}{\text{Mean Lifespan Days} / 365} \right) \times \left( \frac{\text{Mean Lifespan Days}}{365} \right)
   \]
