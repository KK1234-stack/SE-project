<?php
session_start();

// Database configuration
$servername = "localhost";
$username = "root";
$password = "";  // Replace with your MySQL root password if set
$dbname = "vulscan_auth";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Process form data
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];

    // Verify user credentials
    $sql = "SELECT id, password FROM users WHERE username = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $username);
    $stmt->execute();
    $stmt->store_result();
    $stmt->bind_result($user_id, $hashed_password);
    $stmt->fetch();

    if ($stmt->num_rows == 1 && password_verify($password, $hashed_password)) {
        $_SESSION['user_id'] = $user_id;
        $_SESSION['username'] = $username;
        echo "<script>alert('Login successful!'); window.location.href='dashboard.php';</script>";
    } else {
        echo "<script>alert('Invalid username or password.'); window.location.href='login.html';</script>";
    }

    $stmt->close();
}
$conn->close();
?>
