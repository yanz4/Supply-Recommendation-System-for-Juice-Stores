<?php

/**
 * Configuration for database connection
 *
 */

$host = "127.0.0.1:3306";
$username = "root";
$password = "password";
$dbname = "test";
$dsn = "mysql:host=$host;dbname=$dbname";
$options = array(
    PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
);
