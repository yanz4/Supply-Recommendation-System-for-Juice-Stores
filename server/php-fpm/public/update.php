<?php

/**
 * List all users with a link to edit
 */

require "../config.php";
require "../common.php";

$connection = new PDO($dsn, $username, $password, $options);

$sql = "SELECT * FROM Stores";

$statement = $connection->prepare($sql);
$statement->execute();

$result = $statement->fetchAll();
?>

<?php require "templates/header.php";?>

<h2>Update records</h2>

<table>
    <thead>
        <tr>
            <th>storeId</th>
            <th>citysize</th>
             <th>district</th>
             <th>delete</th>
        </tr>
    </thead>
    <tbody>
    <?php foreach ($result as $row): ?>
        <tr>
            <td><?php echo escape($row["storeId"]); ?></td>
            <td><?php echo escape($row["citysize"]); ?></td>
            <td><?php echo escape($row["district"]); ?></td>
            <td><?php echo escape($row["annualOpCost"]); ?></td>
            <td><a href="update-single.php?storeId=<?php echo escape($row["storeId"]); ?>">Edit</a></td>
        </tr>
    <?php endforeach;?>
    </tbody>
</table>

<a href="index.php">Back to home</a>

<?php require "templates/footer.php";?>