function populateEntries(files)
{
    console.log(files);

    container = document.getElementById("contentContainer")
    files.forEach(filename => {
        var words = filename.split("_");
        const date = `${new Date(parseInt(words[2]) * 1000)}`.split("GMT")[0];

        const entry = document.createElement("div"); entry.className = "entry"; entry.setAttribute("filename", filename); 
        entry.style.display ="flex"; 
        entry.style.flexDirection = "row";

        const dataContainer = document.createElement("div"); 
        dataContainer.style.display = "flex"; 
        dataContainer.style.flexDirection = "column";

        const downloadButton = document.createElement("button");
        downloadButton.onclick = function() {event.stopPropagation()};
        downloadButton.onclick = function() {window.location.href = `/serve_backup/${filename}`};
        downloadButton.textContent = "Download";
        downloadButton.style.marginLeft = "auto";


        const header = document.createElement("h3"); header.textContent = filename;
        const dateContainer = document.createElement("p"); dateContainer.textContent = date;



        dataContainer.appendChild(header);
        dataContainer.appendChild(dateContainer);
        
        entry.onclick = function() {select(entry)};

        entry.appendChild(dataContainer);
        entry.appendChild(downloadButton);

        container.appendChild(entry);
    });
}

function populateDeleteForm()
{
    if (selected)
    {
        document.getElementById("deleteFormFilename").value = selected.getAttribute("filename");
    }
}


function populateRollbackForm()
{
    if (!selected) return;
    document.getElementById("rollbackFormContainer").style.display = "flex";
    document.getElementById("rollbackFormFilenameInput").value = selected.getAttribute("filename");
    
}

document.addEventListener("DOMContentLoaded", function() {
    const deleteButton = document.getElementById("deleteEntryButton");
    deleteButton.addEventListener("click", populateDeleteForm)
});