

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