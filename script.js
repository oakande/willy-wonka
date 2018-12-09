//  Current day of week
var dayofWeek = new Date().getDay();

var submitTicket = document.querySelector("#btn");

submitTicket.onclick = function() {  
    var nameField = document.querySelector("#name");
    var ageField = document.querySelector("#age");
    var guestField = document.querySelector("#guest");
    
    if (nameField.value == "" || ageField.value == "" || guestField.value == "") {
        var display = document.querySelector('.error');

        document.querySelector('.error-msg').textContent = "All fields are required";

        display.classList.add("fade-in");
        display.setAttribute("style", "display: block;");

        setTimeout(function(){
            display.className = 'error fade-out';
            display.setAttribute("style", "display: none;");
            display.classList.remove("fade-out");
        }, 3500);
    } else {
        createTicket(nameField.value, ageField.value, guestField.value);
        validateSuccess();
    }

    function validateSuccess () {
        // When user submits form all fields should be cleared out after validation success
        nameField.value = "";
        ageField.value = "";
        guestField.value = "";
    }
}

var showTheTickets = function (tickets) {
    var list = document.querySelector("#list");
    list.innerHTML = "";

    tickets.forEach(function (ticket) {
        var listItem = document.createElement("li");

        listItem.innerHTML += '<div class="quarter">' + 
            '<h3> Thanks for entering our contest ' + '<span>' + ticket.entrant_name + '('+ticket.entrant_age+')' + '</span>' + '</h3>' +
            '<p>Guest: '+ticket.guest_name+'</p>'
            '</div>' +
            '<div class="one-third">' + '<p> </p>' +'</div>'
        
        if (ticket.random_token === dayofWeek ) {
            listItem.className = "winner ticket";
        } else {
            listItem.className = "try ticket";
        }
        
        list.appendChild(listItem);
    });
}   


// post a single ticket --> POST
var createTicket = function (name, age, guest) {
    var data = `name=${encodeURIComponent(name)}`;
    data += `&age=${encodeURIComponent(age)}`;
    data += `&guest=${encodeURIComponent(guest)}`;
    fetch("http://localhost:8080/tickets", {
      method: "POST",
      body: data,
      credentials: 'include',
      headers: {
        "Content-type": "application/x-www-form-urlencoded"
      }
    }).then(function (response) {
        if (response.status == 201) {
            var success = document.querySelector('.success');

            document.querySelector('.success-msg').textContent = "Your ticket has been successfully created";
            
            success.classList.add("fade-in");
            success.setAttribute("style", "display: block;");

            setTimeout(function(){
                success.className = 'success fade-out';
                success.setAttribute("style", "display: none;");
                success.classList.remove("fade-out");
            }, 3500);
                      
            loadTickets();
        } 
        else if(response.status == 403) {
            response.text().then(function (text) {
                var display = document.querySelector('.error');

                document.querySelector('.error-msg').textContent = text;

                display.classList.add("fade-in");
                display.setAttribute("style", "display: block;");

                setTimeout(function(){
                    display.className = 'error fade-out';
                    display.setAttribute("style", "display: none;");
                    display.classList.remove("fade-out");
                }, 3500);
            });
        }
    });
};

// get list of all tickets -> GET
var loadTickets = function () {
    fetch("http://localhost:8080/tickets", {
        credentials: 'include'
    }).then(function (response) {
        response.json().then(function (theTickets) {
            if (response.status == 200) {
                showTheTickets(theTickets);
            }
            else if (response.status == 404) {
                response.text().then(function (text) {
                    alert(text);
                });
            } 
        });
    });
};

loadTickets();