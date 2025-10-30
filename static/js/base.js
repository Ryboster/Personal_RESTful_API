function getCookieByName(name)
{
    var cookiesStr = document.cookie;
    var cookiesArr = cookiesStr.split("; ");
    for (let i = 0; i < cookiesArr.length; i ++)
    {
        var key_val_pair = cookiesArr[i].split("=");
        if (key_val_pair[0] === name)
        {
            return key_val_pair[1]
        }
    }
}

function getAPIURL()
{
    console.log("getting API URL");
    console.log(window.location.href);
    const APIButton = document.getElementById("APIButton");
    APIButton.onclick = () => {
        const finalEndpoint = window.location.href.split("/");
        const APIEndpoint = "api/" + finalEndpoint[finalEndpoint.length - 1];
        window.location.href = APIEndpoint;
    }
}

document.addEventListener("DOMContentLoaded", function() {
    const token = getCookieByName("token");
    const username = getCookieByName("username");
    if (token && username)
    {
        userContainer = document.getElementById("userContainer");
        userContainer.style.display = "flex";
        var loggedAs = document.createElement("p");
        loggedAs.textContent = `Hello ${username}`;
        userContainer.appendChild(loggedAs);
        
        var logButton = document.getElementById("logButton");
        logButton.textContent = "Logout";
        logButton.onclick = function() {window.location.href = "/logout";};   
    }
});