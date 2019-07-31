<?php

/**
 * Use an HTML form to edit an entry in the
 * users table.
 *
 */

require "../config.php";
require "../common.php";

if (isset($_POST['submit'])) {

    try {
        $connection = new PDO($dsn, $username, $password, $options);

        $user = [
            "storeId" => $_POST['storeId'],
            "citySize" => $_POST['citysize'],
            "district" => $_POST['district'],
            "annualOpCost" => $_POST['annualOpCost'],
        ];

        $sql = "UPDATE Stores
            SET
              storeId = :storeId,
              citysize = :citysize,
              district = :district,
              annualOpCost = :annualOpCost
            WHERE storeId = :storeId";

        $statement = $connection->prepare($sql);
        $statement->execute($user);
    } catch (PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
}

if (isset($_GET['storeId'])) {
    try {
        $connection = new PDO($dsn, $username, $password, $options);
        $id = $_GET['storeId'];

        $sql = "SELECT * FROM Stores WHERE storeId = :storeId";
        $statement = $connection->prepare($sql);
        $statement->bindValue(':storeId', $id);
        $statement->execute();

        $user = $statement->fetch(PDO::FETCH_ASSOC);
    } catch (PDOException $error) {
        echo $sql . "<br>" . $error->getMessage();
    }
} else {
    echo "Something went wrong!";
    exit;
}
?>

<?php require "templates/header.php";?>

<?php if (isset($_POST['submit']) && $statement): ?>
    <blockquote><?php echo escape($_POST['storeId']); ?> successfully updated.</blockquote>
<?php endif;?>

<h2>Edit a store record</h2>

<form method="post">
    <input name="csrf" type="hidden" value="<?php echo escape($_SESSION['csrf']); ?>">
    <?php foreach ($user as $key => $value): ?>
        <label for="<?php echo $key; ?>"><?php echo ucfirst($key); ?></label>
        <input type="text" name="<?php echo $key; ?>" id="<?php echo $key; ?>" value="<?php echo escape($value); ?>" <?php echo ($key === 'id' ? 'readonly' : null); ?>>
    <?php endforeach;?>
    <input type="submit" name="submit" value="Submit">
</form>

<a href="index.php">Back to home</a>

<?php require "templates/footer.php";?>
