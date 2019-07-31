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

  try  {
    $connection = new PDO($dsn, $username, $password, $options);

    $sql = "SELECT * 
            FROM Stores
            WHERE district = :district";

    $district = $_POST['district'];
    $statement = $connection->prepare($sql);
    $statement->bindParam(':district', $district, PDO::PARAM_STR);
    $statement->execute();

    $result = $statement->fetchAll();
  } catch(PDOException $error) {
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
                <th>storeId</th>
                <th>citySize</th>
                <th>districts</th>
                <th>annualOpCost</th>
            </tr>
            </thead>
            <tbody>
            <?php foreach($result as $row) { ?>
                <tr>
                    <td><?php echo escape($row["storeId"]); ?></td>
                    <td><?php echo escape($row["citySize"]); ?></td>
                    <td><?php echo escape($row["district"]); ?></td>
                    <td><?php echo escape($row["annualOpCost"]); ?></td>
                </tr>
            <?php } ?>
            </tbody>
        </table>
    <?php } else { ?>
        > No results found for <?php echo escape($_POST['district']); ?>.
    <?php }
} ?>

<h2>Find stores based on their location</h2>

<form method="post">
    <label for="district">district</label>
    <input type="text" id="district" name="district">
    <input type="submit" name="submit" value="View Results">
</form>

<a href="index.php">Back to home</a>


