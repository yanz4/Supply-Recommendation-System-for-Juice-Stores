<?php

/**
 * Function to query information based on
 * a parameter: in this case, location.
 *
 */

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {
    /*  if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();*/

    try {
        $connection = new PDO($dsn, $username, $password, $options);

//        $sql = "
//(SELECT Products.name, COUNT(OrderID) AS Product_Sold FROM Orders, Products, Stores
//WHERE Orders.StoreID=Stores.StoreID AND Orders.productID=Products.productID AND time_sold < '07:00:00'
//GROUP BY Orders.ProductID
//ORDER BY Product_Sold desc
//LIMIT :number)
//
//UNION ALL
//
//(SELECT Products.name, COUNT(OrderID) AS Product_Sold FROM Orders, Products, Stores
//WHERE Orders.StoreID=Stores.StoreID AND Orders.productID=Products.productID AND time_sold > '11:00:00' AND time_sold < '13:00:00'
//GROUP BY Orders.ProductID
//ORDER BY Product_Sold desc
//LIMIT :(%s)
//
//order by Product_Sold desc)
//;
//           ";


        $date_where = "";
        $number = $_POST['number'];
        $start_date = $_POST['start_hour'];
        $end_date = $_POST['end_hour'];

        // SQL
        if (isset($start_date) && !empty($start_hour)) {
            $date_where .= " AND time_sold >= '$start_hour' ";
        }

        if (isset($end_date) && !empty($end_date)) {
            $date_where .= " AND time_sold < '$end_date' ";
        }
        $sql = "
SELECT
	Products.NAME,
	COUNT( OrderID ) AS Product_Sold 
FROM
	Orders,
	Products 
WHERE
	Orders.productID = Products.productID 
	{$date_where} 
GROUP BY
	Orders.ProductID 
ORDER BY
	Product_Sold DESC 
	LIMIT {$number}
";


        $statement = $connection->prepare($sql);
//        $statement->bindParam(':number', $number, PDO::PARAM_STR);
        $statement->execute();

        $result = $statement->fetchAll();
    } catch (PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
        die;
    }
}
?>
<?php require "templates/header.php"; ?>

<?php
if (isset($_POST['submit'])) {
    if ($result && $statement->rowCount() > 0) { ?>
        <h2>Results</h2>

        <table>
            <thead>
            <tr>
                <th>ProductName</th>
                <th>ProductSold</th>
                <!--                <th>citySize</th>-->
                <!--                <th>districts</th>-->
                <!--                <th>annualOpCost</th>-->
            </tr>
            </thead>
            <tbody>
            <?php foreach ($result as $row) { ?>
                <tr>
                    <td><?php echo escape($row["NAME"]); ?></td>
                    <td><?php echo escape($row["Product_Sold"]); ?></td>
                    <!--                    <td>--><?php //echo escape($row["citySize"]); ?><!--</td>-->
                    <!--                    <td>--><?php //echo escape($row["district"]); ?><!--</td>-->
                    <!--                    <td>--><?php //echo escape($row["annualOpCost"]); ?><!--</td>-->
                </tr>
            <?php } ?>
            </tbody>
        </table>
    <?php } else { ?>
        > No results found for <?php echo escape($_POST['number']); ?>.
    <?php }
} ?>

<h2>Find popular products during certaion time of a day</h2>

<form method="post">
    <label for="start_date">start_hour(format:00:00:00)</label>
    <input type="text" id="start_hour" name="start_hour" value="<?php echo isset($start_hour) ? $start_hour : '' ?>">
    <label for="end_date">end_hour(format:00:00:00)</label>
    <input type="text" id="end_hour" name="end_hour" value="<?php echo isset($end_hour) ? $end_hour : '' ?>">
    <label for="number">number</label>
    <input type="text" id="number" name="number" value="<?php echo isset($number) ? $number : '' ?>">
    <input type="submit" name="submit" value="View Results">
</form>

<a href="index.php">Back to home</a>

<?php require "templates/footer.php"; ?>

