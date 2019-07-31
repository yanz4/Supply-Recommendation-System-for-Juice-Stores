# Supply-Recommendation-System-for-Juice-Stores
This Project aims to help juice chainstore owners or regional managers to view and manage products and sales of all stores in this regional. We build the management system with MySQL and PHP so managers could Create, Read, Update and Delete information from local server. We also provide an advanced function named “One-Click Sales Optimization”, which provides a best sales plan to reach maximum profit depending on the sales goal set by user.

In addition to traditional useful functionals such as view and search for sales records, edit store and product information,etc, one major problem that concerns managers is how to maximize profits when they own multiple juice stores. Given that actual profits in each juice store vary with city size and ingredient cost, we think Linear Optimization model could help determine the best sales plan. Given the population is approximately the same within a city, so annual orders, or cups of juice sales, would be about the same in each store. When the cups of juice sales keep relative constant we could maximize total profits by encouraging each local store to promote products with the most profit.
# Enviroment
## Python Part
### 1. Denpendencies.
cd /server/python-cli/

pip3 install

### 2. Run the application
python3 -m flask run

## Database Part:
Three relations are compiled: 
1.	“Orders” contains transaction history from all stores. One order relates to exactly one sale of one product. 10,000 transactions data are generated for entire year 2018. It contains foreign keys “ProductID” and “StoreID”.
2.	“Products” include price, default cost, nutritious information and recipes of all products. These are actual data acquired from online juice recipes. As a chain franchise, a certain product is priced the same despite regional differences
3.	“Stores” has information about the location and operating cost of each store. Then, the operating cost are integrated into default cost of each product, showing the exact profit of any product sold at any store after calculation.

We used a combination of python connector loops and CSV manual imports to bring data to the database.


![ER Diagram](https://github.com/yanz4/Supply-Recommendation-System-for-Juice-Stores/blob/master/ER%20DIAGRAM.png?raw=true)
Taking the product query as an example, here is a screenshot of the interface. When a user selects a period of a day and the number of products they are interested in, the database will return the best sellers during that period.   
![ER Diagram](https://github.com/yanz4/Supply-Recommendation-System-for-Juice-Stores/blob/master/1.png?raw=true)
For example, if we want to find the top 10 best sellers in the morning, we can set the values as shown in the screenshot below. 
![ER Diagram](https://github.com/yanz4/Supply-Recommendation-System-for-Juice-Stores/blob/master/2.png?raw=true)
Click the “View Results” button, you will see the returned results including the name of the products and the number of products sold.
![ER Diagram](https://github.com/yanz4/Supply-Recommendation-System-for-Juice-Stores/blob/master/3.png?raL=true)

# Linear Optimization Part
Big-M method of simplex algorithm was implemented to realize linear programming for one-click optimization function, aiming to help managers to determine the target sales numbers of each product in stores at various city size based on existing sales records and pricing information to maximize profit. 

As all programs are run locally, the regional manager will input from webpage, generating .txt files. We used python to read the inputs, convert them to part of the constraints, and implement queries to read from mysql database to get the rest constraints. These processes are all dynamic. The output of the optimization will generate another .txt file, and then displayed on user interface. This function is for regional manager only, and each local store manager should use this result as a reference to adjust their marketing strategy. Note that local preference on taste, ingredients availability, and other feasibility factors shall be considered and reported to regional manager to justify marketing strategy at each store. 

Built-in constraints are as follows:
1.According to experience, each store has a fixed amount of foot traffic conversion rate, and a fixed amount of sales number of 10k cups per store, regardless of the products offered or marketing efforts.
2.Due to seasonal availability, total pineapple available for each store is 30kg
3.Due to taste preference survey, national total sale of Pumpkin Cordial will not reach 20, Lemon Drop will not reach 30, Arthritis Soother will not reach 10 (unit: k cups)
4.Due to taste preference survey, national total sale of Force Field will be at least 30 (unit: k cups)

The input are as follows:

A. Please input the max possible sales for any product. According to historic data, no product is likely to reach 50k cups in sales in all stores combined. Please enter a number, and it will overwrite the default 50k sales ceiling. If there is no solid evidence on substantial growth of the franchise, please leave it blank.

Max possible sale for any product next year is: (please enter number only)

[________] Unit: k cups. Default value is 50. 

	
B. Please consult with marketing team to determine maximum possible total sales of each product. If no value is entered, default value will be the number from the entered number above. Default for input 1 is 50.

Input Product ID, max total sales (k cups), separated by commas, no space.
Input another constraint after the previous one, separated by a comma, no space. 

Please input product ID as capitalized P followed by its ID, such as ‘P1’.
Please input max total sales as number only.
[________]

e.g. According to survey, total sale of product 2 next year could be up to 30k cups, while product 4 will only be 10k cups.
Input: P2,30,P4,10

e.g. Management plans to cancel product 6 and 7 next year, and would like to see how they should adjust marketing accordingly.
Input: P6,0,P7,0

A sample result is as follows:


Product  Sales_Target
Green Power_L: 0.0

Lemon Drop_L: 30.0

Inner Peach_L: 1.0

Square Root_L: 1.0

Force Field_L: 12.0

Pink Pom_L: 32.5

…...
Maximum Profits = $740.52(k)


This means the regional manager will direct local store managers to market the products respectively to reach target sales number. For example, Green Power_L is 0.00, means that local store managers in large cities should not put any effort on marketing or promoting this product. Pink Pom_L is 32.5, means that local store managers in large cities should market this product to reach the target total sales number of 32.5 k cups. In this case we have 12 stores in large cities, each store has a target sales number of 2708 cups of Pink Pom. And if such plans are executed perfectly, all stores will provide a maximized profit of 740.52k shown at the bottom line.
