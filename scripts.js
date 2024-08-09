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
    
    form.innerHTML = `
        <label for="fname">First name:</label><br>
        <input type="text" id="fname" name="fname" value=""><br>
        <label for="lname">Last name:</label><br>
        <input type="text" id="lname" name="lname" value=""><br><br>
        <input type="submit" value="Submit">
    `;
    
    // Display the form container and append the form to it
    formContainer.style.display = 'block';
    formContainer.appendChild(form);
}

