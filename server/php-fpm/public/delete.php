<?php

/**
 * Delete a user
 */

require "../config.php";
require "../common.php";

$success = null;

if (isset($_POST["submit"])) {
/*  if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();*/

  try {
    $connection = new PDO($dsn, $username, $password, $options);
  
    $id = $_POST["submit"];

    $sql = "DELETE FROM Stores WHERE storeId = :storeId";

    $statement = $connection->prepare($sql);
    $statement->bindValue(':storeId', $id);
    $statement->execute();

    $success = "Store successfully deleted";
  } catch(PDOException $error) {
    echo $sql . "<br>" . $error->getMessage();
  }
}

try {
  $connection = new PDO($dsn, $username, $password, $options);

  $sql = "SELECT * FROM Stores";

  $statement = $connection->prepare($sql);
  $statement->execute();

  $result = $statement->fetchAll();
} catch(PDOException $error) {
  echo $sql . "<br>" . $error->getMessage();
}
?>
<?php require "templates/header.php"; ?>
        
<h2>Delete records</h2>

<?php if ($success) echo $success; ?>

<form method="post">
  <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
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
    <?php foreach ($result as $row) : ?>
      <tr>
        <td><?php echo escape($row["storeId"]); ?></td>
        <td><?php echo escape($row["citysize"]); ?></td>
        <td><?php echo escape($row["district"]); ?></td>
        <td><?php echo escape($row["annualOpCost"]); ?></td>
        <td><button type="submit" name="submit" value="<?php echo escape($row["storeId"]); ?>">Delete</button></td>
      </tr>
    <?php endforeach; ?>
    </tbody>
  </table>
</form>

<a href="index.php">Back to home</a>

<?php require "templates/footer.php"; ?>