# Supply-Recommendation-System-for-Juice-Stores
This Project aims to help juice chainstore owners or regional managers to view and manage products and sales of all stores in this regional. We build the management system with MySQL and PHP so managers could Create, Read, Update and Delete information from local server. We also provide an advanced function named “One-Click Sales Optimization”, which provides a best sales plan to reach maximum profit depending on the sales goal set by user.

In addition to traditional useful functionals such as view and search for sales records, edit store and product information,etc, one major problem that concerns managers is how to maximize profits when they own multiple juice stores. Given that actual profits in each juice store vary with city size and ingredient cost, we think Linear Optimization model could help determine the best sales plan. Given the population is approximately the same within a city, so annual orders, or cups of juice sales, would be about the same in each store. When the cups of juice sales keep relative constant we could maximize total profits by encouraging each local store to promote products with the most profit.

## Database Part:
3 relations are compiled: 
1.	“Orders” contains transaction history from all stores. One order relates to exactly one sale of one product. 10,000 transactions data are generated for entire year 2018. It contains foreign keys “ProductID” and “StoreID”.
2.	“Products” include price, default cost, nutritious information and recipes of all products. These are actual data acquired from online juice recipes. As a chain franchise, a certain product is priced the same despite regional differences
3.	“Stores” has information about the location and operating cost of each store. Then, the operating cost are integrated into default cost of each product, showing the exact profit of any product sold at any store after calculation.

We used a combination of python connector loops and CSV manual imports to bring data to the database.


![ER Diagram](https://github.com/yanz4/Supply-Recommendation-System-for-Juice-Stores/blob/master/ER%20DIAGRAM.png?raw=true)
