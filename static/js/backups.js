function populateEntries(files)
{
    console.log(files);

    container = document.getElementById("contentContainer")
    files.forEach(filename => {
        var words = filename.split("_");
        const date = new Date(parseInt(words[2]) * 1000);

        const entry = document.createElement("div"); entry.className = "entry"; entry.setAttribute("filename", filename);
        const header = document.createElement("h3"); header.textContent = filename;
        const dateContainer = document.createElement("p"); dateContainer.textContent = date;

        entry.onclick = function() {select(entry)};
        entry.appendChild(header);
        entry.appendChild(dateContainer);

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