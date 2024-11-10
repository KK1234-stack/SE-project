<?php
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
    $email = $_POST['email'];
    $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

    // Check if the username or email already exists
    $sql = "SELECT id FROM users WHERE username = ? OR email = ?";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("ss", $username, $email);
    $stmt->execute();
    $stmt->store_result();

    if ($stmt->num_rows > 0) {
        echo "<script>alert('Username or Email already exists.'); window.location.href='signup.html';</script>";
    } else {
        // Insert new user into the database
        $sql = "INSERT INTO users (username, email, password) VALUES (?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("sss", $username, $email, $password);

        if ($stmt->execute()) {
            echo "<script>alert('Account created successfully!'); window.location.href='login.html';</script>";
        } else {
            echo "<script>alert('Error creating account. Please try again.'); window.location.href='signup.html';</script>";
        }
    }

    $stmt->close();
}
$conn->close();
?>
