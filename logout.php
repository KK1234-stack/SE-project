<?php
// Start the session
session_start();

// Destroy all session data
session_destroy();

// Specify content type to avoid download issues
header("Content-Type: text/html; charset=UTF-8");

// Redirect to login.html
header("Location: login.html");
exit();
?>
