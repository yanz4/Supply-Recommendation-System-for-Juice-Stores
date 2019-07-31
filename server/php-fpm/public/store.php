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

//    $sql = "SELECT Stores.storeId, SUM(price) AS Annual_Sales FROM Orders, Products, Stores
//WHERE Orders.StoreID=Stores.storeId AND Orders.productID=Products.productID
//GROUP BY StoreID
//ORDER BY Annual_Sales DESC
//LIMIT %:number %;";


        // #of stores
        $number = $_POST['number'] ?: 10;

        $sql = <<<SQL
SELECT
	s.*,
	SUM(p.price) as Annual_Sales
FROM
	Orders AS o
	LEFT JOIN Stores AS s ON s.storeId = o.storeId
	LEFT JOIN Products AS p ON p.ProductID = o.ProductID
	GROUP BY s.storeId
	ORDER BY Annual_Sales DESC
	LIMIT {$number}
SQL;


        $statement = $connection->prepare($sql);
//    $statement->bindParam(':number', $numbert, PDO::PARAM_STR);
        $statement->execute();

        $result = $statement->fetchAll();
    } catch (PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
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
                <th>StoreId</th>
                <th>citySize</th>
                <th>districts</th>
                <th>annualOpCost</th>
                <th>Annual_Sales</th>
            </tr>
            </thead>
            <tbody>
            <?php foreach ($result as $row) { ?>
                <tr>
                    <td><?php echo escape($row["storeId"]); ?></td>
                    <td><?php echo escape($row["citySize"]); ?></td>
                    <td><?php echo escape($row["district"]); ?></td>
                    <td><?php echo escape($row["annualOpCost"]); ?></td>
                    <td><?php echo escape($row["Annual_Sales"]); ?></td>
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

<h3>Search for most profitable stores and their annual sales, from highest to lowest.</h3>
<h3>Set the number of stores you would like to see.</h3>

<form method="post">
    <label for="number">number</label>
    <input type="text" id="number" name="number" value="<?php echo isset($number) ? $number : '' ?>">
    <input type="submit" name="submit" value="View Results">
</form>

<a href="index.php">Back to home</a>

<?php require "templates/footer.php"; ?>

