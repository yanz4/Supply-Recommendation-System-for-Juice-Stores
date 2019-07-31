<?php

/**
 * Use an HTML form to create a new entry in the
 * users table.
 *
 */

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {
  if (!hash_equals($_SESSION['csrf'], $_POST['csrf'])) die();

  try  {
    $connection = new PDO($dsn, $username, $password, $options);
    
    $new_user = array(
      "storeId" => $_POST['storeId'],
      "citySize"  => $_POST['citySize'],
      "district"  => $_POST['district'],
      "annualOpCost"  => $_POST['annualOpCost'],
  
    );

    $sql =
        sprintf(
      "INSERT INTO %s (%s) values (%s)",
      "Stores",
      implode(", ", array_keys($new_user)),
      ":" . implode(", :", array_keys($new_user))
    );

    $statement = $connection->prepare($sql);
    $statement->execute($new_user);
  } catch(PDOException $error) {
      echo $sql . "<br>" . $error->getMessage();
  }
}
?>
<?php require "templates/header.php"; ?>

  <?php if (isset($_POST['submit']) && $statement) : ?>
    <blockquote><?php echo escape($_POST['storeId']); ?> successfully added.</blockquote>
  <?php endif; ?>

  <h2>Add a record</h2>

  <form method="post">
      <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
    <label for="storeId">storeId</label>
    <input type="text" name="storeId" id="storeId">
    <label for="citySize">citySize</label>
    <input type="text" name="citySize" id="citySize">
    <label for="district">district</label>
    <input type="text" name="district" id="district">
    <label for="annualOpCost">annualOpCost</label>
    <input type="text" name="annualOpCost" id="annualOpCost">
    <input type="submit" name="submit" value="Submit">
  </form>

  <a href="index.php">Back to home</a>

<?php require "templates/footer.php"; ?>
