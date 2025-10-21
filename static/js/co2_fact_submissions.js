function populateEntries(obj)
{
    const container = document.getElementById("contentContainer");
    for (const [key,val] of Object.entries(obj))
    {
        const entry = document.createElement("div"); entry.className = "entry";
        const header = document.createElement("span"); header.className = "entryHeader";
        const source = document.createElement("h3");
        const source_url = document.createElement("a");
        const ID = document.createElement("p");
        const fact = document.createElement("p");
        const footer = document.createElement("span"); footer.className = "entryFooter";
        const co2 = document.createElement("p");
        const timespan = document.createElement("p");

        header.onclick = function() {event.stopPropagation();}
        source.textContent = val["Source"];
        source_url.href = val["Source"];
        fact.textContent = val["Fact"];
        co2.textContent = val["Co2"] + "g";
        timespan.textContent = val["Timespan"] + "s";
        ID.textContent = key;

        source_url.appendChild(source);
        header.appendChild(source_url);
        header.appendChild(ID);
        entry.appendChild(header);
        entry.appendChild(fact);
        entry.appendChild(footer);
        footer.appendChild(co2);
        footer.appendChild(timespan);
        container.appendChild(entry);

        entry.onclick = function() {select(entry)};
        entry.setAttribute("entryID", key);
        entry.setAttribute("entryFact", val["Fact"]);
        entry.setAttribute("entrySource", val["Source"]);
        entry.setAttribute("entryTimespan", val["Timespan"]);
        entry.setAttribute("entryCo2", val["Co2"]);
    }
}

function populateEditForm()
{
    if (!selected) return;
    document.getElementById("editFormIDInput").value = selected.getAttribute("entryID");
    document.getElementById("editFormFactInput").value = selected.getAttribute("entryFact");
    document.getElementById("editFormCo2Input").value = selected.getAttribute("entryCo2");
    document.getElementById("editFormSourceInput").value = selected.getAttribute("entrySource");
    document.getElementById("editFormTimespanInput").value = selected.getAttribute("entryTimespan");
    document.getElementById("editFormCo2Select").value = 1;
    document.getElementById("editFormTimespanSelect").value = 1;
}

function populateDeleteForm()
{
    if (!selected) return;
    document.getElementById("deleteFormIDInput").value = selected.getAttribute("entryID");
    document.getElementById("deleteFormNameInput").value = selected.getAttribute("entryName");
}

document.addEventListener("DOMContentLoaded", function() {
    const editButton = document.getElementById("editEntryButton");
    const deleteButton = document.getElementById("deleteEntryButton");
    editButton.addEventListener("click", populateEditForm)
    deleteButton.addEventListener("click", populateDeleteForm)
});