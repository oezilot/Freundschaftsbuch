function gotologIn() {
    window.location.href = 'logIn.html';
}

function gotobout() {
    window.location.href = 'about.html';
}

function gotoregister() {
    window.location.href = 'register.html';
}

////////////// Home button for all Subpages ////////////////
function gotoindex() {
    window.location.href = 'index.html';
}

////// Wenn man den Form button drückt dann verschwindet der geamte content und es wird weiss ///////////////
function openform() {
    // Hide the entire content
    document.getElementById('content').style.display = 'none';
    
    // Turn the background white
    document.body.style.backgroundColor = 'white';
    
    // Create and display the form
    const formContainer = document.getElementById('form-container');
    const form = document.createElement('form');
    form.action = '/action_page.php';
    form.method = 'POST';
    form.enctype = 'multipart/form-data';  // wichtig für Datei-Uploads
    
    form.innerHTML = `
        <label for="fname">Name:</label><br>
        <input type="text" id="fname" name="fname" value=""><br>

        <label for="fname">Birthday:</label><br>
        <input type="text" id="fname" name="fname" value=""><br>

        <label for="fname">Gender:</label><br>
        <input type="text" id="fname" name="fname" value=""><br><br>

        <!-- file button upload -->
        <label for="file-upload">Upload a file:</label><br>
        <input type="file" id="file-upload" name="file-upload"><br><br><br>

        <!-- buttons for submit and home -->
        <button type="button" id="home-button">Home</button>
        <input type="submit" value="Submit">
    `;
    
    // Display the form container and append the form to it
    formContainer.style.display = 'block';
    formContainer.appendChild(form);

    /////////////// Der Link zum Home button
    document.getElementById('home-button').addEventListener('click', gotoindex);

}

