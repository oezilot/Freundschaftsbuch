<?php
// Check if the form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    
    // Collect and sanitize the form data
    $fname = htmlspecialchars($_POST['fname']);
    $birthday = htmlspecialchars($_POST['birthday']);
    $gender = htmlspecialchars($_POST['gender']);
    
    // Handle file upload
    if (isset($_FILES['file-upload']) && $_FILES['file-upload']['error'] == 0) {
        $upload_dir = 'uploads/';
        $file_name = basename($_FILES['file-upload']['name']);
        $target_file = $upload_dir . $file_name;

        // Check if the directory exists, if not, create it
        if (!file_exists($upload_dir)) {
            mkdir($upload_dir, 0777, true);
        }

        // Save the file to the server
        if (move_uploaded_file($_FILES['file-upload']['tmp_name'], $target_file)) {
            echo "The file ". htmlspecialchars($file_name). " has been uploaded.";
        } else {
            echo "Sorry, there was an error uploading your file.";
        }
    }

    // Optionally save the form data to a database or a file
    // Example: Saving data to a file (for simplicity)
    $data = "Name: $fname, Birthday: $birthday, Gender: $gender, File: $file_name\n";
    file_put_contents('submissions.txt', $data, FILE_APPEND);

    // Provide feedback to the user
    echo "<h1>Thank you for your submission!</h1>";
    echo "<p>Your name: $fname</p>";
    echo "<p>Your birthday: $birthday</p>";
    echo "<p>Your gender: $gender</p>";
    echo "<p>Your uploaded file: $file_name</p>";
} else {
    echo "Form not submitted correctly.";
}
?>
