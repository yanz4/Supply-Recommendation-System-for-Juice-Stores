<?php

use \Psr\Http\Message\ServerRequestInterface as Request;
use \Psr\Http\Message\ResponseInterface as Response;
use Slim\App;

require 'vendor/autoload.php';
require 'config.php';

$pdo = new \FaaPz\PDO\Database($dsn, $username, $password);

// Slim configs
$config = array(
    'settings' => [
        'debug' => true,
        'displayErrorDetails' => true,
    ],
);
$app = new \Slim\App($config);

// Check the user is logged in when necessary.
$loggedInMiddleware = function ($request, $response, $next) {
    $route = $request->getAttribute('route');
    $routeName = $route->getName();
    // $groups = $route->getGroups();
    // $methods = $route->getMethods();
    // $arguments = $route->getArguments();

    # Define routes that user does not have to be logged in with. All other routes, the user
    # needs to be logged in with.
    $publicRoutesArray = array(
        'login',
        'post-login',
        'register',
        'forgot-password',
        'register-post'
    );

    if (!isset($_SESSION['USER']) && !in_array($routeName, $publicRoutesArray)) {
        // redirect the user to the login page and do not proceed.
        $response = $response->withRedirect('/login');
    } else {
        // Proceed as normal...
        $response = $next($request, $response);
    }

    return $response;
};

// Apply the middleware to every request.
$app->add($loggedInMiddleware);


// Define app routes

// Dashboard
$app->get(
    '/',
    function (Request $request, Response $response, array $args) {
        // global $pdo;
        // $selectStatement = $pdo->select()
        //     ->from('Stores');

        // $stmt = $selectStatement->execute();
        // $data = $stmt->fetch();
        // return $response->withJson($data);
    }
)->setName('home');

// Login
$app->get('/login', function (Request $request, Response $response, array $args) { });

$app->run();
